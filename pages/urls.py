from django.urls import path

from . import views
from . import webhooks


app_name = 'pages'

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about,  name="about"),
    path("learning/start/", views.start, name="start"),
    path("pricing/", views.pricing, name="pricing"),
    path("how-does-it-work/", views.how, name="how"),
    path("contact-us/", views.contact, name="contact"),
    
    # Account 
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/files/', views.user_files, name='user_files'),
    
    # Stripe
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('checkout/success/', views.success, name='success'),
    path('checkout/cancel/', views.cancel, name='cancel'),
    path('checkout/webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
