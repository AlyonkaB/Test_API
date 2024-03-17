from django.contrib import admin

from db.models import Bus, Facility, Trip, Order, Ticket

admin.site.register(Bus)
admin.site.register(Facility)
admin.site.register(Trip)
admin.site.register(Order)
admin.site.register(Ticket)
