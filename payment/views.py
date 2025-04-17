from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import hashlib



def payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        amount= str(int(float(amount)*100))

        merchant_id = 'MC19125'
        password = '123456'
        integrity_salt = 'b37fs7g95h'
        return_url = 'http://127.0.0.1:8000/payment/return/'
        post_url = 'https://sandbox.jazzcash.com.pk/CustomerPortal/transactionmanagement/merchantform/'
        txn_ref = 'T' + datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
        txn_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        expiry_datetime = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y%m%d%H%M%S')

        data = {
            'pp_Version': '1.1',
            'pp_TxnType': 'MWALLET',
            'pp_Language': 'EN',
            'pp_MerchantID': merchant_id,
            'pp_Password': password,
            'pp_TxnRefNo': txn_ref,
            'pp_Amount': amount,
            'pp_TxnCurrency': 'PKR',
            'pp_TxnDateTime': txn_datetime,
            'pp_BillReference': 'billRef',
            'pp_Description': 'Test Payment',
            'pp_TxnExpiryDateTime': expiry_datetime,
            'pp_ReturnURL': return_url,
            'pp_SecureHash': '',  # Abhi calculate karenge
            'ppmpf_1': 'custom1',
            'ppmpf_2': 'custom2',
            'ppmpf_3': 'custom3',
            'ppmpf_4': 'custom4',
            'ppmpf_5': 'custom5',
        }

        # SecureHash generate karna
        sorted_keys = sorted(data.keys())
        hash_string = integrity_salt + '&' + '&'.join(f"{key}={data[key]}" for key in sorted_keys)
        secure_hash = hashlib.sha256(hash_string.encode()).hexdigest().upper()
        data['pp_SecureHash'] = secure_hash

        return render(request, 'payment/payment_page.html', {'data': data, 'post_url': post_url})
    
    return render(request, 'payment/payment_page.html')


def payment_response(request):
    return HttpResponse("Payment processed (test mode)")

@csrf_exempt
def payment_return(request):
    if request.method == 'POST':
        response_data = request.POST.dict()

        # Format amount (divide by 100 if it was multiplied)
        amount = int(response_data.get('pp_Amount', 0)) / 100

        # Format date/time (20250416141037 → 2025-04-16 14:10:37)
        raw_datetime = response_data.get('pp_TxnDateTime', '')
        txn_datetime = ''
        if len(raw_datetime) == 14:
            txn_datetime = f"{raw_datetime[:4]}-{raw_datetime[4:6]}-{raw_datetime[6:8]} {raw_datetime[8:10]}:{raw_datetime[10:12]}:{raw_datetime[12:14]}"

        context = {
            'txn_ref': response_data.get('pp_TxnRefNo', 'N/A'),
            'amount': f"{amount:.2f} PKR",
            'status': response_data.get('pp_ResponseMessage', 'Pending'),
            'txn_datetime': txn_datetime,
        }
        return render(request, 'payment/payment_return.html', context)

    return render(request, 'payment/payment_return.html')



