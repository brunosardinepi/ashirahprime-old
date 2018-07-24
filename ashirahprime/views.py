from django.views.generic.base import TemplateView

from allauth.account import views


class HomeView(TemplateView):
    template_name = 'home.html'

class EmailVerificationSentView(views.EmailVerificationSentView):
    template_name = 'verification_sent.html'

class ConfirmEmailView(views.ConfirmEmailView):
    template_name = 'email_confirm.html'

class LoginView(views.LoginView):
    template_name = 'login.html'

class LogoutView(views.LogoutView):
    template_name = 'logout.html'

class SignupView(views.SignupView):
    template_name = 'signup.html'