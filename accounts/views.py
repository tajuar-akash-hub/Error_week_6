from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login,logout
from . forms import UserRegistrationForm,userUpdateFrom
from django.urls import reverse_lazy
from django.views import View

# Create your views here.
class userRegistrationView(FormView):
    template_name='accounts/user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy("profile")
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
class user_login_view(LoginView):
    template_name='accounts/user_login.html'
    def get_success_url(self) :
        return reverse_lazy("home")
    
class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'
    def get(self, request):
        form = userUpdateFrom(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = userUpdateFrom(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})


        
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")
    
    

