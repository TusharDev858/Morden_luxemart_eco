from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        # Honeypot check
        if request.POST.get('website'):
            return redirect('contact:contact')
        ContactMessage.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, "✅ Message sent! We'll get back to you within 24 hours.")
        return redirect('contact:contact')
    return render(request, 'contact/contact.html')

def faq(request):
    faq_sections = [
        ("Orders & Shipping", [
            ("How long does delivery take?", "Standard delivery takes 3–5 business days. Express shipping (1–2 days) is available at checkout. Free standard shipping on orders over $75."),
            ("Can I track my order?", "Yes! Once your order ships you'll receive a tracking number by email. You can also track it anytime from your account dashboard or our Order Tracking page."),
            ("Do you ship internationally?", "We currently ship to over 50 countries. International delivery takes 7–14 business days. Duties and taxes may apply depending on your country."),
            ("What if my package arrives damaged?", "We're so sorry! Please take photos and contact us within 48 hours of delivery. We'll send a replacement or issue a full refund immediately."),
            ("Can I change my delivery address?", "Address changes can be made within 2 hours of placing your order. Contact us immediately via live chat or email for the fastest resolution."),
        ]),
        ("Returns & Refunds", [
            ("What is your return policy?", "We offer a 30-day hassle-free return policy for all unused items in original packaging. Simply initiate a return from your account dashboard."),
            ("How long do refunds take?", "Refunds are processed within 3–5 business days of receiving your return. It may take an additional 3–5 days to appear on your statement depending on your bank."),
            ("Do I pay for return shipping?", "Returns are free for defective or incorrect items. For change-of-mind returns, a prepaid return label is provided for $5.99, deducted from your refund."),
            ("Can I exchange an item?", "Absolutely! The easiest way is to return the item and place a new order. This ensures the fastest turnaround. Contact us if you need help."),
        ]),
        ("Payments & Security", [
            ("What payment methods do you accept?", "We accept Visa, Mastercard, American Express, PayPal, and Cash on Delivery (select regions). All transactions are SSL encrypted."),
            ("Is my payment information secure?", "100%. We never store your card details. All payments are processed by Stripe, a PCI-DSS Level 1 certified payment processor — the highest security standard."),
            ("Do you offer instalment payments?", "Yes! PayPal Pay Later is available at checkout for eligible orders. Split your purchase into 4 interest-free payments."),
            ("Why was my payment declined?", "This is usually a bank security measure. Try again or contact your bank to authorise the transaction. You can also try a different card or PayPal."),
        ]),
        ("Products & Authenticity", [
            ("Are all products authentic?", "Absolutely. We work directly with brands and authorised distributors. Every product is 100% genuine and comes with its original manufacturer warranty."),
            ("How do I find the right size?", "Each product page includes a detailed size guide. If you're unsure, our customer support team is happy to advise based on your measurements."),
            ("Do products come with a warranty?", "Yes. All products include the manufacturer's standard warranty. Electronics typically have a 1-year warranty. Details are listed on each product page."),
            ("Can I request a product not on your site?", "Yes! Use our Contact form to request specific products. We're constantly expanding our catalogue and love hearing what customers want."),
        ]),
        ("Account & Orders", [
            ("How do I create an account?", "Click 'Register' in the top navigation. It takes less than a minute. You'll get order tracking, wishlist, saved addresses, and exclusive member deals."),
            ("I forgot my password. What do I do?", "Click 'Forgot password?' on the login page. We'll email you a secure reset link. Check your spam folder if you don't see it within 2 minutes."),
            ("Can I cancel my order?", "Orders can be cancelled within 2 hours of placement if they haven't been packed yet. Go to My Orders → Cancel, or contact us immediately."),
            ("How do I apply a coupon code?", "Enter your coupon code in the 'Coupon Code' field in your cart or at checkout, then click Apply. The discount will be shown before you confirm your order."),
        ]),
    ]
    return render(request, 'contact/faq.html', {'faq_sections': faq_sections})
