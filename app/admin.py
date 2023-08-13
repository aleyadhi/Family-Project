from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from app.models import Family, Details


User = get_user_model()
admin.site.unregister(User)

class FamilyInline(admin.StackedInline):
    model= Family
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines= [FamilyInline]
    list_display = ['username']

admin.site.register(User, UserAdmin)

class DetailsAdmin(admin.StackedInline):
    model= Details
    extra = 0

class FamilyAdmin(admin.ModelAdmin):
    inlines = [DetailsAdmin]
    list_display = ['id', 'name', 'slug', 'phone']
    search_fields = ['name']

admin.site.register(Family, FamilyAdmin)