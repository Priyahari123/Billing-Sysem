from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Bill
from .utils import render_to_pdf
import math

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={'max_retries': 3})
def send_bill_email(self, bill_id):
    print(f"Sending bill email for Bill ID: {bill_id}")

    bill = Bill.objects.get(id=bill_id)

    rounded_net_price = math.floor(bill.net_price)
    balance_amount = round(bill.paid_amount - rounded_net_price)

    denoms = [500, 200, 100, 50, 20, 10, 5, 2, 1]
    balance = balance_amount
    balance_denoms = []

    for d in denoms:
        count = balance // d
        if count:
            balance_denoms.append({'value': d, 'count': count})
            balance %= d

    context = {
        'bill': bill,
        'rounded_net_price': rounded_net_price,
        'balance_amount': balance_amount,
        'balance_denoms': balance_denoms,
    }

    # HTML Email content
    html_content = render_to_string('bill_invoice.html', context)

    # PDF generation
    pdf_file = render_to_pdf('bill_invoice.html', context)
    print(f"PDF generation {'succeeded' if pdf_file else 'failed'} for Bill ID: {bill_id}")

    email = EmailMultiAlternatives(
        subject=f"Invoice For Your Recent Purchase - Bill ID: {bill.id}",
        body="Please find your invoice attached as PDF.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[bill.customer.email],
    )

    # email.attach_alternative(html_content, "text/html")

    if pdf_file:
        email.attach(
            filename=f"Invoice_{bill.id}.pdf",
            content=pdf_file,
            mimetype="application/pdf"
        )

    email.send()

    bill.is_bill_sent = True
    bill.save()

    print(f"Email + PDF invoice sent successfully for Bill ID: {bill_id}")
