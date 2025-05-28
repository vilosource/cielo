from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from inventory.models import AzureSubscription, VirtualMachine

class Command(BaseCommand):
    help = 'Populates the database with sample AzureSubscription and VirtualMachine data for development.'

    # Define your sample subscription data here
    SAMPLE_SUBSCRIPTIONS = [
        {'name': 'Cielo Production Subscription', 'subscription_id': 'aaaaaaaa-bbbb-cccc-dddd-prod000001'},
        {'name': 'Cielo Development Subscription', 'subscription_id': 'bbbbbbbb-cccc-dddd-eeee-dev000002'},
        {'name': 'Cielo UAT Subscription', 'subscription_id': 'cccccccc-dddd-eeee-ffff-uat0000003'},
    ]

    SAMPLE_VMS_PER_SUBSCRIPTION = {
        'aaaaaaaa-bbbb-cccc-dddd-prod000001': [
            {'name': 'cielo-prod-web-01', 'location': 'East US', 'environment': 'Production'},
            {'name': 'cielo-prod-web-02', 'location': 'East US', 'environment': 'Production'},
            {'name': 'cielo-prod-app-01', 'location': 'East US', 'environment': 'Production'},
            {'name': 'cielo-prod-db-01', 'location': 'East US', 'environment': 'Production'},
            {'name': 'cielo-prod-cache-01', 'location': 'East US', 'environment': 'Production'},
        ],
        'bbbbbbbb-cccc-dddd-eeee-dev000002': [
            {'name': 'cielo-dev-tools-01', 'location': 'West Europe', 'environment': 'Development'},
            {'name': 'cielo-dev-frontend-01', 'location': 'West Europe', 'environment': 'Development'},
            {'name': 'cielo-dev-backend-01', 'location': 'West Europe', 'environment': 'Development'},
            {'name': 'cielo-dev-testrig-01', 'location': 'West Europe', 'environment': 'Development'},
            {'name': 'cielo-dev-sandbox-01', 'location': 'West Europe', 'environment': 'Development'},
            {'name': 'cielo-dev-jumphost-01', 'location': 'West Europe', 'environment': 'Development'},
        ],
        'cccccccc-dddd-eeee-ffff-uat0000003': [
            {'name': 'cielo-uat-app-01', 'location': 'Central US', 'environment': 'UAT'},
            {'name': 'cielo-uat-db-01', 'location': 'Central US', 'environment': 'UAT'},
            {'name': 'cielo-uat-loadgen-01', 'location': 'Central US', 'environment': 'UAT'},
            {'name': 'cielo-uat-reporting-01', 'location': 'Central US', 'environment': 'UAT'},
        ]
    }

    def _create_subscriptions(self):
        created_subs_count = 0
        self.stdout.write(self.style.NOTICE('Creating subscriptions...'))
        for sub_data in self.SAMPLE_SUBSCRIPTIONS:
            subscription, created = AzureSubscription.objects.get_or_create(
                subscription_id=sub_data['subscription_id'],
                defaults={'name': sub_data['name']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Successfully created subscription: "{subscription.name}"'))
                created_subs_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'  Subscription "{subscription.name}" already exists.'))
        self.stdout.write(self.style.SUCCESS(f'{created_subs_count} new subscriptions processed/added.'))


    def _create_virtual_machines(self):
        created_vms_count = 0
        self.stdout.write(self.style.NOTICE('Creating virtual machines...'))
        for sub_id, vms_data in self.SAMPLE_VMS_PER_SUBSCRIPTION.items():
            try:
                subscription = AzureSubscription.objects.get(subscription_id=sub_id)
                self.stdout.write(self.style.NOTICE(f'  Processing VMs for subscription: "{subscription.name}"'))
                for vm_data in vms_data:
                    vm, created = VirtualMachine.objects.get_or_create(
                        name=vm_data['name'],
                        subscription=subscription, # Ensure VMs are linked to the correct subscription
                        defaults={'location': vm_data['location'], 'environment': vm_data['environment']}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'    Successfully created VM: "{vm.name}"'))
                        created_vms_count +=1
                    else:
                        self.stdout.write(self.style.WARNING(f'    VM "{vm.name}" under subscription "{subscription.name}" already exists.'))

            except AzureSubscription.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  Subscription with ID {sub_id} not found. Skipping VMs for it.'))
        self.stdout.write(self.style.SUCCESS(f'{created_vms_count} new virtual machines processed/added.'))

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting to populate inventory data...'))
        self._create_subscriptions()
        self._create_virtual_machines()
        self.stdout.write(self.style.SUCCESS('Finished populating inventory data.'))