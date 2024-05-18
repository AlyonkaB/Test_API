from django.contrib import admin

from db.models import Bus, Facility, Trip, Order, Ticket


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Bus)
admin.site.register(Facility)
admin.site.register(Trip)
admin.site.register(Ticket)
