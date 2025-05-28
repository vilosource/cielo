from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import AzureSubscription, VirtualMachine # Import models


def virtual_machines(request):
    # Fetch VirtualMachine objects from the database
    vm_list = VirtualMachine.objects.select_related('subscription').all().order_by('name')
    # The .select_related('subscription') is an optimization to fetch
    # the related AzureSubscription object in the same query,
    # preventing N+1 queries if you access subscription details in the template.

    paginator = Paginator(vm_list, 5) # Show 5 VMs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/virtual_machines.html', {
        'page_obj': page_obj
    })


def storage_accounts(request):
    accounts = []
    return render(request, 'inventory/storage_accounts.html', {'accounts': accounts})

def azure_subscription_detail(request, pk):
    subscription = get_object_or_404(AzureSubscription, pk=pk)
    # For now, just passing the subscription object.
    # Later, you might fetch VMs or other resources related to this subscription.
    return render(request, 'inventory/azure_subscription_detail.html', {
        'subscription': subscription
    })
