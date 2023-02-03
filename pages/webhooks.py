import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser, StripeCustomer

# Stripe Webhook
@csrf_exempt
def stripe_webhook(request):
    
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        # Invalid Payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid Signature
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'subscription' and session.payment_status == 'paid':
            try:
                current_user = CustomUser.objects.get(id=session.client_reference_id)
            except current_user.DoesNotExist:
                return HttpResponse(status=404)
            
            # Active user premium features
            current_user.is_member = True
            if session['metadata']['product_type'] == '2':
                current_user.is_unlimited = True
                
            # Create new StripeCustomer
            customer = StripeCustomer()
            customer.user = current_user
            customer.stripe_id = session.customer
            customer.is_active = True
            customer.subscription_id = session.subscription
            
            # Save User & Save Customer
            customer.save()
            current_user.save()
    
    return HttpResponse(status=200)