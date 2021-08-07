﻿import urllib.request
import urllib.parse
import json
import hmac
import hashlib
from datetime import datetime
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from users.models import User, BillPay
from VnPay.forms import MomoPaymentForm, PaymentForm
from VnPay.vnpay import vnpay
from django.conf import settings


def index(request):
    return render(request, "VnPay/index.html", {"title": "Danh sách demo"})

# VNPAY
def payment(request):
    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        user = request.user
        datetCreate = datetime.now().strftime('%Y%m%d%H%M%S')
        if form.is_valid():
            # get values
            amount = form.cleaned_data['amount']
            # order_id = form.cleaned_data['order_id']
            order_id = datetCreate
            order_type = form.cleaned_data['order_type']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # create bill
            if user.is_authenticated:
                print('logged in')
                bill = BillPay(user=user,amount=amount)
                bill.save()
                order_id = order_id +"_order_id"+ str(bill.id)
            else:
                return JsonResponse({'code': '403', 'Message': 'Hay dang nhap truoc', 'data': ''})
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            # vnp.requestData['vnp_Merchant'] = 'DEMO'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetCreate  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            # 
            
            if request.is_ajax():
                # Show VNPAY Popup
                result = JsonResponse({'code': '00', 'Message': 'Init Success', 'data': vnpay_payment_url})
                return result
            else:
                # Redirect to VNPAY
                return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "VnPay/payment.html", {"title": "Thanh toán"})


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            if firstTimeUpdate:
                if vnp_ResponseCode == '00':
                    bill_id = int(order_id.split("_order_id")[1])
                    bill = BillPay.objects.filter(id=bill_id).first()
                    if bill:
                        bill.status = 1
                        user = bill.user
                        if user:
                            user.coin += bill.amount
                            bill.save()
                            user.save()
                            print('Payment Success. Your code implement here')
                else:
                    print('Payment Error. Your code implement here')

                # Return VNPAY: Merchant update success
                result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
            else:
                # Already Update
                result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})

        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "VnPay/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "VnPay/payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "VnPay/payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "VnPay/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def query(request):
    if request.method == 'GET':
        return render(request, "VnPay/query.html", {"title": "Kiểm tra kết quả giao dịch"})
    else:
        # Add paramter
        vnp = vnpay()
        vnp.requestData = {}
        vnp.requestData['vnp_Command'] = 'querydr'
        vnp.requestData['vnp_Version'] = '2.0.0'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
        vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
        vnp.requestData['vnp_TransDate'] = request.POST['trans_date']  # 20150410063022
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
        vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
        requestUrl = vnp.get_payment_url(settings.VNPAY_API_URL, settings.VNPAY_HASH_SECRET_KEY)
        try:
            responseData = urllib.request.urlopen(requestUrl).read().decode()
        except:
            return render(request, "VnPay/query.html", {"title": "Kiểm tra kết quả giao dịch", "data": {"message":"server vnpay không phản hồi"}})
        print('RequestURL:' + requestUrl)
        print('VNPAY Response:' + responseData)
        data = responseData.split('&')
        for x in data:
            tmp = x.split('=')
            if len(tmp) == 2:
                vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')
        if vnp.responseData['vnp_ResponseCode'] == '00':
            print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
        return render(request, "VnPay/query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


def refund(request):
    return render(request, "VnPay/refund.html", {"title": "Gửi yêu cầu hoàn tiền"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# MOMO
def momo_payment(request):
    if request.method == 'POST':
        # momo
        form = MomoPaymentForm(request.POST)
        user = request.user
        datetCreate = datetime.now().strftime('%Y%m%d%H%M%S')
        if form.is_valid():
            # get values
            username = form.cleaned_data['username']
            amount = str(form.cleaned_data['amount'])
            orderInfo = form.cleaned_data['order_desc']

            #parameters send to MoMo get get payUrl
            endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
            # endpoint = "https://payment.momo.vn"

            partnerCode = "MOMONCUJ20210804"
            accessKey = "q4jewga5A5QURIBN"
            serectkey = b"KDbueVZray9IZpODOLJvsx7XFDcyNmZ4"

            returnUrl = settings.MOMO_RETURN_URL
            notifyurl = settings.MOMO_IPN_URL

            orderId = datetCreate
            # create bill
            if user.is_authenticated:
                print('logged in')
                bill = BillPay(user=user,amount=int(amount))
                bill.save()
                orderId = orderId +"_order_id"+ str(bill.id)
            else:
                return JsonResponse({'code': '403', 'Message': 'Hay dang nhap truoc', 'data': ''})
            requestId = datetCreate +"_username_"+ username
            requestType = "captureMoMoWallet"
            extraData = "" #pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store

            #before sign HMAC SHA256 with format
            #partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
            rawSignature = "partnerCode="+partnerCode+"&accessKey="+accessKey+"&requestId="+requestId+"&amount="+amount+"&orderId="+orderId+"&orderInfo="+orderInfo+"&returnUrl="+returnUrl+"&notifyUrl="+notifyurl+"&extraData="+extraData
            rawSignature = bytes(rawSignature,'utf-8')

            #puts raw signature
            print("--------------------RAW SIGNATURE----------------")
            print(rawSignature)
            #signature
            h = hmac.new( serectkey, rawSignature, hashlib.sha256 )
            signature = h.hexdigest()
            print("--------------------SIGNATURE----------------")
            print(signature)

            #json object send to MoMo endpoint

            data = {
                    'partnerCode' : partnerCode,
                    'accessKey' : accessKey,
                    'requestId' : requestId,
                    'amount' : amount,
                    'orderId' : orderId,
                    'orderInfo' : orderInfo,
                    'returnUrl' : returnUrl,
                    'notifyUrl' : notifyurl,
                    'extraData' : extraData,
                    'requestType' : requestType,
                    'signature' : signature
            }
            print("--------------------JSON REQUEST----------------\n")
            data = json.dumps(data).encode('utf-8')
            print(data)

            clen = len(data)

            headers = {}
            headers['Content-Type']='application/json; charset=UTF-8'
            headers['Content-Length']=clen

            try:
                req = urllib.request.Request(endpoint, data=data, headers=headers)
                f = urllib.request.urlopen(req)

                response = f.read()
                f.close()
                print("--------------------JSON response----------------\n")
                print(response.decode('utf-8')+"\n")
                
                payUrl = json.loads(response)['payUrl']
                print("payUrl\n")
                print(payUrl+"\n")
                if request.is_ajax():
                    # Show Momo Popup
                    result = JsonResponse({'code': '00', 'Message': 'Init Success', 'data': payUrl})
                    return result
                else:
                    # Redirect to Momo
                    return redirect(payUrl)
            except:
                result = JsonResponse({'code': '403', 'Message': 'không thể kết nối tới momo', 'data': ""})
                return result
        else:
            print("Form input not validate")
            result = JsonResponse({'code': '-1', 'Message': 'Form input not validate', 'data': ""})
            return result
    else:
        return render(request, "VnPay/momo_payment.html", {"title": "Thanh toán"})

@csrf_exempt
def momo_payment_ipn(request):
    if request.method == "POST":
        inputData = request.POST
        if inputData:
            partnerCode = inputData['partnerCode']
            accessKey = inputData['accessKey']
            requestId = inputData['requestId']
            orderId = inputData['orderId']
            orderInfo = inputData['orderInfo']
            amount = int(inputData['amount'])
            transId = inputData['transId']
            message = inputData['message']
            localMessage = inputData['localMessage']
            errorCode = int(inputData['errorCode'])
            extraData = inputData['extraData']


            if errorCode == 0:
                # cộng tiền vào tài khoản admin
                user = User.objects.filter(username='admin').first()
                if user:
                    bill = BillPay(user=user,amount=amount, status=1)
                    bill.save()
                    user.coin += bill.amount
                    user.save()
                    print('Payment Success. Your code implement here')
                    message = "Hoàn thành giao dịch."
                else:
                    message = "Không tồn tại user admin"
            else:
                message = "giao dịch không thành công"

            # Signature
            serectkey = b"KDbueVZray9IZpODOLJvsx7XFDcyNmZ4"
            responseTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rawSignature = "partnerCode="+partnerCode+"&accessKey="+accessKey+"&requestId="+requestId+"&orderId="+orderId+"&errorCode="+str(errorCode)+"&message="+message+"&responseTime="+responseTime+"&extraData="+extraData
            rawSignature = bytes(rawSignature,'utf-8')
            h = hmac.new( serectkey, rawSignature, hashlib.sha256 )
            signature = h.hexdigest()

            data = {
                'partnerCode' : partnerCode,
                'accessKey' : accessKey,
                'requestId' : requestId,
                'orderId' : orderId,
                'errorCode' : errorCode,
                'message' : message,
                'responseTime' : responseTime,
                'extraData' : extraData,
                'signature' : signature
            }
            return JsonResponse(data ,status=200, content_type='application/json;charset=UTF-8')
    return JsonResponse({"message":"Ko có thông tin"},status=200, content_type='application/json;charset=UTF-8')


def momo_payment_return(request):
    inputData = request.GET
    if inputData:
        requestId = inputData['requestId']
        orderId = inputData['orderId']
        amount = int(inputData['amount'])
        orderInfo = inputData['orderInfo']
        transId = inputData['transId']
        message = inputData['message']
        localMessage = inputData['localMessage']
        responseTime = inputData['responseTime']
        errorCode = int(inputData['errorCode'])

        return render(request, "VnPay/momo_payment_return.html",
                        {"title": "Kết quả thanh toán",
                        "requestId": requestId,
                        "orderId": orderId,
                        "amount": amount,
                        "orderInfo": orderInfo,
                        "transId": transId,
                        "message": message,
                        "localMessage": localMessage,
                        "errorCode": errorCode,
                        "responseTime": responseTime
                        }
    )
    else:
        return render(request, "VnPay/momo_payment_return.html", {"title": "Kết quả thanh toán", "localMessage": ""})
