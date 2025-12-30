from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from .tasks import send_bill_email

from .utils import calculate_balance_denominations
def billing_page(request):
    denoms = Denomination.objects.all().order_by('-value')
    return render(request, 'billing_page.html', {'denoms': denoms})

def generate_bill(request):
    email = request.POST.get('email')
    product_ids = request.POST.getlist('product_id[]')
    quantities = request.POST.getlist('quantity[]')
    paid_amount = float(request.POST.get('paid_amount'))

    customer, _ = Customer.objects.get_or_create(email=email)

    total_price = 0
    total_tax = 0

    bill = Bill.objects.create(
        customer=customer,
        total_price=0,
        total_tax=0,
        net_price=0,
        paid_amount=paid_amount,
        balance_amount=0
    )

    for pid, qty in zip(product_ids, quantities):
        product = Product.objects.get(product_id=pid)
        qty = int(qty)

        price = product.unit_price * qty
        tax = price * product.tax_percentage / 100

        total_price += price
        total_tax += tax

        BillItem.objects.create(
            bill=bill,
            product=product,
            quantity=qty,
            total_price=price + tax
        )

        product.available_stock -= qty
        product.save()

    net_price = total_price + total_tax
    balance = paid_amount - net_price

    bill.total_price = total_price
    bill.total_tax = total_tax
    bill.net_price = net_price
    bill.balance_amount = round(balance)
    bill.save()
    send_bill_email.delay(bill.id)
    return JsonResponse({"bill_id": bill.id})


def calculate_balance_denominations(balance):
    result = []
    denoms = Denomination.objects.order_by('-value')

    for d in denoms:
        count = int(balance // d.value)
        if count > 0:
            result.append({
                "value": d.value,
                "count": count
            })
            balance -= d.value * count

    return result


def bill_view(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    rounded_net_price = round(bill.net_price)
    balance_amount = bill.paid_amount - rounded_net_price

    balance_denoms = calculate_balance_denominations(balance_amount)

    context = {
        'bill': bill,
        'rounded_net_price': rounded_net_price,
        'balance_amount': balance_amount,
        'balance_denoms': balance_denoms
    }

    return render(request, 'bill_view.html', context)
