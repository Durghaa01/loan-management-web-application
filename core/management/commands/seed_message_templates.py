from django.core.management.base import BaseCommand
from core.models import MessageTemplate


class Command(BaseCommand):
    help = "Seed default message templates"

    def handle(self, *args, **options):
        templates = [
            ("PRE_REGISTER", "EN", "Pre-registration Link",
             "Hello {CUSTOMER_NAME}, please complete your pre-registration using this link: {LINK}. Thank you."),

            ("PRE_REGISTER", "BM", "Pautan Pra-Pendaftaran",
             "Hello {CUSTOMER_NAME}, sila lengkapkan pra-pendaftaran anda melalui pautan ini: {LINK}. Terima kasih."),

            ("LOGIN_TEMP_PASSWORD", "EN", "Staff Login + Temporary Password",
             "Hello {STAFF_NAME}, your login account has been created. Please login here: {LINK}. Your temporary password is: {PASSWORD}"),

            ("LOGIN_TEMP_PASSWORD", "BM", "Log Masuk Staf + Kata Laluan Sementara",
             "Hello {STAFF_NAME}, akaun log masuk anda telah dibuat. Sila log masuk di sini: {LINK}. Kata laluan sementara anda ialah: {PASSWORD}"),

            ("CUSTOMER_REMINDER", "EN", "Customer Reminder",
             "Hello {CUSTOMER_NAME}, this is a reminder regarding your agreement {AGREEMENT_NO}. Please contact us if you need assistance."),

            ("CUSTOMER_REMINDER", "BM", "Peringatan Pelanggan",
             "Hello {CUSTOMER_NAME}, ini adalah peringatan berkenaan perjanjian anda {AGREEMENT_NO}. Sila hubungi kami jika perlukan bantuan."),

            ("PAYMENT_REMINDER", "EN", "Payment Reminder",
             "Hello {CUSTOMER_NAME}, your payment of RM {AMOUNT} for agreement {AGREEMENT_NO} is due on {DUE_DATE}. Thank you."),

            ("PAYMENT_REMINDER", "BM", "Peringatan Bayaran",
             "Hello {CUSTOMER_NAME}, bayaran anda sebanyak RM {AMOUNT} untuk perjanjian {AGREEMENT_NO} perlu dibayar pada {DUE_DATE}. Terima kasih."),

            ("CUSTOM", "EN", "Custom Message", "{CUSTOM_MESSAGE}"),
            ("CUSTOM", "BM", "Mesej Tersuai", "{CUSTOM_MESSAGE}"),
        ]

        for key, language, title, body in templates:
            MessageTemplate.objects.update_or_create(
                key=key,
                language=language,
                defaults={
                    "title": title,
                    "body": body,
                    "is_active": True,
                }
            )

        self.stdout.write(self.style.SUCCESS("Message templates seeded successfully."))