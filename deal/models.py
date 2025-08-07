import datetime
from django.db import models, transaction
from django.core.exceptions import ValidationError
from users.models import App_users

STATUS = [
    ('c', 'Completed'),
    ('p', 'Pending'),
    ('i', 'Incomplete'),
    ('x', 'Closed'),
]

CONTRACT_TYPES = [
    ('invest', 'Investments'),
    ('sale', 'Sales'),
    ('rent', 'Rental'),
]

PROPERTY_TYPES = [
    ('land', 'Land'),
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('hut', 'Hut'),
]


class Contract(models.Model):
    open_at = models.DateTimeField("publish at", default=datetime.datetime.now, null=False)
    created_by = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='contracts_created')
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES, null=False)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_deal = models.ForeignKey('Deal', null=True, blank=True, on_delete=models.SET_NULL, related_name='closed_contracts')

    def __str__(self):
        return f"Contract {self.id} - {self.contract_type} - {self.property_type}"

    def clean(self):
        if self.open_at < datetime.datetime.now():
            raise ValidationError({'open_at': 'The contract publication date cannot be in the past.'})
        super().clean()

    @transaction.atomic
    def close_contract(self, deal):
        if self.closed_at:
            raise ValidationError("This contract is already closed.")

        self.closed_deal = deal
        self.closed_at = datetime.datetime.now()
        self.save()

        deal.status = 'c'
        deal.save()

    def add_comment(self, user, content):
        comment = ContractComment(contract=self, user=user, content=content)
        comment.save()


class AbstractPropertyContract(Contract):
    num_bedrooms = models.IntegerField(default=1)
    num_bathrooms = models.IntegerField(default=1)

    def clean(self):
        if self.num_bedrooms < 1:
            raise ValidationError({'num_bedrooms': 'Number of bedrooms must be at least 1.'})
        if self.num_bathrooms < 1:
            raise ValidationError({'num_bathrooms': 'Number of bathrooms must be at least 1.'})
        super().clean()

    def __str__(self):
        return f"{self.property_type.capitalize()} Contract {self.id}"


class LandContract(AbstractPropertyContract):
    land_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size of the land in square meters")
    is_agricultural = models.BooleanField(default=False, help_text="Indicates if land is agricultural")

    def clean(self):
        if self.land_size <= 0:
            raise ValidationError({'land_size': 'Land size must be greater than zero.'})
        super().clean()

    def __str__(self):
        return f"Land Contract {self.id}"


class ApartmentContract(AbstractPropertyContract):
    floor_number = models.IntegerField()
    has_parking = models.BooleanField(default=False)

    def clean(self):
        if self.floor_number < 1:
            raise ValidationError({'floor_number': 'Floor number must be at least 1.'})
        super().clean()

    def __str__(self):
        return f"Apartment Contract {self.id}"


class HouseContract(AbstractPropertyContract):
    has_garden = models.BooleanField(default=False)

    def clean(self):
        super().clean()  # No extra validations specific to House contract
        return super().clean()

    def __str__(self):
        return f"House Contract {self.id}"


class HutContract(Contract):
    is_rural = models.BooleanField(default=False, help_text="Indicates if hut is in a rural area")

    def __str__(self):
        return f"Hut Contract {self.id}"

    def clean(self):
        super().clean()  # No additional validations required here.


class Deal(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='deals')
    contract_owner = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='deals_owned')
    witness_1 = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='witness_1', null=True, blank=True)
    witness_2 = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='witness_2', null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='p')

    def __str__(self):
        return f"Deal {self.id} for Contract {self.contract.id} - Status: {self.get_status_display()}"

    def clean(self):
        if not self.contract_owner:
            raise ValidationError({'contract_owner': 'A valid contract owner must be specified.'})

        if not self.witness_1 and not self.witness_2:
            raise ValidationError({'witnesses': 'At least one witness must be provided.'})

        if self.status not in dict(STATUS):
            raise ValidationError({'status': 'Invalid status.'})

        super().clean()

    def add_comment(self, user, content):
        """ Reusable method to add comments to the deal. """
        comment = DealComment(deal=self, user=user, content=content)
        comment.save()


class ContractComment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='contract_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Contract {self.contract.id} by {self.user.username}"

    class Meta:
        ordering = ['created_at']


class DealComment(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(App_users, on_delete=models.CASCADE, related_name='deal_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Deal {self.deal.id} by {self.user.username}"

    class Meta:
        ordering = ['created_at']
