from django.urls import path
from django.contrib.auth import views as auth_views
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('individual-registration', views.IndividualRegistrationView.as_view(),name='individual-registration'),
    path('individual-detail/<int:pk>/', views.IndividualDetailView.as_view(),name='individual-detail'),
    path('individual-detail/update/<int:pk>/', views.IndividualUpdateView.as_view(),name='individual-detail-update'),
    path('individual-registrations', views.IndividualRegistrations.as_view(),name='individual-registrations'),
    path('registration-success', views.RegistrationSuccessView.as_view(),name='registration-success'),
    path('corporate-registration', views.CorporateRegistrationView.as_view(),name='corporate-registration'),
    path('corporate-registrations', views.CorporateRegistrations.as_view(),name='corporate-registrations'),
    path('corporate-detail/<int:pk>/', views.CorporateDetailView.as_view(),name='corporate-detail'),
    path('corporate-detail/update/<int:pk>/', views.CorporateUpdateView.as_view(),name='corporate-detail-update'),
    path('tax-office-create', views.TaxOfficeCreateView.as_view(),name='tax-office-create'),
    path('tax-office-update/<int:pk>/', views.TaxOfficeUpdateView.as_view(),name='tax-office-update'),
    path('tax-office-detail/<int:pk>/', views.TaxOfficeDetailView.as_view(),name='tax-office-detail'),
    path('tax-offices', views.TaxOfficeListView.as_view(),name='tax-offices'),
    path('subsidiary-registration', views.SubsidiaryRegistrationView.as_view(),name='subsidiary-registration'),
    path('subsidiary-registrations', views.SubsidiaryRegistrations.as_view(),name='subsidiary-registrations'),
    path('subsidiary-detail/<int:pk>/', views.SubsidiaryDetailView.as_view(),name='subsidiary-detail'),
    path('subsidiary-detail/update/<int:pk>/', views.SubsidiaryUpdateView.as_view(),name='subsidiary-detail-update'),
    path('individual-shareholder-create/<int:pk>', views.IndividualShareholderCreateView.as_view(),name='individual-shareholder-create'),
    path('corporate-shareholder-create/<int:pk>', views.CorporateShareholderCreateView.as_view(),name='corporate-shareholder-create'),
    path('individual-taxpayer-report', views.IndividualTaxPayerReport.as_view(),name='individual-taxpayer-report'),
    path('individual-taxpayer-report-view/<int:tax_office>/<start_date>/<end_date>/', views.IndividualTaxPayerReportView.as_view(),name='individual-taxpayer-report-view'),
    path('corporate-taxpayer-report', views.CorporateTaxPayerReport.as_view(),name='corporate-taxpayer-report'),
    path('corporate-taxpayer-report-view/<int:tax_office>/<start_date>/<end_date>/', views.CorporateTaxPayerReportView.as_view(),name='corporate-taxpayer-report-view'),
    path('biometric-capture/<int:pk>', views.BiometricCreateView.as_view(),name='biometric-capture'),
    path('bvn-initiate-data', views.BVNInitiateData.as_view(),name='bvn-initiate-data'),
    path('bvn-request-data', views.BVNRequestData.as_view(),name='bvn-request-data'),
    path('bvn-list-data', views.BVNListData.as_view(),name='bvn-list-data'),
    path('bvn-detail-data/<int:pk>/', views.BVNDetailData.as_view(),name='bvn-detail-data'),
]
