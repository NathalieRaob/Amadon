from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

# Create your views here.
def index(request):
    context = {
        'all_products': Product.objects.all()
    }
    return render(request, 'index.html', context)

def checkout(request):
    last = Order.objects.last()
    price = last.total_price
    whole_order = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    whole_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    context = {
        'orders': whole_order,
        'total': whole_price,
        'bill': price,
    }
    return render(request, 'checkout.html', context)

def purchase(request):
    if request.method == 'POST':
        this_product = Product.objects.filter(id=request.POST['id'])
        if not this_product:
            return redirect('/checkout')
        else:
            quantity = int(request.POST['quantity'])
            total_charge = quantity*(float(this_product[0].price))
            Order.objects.create(quantity_ordered=quantity, total_price=total_charge)
            return redirect('/checkout')
    else:
        return redirect('/')

    