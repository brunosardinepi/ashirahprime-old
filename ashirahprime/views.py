from django.views.generic.base import TemplateView

from allauth.account import views


class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(views.LoginView):
    template_name = 'login.html'

class LogoutView(views.LogoutView):
    template_name = 'logout.html'

class SignupView(views.SignupView):
    template_name = 'signup.html'