"""
URL configuration for HomeLoanAutomation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from homeloanapp.views import Dashboard, ApplicationView, DisplayClients
from django.contrib.auth import views as auth_views 
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView 
from homeloanapp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('application/', views.ApplicationView.as_view(), name='application'),
    path('display_clients/', views.DisplayClients.as_view(), name='display_clients'),
    path('client_update/<int:pk>', views.ClientUpdate.as_view(), name='client_update'),
    path('<pk>/client_detail/', views.ClientDetail.as_view(), name='client_detail'),
    path('<pk>/client_delete', views.ClientDelete.as_view(), name = 'client_delete'),
    path('emi/', views.EmiCal, name = 'emi'),
    path('approve_reject/<int:id>', views.Approve_Reject, name= 'approve_reject'),
    path('loan_status/', views.LoanStatus.as_view(), name='loan_status'),
    path('ai_predict/<int:pk>', views.AutomaticLoanApprove.as_view(), name='ai_predict'),
    path('creditresult_csv/', views.CreditResult_Csv, name='creditresult_csv'),
    path('client/<int:client_id>/disburse/', views.LoanDisbursementCreate.as_view(), name='loan_disbursement'),
    path('loan-settlement/', views.LoanSettlementView.as_view(), name='loan_settlement'),
    path('settle-loan/<int:disbursement_id>/', views.SettleLoanAccount.as_view(), name='settle_loan_account'),
    path('loan-settlement/success/', views.LoanSettlementSuccessView.as_view(), name='loan_settlement_success'),
    path('client-status/', views.ClientStatusView.as_view(), name='client_status'),
]
