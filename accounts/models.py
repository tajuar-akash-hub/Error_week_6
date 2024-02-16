from django.db import models
from django.contrib.auth.models import User
from . constants import ACCOUNT_TYPE,GENDER_TYPE

# handling django user registration related processes 

class userBankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField( max_length=50,choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique= True)
    birth_date = models.DateField(blank=True,null=True)
    gender_type = models.CharField(max_length=50,choices=GENDER_TYPE)
    initial_deposite_date= models.DateField(auto_now_add=True) #the date when created the account
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    def __str__(self) -> str:
        return f'account no : {self.account_no}'

class userAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address= models.CharField(max_length=100)
    city = models.CharField( max_length=50)
    postal_code = models.IntegerField()
    country= models.CharField(max_length=100)
    def __str__(self) :
        return f'{self.user.email}'
    
# all the constant like of choice filed are stored in constant.py 

