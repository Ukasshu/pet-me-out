from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserData)
admin.site.register(Pet)
admin.site.register(Stay)
admin.site.register(StayRequest)
admin.site.register(StayPossibility)
admin.site.register(Conversation)
admin.site.register(Message)

