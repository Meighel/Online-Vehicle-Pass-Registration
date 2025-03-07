from django.contrib import admin
from .models import User, Security, Cashier, Vehicle, Registration, Verified


admin.site.register(User)
admin.site.register(Security)
admin.site.register(Cashier)
admin.site.register(Vehicle)
admin.site.register(Registration)
admin.site.register(Verified)


#for future revision
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('lastName', 'dlNumber', 'corporateemail')