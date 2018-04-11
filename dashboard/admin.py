from django.contrib import admin
from dashboard.models import IndividualTaxPayer, CorporateTaxPayer, TaxOffice

# Register your models here.
class IndividualAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        super(IndividualAdmin, self).save_model(request, obj, form, change)

class CorporateAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        super(CorporateAdmin, self).save_model(request, obj, form, change)

class TaxOfficeAdmin(admin.ModelAdmin):
    exclude = ('create_time','create_user','update_time','update_user')
    list_display = ('name','state','lga','address','status')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_user = request.user
        obj.update_user = request.user
        super(TaxOfficeAdmin, self).save_model(request, obj, form, change)

admin.site.register(IndividualTaxPayer, IndividualAdmin)
admin.site.register(CorporateTaxPayer, CorporateAdmin)
admin.site.register(TaxOffice, TaxOfficeAdmin)
