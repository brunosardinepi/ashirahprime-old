from django.contrib import admin
from django.urls import include, path, re_path

from . import secrets
from . import views


urlpatterns = [
    path('{}/'.format(secrets.settings['admin']), admin.site.urls),
    path('accounts/confirm-email/', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('accounts/confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', views.PasswordResetFromKeyView.as_view(), name='password_reset_from_key'),
    path('accounts/password/reset/key/done/', views.PasswordResetFromKeyDoneView.as_view(), name='password_reset_from_key_done'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('characters/', include('characters.urls')),
    path('', views.HomeView.as_view(), name='home'),
]
