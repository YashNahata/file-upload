from django.contrib import admin
from django.urls import path
from upload import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.handleLogin, name="handleLogin"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('upload', views.handleUpload, name="handleUpload"),
    path('bin', views.handleBin, name="handleBin"),
    path('delete<int:file_id>', views.handleDelete, name="handleDelete"),
    path('bin-delete<int:file_id>', views.handleBinDelete, name="handleBinDelete"),
    path('bin-restore<int:file_id>', views.handleBinRestore, name="handleDelete"),
    path('media/documents/<str:file_name>', views.handleMedia, name="handleMedia")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
