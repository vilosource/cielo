from django.shortcuts import render


def virtual_machines(request):
    vms = []
    return render(request, 'inventory/virtual_machines.html', {'vms': vms})


def storage_accounts(request):
    accounts = []
    return render(request, 'inventory/storage_accounts.html', {'accounts': accounts})
