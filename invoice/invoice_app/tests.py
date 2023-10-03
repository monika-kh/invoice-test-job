from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail


class InvoiceViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_invoice_with_details(self):
        data = {
            "customer_name": "Test Customer",
            "details": [
                {
                    "description": "Item 1",
                    "quantity": 2,
                    "unit_price": "10.00",
                    "price": "20.00",
                },
                {
                    "description": "Item 2",
                    "quantity": 3,
                    "unit_price": "15.00",
                    "price": "45.00",
                },
            ],
        }

        response = self.client.post("/api/invoices/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        invoice = Invoice.objects.get(id=response.data["id"])
        self.assertEqual(invoice.customer_name, "Test Customer")
        self.assertEqual(invoice.details.count(), 2)

    def test_update_invoice_with_details(self):
        invoice = Invoice.objects.create(customer_name="Initial Customer")
        InvoiceDetail.objects.create(
            invoice=invoice,
            description="Initial Item",
            quantity=1,
            unit_price="5.00",
            price=20,
        )

        data = {
            "id": 1,
            "customer_name": "Updated Customer",
            "details": [
                {
                    "id": 1,
                    "description": "Updated Item",
                    "quantity": 2,
                    "unit_price": "10.00",
                    "price": "20",
                }
            ],
        }

        response = self.client.put(f"/api/invoices/{invoice.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invoice = Invoice.objects.get(id=invoice.id)
        self.assertEqual(invoice.customer_name, "Updated Customer")
        self.assertEqual(invoice.details.count(), 1)
        detail = invoice.details.first()
        self.assertEqual(detail.description, "Updated Item")
        self.assertEqual(detail.quantity, 2)

    def test_update_invoice_with_non_existing_details(self):
        invoice = Invoice.objects.create(customer_name="Initial Customer")
        InvoiceDetail.objects.create(
            invoice=invoice,
            description="Initial Item",
            quantity=1,
            unit_price="5.00",
            price=20,
        )

        data = {
            "customer_name": "Updated Customer",
            "details": [
                {
                    "id": 999,  # Non-existing detail ID
                    "description": "Updated Item",
                    "quantity": 2,
                    "unit_price": "10.00",
                    "price": 20,
                }
            ],
        }

        response = self.client.put(f"/api/invoices/{invoice.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
