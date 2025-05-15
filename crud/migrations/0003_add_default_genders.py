from django.db import migrations

def add_default_genders(apps, schema_editor):
    Gender = apps.get_model('crud', 'Gender')
    for gender_name in ['Male', 'Female', 'Others']:
        Gender.objects.get_or_create(name=gender_name)

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_alter_gender_name_profile'),
    ]

    operations = [
        migrations.RunPython(add_default_genders),
    ]
