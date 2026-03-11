# ================================================================
#  mental/urls.py
#  Project-level URL configuration for MindWell Django app
# ================================================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ── DJANGO ADMIN ────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── PASSWORD RESET FLOW ───────────────────────────────────
    # NOTE: login/logout/register are handled inside mentalapp/urls.py
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='mentalapp/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='mentalapp/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='mentalapp/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='mentalapp/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # ── APP URLS ───────────────────────────────────────────────
    path('', include('mentalapp.urls', namespace='mentalapp')),
]

# ── MEDIA FILES (DEV ONLY) ─────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)