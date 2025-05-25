from django.contrib import admin
from .models import ClientDetails, LoanDisbursement, LoanSettlement

class ClientDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'citizenship', 'loan_amount', 'tenure', 'interest', 'loan_status')
    list_filter = ('loan_status', 'sex', 'martial', 'education')
    search_fields = ('name', 'citizenship', 'address')
    readonly_fields = (
        'yearly_income', 'monthly_income', 'actual_loan_amt', 'selfinvest', 
        'tot_coll', 'monthly_saving', 'emi', 'loan_to_coll', 'loan_to_invest',
        'kista_to_income', 'total_score', 'credit_result'
    )
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'name', 'dob', 'citizenship', 'sex', 'martial', 'father', 
                'education', 'address', 'dependent'
            )
        }),
        ('Employment Information', {
            'fields': ('employer', 'position', 'service_time'),
            'classes': ('collapse',)
        }),
        ('Business Information', {
            'fields': ('firm_name', 'business_type', 'pan_no', 'firm_address'),
            'classes': ('collapse',)
        }),
        ('Income Information', {
            'fields': (
                'salary', 'business_income', 'agriculture', 
                'house_rent', 'family_income', 'other_income'
            )
        }),
        ('Loan Information', {
            'fields': ('loan_amount', 'tenure', 'interest', 'loan_type')
        }),
        ('Collateral Information', {
            'fields': (
                'plot_no', 'plot_area', 'plot_address', 'plot_owner',
                'plot_value', 'home_value', 'plot_market_value'
            ),
            'classes': ('collapse',)
        }),
        ('Other Property', {
            'fields': ('land_value', 'buildingvalue', 'family_property', 'vehicle'),
            'classes': ('collapse',)
        }),
        ('Credit Score Factors', {
            'fields': (
                'collateral_place', 'income_tenure', 'client_distance',
                'banking_history', 'banking_year', 'loan_committee'
            ),
            'classes': ('collapse',)
        }),
        ('Calculated Fields', {
            'fields': (
                'yearly_income', 'monthly_income', 'actual_loan_amt', 
                'selfinvest', 'tot_coll', 'monthly_saving', 'emi',
                'loan_to_coll', 'loan_to_invest', 'kista_to_income',
                'total_score', 'credit_result'
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('loan_status',)
        })
    )

class LoanDisbursementAdmin(admin.ModelAdmin):
    list_display = ('client', 'account_no', 'disbursement_date', 'disbursement_status')
    list_filter = ('disbursement_status',)
    search_fields = ('client__name', 'account_no')
    raw_id_fields = ('client',)

class LoanSettlementAdmin(admin.ModelAdmin):
    list_display = ('client', 'settle_date', 'settle_status')
    list_filter = ('settle_status',)
    search_fields = ('client__name',)
    raw_id_fields = ('client',)

admin.site.register(ClientDetails, ClientDetailsAdmin)
admin.site.register(LoanDisbursement, LoanDisbursementAdmin)
admin.site.register(LoanSettlement, LoanSettlementAdmin)