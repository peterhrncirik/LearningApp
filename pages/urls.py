from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about,  name="about"),
    path("start/", views.start, name="start"),
    path("pricing/", views.pricing, name="pricing"),
    
    # Stripe
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('checkout/success', views.success, name='success'),
    path('checkout/cancel/', views.cancel, name='cancel'),
]
