import math
from django.shortcuts import render
from .models import Product, Purchase, PurchaseItem
import threading
from django.core.mail import EmailMessage
from django.conf import settings

def send_invoice_mail(email, items, total_without_tax, total_tax, net_price, rounded_price, paid):

    html_message = f"""
    <h2>Invoice</h2>
    <p><b>Customer:</b> {email}</p>

    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>Product.ID</th>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Tax</th>
            <th>Total</th>
        </tr>
    """

    for item in items:
        html_message += f"""
        <tr>
            <td>{item['id']}</td>
            <td>{item['name']}</td>
            <td>{item['qty']}</td>
            <td>{item['price']}</td>
            <td>{item['tax_amount']}</td>
            <td>{item['total_price']}</td>
        </tr>
        """

    html_message += f"""
    </table>

    <br>
    <p>Total without tax: {total_without_tax}</p>
    <p>Total tax: {total_tax}</p>
    <p>Net amount: {net_price}</p>
    <p>Rounded amount: {rounded_price}</p>
    <p>Paid: {paid}</p>
    
    """

    email_msg = EmailMessage(
        "Your Billing Invoice",
        html_message,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email_msg.content_subtype = "html"
    email_msg.send()

def billing_page(request):
    products = Product.objects.all()

    if request.method == "POST":
        email = request.POST.get("email")
        product_ids = request.POST.getlist("product_id[]")
        quantities = request.POST.getlist("quantity[]")

        purchase = Purchase.objects.create(
            customer_email=email,
            total_amount=0
        )

        items = []
        total_without_tax = 0
        total_tax = 0

        for pid, qty in zip(product_ids, quantities):
            product = Product.objects.get(id=pid)

            price = product.price
            tax_percent = product.tax

            purchase_price = price * int(qty)
            tax_amount = purchase_price * tax_percent / 100
            total_price = purchase_price + tax_amount

            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=qty,
                price=price
            )

            items.append({
                "id": product.product_id,
                "name": product.name,
                "price": price,
                "qty": qty,
                "purchase_price": purchase_price,
                "tax_percent": tax_percent,
                "tax_amount": tax_amount,
                "total_price": total_price
            })

            total_without_tax += purchase_price
            total_tax += tax_amount

        net_price = total_without_tax + total_tax
        rounded_price = math.floor(net_price)

        paid = int(request.POST.get("paid"))
        balance = paid - rounded_price

        denomination = calculate_change(balance)

        # ✅ Save final total
        purchase.total_amount = net_price
        purchase.save()

       
        

        
        threading.Thread(
    target=send_invoice_mail,
    args=(email, items, total_without_tax, total_tax, net_price, rounded_price, paid)
).start()

        return render(request, "billing/invoice.html", {
            "email": email,
            "items": items,
            "total_without_tax": total_without_tax,
            "total_tax": total_tax,
            "net_price": net_price,
            "rounded_price": rounded_price,
            "balance": balance,
            "denomination": denomination
        })
    

    return render(request, "billing/billing.form.html", {"products": products})
def calculate_change(balance):

    notes = [500, 50, 20, 10, 5, 2, 1]
    result = {}

    for note in notes:
        count = balance // note
        balance = balance % note
        result[note] = count

    return result



def purchase_history(request):
    email=request.GET.get('email')
    items = PurchaseItem.objects.filter(purchase__customer_email=email).order_by('-purchase__created_at')

    return render(request, "billing/purchase_detail.html", {
        "items": items
    })




