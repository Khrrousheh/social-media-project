import datetime
from django.db import models


STATUS = [
    ('c', 'Completed'),
    ('p', 'Pending'),
    ('i', 'Incomplete'),
]


DEAL_TYPES = [
    ('invest', 'Investments'),
    ('sale', 'Sales'),
    ('rent', 'Rental'),
]

properties_type = [
    ('land', 'Land'),
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('hut', 'Hut'),
]

# class Deal(models):
#     # created_at = models.DateField(default=datetime.datetime.now().date())
#     pass
