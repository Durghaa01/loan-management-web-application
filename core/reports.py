from django.db.models import Sum, Count
from core.models import (
    Agreement,
    Payment,
    InternalLedgerEntry,
    OfficialLedgerRecord,
    Receipt,
    ActivityLog,
)

def internal_summary(date_from=None, date_to=None):
    qs = Payment.objects.all()

    if date_from:
        qs = qs.filter(payment_date__gte=date_from)
    if date_to:
        qs = qs.filter(payment_date__lte=date_to)

    return {
        "total_principal": qs.aggregate(Sum("amount_principal"))["amount_principal__sum"] or 0,
        "total_interest": qs.aggregate(Sum("amount_interest"))["amount_interest__sum"] or 0,
        "total_payments": qs.count(),
        "total_agreements": Agreement.objects.filter(status="ACTIVE").count(),
    }


def official_summary(date_from=None, date_to=None):
    qs = OfficialLedgerRecord.objects.all()

    if date_from:
        qs = qs.filter(record_date__gte=date_from)
    if date_to:
        qs = qs.filter(record_date__lte=date_to)

    return {
        "reported_principal": qs.aggregate(Sum("principal_amount_reported"))["principal_amount_reported__sum"] or 0,
        "reported_interest": qs.aggregate(Sum("interest_amount_reported"))["interest_amount_reported__sum"] or 0,
        "ledger_count": qs.count(),
    }


def activity_summary(date_from=None, date_to=None):
    qs = ActivityLog.objects.all().order_by("-created_at")

    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    return qs
