from rest_framework import serializers
from dashboard.models import IndividualTaxPayer, CorporateTaxPayer, Country, State, Lga

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id','name')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id','name')

class LgaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lga
        fields = ('id','state','name')

class IndividualTaxPayerSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return IndividualTaxPayer.objects.create(**validated_data)

    class Meta:
        model = IndividualTaxPayer
        fields = ('surname', 'first_name', 'other_name', 'marital_status','gender', 'dob', 'tin', 'lga_of_origin',
        'state_of_origin', 'nationality', 'tax_payer_company', 'occupation', 'employment_status', 'residential_address',
        'phone', 'email')


class CorporateTaxPayerSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return CorporateTaxPayer.objects.create(**validated_data)

    class Meta:
        model = CorporateTaxPayer
        exclude = ('create_time','create_user','update_time','update_user')
