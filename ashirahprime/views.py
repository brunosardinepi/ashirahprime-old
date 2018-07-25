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

class PasswordChangeView(views.PasswordChangeView):
    template_name = 'password_change.html'

class PasswordResetView(views.PasswordResetView):
    template_name = 'password_reset.html'

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class PasswordResetFromKeyView(views.PasswordResetFromKeyView):
    template_name = 'password_reset_from_key.html'

class PasswordResetFromKeyDoneView(views.PasswordResetFromKeyDoneView):
    template_name = 'password_reset_from_key_done.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'