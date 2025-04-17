from django.shortcuts import render,redirect
from .models import Product, Contact, Order,OrderUpdate
from math import ceil

from payment.views import payment
from .models import Order


# Create your views here.
from django.http import HttpResponse,JsonResponse


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html',{'thank':thank})


def tracker(request):
    if request.method=="POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsjson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')





def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product':product[0]})


  # or whatever your payment view is



def checkout(request):
    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            amount=request.POST.get('amount'),
            items_json=request.POST.get('itemsJson'),
            phone=request.POST.get('phone'),
        )
        request.session['order_id'] = order.order_id
        request.session['amount'] = request.POST.get('amount')
        return redirect('payment')  # redirect to payment page

    return render(request, 'shop/checkout.html')  # Show checkout form on GET


def catagories(request):
    return render(request, 'shop/catagories.html')



