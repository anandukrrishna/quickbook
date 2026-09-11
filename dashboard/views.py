from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import User
from events.models import Event
from bookings.models import Booking


@login_required
@never_cache
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




@login_required
def event_list(request):

    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    events = Event.objects.all().order_by('-date')

    search = request.GET.get('search')
    venue = request.GET.get('venue')

    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if venue:
        events = events.filter(
            venue__icontains=venue
        )

    paginator = Paginator(events, 5)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'dashboard/event_list.html',
        {
            'page_obj': page_obj,
            'search': search,
            'venue': venue,
        }
    )


@login_required
def add_event(request):

    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    vendors = User.objects.filter(role='VENDOR')

    if request.method == 'POST':

        vendor_id = request.POST.get('vendor')

        date = parse_datetime(
            request.POST.get('date')
        )

        if date and timezone.is_naive(date):
            date = timezone.make_aware(date)

        total_seats = int(
            request.POST.get('total_seats')
        )

        Event.objects.create(
            vendor_id=vendor_id,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            venue=request.POST.get('venue'),
            date=date,
            total_seats=total_seats,
            available_seats=total_seats
        )

        return redirect('event_list')

    return render(
        request,
        'dashboard/add_event.html',
        {'vendors': vendors}
    )


@login_required
def edit_event(request, event_id):

    if not request.user.is_staff:
        return render(request, 'dashboard/access_denied.html')

    event = get_object_or_404(
        Event,
        id=event_id
    )

    vendors = User.objects.filter(
        role='VENDOR'
    )

    if request.method == 'POST':

        date = parse_datetime(
            request.POST.get('date')
        )

        if date and timezone.is_naive(date):
            date = timezone.make_aware(date)

        new_total_seats = int(
            request.POST.get('total_seats')
        )

        booked_seats = (
            event.total_seats -
            event.available_seats
        )

        if new_total_seats < booked_seats:

            return render(
                request,
                'dashboard/edit_event.html',
                {
                    'event': event,
                    'vendors': vendors,
                    'error': (
                        'Total seats cannot be less '
                        'than already booked seats.'
                    )
                }
            )

        event.vendor_id = request.POST.get('vendor')
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.venue = request.POST.get('venue')
        event.date = date

        event.total_seats = new_total_seats

        event.available_seats = (
            new_total_seats -
            booked_seats
        )

        event.save()

        return redirect('event_list')

    return render(
        request,
        'dashboard/edit_event.html',
        {
            'event': event,
            'vendors': vendors
        }
    )


@login_required
def delete_event(request, event_id):

    if not request.user.is_staff:
        return render(
            request,
            'dashboard/access_denied.html'
        )

    event = get_object_or_404(
        Event,
        id=event_id
    )

    if request.method == 'POST':
        event.delete()

        return redirect('event_list')

    return render(
        request,
        'dashboard/delete_event.html',
        {'event': event}
    )


@login_required
def user_list(request):

    if not request.user.is_staff:
        return render(
            request,
            'dashboard/access_denied.html'
        )

    users = User.objects.all().order_by('-date_joined')

    search = request.GET.get('search')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    paginator = Paginator(users, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'dashboard/user_list.html',
        {
            'page_obj': page_obj,
            'search': search,
        }
    )


@login_required
def user_detail(request, user_id):

    if not request.user.is_staff:
        return render(
            request,
            'dashboard/access_denied.html'
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    def count_team(current_user):

        total = 0

        for referral in current_user.referrals.all():

            total += 1

            total += count_team(referral)

        return total

    left_user = user.referrals.filter(
        referral_position='LEFT'
    ).first()

    right_user = user.referrals.filter(
        referral_position='RIGHT'
    ).first()

    left_team_count = (
        1 + count_team(left_user)
        if left_user else 0
    )

    right_team_count = (
        1 + count_team(right_user)
        if right_user else 0
    )

    def build_tree(current_user):

        referrals = current_user.referrals.all()

        return {
            'user': current_user,

            'children': [
                build_tree(referral)
                for referral in referrals
            ]
        }


    referral_tree = build_tree(user)


    def get_all_referrals(current_user):

        referrals_list = []

        for referral in current_user.referrals.all():

            referrals_list.append(referral)

            referrals_list.extend(
                get_all_referrals(referral)
            )

        return referrals_list


    search = request.GET.get(
        'search',
        ''
    ).strip()


    search_results = []


    if search:

        all_referrals = get_all_referrals(user)

        for referral in all_referrals:

            if (
                search.lower() in referral.username.lower()
                or search.lower() in referral.email.lower()
            ):

                search_results.append(referral)


    return render(
        request,
        'dashboard/user_detail.html',
        {
            'user': user,

            'left_team_count': left_team_count,

            'right_team_count': right_team_count,

            'referral_tree': referral_tree,

            'search': search,

            'search_results': search_results,
        }
    )