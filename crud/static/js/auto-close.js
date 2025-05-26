document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        var alertList = document.querySelectorAll('.alert-dismissible');
        alertList.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
