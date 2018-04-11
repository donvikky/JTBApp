from django.shortcuts import render
from rest_framework import viewsets
from dashboard.models import IndividualTaxPayer, CorporateTaxPayer
from api.serializers import IndividualTaxPayerSerializer, CorporateTaxPayerSerializer

# Create your views here.
class IndividualTaxPayerViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows an Individual Tax Payer to be viewed or edited.
    """
    queryset = IndividualTaxPayer.objects.all().order_by('-create_time')
    serializer_class = IndividualTaxPayerSerializer

class CorporateTaxPayerViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows a Corprate Tax Payer to be viewed or edited.
    """
    queryset = CorporateTaxPayer.objects.all().order_by('-create_time')
    serializer_class = CorporateTaxPayerSerializer
