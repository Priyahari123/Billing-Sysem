

from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Denomination)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(BillItem)

