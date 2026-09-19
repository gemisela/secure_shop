from django.contrib import admin
from .models import Transaction
admin.site.register(Transaction)


from .models import SecurityEvent

@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "test_type", "user", "hmac_valid", "nonce_valid", "accepted")
    list_filter = ("test_type", "hmac_valid", "nonce_valid", "accepted")
    search_fields = ("nonce", "received_hmac", "calculated_hmac", "reason")
