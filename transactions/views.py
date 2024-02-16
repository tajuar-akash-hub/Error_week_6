from django.shortcuts import render
from django.views.generic import CreateView,ListView
from transactions.models import transactions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from transactions.forms import Deposite_form,withdrawForm,LoanRequestForm
from transactions.constant import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.views import View
from transactions.models import transactions
# Create your views here.
class transactionsCreateMixin(LoginRequiredMixin,CreateView):
    template_name='transactions/transaction_form.html'
    model=transactions
    title = ''    #html page titile
    success_url=reverse_lazy("transaction_report")
    
    def get_form_kwargs(self) :
        kwargs= super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account
        })
        return kwargs
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context
    
class DepositeMoneyView(transactionsCreateMixin):
    form_class=Deposite_form
    title = 'Deposit Form'

    def get_initial(self) :
        initial = {'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account_balance +=amount
        account.save(
            update_fields= [
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:.2f} " .format(float(amount))}$ was deposited to your account successfully'

        )
        
        return super().form_valid(form)
    

class withdrawMoneyView(transactionsCreateMixin):
    form_class=withdrawForm
    title = 'withdraw money'

    def get_initial(self) :
        initial = {'transaction_type':WITHDRAWAL}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'{"{:.2f} " .format(float(amount))}$ was added to your account successfully'
        )
        return super().form_valid(form)
    

class LoanRequestView(transactionsCreateMixin):
    form_class=LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self) :
        initial = {'transaction_type':LOAN}
        return initial
    
    def form_valid(self,form):
        amount = form.cleaned_data.get('amount')

        current_loan_count = transactions.objects.filter(account=self.request.user.account, transaction_type=3,loan_approve=True).count()

        if current_loan_count>=3:
            return HttpResponse("you have cross the loan limits")
        messages.success(
            self.request,
            f'{"{:.2f} " .format(float(amount))}$ you loan request submitted  successfully'

        )
        return super().form_valid(form)
    


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = transactions
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
            # account=self.request.user.transactions
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = transactions.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
    

class LoanListView(LoginRequiredMixin,ListView):
    model = transactions
    template_name = 'transactions/loan_request.html'
    context_object_name = 'loans' # loan list ta ei loans context er moddhe thakbe
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = transactions.objects.filter(account=user_account,transaction_type=3)
        return queryset
    

class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(transactions, id=loan_id)
        print(loan)
        if loan.loan_approve:
            user_account = loan.account
              
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approve = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                # return redirect('transactions:loan_list')
            else:
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )

        # return redirect('loan_list')
    

    


    

