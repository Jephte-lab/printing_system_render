from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import ClientForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def clients_list(request):
    query = request.GET.get('q')

    clients = Client.objects.all().order_by('-id')

    if query:
        clients = clients.filter(name__icontains=query)

    return render(request, 'clients/clients_list.html', {
        'clients': clients,
        'query': query,
    })

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'client': client
    })

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.delete()

    return redirect('clients_list')


@csrf_exempt
def client_ajax_add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                "success": True,
                "id": client.id,
                "label": str(client)
            })
        return JsonResponse({"success": False, "errors": form.errors})

@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('clients_list')

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Add Client'
    })
