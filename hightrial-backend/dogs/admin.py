from django.contrib import admin
from .models import Dog, Kennel, ColorGenetics, Wallet, Litter

# Register your models here.
admin.site.register(Dog)
admin.site.register(Kennel)
admin.site.register(ColorGenetics)
admin.site.register(Wallet)
admin.site.register(Litter)