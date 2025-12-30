from django.urls import path
from .views import *

urlpatterns = [
    path('', billing_page, name='billing'),
    path('generate-bill/', generate_bill, name='generate_bill'),
    path('bill/<int:bill_id>/', bill_view, name='bill_view'),
]
