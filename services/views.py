# services/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service


@login_required
def services_list(request):
    query = request.GET.get('q', '').strip()

    services = Service.objects.all().order_by('-id')

    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'services/services_list.html', {
        'services': services,
        'query': query
    })


@login_required
def service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm()

    return render(request, 'services/service_form.html', {
        'form': form,
        'title': 'Add Service'
    })


@login_required
def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'services/service_form.html', {
        'form': form,
        'title': f'Edit Service: {service.name}'
    })


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        service.delete()
        return redirect('services_list')

@csrf_exempt
def service_ajax_add(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            return JsonResponse({
                "success": True,
                "id": service.id,
                "label": service.name
            })
        return JsonResponse({"success": False, "errors": form.errors})