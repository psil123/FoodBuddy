from django.contrib import admin

from .models import *

#Used for admin page. All models displayed there need to be registered here
admin.site.register(UserDetail)
# admin.site.register(Employee)
admin.site.register(Restaurant)
admin.site.register(Bookings)
# admin.site.register(Prices)
# admin.site.register(Restaurant_Item)
# admin.site.register(Order)
# admin.site.register(Delivery_Item)