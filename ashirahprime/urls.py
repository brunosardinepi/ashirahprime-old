from django.contrib import admin
from django.urls import include, path

from . import secrets
from . import views


urlpatterns = [
    path('{}/'.format(secrets.settings['admin']), admin.site.urls),
    path('accounts/confirm-email/', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('accounts/confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('', views.HomeView.as_view(), name='home'),
]
