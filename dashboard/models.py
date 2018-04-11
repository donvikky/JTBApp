from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.urls import reverse

# Create your models here.
User = get_user_model()

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Lga(models.Model):
    state = models.ForeignKey(State,related_name='lgas',on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class TaxOffice(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    state = models.ForeignKey(State,related_name='state',on_delete=models.CASCADE)
    lga = models.ForeignKey(Lga,related_name='lga',on_delete=models.CASCADE)
    name = models.CharField('Tax Office Name',max_length=250)
    address = models.TextField()
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='taxoffice_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='taxoffice_updater',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class IndividualTaxPayer(models.Model):
    MARITAL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    EMPLOYMENT_STATUS_CHOICES = (
        ('Unemployed', 'Unemployed'),
        ('Self Employed', 'Self Employed'),
        ('Employed', 'Employed'),
    )
    surname = models.CharField('Surname', max_length=75)
    first_name = models.CharField('First Name', max_length=75)
    other_name = models.CharField('Other Name', max_length=75, null=True)
    marital_status = models.CharField('Marital Status', max_length=20, choices=MARITAL_STATUS_CHOICES)
    gender = models.CharField('Gender', max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField('Date of Birth')
    tin = models.CharField('JTB TIN', max_length=10,blank=True, null=True, unique=True)
    lga_of_origin = models.ForeignKey(Lga,related_name='individual_lga',on_delete=models.CASCADE)
    state_of_origin = models.ForeignKey(State,related_name='individual_state',on_delete=models.CASCADE)
    nationality = models.ForeignKey(Country,related_name='individual_nationality',on_delete=models.CASCADE)
    tax_payer_company = models.CharField('Company', max_length=150)
    occupation = models.CharField('Occupation', max_length=75)
    employment_status = models.CharField('Employment Status', max_length=20, choices=EMPLOYMENT_STATUS_CHOICES)
    residential_address = models.TextField()
    phone = models.CharField('Phone', max_length=15,)
    email = models.EmailField('Email', unique=True)
    tax_office = models.ForeignKey(TaxOffice,related_name='individual_tax_office',null=True,on_delete=models.CASCADE)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='individual_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='individual_updater',null=True,on_delete=models.CASCADE)

    def full_name(self):
        return '{} {}'.format(self.first_name, self.surname)
    
    def __str__(self):
        return '{} (TIN: {})'.format(self.full_name, self.tin or 'N/A')

    def lga(self):
        return self.lga_of_origin.id

    def full_name(self):
        return ''.format(self.first_name, self.surname)

    def TIN(self):
        return '%s%s' % (self.tin, settings.JTB_INDIVIVIDUAL_REG_IDENTIFIER)

class CorporateTaxPayer(models.Model):
    COMPANY_SIZE_CHOICES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )
    OWNERSHIP_TYPE_CHOICES = (
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('Trusteeship', 'Trusteeship'),
        ('Companies Limited By Guarantee', 'Companies Limited By Guarantee'),
        ('Federal MDAs', 'Federal MDAs'),
        ('State MDAs', 'State MDAs'),
        ('Foreign/Non-resident Companies', 'Foreign/Non-resident Companies'),
        ('Partnership', 'Partnership'),
        ('Private Unlimited Company', 'Private Unlimited Company'),
        ('Sole Proprietorship', 'Sole Proprietorship'),
    )
    REGISTRATION_STATUS_CHOICES = (
        ('Registered', 'Registered'),
        ('Unregistered', 'Unregistered'),
    )
    name = models.CharField('Registration Name', max_length=150)
    address = models.TextField()
    trade_name = models.CharField('Trade Name', max_length=150)
    phone = models.CharField('Phone', max_length=15)
    email = models.EmailField('Email')
    tin = models.CharField('JTB TIN', max_length=10, blank=True, null=True, unique=True)
    company_size = models.CharField('Company Size', max_length=20, choices=COMPANY_SIZE_CHOICES)
    ownership_type = models.CharField('Organization Type', max_length=75, choices=OWNERSHIP_TYPE_CHOICES)
    reg_status = models.CharField('Registration Status', max_length=20, choices=REGISTRATION_STATUS_CHOICES)
    reg_date = models.DateField('CAC Registration Date', blank=True, null=True)
    start_date = models.DateField('Business Start Date')
    reg_no = models.CharField('Registration Number', max_length=20, blank=True, null=True)
    line_of_business = models.CharField('Line of Business', max_length=75)
    sector = models.CharField('Sector', max_length=75)
    contact_name = models.CharField('Contact Name', max_length=150)
    tax_office = models.ForeignKey(TaxOffice,related_name='corporate_tax_office',null=True,on_delete=models.CASCADE)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='corporate_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='corporate_updater',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return '{} (TIN: {})'.format(self.name, self.tin or 'N/A')

    def TIN(self):
        return '%s%s' % (self.tin, settings.JTB_CORPORATE_REG_IDENTIFIER)

    class Meta:
        verbose_name = 'Corporate Tax Payer'


class SubsidiaryTaxPayer(models.Model):
    COMPANY_SIZE_CHOICES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )
    OWNERSHIP_TYPE_CHOICES = (
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('Trusteeship', 'Trusteeship'),
        ('Companies Limited By Guarantee', 'Companies Limited By Guarantee'),
        ('Federal MDAs', 'Federal MDAs'),
        ('State MDAs', 'State MDAs'),
        ('Foreign/Non-resident Companies', 'Foreign/Non-resident Companies'),
        ('Partnership', 'Partnership'),
        ('Private Unlimited Company', 'Private Unlimited Company'),
        ('Sole Proprietorship', 'Sole Proprietorship'),
    )
    REGISTRATION_STATUS_CHOICES = (
        ('Registered', 'Registered'),
        ('Unregistered', 'Unregistered'),
    )
    parent_company = models.ForeignKey(CorporateTaxPayer,related_name='parent_company',null=True,on_delete=models.CASCADE)
    name = models.CharField('Registration Name', max_length=150)
    address = models.TextField()
    trade_name = models.CharField('Trade Name', max_length=150)
    phone = models.CharField('Phone', max_length=15)
    email = models.EmailField('Email')
    tin = models.CharField('JTB TIN', max_length=10, blank=True, null=True, unique=True)
    company_size = models.CharField('Company Size', max_length=20, choices=COMPANY_SIZE_CHOICES)
    ownership_type = models.CharField('Organization Type', max_length=75, choices=OWNERSHIP_TYPE_CHOICES)
    reg_status = models.CharField('Registration Status', max_length=20, choices=REGISTRATION_STATUS_CHOICES)
    reg_date = models.DateField('CAC Registration Date', blank=True, null=True)
    start_date = models.DateField('Business Start Date')
    reg_no = models.CharField('Registration Number', max_length=20, blank=True, null=True)
    line_of_business = models.CharField('Line of Business', max_length=75)
    sector = models.CharField('Sector', max_length=75)
    contact_name = models.CharField('Contact Name', max_length=150)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='subsidiary_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='subsidiary_updater',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return '{} (TIN: {})'.format(self.name, self.tin or 'N/A')

    def TIN(self):
        return '%s%s' % (self.tin, settings.JTB_SUBSIDIARY_REG_IDENTIFIER)

    class Meta:
        verbose_name = 'Subsidiary Company'


class Biometric(models.Model):
    '''Biometric data of individual tax payers. Biometric fields are base64 encoded strings.'''
    tax_payer = models.OneToOneField(IndividualTaxPayer, on_delete=models.CASCADE, related_name='biometrics')
    pic = models.TextField('Passport Photo')
    f1 = models.TextField('Finder #1')
    f2 = models.TextField('Finder #2')
    f3 = models.TextField('Finder #3')
    f4 = models.TextField('Finder #4')
    f5 = models.TextField('Finder #5')
    f6 = models.TextField('Finder #6')
    f7 = models.TextField('Finder #7')
    f8 = models.TextField('Finder #8')
    f9 = models.TextField('Finder #9')
    f10 = models.TextField('Finder #10')

# this function generates an Individual TIN by incrementing the last TIN
def generate_individual_TIN():
    tin = None
    max_tin = IndividualTaxPayer.objects.all().aggregate(Max('tin'))
    if max_tin['tin__max'] is None: # no tin exists
        tin = settings.JTB_INDIVIDUAL_START
    else:
        tin = int(max_tin['tin__max']) + 1
    return tin

# this function generates an Individual TIN by incrementing the last TIN
def generate_corporate_TIN():
    tin = None
    max_tin = CorporateTaxPayer.objects.all().aggregate(Max('tin'))
    if max_tin['tin__max'] is None: # no tin exists
        tin = settings.JTB_CORPORATE_START
    else:
        tin = int(max_tin['tin__max']) + 1
    return tin


@receiver(post_save, sender=IndividualTaxPayer)
def update_individual_TIN(sender, instance, created, **kwargs):
    # update the customer's tin number
    if created:
        instance.tin = generate_individual_TIN()
        instance.save()

@receiver(post_save, sender=CorporateTaxPayer)
def update_corporate_TIN(sender, instance, created, **kwargs):
    # update the customer's tin number
    if created:
        instance.tin = generate_corporate_TIN()
        instance.save()

# signal to create a token for user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class IndividualShareholder(models.Model):
    STATUS_CHOICES = (
        ('Appointed', 'Appointed'),
        ('Reappointed', 'Re-appointed'),
        ('Resigned', 'Resigned'),
        ('Removed', 'Removed'),
    )
    company = models.ForeignKey(CorporateTaxPayer,related_name='shareholders',null=True,on_delete=models.CASCADE)
    surname = models.CharField('Surname', max_length=75)
    first_name = models.CharField('First Name', max_length=75)
    other_name = models.CharField('Other Name', max_length=75, null=True) 
    nationality = models.ForeignKey(Country,related_name='individual_shareholder_nationality',on_delete=models.CASCADE)    
    residential_address = models.TextField()
    phone = models.CharField('Phone', max_length=15,)
    email = models.EmailField('Email', blank=True, null=True)
    position = models.CharField('Position', max_length=250,blank=True, null=True)
    bvn = models.BigIntegerField()    
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    share = models.IntegerField()
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='individual_shareholder_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='individual_shareholder_updater',null=True,on_delete=models.CASCADE)

    def full_name(self):
        return '{} {}'.format(self.first_name, self.surname)
    
    def __str__(self):
        return '{} (TIN: {})'.format(self.full_name, self.tin or 'N/A')    

    def get_absolute_url(self):
       return reverse('dashboard:corporate-detail', kwargs={'pk': self.company.pk})

    class Meta:
        verbose_name = 'Individual Shareholder'


class CorporateShareholder(models.Model):    
    REGISTRATION_STATUS_CHOICES = (
        ('Registered', 'Registered'),
        ('Unregistered', 'Unregistered'),
    )
    STATUS_CHOICES = (
        ('Appointed', 'Appointed'),
        ('Reappointed', 'Re-appointed'),
        ('Resigned', 'Resigned'),
        ('Removed', 'Removed'),
    )
    company = models.ForeignKey(CorporateTaxPayer,related_name='corporate_company',null=True,on_delete=models.CASCADE)
    name = models.CharField('Registration Name', max_length=150)
    address = models.TextField()
    trade_name = models.CharField('Trade Name', max_length=150)
    phone = models.CharField('Phone', max_length=15)
    email = models.EmailField('Email')
    tin = models.CharField('JTB TIN', max_length=10, blank=True, null=True)
    reg_status = models.CharField('Registration Status', max_length=20, choices=REGISTRATION_STATUS_CHOICES)
    bvn = models.BigIntegerField()    
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES)
    share = models.IntegerField()
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.ForeignKey(User,related_name='corporate_shareholder_creater',null=True,on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User,related_name='corporate_shareholder_updater',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return '{} (TIN: {})'.format(self.name, self.tin or 'N/A')

    def get_absolute_url(self):
        return reverse('dashboard:corporate-detail', kwargs={'pk': self.company.pk})

    class Meta:
        verbose_name = 'Corporate Shareholder'

    