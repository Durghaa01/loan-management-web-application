from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email).lower()

        # Keep username as email (your design)
        extra_fields.setdefault("username", email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        extra_fields.setdefault("role", User.Role.MASTER_ADMIN)
        extra_fields.setdefault("can_steps_1_4", True)
        extra_fields.setdefault("can_steps_5_7", True)
        extra_fields.setdefault("must_change_password", False)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        MASTER_ADMIN = "MASTER_ADMIN", "Master Admin"
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"

    username = models.CharField(max_length=255, unique=True)  # you keep it
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(max_length=100, blank=True)

    # Permissions by steps (NOT company)
    can_steps_1_4 = models.BooleanField(default=False)
    can_steps_5_7 = models.BooleanField(default=False)

    must_change_password = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)

    # ✅ Needed for Django admin + auth
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


class ActivityLog(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=200)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} - {self.action}"


class Application(models.Model):
    
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    MARITAL_SINGLE = "SINGLE"
    MARITAL_MARRIED = "MARRIED"
    MARITAL_WIDOW = "WIDOW"

    MARITAL_CHOICES = [
        (MARITAL_SINGLE, "Single / Bujang"),
        (MARITAL_MARRIED, "Married / Berkahwin"),
        (MARITAL_WIDOW, "Widow / Janda"),
    ]

    YES = "YES"
    NO = "NO"

    YES_NO_CHOICES = [
        (YES, "Yes / Ya"),
        (NO, "No / Tidak"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    full_name = models.CharField(max_length=200)
    ic_or_passport_no = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_CHOICES,
        blank=True
    )

    home_address = models.TextField(blank=True)

    phone_number_2 = models.CharField(
        max_length=30,
        blank=True
    )

    home_phone_number = models.CharField(
        max_length=30,
        blank=True
    )

    employer_name = models.CharField(
        max_length=200,
        blank=True
    )

    employer_address = models.TextField(blank=True)

    office_phone_number = models.CharField(
        max_length=30,
        blank=True
    )

    total_working_years = models.CharField(
        max_length=50,
        blank=True
    )

    net_salary_after_deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_bank = models.CharField(
        max_length=100,
        blank=True
    )

    salary_bank_other = models.CharField(
        max_length=100,
        blank=True
    )

    has_other_income = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        blank=True
    )

    other_income_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    other_income_name = models.CharField(
        max_length=200,
        blank=True
    )

    spouse_full_name = models.CharField(
        max_length=200,
        blank=True
    )

    spouse_ic_number = models.CharField(
        max_length=50,
        blank=True
    )

    spouse_job = models.CharField(
        max_length=200,
        blank=True
    )

    spouse_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    number_of_children = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    number_of_working_children = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    borrowing_from_licensed_lender = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        blank=True
    )

    licensed_lender_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    has_other_loans = models.CharField(
        max_length=10,
        choices=YES_NO_CHOICES,
        blank=True
    )

    car_loan_commitment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    house_loan_commitment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    house_rental_commitment = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
)

    motorcycle_commitment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    other_commitment_name = models.CharField(
        max_length=200,
        blank=True
    )

    other_commitment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    amount_wanted_to_borrow = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    loan_reason = models.TextField(blank=True)

    referred_by = models.CharField(
        max_length=200,
        blank=True
    )

    support_status = models.CharField(
        max_length=20,
        choices=[
            ("SUPPORT", "Support"),
            ("NOT_SUPPORT", "Not Support"),
        ],
        blank=True
    )

    support_reason = models.TextField(blank=True)

    submitted_by_staff = models.BooleanField(
        default=False
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # admin-only fields
    admin_note = models.TextField(blank=True, null=True)

    # ✅ MUST be inside the model
    rejection_reason = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.full_name} ({self.ic_or_passport_no}) - {self.status}"

    is_converted_to_customer = models.BooleanField(default=False)

    @property
    def application_number(self):
        return f"APP-{self.pk:06d}"
    

    
    

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    ic_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    id_type = models.CharField(max_length=20,blank=True)

    # Core profile fields (basic for now)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True)  # later can convert to choices
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    marital_status = models.CharField(
        max_length=30,
        blank=True
    )

    home_address_1 = models.TextField(
    blank=True
    )

    home_address_2 = models.TextField(
    blank=True
    )

    home_address_3 = models.TextField(
    blank=True
    )

    home_phone_number = models.CharField(
    max_length=30,
    blank=True
    )

    phone_number_2 = models.CharField(
    max_length=30,
    blank=True
    )

    working_status = models.CharField(
    max_length=30,
    blank=True
    )

    employer_name = models.CharField(
    max_length=255,
    blank=True
    )

    employer_address = models.TextField(
    blank=True
    )

    office_phone_number = models.CharField(
    max_length=30,
    blank=True
    )   

    total_working_years = models.CharField(
    max_length=50,
    blank=True
    )

    spouse_name = models.CharField(
    max_length=255,
    blank=True
    )

    spouse_ic_number = models.CharField(
    max_length=20,
    blank=True
    )

    spouse_age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    spouse_job = models.CharField(
    max_length=255,
    blank=True
    )

    spouse_monthly_income = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    number_of_children = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    number_of_schooling_children = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    number_of_working_children = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    working_children_total_income = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    monthly_net_income = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    basic_monthly_salary = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    other_income_name = models.CharField(
    max_length=255,
    blank=True
    )

    other_income_total = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    car_loan = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    house_loan = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    motorcycle_loan = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    other_loan = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    monthly_loan_total = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    house_type = models.CharField(
    max_length=100,
    blank=True
    )

    house_ownership = models.CharField(
    max_length=50,
    blank=True
    )

    house_monthly_rental = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    house_monthly_bank_payment = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True
    )

    vehicle_type = models.CharField(
    max_length=100,
    blank=True
    )

    vehicle_name = models.CharField(
    max_length=255,
    blank=True
    )

    vehicle_registration_number = models.CharField(
    max_length=50,
    blank=True
    )

    vehicle_color = models.CharField(
        max_length=100,
        blank=True
    )

    vehicle_monthly_bank_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    payment_bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    payment_other_bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    balance_transfer_bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    balance_transfer_other_bank_name = models.CharField(
        max_length=100,
        blank=True
    )

    balance_transfer_account_number = models.CharField(
        max_length=50,
        blank=True
    )

    balance_transfer_account_owner = models.CharField(
        max_length=255,
        blank=True
    )

    introduced_by = models.CharField(
        max_length=255,
        blank=True
    )

    introducer_ic_number = models.CharField(
        max_length=20,
        blank=True
    )

    note = models.TextField(
        blank=True
    )

    internal_note = models.TextField(blank=True)

    application = models.OneToOneField(
        "core.Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    customer_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    customer_photo = models.ImageField(
        upload_to="customer_photos/",
        blank=True,
        null=True
    )

    mykad_photo = models.ImageField(
        upload_to="mykad_photos/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.ic_number})"

    @property
    def display_photo(self):
        if self.customer_photo:
            return self.customer_photo

        if self.mykad_photo:
            return self.mykad_photo

        return None

    @property
    def customer_reference(self):
        return f"CUS-{self.pk:06d}"

class CustomerDocument(models.Model):
    customer = models.ForeignKey(
        "core.Customer",
        on_delete=models.CASCADE,
        related_name="documents"
    )

    doc_type = models.CharField(max_length=50)

    file = models.FileField(upload_to="customer_docs/")

    note = models.CharField(max_length=255, blank=True)

    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer.ic_number} - {self.doc_type}"



class Agreement(models.Model):

    agreement_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="agreements"
    )

    agreement_date = models.DateField()

    principal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    principal_amount_words = models.CharField(
        max_length=255,
        blank=True
    )

    interest_rate_words = models.CharField(
        max_length=100,
        blank=True
    )

    interest_rate_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    monthly_repayment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_repayment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    book = models.CharField(
    max_length=20,
    blank=True,
    default=""
)

    def save(self, *args, **kwargs):

        if not self.agreement_number:

            last_agreement = Agreement.objects.order_by(
                "-id"
            ).first()

            if last_agreement:
                last_number = int(
                    last_agreement.agreement_number.replace(
                        "AGR-",
                        ""
                    )
                )
            else:
                last_number = 0

            self.agreement_number = f"AGR-{last_number + 1:06d}"

        super().save(*args, **kwargs)

    def str(self):
        return self.agreement_number


class InternalLedgerEntry(models.Model):
    TYPE_DISBURSED = "DISBURSED"
    TYPE_PAYMENT = "PAYMENT"
    TYPE_INTEREST = "INTEREST"
    TYPE_ADJUSTMENT = "ADJUSTMENT"

    TYPE_CHOICES = [
        (TYPE_DISBURSED, "Disbursed"),
        (TYPE_PAYMENT, "Payment"),
        (TYPE_INTEREST, "Interest"),
        (TYPE_ADJUSTMENT, "Adjustment"),
    ]

    agreement = models.ForeignKey("Agreement", on_delete=models.CASCADE, related_name="internal_ledger_entries")

    entry_date = models.DateField()
    entry_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    principal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Internal {self.agreement.agreement_number} - {self.entry_type} - {self.entry_date}"


class OfficialLedgerRecord(models.Model):
    TYPE_DISBURSED = "DISBURSED"
    TYPE_PAYMENT = "PAYMENT"
    TYPE_INTEREST = "INTEREST"
    TYPE_ADJUSTMENT = "ADJUSTMENT"

    TYPE_CHOICES = [
        (TYPE_DISBURSED, "Disbursed"),
        (TYPE_PAYMENT, "Payment"),
        (TYPE_INTEREST, "Interest"),
        (TYPE_ADJUSTMENT, "Adjustment"),
    ]

    agreement = models.ForeignKey("Agreement", on_delete=models.CASCADE, related_name="official_ledger_records")

    ledger_open_no = models.PositiveIntegerField()

    record_date = models.DateField()
    record_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    principal_amount_reported = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_amount_reported = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("agreement", "ledger_open_no")

    def save(self, *args, **kwargs):
        if not self.ledger_open_no:
            last_no = (
                OfficialLedgerRecord.objects.filter(agreement=self.agreement)
                .order_by("-ledger_open_no")
                .values_list("ledger_open_no", flat=True)
                .first()
            )
            self.ledger_open_no = (last_no or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Official {self.agreement.agreement_number} - L{self.ledger_open_no} - {self.record_type}"


class Payment(models.Model):
    METHOD_CASH = "CASH"
    METHOD_TRANSFER = "TRANSFER"
    METHOD_CHEQUE = "CHEQUE"
    METHOD_OTHER = "OTHER"

    METHOD_CHOICES = [
        (METHOD_CASH, "Cash"),
        (METHOD_TRANSFER, "Bank Transfer"),
        (METHOD_CHEQUE, "Cheque"),
        (METHOD_OTHER, "Other"),
    ]

    agreement = models.ForeignKey("Agreement", on_delete=models.CASCADE, related_name="payments")

    payment_date = models.DateField()
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_CASH)

    amount_principal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    reported_principal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    reported_interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    reference_note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PAY-{self.pk} {self.agreement.agreement_number} {self.payment_date}"


class Receipt(models.Model):
    receipt_number = models.CharField(max_length=30, unique=True, blank=True)

    payment = models.OneToOneField("Payment", on_delete=models.CASCADE, related_name="receipt")
    agreement = models.ForeignKey("Agreement", on_delete=models.CASCADE, related_name="receipts")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="receipts")

    receipt_date = models.DateField()

    principal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    method = models.CharField(max_length=20, blank=True)
    reference_note = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last_id = Receipt.objects.count() + 1
            self.receipt_number = f"R{last_id:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_number} ({self.customer.full_name})"


class MessageTemplate(models.Model):
    KEY_PRE_REGISTER = "PRE_REGISTER"
    KEY_LOGIN_TEMP_PASSWORD = "LOGIN_TEMP_PASSWORD"
    KEY_CUSTOMER_REMINDER = "CUSTOMER_REMINDER"
    KEY_PAYMENT_REMINDER = "PAYMENT_REMINDER"
    KEY_CUSTOM = "CUSTOM"
    KEY_USER="USER"

    KEY_CHOICES = [
        (KEY_PRE_REGISTER, "Pre-registration Link"),
        (KEY_LOGIN_TEMP_PASSWORD, "Staff Login + Temporary Password"),
        (KEY_CUSTOMER_REMINDER, "Customer Reminder"),
        (KEY_PAYMENT_REMINDER, "Payment Reminder"),
        (KEY_CUSTOM, "Custom Message"),
        (KEY_USER, "User-created Template"),
    ]

    LANG_EN = "EN"
    LANG_BM = "BM"

    LANG_CHOICES = [
        (LANG_EN, "English"),
        (LANG_BM, "Malay"),
    ]

    key = models.CharField(max_length=50, choices=KEY_CHOICES)
    language = models.CharField(max_length=2, choices=LANG_CHOICES, default=LANG_EN)
    title = models.CharField(max_length=120)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.language})"


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=150)
    message = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    company_code = models.CharField(max_length=10, blank=True , null=True)  # A or B

    def __str__(self):
        return f"{self.title} - {self.user}"

