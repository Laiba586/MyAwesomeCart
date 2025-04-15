from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def payment(request):
    if request.method == "POST":
        amount = request.POST['amount']
        return render(request, 'payment/processing.html', {'amount': amount})
    return render(request, 'payment/payment_page.html')


@csrf_exempt
def payment_response(request):
    return HttpResponse("Payment processed (test mode)")