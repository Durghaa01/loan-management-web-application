from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, ActivityLog
from .models import Application
from .models import Customer
from core.models import Agreement



@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("email", "full_name", "role", "can_steps_1_4", "can_steps_5_7", "is_active")
    list_filter = ("role", "can_steps_1_4", "can_steps_5_7", "is_active")
    ordering = ("email",)
    search_fields = ("email", "full_name")

    fieldsets = (
        (None, {"fields": ("email", "password", "full_name")}),
        ("Permissions", {"fields": ("role", "can_steps_1_4", "can_steps_5_7", "is_active")}),
        ("Admin Flags", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "full_name", "role", "can_steps_1_4", "can_steps_5_7", "password1", "password2")}),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action")
    search_fields = ("action", "user__email")
    list_filter = ("created_at",)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "ic_or_passport_no", "phone_number", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "ic_or_passport_no", "phone_number")


    def has_change_permission(self, request, obj=None):
        # Only admin can approve/reject
        if request.user.role in ["ADMIN", "MASTER_ADMIN"]:
            return True
        return False

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "ic_number", "phone", "is_active")
    search_fields = ("full_name", "ic_number", "phone", "email")
    list_filter = ("is_active", "created_at")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic", {"fields": ("full_name", "ic_number", "phone", "email", "is_active")}),
        ("Profile", {"fields": ("address", "gender", "date_of_birth")}),
        ("Application Link", {"fields": ("application",)}),
        ("Internal", {"fields": ("internal_note",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

from .models import CustomerDocument

@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ("uploaded_at", "customer", "doc_type", "note")
    list_filter = ("doc_type", "uploaded_at")
    search_fields = ("customer__ic_number", "customer__full_name", "note")



@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ("agreement_number", "customer", "status", "agreement_date")
    list_filter = ("status", )
    search_fields = ("agreement_number", "customer__full_name")

from core.models import InternalLedgerEntry, OfficialLedgerRecord

@admin.register(InternalLedgerEntry)
class InternalLedgerEntryAdmin(admin.ModelAdmin):
    list_display = ("entry_date", "agreement", "entry_type", "principal_amount", "interest_amount", "created_by")
    list_filter = ("entry_type", "entry_date")
    search_fields = ("agreement__agreement_number", "agreement__customer__full_name")

@admin.register(OfficialLedgerRecord)
class OfficialLedgerRecordAdmin(admin.ModelAdmin):
    list_display = ("record_date", "agreement", "ledger_open_no", "record_type", "principal_amount_reported", "interest_amount_reported", "created_by")
    list_filter = ("record_type", "record_date")
    search_fields = ("agreement__agreement_number", "agreement__customer__full_name")

from core.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_date", "agreement", "method",
        "amount_principal", "amount_interest",
        "reported_principal", "reported_interest",
        "created_by"
    )
    list_filter = ("method", "payment_date")
    search_fields = ("agreement__agreement_number", "agreement__customer__full_name", "reference_note")

from core.models import Receipt

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "receipt_date", "customer", "agreement", "payment", "total_amount", "created_by")
    list_filter = ("receipt_date",)
    search_fields = ("receipt_number", "customer__full_name", "agreement__agreement_number")

from core.models import MessageTemplate

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "language", "title", "is_active", "created_by", "created_at")
    list_filter = ("key", "language", "is_active")
    search_fields = ("title", "body")

from core.models import SystemSetting

@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at", "updated_by")
    search_fields = ("key", "value")
