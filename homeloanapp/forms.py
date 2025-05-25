from django import forms  
from .models import ClientDetails,LoanDisbursement, LoanSettlement

class ClientDetailsForm(forms.ModelForm):
    class Meta:
        Model = ClientDetails 
        fields = '__all__'
        
        
class EmiForm(forms.Form):
    principle = forms.FloatField()
    rate = forms.FloatField()
    time = forms.FloatField()

class LoanDisbursementForm(forms.ModelForm):
    class Meta:
        model = LoanDisbursement
        fields = ['account_no', 'disbursement_date', 'disbursement_status']
        widgets = {
            'disbursement_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LoanSettlementForm(forms.ModelForm):
    class Meta:
        model = LoanSettlement
        fields = ['client', 'settle_date', 'settle_status']
        widgets = {
            'settle_date': forms.DateInput(attrs={'type': 'date'}),
        }    

class LoanSettlementSearchForm(forms.Form):
    account_no = forms.CharField(
        label='Account Number',
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter account number to search'
        })
    )           