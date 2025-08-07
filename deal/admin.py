from django.contrib import admin
from .models import Contract, LandContract, ApartmentContract, HouseContract, HutContract, Deal, ContractComment, DealComment

class DealCommentInline(admin.TabularInline):
    model = DealComment
    extra = 1
    readonly_fields = ['created_at']
    fields = ['user', 'content', 'created_at']

class ContractCommentInline(admin.TabularInline):
    model = ContractComment
    extra = 1
    readonly_fields = ['created_at']
    fields = ['user', 'content', 'created_at']

# Base contract admin customization
class ContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract_type', 'property_type', 'created_by', 'open_at', 'closed_at']
    search_fields = ['created_by__username', 'contract_type', 'property_type']
    list_filter = ['contract_type', 'property_type', 'created_by']
    ordering = ['open_at']
    date_hierarchy = 'open_at'
    inlines = [ContractCommentInline]

    fieldsets = (
        (None, {
            'fields': ('created_by', 'contract_type', 'property_type', 'open_at')
        }),
        ('Contract Closure', {
            'fields': ('closed_at', 'closed_deal'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

class LandContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'land_size', 'is_agricultural', 'created_by', 'open_at', 'closed_at']
    search_fields = ['created_by__username', 'land_size']
    list_filter = ['is_agricultural', 'created_by']
    inlines = [ContractCommentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

class ApartmentContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'floor_number', 'num_bedrooms', 'has_parking', 'created_by', 'open_at', 'closed_at']
    search_fields = ['created_by__username', 'floor_number', 'num_bedrooms']
    list_filter = ['has_parking', 'created_by']
    inlines = [ContractCommentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

class HouseContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'num_bedrooms', 'num_bathrooms', 'has_garden', 'created_by', 'open_at', 'closed_at']
    search_fields = ['created_by__username', 'num_bedrooms', 'num_bathrooms']
    list_filter = ['has_garden', 'created_by']
    inlines = [ContractCommentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

class HutContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_rural', 'created_by', 'open_at', 'closed_at']
    search_fields = ['created_by__username']
    list_filter = ['is_rural', 'created_by']
    inlines = [ContractCommentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by')

class DealAdmin(admin.ModelAdmin):
    list_display = ['id', 'contract', 'contract_owner', 'witness_1', 'witness_2', 'status', 'get_contract_display']
    search_fields = ['contract_owner__username', 'contract__id']
    list_filter = ['status', 'contract_owner']
    ordering = ['status', 'contract__open_at']
    inlines = [DealCommentInline]

    def get_contract_display(self, obj):
        return f"Contract {obj.contract.id}"
    get_contract_display.short_description = 'Contract'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('contract', 'contract_owner', 'witness_1', 'witness_2')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class DealCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'deal', 'user', 'created_at']
    search_fields = ['deal__id', 'user__username']
    list_filter = ['created_at']
    ordering = ['created_at']

# Register models with the admin interface
admin.site.register(Contract, ContractAdmin)
admin.site.register(LandContract, LandContractAdmin)
admin.site.register(ApartmentContract, ApartmentContractAdmin)
admin.site.register(HouseContract, HouseContractAdmin)
admin.site.register(HutContract, HutContractAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(ContractComment)
admin.site.register(DealComment, DealCommentAdmin)
