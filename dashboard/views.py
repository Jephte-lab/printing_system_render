from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from clients.models import Client
from datetime import date, timedelta
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from services.models import Service
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from orders.models import Order


@login_required
def dashboard_home(request):
    filter_type = request.GET.get('filter', 'today')

    today = timezone.now().date()
    current_year = today.year

    # -------------------
    # CLIENTS (ALWAYS ALL)
    # -------------------
    clients_all = Client.objects.all()

    # -------------------
    # FILTERED ORDERS
    # -------------------
    if filter_type == 'today':
        orders_qs = Order.objects.filter(created_at__date=today)

    elif filter_type == 'week':
        start_week = today - timedelta(days=today.weekday())  # Monday
        end_week = start_week + timedelta(days=6)            # Sunday
        orders_qs = Order.objects.filter(created_at__date__range=(start_week, end_week))

    elif filter_type == 'last_week':
        start_last_week = today - timedelta(days=today.weekday() + 7)
        end_last_week = start_last_week + timedelta(days=6)
        orders_qs = Order.objects.filter(created_at__date__range=(start_last_week, end_last_week))

    elif filter_type == 'year':
        orders_qs = Order.objects.filter(created_at__year=current_year)

    else:  # all
        orders_qs = Order.objects.all()

    # -------------------
    # CARDS DATA
    # -------------------
    total_clients = clients_all.count()          # ALWAYS ALL
    total_orders = orders_qs.count()             # FILTERED
    total_revenue = sum(o.total_price for o in orders_qs)
    total_services = Service.objects.count()

    recent_orders = orders_qs.order_by('-created_at')[:10]

    # -------------------
    # GRAPH DATA (MONTHLY – CURRENT YEAR)
    # -------------------
    months_labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    orders_per_month = []
    revenue_per_month = []

    for month in range(1, 13):
        month_orders = Order.objects.filter(
            created_at__year=current_year,
            created_at__month=month
        )
        orders_per_month.append(month_orders.count())
        revenue_per_month.append(
            sum(o.total_price for o in month_orders)
        )

    # -------------------
    # CONTEXT
    # -------------------
    context = {
        'filter_type': filter_type,

        # cards
        'total_clients_today': total_clients,
        'total_orders_today': total_orders,
        'total_revenue_today': total_revenue,
        'total_services': total_services,

        # table
        'recent_orders': recent_orders,

        # graphs
        'months_labels': months_labels,
        'orders_per_month': orders_per_month,
        'revenue_per_month': revenue_per_month,
    }

    return render(request, 'dashboard/home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_home')
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})

    return render(request, 'dashboard/login.html')

@login_required
@csrf_exempt  # or handle csrf in JS
def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        if not order_id or not status:
            return JsonResponse({'success': False, 'message': 'Invalid request'})

        try:
            order = Order.objects.get(id=order_id)
            order.status = status  # make sure Order model has a 'status' field
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})



@login_required
def clients_list(request):
    clients = Client.objects.order_by('-created_at')
    return render(request, 'dashboard/clients_list.html', {'clients': clients})

@login_required
def client_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if name:
            Client.objects.create(name=name, phone=phone, email=email)
            messages.success(request, f'Client "{name}" added successfully!')
            return redirect('clients_list')
        else:
            messages.error(request, 'Name is required.')

    return render(request, 'dashboard/client_form.html', {'action': 'Add'})

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if name:
            client.name = name
            client.phone = phone
            client.email = email
            client.save()
            messages.success(request, f'Client "{name}" updated successfully!')
            return redirect('clients_list')
        else:
            messages.error(request, 'Name is required.')

    return render(request, 'dashboard/client_form.html', {'action': 'Edit', 'client': client})

@login_required
def orders_list(request):
    # You can later add filters here for today/week/year
    orders = Order.objects.order_by('-created_at')
    return render(request, 'dashboard/orders_list.html', {'orders': orders})


@login_required
def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/clients_list.html', {'clients': clients})


@login_required
def client_add(request):
    if request.method == 'POST':
        Client.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone']
        )
        return redirect('clients_list')
    return render(request, 'dashboard/client_form.html')


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.name = request.POST['name']
        client.phone = request.POST['phone']
        client.save()
        return redirect('clients_list')

    return render(request, 'dashboard/client_form.html', {'client': client})


from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def orders_list(request):
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('search', '').strip()
    today = timezone.now().date()

    # Start with all orders
    orders = Order.objects.all()

    # Apply date filter only if there's no search query
    if not search_query:
        if filter_type == 'today':
            orders = orders.filter(created_at__date=today)
        elif filter_type == 'week':
            orders = orders.filter(created_at__date__gte=today - timedelta(days=7))
        elif filter_type == 'year':
            orders = orders.filter(created_at__year=today.year)

    # Apply search across all orders regardless of date filter
    if search_query:
        orders = orders.filter(
            Q(name__icontains=search_query) | Q(client__name__icontains=search_query)
        )

    total_revenue = sum(o.total_price for o in orders)

    return render(request, 'orders/orders_list.html', {
        'orders': orders.order_by('-created_at'),
        'filter_type': filter_type,
        'total_revenue': total_revenue,
        'search_query': search_query,
    })


def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def manage_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'dashboard/manage_users.html', {
        'users': users
    })


@login_required
@user_passes_test(admin_only)
@require_POST
def add_staff(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists")
        return redirect('manage_users')

    user = User.objects.create_user(
        username=username,
        password=password,
        is_staff=True
    )

    messages.success(request, f"Staff '{username}' added")
    return redirect('manage_users')

@login_required
@user_passes_test(admin_only)
def toggle_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    return redirect('manage_users')


@login_required
@user_passes_test(admin_only)
def toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('manage_users')