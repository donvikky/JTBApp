from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.models import Token
from account.forms import UserRegistrationForm
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    elif request.user.is_staff:
        return redirect('dashboard:index')
    else:
        return redirect('account:home')

class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = '/account/register-success'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        user = User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

class RegisterSuccessView(TemplateView):
    template_name = 'account/success.html'

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'account/index.html'

def token(request):
    token = Token.objects.get(user=request.user)
    return render(request, 'account/token.html', {'token':token})
