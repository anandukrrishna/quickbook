from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_home(request):
    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    return render(request, 'dashboard/home.html')

