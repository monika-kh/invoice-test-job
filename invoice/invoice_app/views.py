from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer


class InvoiceView(APIView):
    def post(self, request, format=None):
        invoice_data = request.data
        details_data = invoice_data.pop("details", [])
        try:
            invoice_serializer = InvoiceSerializer(data=invoice_data)
            if invoice_serializer.is_valid():
                invoice = invoice_serializer.save()
                for detail_data in details_data:
                    detail_data["invoice"] = invoice_serializer.data["id"]
                    detail_serializer = InvoiceDetailSerializer(data=detail_data)
                    if detail_serializer.is_valid():
                        detail_serializer.save()
                    else:
                        return Response(
                            detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )

                return Response(invoice_serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(e)

    def put(self, request, invoice_id, format=None):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND
            )

        invoice_data = request.data
        details_data = invoice_data.pop("details", [])
        invoice_serializer = InvoiceSerializer(instance=invoice, data=invoice_data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            if invoice:
                for detail_data in details_data:
                    detail_data["invoice"] = invoice_id
                    invoice_detail = InvoiceDetail.objects.get(id=detail_data["id"])
                    if invoice_detail and (invoice_detail.invoice_id == invoice_id):
                        detail_serializer = InvoiceDetailSerializer(
                            invoice_detail, data=detail_data
                        )
                        if detail_serializer.is_valid():
                            detail_serializer.save()
                        else:
                            return Response(
                                detail_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        return Response(
                            {"error: object not found"},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                return Response(invoice_serializer.data, status=status.HTTP_200_OK)
        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
