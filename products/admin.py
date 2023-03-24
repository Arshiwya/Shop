from django.contrib import admin
from .models import Category  , Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price' , 'status' ]
    ordering = ['-price']

    # prepopulated_fields = {
    #     'slug' : ('name' , )
    # }



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug' , 'parent']
    ordering = ['name']

    # prepopulated_fields = {
    #     'slug' : ('name' , )
    # }




admin.site.register(Category , CategoryAdmin)
admin.site.register(Product , ProductAdmin)

