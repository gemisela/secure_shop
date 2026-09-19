from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = "Crée les produits de démonstration avec leurs images."

    def handle(self, *args, **kwargs):
        data = [
            ('Ordinateur Portable', 'Dell Inspiron 15', 500, 'ordinateur-portable.png'),
            ('Smartphone', 'Samsung Galaxy', 300, 'smartphone.png'),
            ('Casque Audio', 'Casque stéréo', 50, 'casque-audio.png'),
            ('Montre Connectée', 'Smart Watch', 120, 'montre-connectee.png'),
            ('Clavier Mécanique', 'Clavier professionnel', 40, 'clavier-mecanique.png'),
            ('Souris Sans Fil', 'Souris ergonomique', 25, 'souris-sans-fil.png'),
        ]
        for name, description, price, filename in data:
            product, _ = Product.objects.update_or_create(
                name=name,
                defaults={'description': description, 'price': price},
            )
            source = Path(settings.MEDIA_ROOT) / 'products' / filename
            if source.exists() and not product.image:
                # Les images sont déjà dans MEDIA_ROOT; enregistrer seulement le chemin relatif.
                product.image.name = f'products/{filename}'
                product.save(update_fields=['image'])
        self.stdout.write(self.style.SUCCESS('Produits avec images créés/mis à jour.'))
