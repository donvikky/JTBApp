from django import forms
from django.forms import ModelForm
from django.forms import Form
from dashboard.models import (IndividualTaxPayer, CorporateTaxPayer, TaxOffice, SubsidiaryTaxPayer,
IndividualShareholder, CorporateShareholder)

class IndividualTaxPayerForm(ModelForm):
    class Meta:
        model = IndividualTaxPayer
        exclude = ('create_time','create_user','update_time','update_user','tin')
        widgets = {
            'surname':forms.TextInput(attrs={'class':'form-control','placeholder':'surname'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}),
            'other_name':forms.TextInput(attrs={'class':'form-control','placeholder':'other names'}),
            'marital_status':forms.Select(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'dob':forms.DateInput(attrs={'type':'date','class':'form-control','placeholder':'date of birth','pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}'}),
            'nationality':forms.Select(attrs={'class':'form-control','placeholder':'nationality'}),
            'state_of_origin':forms.Select(attrs={'class':'form-control'}),
            'lga_of_origin':forms.Select(attrs={'class':'form-control'}),
            'tax_payer_company':forms.TextInput(attrs={'class':'form-control','placeholder':'company name'}),
            'occupation':forms.TextInput(attrs={'class':'form-control','placeholder':'occupation'}),
            'employment_status':forms.Select(attrs={'class':'form-control'}),
            'residential_address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Residential Address'}),
            'phone':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'tax_office':forms.Select(attrs={'class':'form-control'}),
        }

class CorporateTaxPayerForm(ModelForm):
    class Meta:
        model = CorporateTaxPayer
        exclude = ('create_time','create_user','update_time','update_user')
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'address'}),
            'trade_name':forms.TextInput(attrs={'class':'form-control','placeholder':'trade name'}),
            'phone':forms.NumberInput(attrs={'class':'form-control','placeholder':'phone number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'tin':forms.TextInput(attrs={'class':'form-control','placeholder':'TIN'}),
            'company_size':forms.Select(attrs={'class':'form-control'}),
            'ownership_type':forms.Select(attrs={'class':'form-control',}),
            'reg_status':forms.Select(attrs={'class':'form-control',}),
            'reg_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'reg_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Registration Number'}),
            'line_of_business':forms.TextInput(attrs={'class':'form-control','placeholder':'Line of Business'}),
            'sector':forms.TextInput(attrs={'class':'form-control','placeholder':'Sector'}),
            'contact_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Contact name'}),
            'tax_office':forms.Select(attrs={'class':'form-control'}),
        }


class TaxOfficeForm(ModelForm):
    class Meta:
        model = TaxOffice
        exclude = ('create_time','create_user','update_time','update_user')
        widgets = {
            'state':forms.Select(attrs={'class':'form-control',}),
            'lga':forms.Select(attrs={'class':'form-control',}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'address'}),
            'status':forms.Select(attrs={'class':'form-control'}),            
        }

class SubsidiaryTaxPayerForm(ModelForm):
    class Meta:
        model = SubsidiaryTaxPayer
        exclude = ('create_time','create_user','update_time','update_user')
        widgets = {
            'parent_company':forms.Select(attrs={'class':'form-control',}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'name'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'address'}),
            'trade_name':forms.TextInput(attrs={'class':'form-control','placeholder':'trade name'}),
            'phone':forms.NumberInput(attrs={'class':'form-control','placeholder':'phone number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'tin':forms.TextInput(attrs={'class':'form-control','placeholder':'TIN'}),
            'company_size':forms.Select(attrs={'class':'form-control'}),
            'ownership_type':forms.Select(attrs={'class':'form-control',}),
            'reg_status':forms.Select(attrs={'class':'form-control',}),
            'reg_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'start_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'reg_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Registration Number'}),
            'line_of_business':forms.TextInput(attrs={'class':'form-control','placeholder':'Line of Business'}),
            'sector':forms.TextInput(attrs={'class':'form-control','placeholder':'Sector'}),
            'contact_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Contact name'}),
        }

class IndividualShareholderForm(ModelForm):
    class Meta:
        model = IndividualShareholder
        exclude = ('create_time','create_user','update_time','update_user','tin')
        widgets = {
            'company':forms.Select(attrs={'class':'form-control'}),
            'surname':forms.TextInput(attrs={'class':'form-control','placeholder':'surname'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}),
            'other_name':forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}),
            'nationality':forms.Select(attrs={'class':'form-control','placeholder':'nationality'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'residential_address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Residential Address'}),
            'position':forms.TextInput(attrs={'class':'form-control','placeholder':'Position'}),
            'phone':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'bvn':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BVN'}),
            'status':forms.Select(attrs={'class':'form-control', 'placeholder':'Status'}),
            'share':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Share holding'}),
        }

class CorporateShareholderForm(ModelForm):
    class Meta:
        model = CorporateShareholder
        exclude = ('create_time','create_user','update_time','update_user','tin')
        widgets = {
            'company':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'trade_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Trade name'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'address':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Address'}),
            'phone':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'reg_status':forms.Select(attrs={'class':'form-control', 'placeholder':'Registration Status'}),
            'tin':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'TIN'}),
            'bvn':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'BVN'}),
            'status':forms.Select(attrs={'class':'form-control', 'placeholder':'Status'}),
            'share':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Share holding'}),
        }

class IndividualTaxPayerReportForm(Form):
    tax_office = forms.CharField(label='Tax Office',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'Start Date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'End Date'}))

class CorporateTaxPayerReportForm(Form):
    tax_office = forms.CharField(label='Tax Office',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'Start Date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','placeholder':'End Date'}))
