from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import AzureSubscription, VirtualMachine # Import models
import logging

logger = logging.getLogger(__name__)


def virtual_machines(request):
    logger.debug(f"virtual_machines view called by user: {request.user}")
    logger.debug(f"User authenticated: {request.user.is_authenticated}")
    # Fetch VirtualMachine objects from the database
    vm_list = VirtualMachine.objects.select_related('subscription').all().order_by('name')
    # The .select_related('subscription') is an optimization to fetch
    # the related AzureSubscription object in the same query,
    # preventing N+1 queries if you access subscription details in the template.

    paginator = Paginator(vm_list, 5) # Show 5 VMs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    logger.debug(f"Rendering virtual_machines template with {len(vm_list)} VMs")
    return render(request, 'inventory/virtual_machines.html', {
        'page_obj': page_obj
    })


def storage_accounts(request):
    logger.debug(f"storage_accounts view called by user: {request.user}")
    accounts = []
    return render(request, 'inventory/storage_accounts.html', {'accounts': accounts})

def azure_subscription_detail(request, pk):
    logger.debug(f"azure_subscription_detail view called by user: {request.user} for pk: {pk}")
    subscription = get_object_or_404(AzureSubscription, pk=pk)
    # For now, just passing the subscription object.
    # Later, you might fetch VMs or other resources related to this subscription.
    return render(request, 'inventory/azure_subscription_detail.html', {
        'subscription': subscription
    })
