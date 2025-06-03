from django.contrib import admin
from .models import Register,Product,Feedback,Cart,Payment,staff_login,FoodItem,YemaniFoodItem,yemani_login


admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(staff_login)
admin.site.register(FoodItem)
admin.site.register(YemaniFoodItem)
admin.site.register(yemani_login)


# Register your models here.