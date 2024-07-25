import requests

def verify_payment(payment_ref):
    url = f'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/{payment_ref}'
    headers = {
        'Ocp-Apim-Subscription-Key': 'YOUR_SUBSCRIPTION_KEY',
        'X-Reference-Id': payment_ref,
        'X-Target-Environment': 'sandbox',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get('status')
        return status == 'SUCCESSFUL'
    return False
