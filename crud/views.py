from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from .forms import UserCreateForm, UserUpdateForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def user_list(request):
    search_query = request.GET.get('search', '')
    users = User.objects.all().order_by('id')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        users_data = []
        for user in page_obj:
            gender_name = ''
            address = ''
            date_of_birth = ''
            if hasattr(user, 'profile'):
                if user.profile.gender:
                    gender_name = user.profile.gender.name
                address = user.profile.address or ''
                date_of_birth = user.profile.date_of_birth or ''
            users_data.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'gender': gender_name,
                'address': address,
                'date_of_birth': date_of_birth,
            })
        data = {
            'users': users_data,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'current_page': page_obj.number,
            'num_pages': paginator.num_pages,
        }
        return JsonResponse(data)

    return render(request, 'user_list.html', {'page_obj': page_obj, 'search_query': search_query})

@login_required(login_url='login')
def user_add(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            if gender:
                user.profile.gender = gender
            if address:
                user.profile.address = address
            if date_of_birth:
                user.profile.date_of_birth = date_of_birth
            user.profile.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'user_form.html', {'form': form, 'title': 'Add User'})

@login_required(login_url='login')
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user, user_id=user_id)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            if gender:
                user.profile.gender = gender
            else:
                user.profile.gender = None
            user.profile.address = address
            user.profile.date_of_birth = date_of_birth
            user.profile.save()
            return redirect('user_list')
    else:
        initial = {}
        if hasattr(user, 'profile'):
            if user.profile.gender:
                initial['gender'] = user.profile.gender
            initial['address'] = user.profile.address
            initial['date_of_birth'] = user.profile.date_of_birth
        form = UserUpdateForm(instance=user, user_id=user_id, initial=initial)
    return render(request, 'user_form.html', {'form': form, 'title': 'Edit User'})

@login_required(login_url='login')
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

from .models import Gender
from .forms import GenderForm

@login_required(login_url='login')
def gender_list(request):
    genders = Gender.objects.all().order_by('id')
    return render(request, 'gender_list.html', {'genders': genders})

@login_required(login_url='login')
def gender_add(request):
    if request.method == 'POST':
        form = GenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gender_list')
    else:
        form = GenderForm()
    return render(request, 'gender_form.html', {'form': form, 'title': 'Add Gender'})

@login_required(login_url='login')
def gender_edit(request, gender_id):
    gender = get_object_or_404(Gender, pk=gender_id)
    if request.method == 'POST':
        form = GenderForm(request.POST, instance=gender)
        if form.is_valid():
            form.save()
            return redirect('gender_list')
    else:
        form = GenderForm(instance=gender)
    return render(request, 'gender_form.html', {'form': form, 'title': 'Edit Gender'})

@login_required(login_url='login')
def gender_delete(request, gender_id):
    gender = get_object_or_404(Gender, pk=gender_id)
    if request.method == 'POST':
        gender.delete()
        return redirect('gender_list')
    return render(request, 'gender_confirm_delete.html', {'gender': gender})

@login_required(login_url='login')
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user, user_id=user.id)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            if gender:
                user.profile.gender = gender
            else:
                user.profile.gender = None
            user.profile.address = address
            user.profile.date_of_birth = date_of_birth
            user.profile.save()
            return redirect('user_list')
    else:
        initial = {}
        if hasattr(user, 'profile'):
            if user.profile.gender:
                initial['gender'] = user.profile.gender
            initial['address'] = user.profile.address
            initial['date_of_birth'] = user.profile.date_of_birth
        form = UserUpdateForm(instance=user, user_id=user.id, initial=initial)
    return render(request, 'user_form.html', {'form': form, 'title': 'Edit Profile'})
