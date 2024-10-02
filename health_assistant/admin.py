from django.contrib import admin
from .models import CustomUser, Profile, Patient
from django.contrib.auth.admin import UserAdmin

# Register the CustomUser with the default UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

# Register the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'location', 'birth_date']
    search_fields = ['user__username', 'bio', 'location']

# Register the Patient model
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'symptoms', 'predicted_disease']
    search_fields = ['name', 'symptoms', 'predicted_disease']
    list_filter = ['user']

# Register the models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Patient, PatientAdmin)
