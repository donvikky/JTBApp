from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView, ListView, DetailView,
 UpdateView, FormView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from dashboard.models import (IndividualTaxPayer, CorporateTaxPayer, TaxOffice, SubsidiaryTaxPayer,
IndividualShareholder, CorporateShareholder, Biometric, Agency, Bvn, Country, State, Lga)
from dashboard.forms import (IndividualTaxPayerForm, CorporateTaxPayerForm, TaxOfficeForm,
SubsidiaryTaxPayerForm, IndividualShareholderForm, CorporateShareholderForm,
IndividualTaxPayerReportForm, CorporateTaxPayerReportForm, BiometricForm)
from django.urls import reverse, reverse_lazy
import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
import requests


# Create your views here.
class StaffMemberMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class IndexView(LoginRequiredMixin, StaffMemberMixin,TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['individual_count'] = IndividualTaxPayer.objects.count()
        context['corporate_count'] = CorporateTaxPayer.objects.count()
        context['user_count'] = User.objects.count()
        # todays registrations
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        context['individual_today']= IndividualTaxPayer.objects.filter(create_time__range=(today_min, today_max)).count()
        context['corporate_today']= CorporateTaxPayer.objects.filter(create_time__range=(today_min, today_max)).count()
                
        # recent registrations
        context['individual_registrations'] = IndividualTaxPayer.objects.all().order_by('-create_time')[:5]
        context['corporate_registrations'] = CorporateTaxPayer.objects.all().order_by('-create_time')[:5]
        return context

class IndividualRegistrationView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/individual/individual_form.html'
    model = IndividualTaxPayer
    form_class = IndividualTaxPayerForm
    success_url = '/dashboard/registration-success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        office = self.request.user.profile.office
        context['office'] = office
        return context

    def form_valid(self, form):
        try:
            agency = Agency.objects.get(abbreviation='JTB')
        except Agency.DoesNotExist:
            agency = None

        form.instance.agency = agency
        form.instance.create_user = self.request.user
        return super().form_valid(form)

class IndividualRegistrations(StaffMemberMixin, ListView):
    model = IndividualTaxPayer
    template_name = 'dashboard/individual/individual_registrations.html'
    context_object_name = 'registrations'

class IndividualDetailView(StaffMemberMixin, DetailView):
    model = IndividualTaxPayer
    template_name = 'dashboard/individual/individual_detail.html'
    context_object_name = 'registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tax_payer = IndividualTaxPayer.objects.get(id=self.kwargs['pk'])
        try:
            context['biometric'] = Biometric.objects.get(tax_payer=tax_payer)
        except Biometric.DoesNotExist:
            context['biometric'] = None        
        return context

class IndividualUpdateView(StaffMemberMixin, UpdateView):
    template_name = 'dashboard/individual/individual_form.html'
    model = IndividualTaxPayer
    form_class = IndividualTaxPayerForm
    success_url = '/dashboard/registration-success'

    def form_valid(self, form):        
        form.instance.update_user = self.request.user       
        return super().form_valid(form)


class RegistrationSuccessView(TemplateView):
    template_name = 'dashboard/registration_success.html'

class CorporateRegistrationView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/corporate/corporate_form.html'
    model = CorporateTaxPayer
    form_class = CorporateTaxPayerForm
    success_url = '/dashboard/registration-success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        office = self.request.user.profile.office # tax office for the current user
        context['office'] = office
        return context

    def form_valid(self, form):
        try:
            agency = Agency.objects.get(abbreviation='JTB')
        except Agency.DoesNotExist:
            agency = None

        form.instance.agency = agency        
        form.instance.create_user = self.request.user
        form.instance.tax_office = self.request.user.profile.office       
        return super().form_valid(form)

class CorporateRegistrations(StaffMemberMixin, ListView):
    model = CorporateTaxPayer
    template_name = 'dashboard/corporate/corporate_registrations.html'
    context_object_name = 'registrations'

class CorporateDetailView(StaffMemberMixin, DetailView):
    model = CorporateTaxPayer
    template_name = 'dashboard/corporate/corporate_detail.html'
    context_object_name = 'registration'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        company = CorporateTaxPayer.objects.get(id=self.kwargs['pk'])
        context['ind_shareholders'] = IndividualShareholder.objects.filter(company=company)
        context['corp_shareholders'] = CorporateShareholder.objects.filter(company=company)
        return context

class CorporateUpdateView(StaffMemberMixin, UpdateView):
    template_name = 'dashboard/corporate/corporate_form.html'
    model = CorporateTaxPayer
    form_class = CorporateTaxPayerForm
    success_url = '/dashboard/registration-success'

    def form_valid(self, form):        
        form.instance.update_user = self.request.user       
        return super().form_valid(form)

class TaxOfficeListView(StaffMemberMixin, ListView):
    model = TaxOffice
    template_name = 'dashboard/tax_office/tax_offices.html'
    context_object_name = 'offices'

class TaxOfficeCreateView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/tax_office/tax_offices_form.html'
    model = TaxOffice
    form_class = TaxOfficeForm
    success_url = '/dashboard/registration-success'

    def form_valid(self, form):        
        form.instance.create_user = self.request.user       
        return super().form_valid(form)

class TaxOfficeUpdateView(StaffMemberMixin, UpdateView):
    template_name = 'dashboard/tax_office/tax_offices_form.html'
    model = TaxOffice
    form_class = TaxOfficeForm
    success_url = '/dashboard/registration-success'

    def form_valid(self, form):        
        form.instance.update_user = self.request.user       
        return super().form_valid(form)

class TaxOfficeDetailView(StaffMemberMixin, DetailView):
    model = TaxOffice
    template_name = 'dashboard/tax_office/tax_offices_detail.html'
    context_object_name = 'office'

class SubsidiaryRegistrationView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/subsidiary/subsidiary_form.html'
    model = SubsidiaryTaxPayer
    form_class = SubsidiaryTaxPayerForm
    success_url = '/dashboard/registration-success'

class SubsidiaryRegistrations(StaffMemberMixin, ListView):
    model = SubsidiaryTaxPayer
    template_name = 'dashboard/subsidiary/subsidiary_registrations.html'
    context_object_name = 'subsidiaries'

class SubsidiaryDetailView(StaffMemberMixin, DetailView):
    model = SubsidiaryTaxPayer
    template_name = 'dashboard/subsidiary/subsidiary_detail.html'
    context_object_name = 'subsidiary'

class SubsidiaryUpdateView(StaffMemberMixin, UpdateView):
    template_name = 'dashboard/subsidiary/subsidiary_form.html'
    model = SubsidiaryTaxPayer
    form_class = SubsidiaryTaxPayerForm
    success_url = '/dashboard/registration-success'

    def form_valid(self, form):        
        form.instance.update_user = self.request.user       
        return super().form_valid(form)

class IndividualShareholderCreateView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/individual_shareholder/individual_form.html'
    model = IndividualShareholder
    form_class = IndividualShareholderForm
    #success_url = reverse('dashboard:corporate-detail', kwargs={'pk': self.company.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['company'] = CorporateTaxPayer.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):        
        form.instance.create_user = self.request.user       
        return super().form_valid(form)
"""
# Not yet implemented
class IndividualShareholderUpdateView(StaffMemberMixin, UpdateView):
    template_name = 'dashboard/individual_shareholder/individual_form.html'
    model = IndividualShareholder
    form_class = IndividualShareholderForm
    #success_url = '/dashboard/registration-success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['company'] = CorporateTaxPayer.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):        
        form.instance.update_user = self.request.user       
        return super().form_valid(form)

class IndividualShareholderListView(StaffMemberMixin, ListView):
    model = IndividualTaxPayer
    template_name = 'dashboard/individual_shareholder/individual_shareholders.html'
    context_object_name = 'shareholders'

class IndividualShareholderDetailView(StaffMemberMixin, DetailView):
    model = IndividualTaxPayer
    template_name = 'dashboard/individual/individual_detail.html'
    context_object_name = 'registration'
"""
class CorporateShareholderCreateView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/corporate_shareholder/corporate_form.html'
    model = CorporateShareholder
    form_class = CorporateShareholderForm
    #success_url = reverse('dashboard:corporate-detail', kwargs={'pk': self.company.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['company'] = CorporateTaxPayer.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):        
        form.instance.create_user = self.request.user       
        return super().form_valid(form)


class IndividualTaxPayerReport(StaffMemberMixin, FormView):
    template_name = 'dashboard/reports/individual_form.html'
    model = IndividualTaxPayer
    form_class = IndividualTaxPayerReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offices'] = TaxOffice.objects.all()
        return context

    def form_valid(self, form):
        tax_office = self.request.POST['tax_office']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        return HttpResponseRedirect(reverse('dashboard:individual-taxpayer-report-view',
        kwargs={'tax_office': tax_office,'start_date':start_date, 'end_date': end_date}))
    
class IndividualTaxPayerReportView(StaffMemberMixin, TemplateView):
    template_name = 'dashboard/reports/individual_report.html'

    def get_context_data(self, **kwargs):
        tax_office_id = self.kwargs['tax_office']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        tax_office = TaxOffice.objects.get(id=tax_office_id)
        context = super().get_context_data(**kwargs)
        context['office'] = tax_office
        context['registrations'] = IndividualTaxPayer.objects.filter(tax_office=tax_office).filter(
            create_time__range=(start_date, end_date)
        )
        return context

class CorporateTaxPayerReport(StaffMemberMixin, FormView):
    template_name = 'dashboard/reports/corporate_form.html'
    form_class = CorporateTaxPayerReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offices'] = TaxOffice.objects.all()
        return context

    def form_valid(self, form):
        tax_office = self.request.POST['tax_office']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        return HttpResponseRedirect(reverse('dashboard:corporate-taxpayer-report-view',
         kwargs={'tax_office': tax_office,'start_date':start_date, 'end_date': end_date}))
    
class CorporateTaxPayerReportView(StaffMemberMixin, TemplateView):
    template_name = 'dashboard/reports/corporate_report.html'

    def get_context_data(self, **kwargs):
        tax_office_id = self.kwargs['tax_office']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        tax_office = TaxOffice.objects.get(id=tax_office_id)
        context = super().get_context_data(**kwargs)
        context['office'] = tax_office
        context['registrations'] = CorporateTaxPayer.objects.filter(tax_office=tax_office).filter(
            create_time__range=(start_date, end_date)
        )
        return context

class BiometricCreateView(StaffMemberMixin, CreateView):
    template_name = 'dashboard/biometric/form.html'
    model = Biometric
    form_class = BiometricForm    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tax_payer'] = IndividualTaxPayer.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):        
        form.instance.create_user = self.request.user       
        return super().form_valid(form)

class BVNInitiateData(StaffMemberMixin, TemplateView):
    template_name = 'dashboard/bvn/index.html'

class BVNRequestData(StaffMemberMixin, TemplateView):  
    template_name = 'dashboard/bvn/request.html'

    def get(self, request):
        # get BVN url and access token
        records = []
        old_records = []
        new_records = []
        message = ''
        bvn_info = get_object_or_404(Agency,abbreviation='BVN')
        url = bvn_info.url
        access_token = bvn_info.access_token
        headers = {'Authorization':'Bearer '+ access_token}

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            response = r.json()
            if len(response) < 1:
                message = 'No records were returned'
            else:
                records = response
                # check if record already exists in database
                for record in records:
                    # fetch details and create new object
                    lga = Lga.objects.get(pk=record['lga_of_origin_id'])
                    state = State.objects.get(pk=record['state_of_origin_id'])
                    nationality = Country.objects.get(pk=record['nationality_id'])                    

                    # save new record
                    b = Bvn()
                    b.surname = record['surname']
                    b.first_name = record['first_name']
                    b.other_name = record['other_name']
                    b.marital_status = record['marital_status']
                    b.gender = record['gender']
                    b.dob = record['dob']
                    b.bvn = record['bvn']
                    b.lga_of_origin = lga
                    b.state_of_origin = state
                    b.nationality = nationality
                    b.occupation = record['occupation']
                    b.employment_status = record['employment_status']
                    b.residential_address = record['residential_address']
                    b.phone = record['phone']
                    b.email = record['email']
                    b.tax_office = request.user.profile.office
                    b.agency = Agency.objects.get(abbreviation='BVN')                    

                    rec = Bvn.objects.filter(bvn=record['bvn']) # check if this record exists
                    if rec:
                        for r in rec:                        
                            old_records.append(r)                        
                    else:
                        b.save()                        
                        new_records.append(b)
                
                    
        else:
            raise Http404('The request was not successful. Reason:'+ r.reason)
        
        return render(request, self.template_name, {'message':message,'old_records':old_records,
        'new_records':new_records})

class BVNListData(StaffMemberMixin, View):
    pass


class BVNDetailData(StaffMemberMixin, DetailView):
    template_name = 'dashboard/bvn/detail.html'
    context_object_name = 'registration'
    model = Bvn   


class BVNGenerateTIN(StaffMemberMixin, TemplateView):
    pass

