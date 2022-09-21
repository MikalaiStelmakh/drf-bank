from django.contrib import admin

from bank.models import (Customer, Account,
                         Replenishment, Transfer)


admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Replenishment)
admin.site.register(Transfer)
