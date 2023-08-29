from django.urls import path, include, re_path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.views.static import serve

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

app_name = 'app'

urlpatterns = [
    path('setup/', views.Setup.as_view(), name="setup"),



    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),
    path('app/<str:id>', views.App.as_view(), name="app"),
    path('user_profile/', views.UserProfile.as_view(), name="user_profile"),
    path('upload_files/', views.UploadFiles.as_view(), name='upload_files'),
    path('api/download/', views.DownloadPDF.as_view(), name="download"),
    path('api/download_docx/', views.DownloadDOCX.as_view(), name="download_docx"),

    path('update_profile/', views.Update_profile.as_view(), name='update_profile'),
    re_path(r'^build/(?P<path>.*)$', serve, {'document_root': str(settings.BASE_DIR) + '/build'}),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)