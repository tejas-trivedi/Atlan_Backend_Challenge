from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from gsheets import mixins
from uuid import uuid4

class Client_Income_Data(#mixins.SheetSyncableMixin,
 models.Model):
    # spreadsheet_id = '18F_HLftNtaouHgA3fmfT2M1Va9oO-YWTBw2EDsuz8V4'
    # model_id_field = 'guid'
    # guid = models.CharField(primary_key=True, max_length=255, default=uuid4)

    client_email = models.EmailField(blank=True)
    client_name = models.CharField(max_length=255, blank=True)
    income_per_annum = models.FloatField(blank=True, default=None)
    savings_per_annum = models.FloatField(blank=True, default=None)
    mobile_number = PhoneNumberField(null=False, blank=False, unique=True)






