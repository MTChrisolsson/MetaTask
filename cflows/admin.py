from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Car
from .models.station import StationConfiguration

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'make', 'model', 'color', 'year', 
                   'mileage', 'organization', 'status_badge', 'created_at')
    list_filter = ('organization', 'make', 'year', 'is_active', 'is_archived')
    search_fields = ('registration_number', 'make', 'model')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'organization',
                ('make', 'model'),
                ('registration_number', 'color'),
                ('year', 'mileage'),
            )
        }),
        ('Status Information', {
            'fields': (
                'is_active',
                'is_archived',
                'is_deleted',
                ('created_at', 'updated_at'),
            )
        }),
        ('Station & Workflow', {
            'fields': ('station_fields',),
            'classes': ('collapse',),
            'description': 'Current status and history in different stations'
        }),
        ('Additional Information', {
            'fields': (
                'files',
                'metadata',
                'tags',
                'notes',
                'messages',
                'custom_car_info'
            ),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        """Display status as a colored badge"""
        if not obj.is_active:
            return format_html(
                '<span style="background-color: #ff6b6b; color: white; padding: 3px 10px; border-radius: 3px;">Inactive</span>'
            )
        if obj.is_archived:
            return format_html(
                '<span style="background-color: #868e96; color: white; padding: 3px 10px; border-radius: 3px;">Archived</span>'
            )
        if obj.is_deleted:
            return format_html(
                '<span style="background-color: #e03131; color: white; padding: 3px 10px; border-radius: 3px;">Deleted</span>'
            )
        
        # Get current station status
        for station, data in obj.station_fields.items():
            if isinstance(data, dict) and data.get('status'):
                return format_html(
                    '<span style="background-color: #37b24d; color: white; padding: 3px 10px; border-radius: 3px;">{}: {}</span>',
                    station.title(),
                    data['status']
                )
        
        return format_html(
            '<span style="background-color: #37b24d; color: white; padding: 3px 10px; border-radius: 3px;">Active</span>'
        )
    
    status_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        """Ensure proper handling when saving from admin"""
        if not change:  # If this is a new car
            if not obj.organization and request.user.organization:
                obj.organization = request.user.organization
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Filter cars based on user's organization unless superuser"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter organization choices based on user's access"""
        if db_field.name == "organization" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.organization.__class__.objects.filter(
                id=request.user.organization.id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
        js = ('js/admin/car_admin.js',)

@admin.register(StationConfiguration)
class StationConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'order', 'is_active', 'required', 'default_status')
    list_filter = ('organization', 'is_active', 'required')
    search_fields = ('name', 'organization__name')
    ordering = ('organization', 'order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'organization',
                'name',
                'description',
                'order',
            )
        }),
        ('Status Configuration', {
            'fields': (
                'default_status',
                'allowed_statuses',
                'is_active',
                'required',
            ),
            'description': 'Configure the possible statuses for this station'
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.organization.__class__.objects.filter(
                id=request.user.organization.id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)

    def save_model(self, request, obj, form, change):
        if not change and not obj.organization and request.user.organization:
            obj.organization = request.user.organization
        super().save_model(request, obj, form, change)
