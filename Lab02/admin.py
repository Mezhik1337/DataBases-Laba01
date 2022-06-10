from django.contrib import admin
from .models import City, Competition,Judje, Sportsman, Team, Trainer
admin.site.register(City)
admin.site.register(Judje)
admin.site.register(Team)
admin.site.register(Trainer)
admin.site.register(Sportsman)
admin.site.register(Competition)
# Register your models here.
