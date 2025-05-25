import csv
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import (
    ClientDetailsForm,
    EmiForm,
    LoanDisbursementForm,
    LoanSettlementForm,
    LoanSettlementSearchForm,
)
from .models import ClientDetails, LoanDisbursement, LoanSettlement

# Create your views here.

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
class ApplicationView(LoginRequiredMixin, CreateView):
    model = ClientDetails
    form_name = ClientDetailsForm
    fields = "__all__"
    template_name='application.html'
    success_url = '/application/'


class DisplayClients(LoginRequiredMixin, ListView):
    model = ClientDetails
    template_name = 'client_list.html'
    context_object_name = 'clients'
 
class ClientUpdate(UpdateView):   
    model = ClientDetails
    template_name = 'client_update.html'
    form_name = ClientDetailsForm
    fields ='__all__'
    success_url = '/display_clients/'
                                
class ClientDetail(DetailView):
    model = ClientDetails
    template_name = 'client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Context Data:", context)  # Check terminal for this output
        return context
    
            
class ClientDelete(DeleteView):
    model = ClientDetails
    context_object_name = 'client'
    template_name = 'client_delete.html'
    success_url = '/display_clients/'
    # success_url=reverse_lazy('')
   
 
    
def calculate_emi(principal, annual_rate, years):
    """
    Helper function to calculate EMI
    """
    monthly_rate = annual_rate / 1200  # Convert annual % to monthly decimal
    months = years * 12
    factor = pow(1 + monthly_rate, months)
    return (principal * monthly_rate * factor) / (factor - 1)

def EmiCal(request):
    emi = None  # Initialize as None instead of 0.0 for better state tracking
    fm = EmiForm(request.POST or None)  # Handles both GET and POST
    
    if request.method == 'POST' and fm.is_valid():
        p = fm.cleaned_data['principle']
        r = fm.cleaned_data['rate']
        t = fm.cleaned_data['time']
        
        emi = calculate_emi(p, r, t)
        emi = round(emi, 2)
    
    return render(request, 'emi.html', {'form': fm, 'emi': emi})
              
                  
def Approve_Reject(request, id):
    if request.method == 'POST':
        obj = ClientDetails.objects.get(pk=id) 
        if request.POST.get("approved"):
            obj.loan_status = "approved"
            obj.save(update_fields=["loan_status"])
            #messages.success(request, '1 Client(s) is send for Approved Successfully !!! ')
        if request.POST.get("rejected"):
            obj.loan_status = "rejected"
            obj.save(update_fields=["loan_status"])    
    
    return HttpResponseRedirect('/display_clients/')        

class LoanStatus(LoginRequiredMixin, ListView):
    model = ClientDetails
    template_name = 'loan_status.html'
    context_object_name = 'approved_clients'    
    
    def get_queryset(self):
        #Filter onlye approved clients
        return ClientDetails.objects.filter(loan_status ='approved').order_by('name')
        
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)    
        #Add any additional context data if needed 
        context['title'] = 'Approved Clients'
        return context

   
class AutomaticLoanApprove(UpdateView):   
    model = ClientDetails
    template_name = 'ai_predict.html'
    form_name = ClientDetailsForm
    fields ='__all__'
    success_url = '/display_clients/'

#Loan Disbrusement
class LoanDisbursementCreate(LoginRequiredMixin, CreateView):
    model = LoanDisbursement
    form_class = LoanDisbursementForm
    template_name = 'loan_disbursement_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = get_object_or_404(ClientDetails, pk=self.kwargs['client_id'])
        context['client'] = client
        return context
    
    def form_valid(self, form):
        client = get_object_or_404(ClientDetails, pk=self.kwargs['client_id'])
        form.instance.client = client
        form.instance.disbursement_status = 'Disbursed'
        
        # Update client's loan status
        client.loan_status = 'disbursed'
        client.save(update_fields=['loan_status'])
       
            
        messages.success(self.request, 'Loan successfully disbursed!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('client_detail', kwargs={'pk': self.kwargs['client_id']})
    
#Loan Settlement
class LoanSettlementView(LoginRequiredMixin, View):
    template_name = 'loan_settlement.html'
    
    def get(self, request):
        form = LoanSettlementSearchForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoanSettlementSearchForm(request.POST)
        if form.is_valid():
            account_no = form.cleaned_data['account_no']
            try:
                disbursement = Loan_Disbursement.objects.select_related('client').get(
                    Q(account_no=account_no) & 
                    Q(disbursement_status='Disbursed') &
                    Q(client__loan_status='disbursed')
                )
                return render(request, self.template_name, {
                    'form': form,
                    'disbursement': disbursement,
                    'show_settle_button': True
                })
            except Loan_Disbursement.DoesNotExist:
                messages.error(request, 'No active loan found with this account number')
        return render(request, self.template_name, {'form': form})

class SettleLoanAccount(LoginRequiredMixin, View):
    def post(self, request, disbursement_id):
        disbursement = get_object_or_404(Loan_Disbursement, pk=disbursement_id)
        
        # Update disbursement status
        disbursement.disbursement_status = 'Settled'
        disbursement.save()
        
        # Update client loan status
        client = disbursement.client
        client.loan_status = 'settled'
        client.save()
        
        # Create settlement record
        Loan_Settlement.objects.create(
            client=client,
            settle_date=timezone.now().date(),
            settle_status='Closed'
        )
        
        # Store client details in session for the success page
        request.session['settled_client'] = {
            'name': client.name,
            'account_no': disbursement.account_no,
            'settle_date': timezone.now().date().strftime('%Y-%m-%d'),
            'loan_amount': client.loan_amount
        }
        
        return redirect('loan_settlement_success')

#Loan Settlement Success Page
from django.http import Http404

class LoanSettlementSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'loan_settlement_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settled_client = self.request.session.get('settled_client')
        
        if not settled_client:
            raise Http404("No settlement information found")
            
        context.update(settled_client)
        # Clear the session data after displaying
        del self.request.session['settled_client']
        return context

#Client Status List
class ClientStatusView(LoginRequiredMixin, ListView):
    model = ClientDetails
    template_name = 'client_status.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'all')
        
        queryset = ClientDetails.objects.all().order_by('name')
        
        if status == 'pending':
            return queryset.filter(loan_status='preview')
        elif status == 'approved':
            return queryset.filter(loan_status='approved')
        elif status == 'rejected':
            return queryset.filter(loan_status='rejected')
        elif status == 'disbursed':
            return queryset.filter(loan_status='disbursed')
        elif status == 'settled':
            return queryset.filter(loan_status='settled')
        else:  # 'all' or any other value
            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        context['status_choices'] = [
            ('all', 'All Clients'),
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('disbursed', 'Disbursed'),
            ('settled', 'Settled'),
        ]
        return context
    
        
#Printing Reports
def CreditResult_Csv(request):
    credit_result = ClientDetails.objects.all()
    response= HttpResponse(content_type= 'text/csv')
    response['Content-Disposition']= 'attachment; filename= credit_data.csv'
    writer= csv.writer(response) 
    writer.writerow(['Gender', 'MartialStatus','ClientIncome','FamilyIncome', 'LoanType', 'LoanAmount', 'InterestRate', 'HomeValue', 'LandDistressValue','Tenure','OtherProperty','LoanStatus'])
    clients = credit_result.values_list('sex','martial','salary','family_income','loan_type','loan_amount', 'interest', 'home_value','plot_value','tenure','land_value','loan_status')
    for client in clients:
        writer.writerow(client)
    return response   
        
