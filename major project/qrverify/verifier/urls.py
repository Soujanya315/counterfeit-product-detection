from django.urls import path
from . import views

urlpatterns = [
    # ---------- LOGIN SYSTEM ----------
    path('', views.login_selection, name='login_selection'),
    path('client_login/', views.client_login, name='client_login'),
    path('manufacturer_login/', views.manufacturer_login, name='manufacturer_login'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('manufacturer_dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),

    # ---------- EXISTING SYSTEM ----------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_product_view, name='register_product'),
    path('qr_scan/', views.qr_scan, name='qr_scan'),
    path('verify_qr/', views.verify_qr, name='verify_qr'),
    path('image-scan/', views.image_scan, name='image_scan'),
    path('verify-image/', views.verify_image, name='verify_image'),
    path('verify_combined/', views.verify_combined, name='verify_combined'),
]
