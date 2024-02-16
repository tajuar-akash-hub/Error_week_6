from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . models import transactions
from django import forms


class transaction_form(forms.ModelForm):
    class Meta:
        model = transactions
        fields= ['amount','transaction_type']

    def __init__(self,*args,**kwargs):
        self.account = kwargs.pop('account') #poping account value and storing
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled=True
        self.fields['transaction_type'].widget=forms.HiddenInput()
        
    def save(self,commit=True):
        self.instance.account=self.account
        self.instance.balance_after_transaction=self.account.balance
        return super().save()


class Deposite_form(transaction_form):
    def clean_amount(self):
        min_deposite_amount=100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposite_amount:
            raise forms.ValidationError(
                f'you need to deposite at least {min_deposite_amount}'
            )
        return amount
    
class withdrawForm(transaction_form):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount=20000
        balance = account.balance #100
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'you can withdraw at least {min_withdraw_amount} $'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount}'

            )
        if amount > balance:
            raise forms.ValidationError(
                f'you have {balance}$ in your account. ' 'you can not withdraw more than your account balance'
            )
        return amount
    
class LoanRequestForm(transaction_form):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount