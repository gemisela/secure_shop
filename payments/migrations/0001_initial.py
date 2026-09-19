# Generated for SecureShop academic project
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=40, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nonce', models.CharField(max_length=64, unique=True)),
                ('hmac_signature', models.CharField(max_length=64)),
                ('status', models.CharField(default='VALIDEE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_type', models.CharField(choices=[('normal','Transaction normale'),('tamper_amount','Altération du montant'),('replay','Attaque par rejeu'),('fake_hmac','Falsification HMAC'),('manual_tamper','Manipulation manuelle'),('manual_replay','Rejeu manuel')], max_length=30)),
                ('original_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('received_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('nonce', models.CharField(max_length=128)),
                ('received_hmac', models.CharField(max_length=128)),
                ('calculated_hmac', models.CharField(max_length=128)),
                ('hmac_valid', models.BooleanField(default=False)),
                ('nonce_valid', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('reason', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='security_events', to='payments.transaction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering':['-created_at']},
        ),
    ]
