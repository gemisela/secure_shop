import hmac,hashlib,secrets
from django.conf import settings

def generate_nonce(): return secrets.token_hex(16)
def sign(reference,amount,nonce):
 msg=f'{reference}|{amount}|{nonce}'.encode(); return hmac.new(settings.PAYMENT_HMAC_KEY.encode(),msg,hashlib.sha256).hexdigest()
def verify(reference,amount,nonce,signature): return hmac.compare_digest(sign(reference,amount,nonce),signature)
