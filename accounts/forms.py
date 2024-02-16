# from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import userBankAccount,userAddress

# from django.forms import forms
from django import forms 
from . constants import ACCOUNT_TYPE,GENDER_TYPE

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    street_address= forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country= forms.CharField(max_length=100)
    account_type = forms.ChoiceField( choices=ACCOUNT_TYPE )
    gender_type = forms.ChoiceField( choices=GENDER_TYPE )
    class Meta:
        model= User
        fields = ['username','first_name','last_name','password1','password2','gender_type','email','account_type','postal_code','city','country']
    
    #explanation : first e user e amader field gula diye disi, ekhon amader field gular sathe model er field er connection create korte hobe 
        
    def save(self, commit = True):
        our_user = super().save(commit=False)
        if commit==True:
            our_user.save()
            #now time to save user Bank details
            account_type = self.cleaned_data.get("account_type")
            gender_type = self.cleaned_data.get("gender_type")
            postal_code=self.cleaned_data.get("postal_code")
            country = self.cleaned_data.get("country")
            birth_date=self.cleaned_data.get("birth_date")
            city=self.cleaned_data.get("city")
            street_address = self.cleaned_data.get("street_address")

        # amader User form theke detials gula niye ashlam, ebar ashol model er sathe connection 
            
            userBankAccount.objects.create(
                user = our_user,
                account_type=account_type,
                account_no=100000+our_user.id,
                birth_date=birth_date,
                gender_type=gender_type,
            )

            userAddress.objects.create(
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )
            return our_user

     #init for override    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

#handling profile page, where user can update his info
            
class userUpdateFrom(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    street_address= forms.CharField(max_length=100)
    city = forms.CharField( max_length=50)
    postal_code = forms.IntegerField()
    country= forms.CharField(max_length=100)
    account_type = forms.ChoiceField( choices=ACCOUNT_TYPE )
    gender_type = forms.ChoiceField( choices=GENDER_TYPE)

    class Meta:
        model = User
        fields=['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

            if self.instance :
                try:
                    user_account=self.instance.account
                    user_address=self.instance.address
                except:
                    user_account=None
                    user_address=None

                if user_account:
                    self.fields['account_type'].initial = user_account.account_type
                    self.fields['gender_type'].initial = user_account.gender_type
                    self.fields['birth_date'].initial = user_account.birth_date 
                    self.fields['street_address'].initial = user_address.street_address
                    self.fields['city'].initial = user_address.city
                    self.fields['postal_code'].initial = user_address.postal_code
                    self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = userBankAccount.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address, created = userAddress.objects.get_or_create(user=user) 

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender_type = self.cleaned_data['gender_type']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user

                    



            