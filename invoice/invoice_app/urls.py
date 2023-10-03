from django.urls import path
from .views import InvoiceView

urlpatterns = [
    path("invoices/", InvoiceView.as_view(), name="invoice"),
    path("invoices/<int:invoice_id>", InvoiceView.as_view(), name="invoice-update"),
]
