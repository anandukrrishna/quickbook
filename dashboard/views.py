from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404

from accounts.models import User
from events.models import Event
from bookings.models import Booking


@login_required
def dashboard_home(request):

    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    context = {
        'total_customers': User.objects.filter(
            role='CUSTOMER'
        ).count(),

        'total_vendors': User.objects.filter(
            role='VENDOR'
        ).count(),

        'total_events': Event.objects.count(),

        'total_bookings': Booking.objects.count(),
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )


@login_required
def vendor_list(request):
    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    vendors = User.objects.filter(role='VENDOR')

    return render(
        request,
        'dashboard/vendor_list.html',
        {'vendors': vendors}
    )


@login_required
def add_vendor(request):
    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='VENDOR'
        )

        return redirect('vendor_list')

    return render(request, 'dashboard/add_vendor.html')

@login_required
def edit_vendor(request, vendor_id):
    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    vendor = get_object_or_404(
        User,
        id=vendor_id,
        role='VENDOR'
    )

    if request.method == 'POST':
        vendor.username = request.POST.get('username')
        vendor.email = request.POST.get('email')

        vendor.save()

        return redirect('vendor_list')

    return render(
        request,
        'dashboard/edit_vendor.html',
        {'vendor': vendor}
    )

@login_required
def delete_vendor(request, vendor_id):

    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    vendor = get_object_or_404(
        User,
        id=vendor_id,
        role='VENDOR'
    )

    if request.method == 'POST':
        vendor.delete()
        return redirect('vendor_list')

    return render(
        request,
        'dashboard/delete_vendor.html',
        {'vendor': vendor}
    )

