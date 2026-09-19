from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Transaction, SecurityEvent
from .security import sign
import hmac

@login_required
def payment_journal(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/payment_journal.html', {'transactions': transactions})

@login_required
def integrity_lab(request, tx_id):
    tx = get_object_or_404(Transaction, id=tx_id, user=request.user)
    result = None
    form_data = {
        'reference': tx.reference,
        'amount': str(tx.amount),
        'nonce': tx.nonce,
        'signature': tx.hmac_signature,
    }

    if request.method == 'POST':
        form_data = {
            'reference': request.POST.get('reference', '').strip(),
            'amount': request.POST.get('amount', '').strip(),
            'nonce': request.POST.get('nonce', '').strip(),
            'signature': request.POST.get('signature', '').strip(),
        }
        try:
            received_amount = Decimal(form_data['amount'])
            calculated = sign(form_data['reference'], str(received_amount), form_data['nonce'])
            hmac_valid = hmac.compare_digest(form_data['signature'], calculated)

            # A nonce is legitimate only for the original payment it belongs to.
            nonce_owner = Transaction.objects.filter(nonce=form_data['nonce']).first()
            nonce_valid = nonce_owner is not None and nonce_owner.id == tx.id
            reference_valid = form_data['reference'] == tx.reference
            amount_unchanged = received_amount == tx.amount

            # Re-submitting the exact original payment is treated as replay in the lab.
            exact_original = reference_valid and amount_unchanged and form_data['nonce'] == tx.nonce and hmac_valid
            replay = exact_original

            if not hmac_valid:
                accepted = False
                reason = "Intégrité compromise : la signature HMAC reçue ne correspond pas au message recalculé."
                event_type = 'manual_tamper'
            elif not nonce_valid:
                accepted = False
                reason = "Attaque par rejeu / nonce invalide : ce nonce n'appartient pas à la transaction sélectionnée."
                event_type = 'manual_replay'
            elif replay:
                accepted = False
                reason = "Attaque par rejeu détectée : cette transaction a déjà été acceptée et son nonce a déjà été consommé."
                event_type = 'manual_replay'
            else:
                accepted = False
                reason = "Transaction refusée : les données ne correspondent pas au paiement original."
                event_type = 'manual_tamper'

            SecurityEvent.objects.create(
                test_type=event_type,
                user=request.user,
                transaction=tx,
                original_amount=tx.amount,
                received_amount=received_amount,
                nonce=form_data['nonce'],
                received_hmac=form_data['signature'],
                calculated_hmac=calculated,
                hmac_valid=hmac_valid,
                nonce_valid=nonce_valid and not replay,
                accepted=accepted,
                reason=reason,
            )
            result = {
                'accepted': accepted,
                'reason': reason,
                'calculated_hmac': calculated,
                'hmac_valid': hmac_valid,
                'nonce_valid': nonce_valid and not replay,
                'replay': replay,
                'https_active': request.is_secure(),
            }
        except (InvalidOperation, ValueError):
            result = {'accepted': False, 'reason': 'Montant invalide.', 'hmac_valid': False, 'nonce_valid': False, 'https_active': request.is_secure()}

    security_events = SecurityEvent.objects.filter(user=request.user, transaction=tx).order_by('-created_at')[:20]
    return render(request, 'payments/integrity_lab.html', {'tx': tx, 'form_data': form_data, 'result': result, 'security_events': security_events})

@login_required
def security_journal(request):
    events = SecurityEvent.objects.filter(user=request.user).select_related('transaction').order_by('-created_at')
    return render(request, 'payments/security_journal.html', {'events': events})
