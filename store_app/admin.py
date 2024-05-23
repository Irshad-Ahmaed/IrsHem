from django.contrib import admin

# Register your models here.
from .models import *

class ImagesTabularinline(admin.TabularInline):
    model = Photo

class TagsTabularinline(admin.TabularInline):
    model = Tags

class ProductAdmin(admin.ModelAdmin):
    inlines =[ImagesTabularinline,TagsTabularinline]

class OrderItemTabularinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines =[OrderItemTabularinline]

admin.site.register(Photo)
admin.site.register(Tags)

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)

admin.site.register(Product,ProductAdmin)

admin.site.register(Contact_us)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Product_review)
