from decimal import Decimal
from io import BytesIO
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.models import User
from urllib import request
from django.views.decorators.cache import never_cache
from .models import Notification
from core.models import User
from django.contrib import messages
from collections import Counter
from datetime import datetime
from django.utils.timesince import timesince
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from core.utils import log_activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import ActivityLog, Notification
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import CustomerDocument
from django.http import JsonResponse
from django.http import FileResponse
import json
from docx import Document
from django.contrib import messages
from io import BytesIO
from django.db.models import Q
from core.models import (
    Agreement,
    Application,
    Customer,
    CustomerDocument,
    InternalLedgerEntry,
    MessageTemplate,
    OfficialLedgerRecord,
    Payment,
    Receipt,
)
from core.reports import activity_summary, internal_summary, official_summary
from core.utils import log_activity, require_steps_1_4, require_steps_5_7

def require_steps_8_10(user):
    # Example logic: restrict to ADMIN and MASTER_ADMIN, adjust as needed
    return getattr(user, "role", None) in ["ADMIN", "MASTER_ADMIN"]
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.shortcuts import redirect

@login_required
def customer_document_file_download(request, document_id):

    document = get_object_or_404(
        CustomerDocument,
        id=document_id
    )

    customer = document.customer

    Notification.objects.create(
        user=request.user,
        title="Document Downloaded",
        message=f"{document.doc_type} downloaded for {customer.full_name}.",
        url=f"/customers/{customer.pk}/"
    )

    log_activity(
        request.user,
        f"Document downloaded: {document.doc_type}",
        customer_id=customer.pk
    )

    messages.success(
            request,
            "Document downloaded successfully"
        )

    return FileResponse(
        document.file.open("rb"),
        as_attachment=True,
        filename=document.file.name.split("/")[-1]
    )
@login_required
def customer_document_delete(request, document_id):

    document = get_object_or_404(
        CustomerDocument,
        id=document_id
    )

    customer = document.customer
    document_type = document.doc_type

    if request.method == "POST":

        if document.file:
            document.file.delete()

        document.delete()

        Notification.objects.create(
            user=request.user,
            title="Document Deleted",
            message=f"{document_type} deleted for {customer.full_name}.",
            url=f"/customers/{customer.pk}/"
        )

        log_activity(
            request.user,
            f"Document deleted: {document_type}",
            customer_id=customer.pk
        )

        messages.success(
            request,
            "Document deleted successfully"
        )

    return redirect(
        "customer_documents_download",
        customer_id=customer.pk
    )

def create_notification(user, title, message, url="", company_code=None):
    if user is None:
        return

    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        url=url,
        company_code=company_code
    )
# ---------------------------
# 1) Pre-Registration (Public)
# ---------------------------
@never_cache
def pre_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        ic = request.POST.get("ic_or_passport_no", "").strip()
        phone = request.POST.get("phone_number", "").strip()

        app = Application.objects.create(
            full_name=full_name,
            ic_or_passport_no=ic,
            phone_number=phone,
            marital_status=request.POST.get("marital_status"),
            home_address=request.POST.get("home_address"),
            phone_number_2=request.POST.get("phone_number_2"),
            home_phone_number=request.POST.get("home_phone_number"),
            employer_name=request.POST.get("employer_name"),
            employer_address=request.POST.get("employer_address"),
            office_phone_number=request.POST.get("office_phone_number"),
            total_working_years=request.POST.get("total_working_years"),
            net_salary_after_deductions=request.POST.get("net_salary_after_deductions"),
            salary_bank=request.POST.get("salary_bank"),
            salary_bank_other=request.POST.get("salary_bank_other"),
            amount_wanted_to_borrow=request.POST.get("amount_wanted_to_borrow"),
            loan_reason=request.POST.get("loan_reason"),
            referred_by=request.POST.get("referred_by"),
            has_other_income=request.POST.get("has_other_income"),
            other_income_amount=request.POST.get("other_income_amount") or None,
            other_income_name=request.POST.get("other_income_name"),
            spouse_full_name=request.POST.get("spouse_full_name"),
            spouse_ic_number=request.POST.get("spouse_ic_number"),
            spouse_job=request.POST.get("spouse_job"),
            spouse_income=request.POST.get("spouse_income") or None,
            number_of_children=request.POST.get("number_of_children") or None,
            number_of_working_children=request.POST.get("number_of_working_children") or None,
            borrowing_from_licensed_lender=request.POST.get("borrowing_from_licensed_lender"),
            licensed_lender_balance=request.POST.get("licensed_lender_balance") or None,
            car_loan_commitment=request.POST.get("car_loan_commitment") or None,
            house_loan_commitment=request.POST.get("house_loan_commitment") or None,
            house_rental_commitment=request.POST.get("house_rental_commitment") or None,
            motorcycle_commitment=request.POST.get("motorcycle_commitment") or None,
            other_commitment_name=request.POST.get("other_commitment_name"),
            other_commitment_amount=request.POST.get("other_commitment_amount") or None,
        )

        

        # Log (no user because public form)
        admin_user = User.objects.filter(
            is_superuser=True
        ).first()

        if admin_user:
            log_activity(
        admin_user,
        "Application submitted",
        application_id=app.pk,
        ic_or_passport_no=ic
    )



        
        admin_users = User.objects.filter(
    is_superuser=True
)

        for admin in admin_users:

            Notification.objects.create(
            user=admin,
            title="New Application Submitted",
            message=f"{app.full_name} submitted a new application",
            url=f"/applications/{app.pk}/"
    )

        language = request.POST.get(
        "selected_language",
        "en"
)

        request.session["application_language"] = language

        return redirect("pre_register_success")

    return render(request, "core/pre_register.html")

@login_required
def application_bulk_delete(request):

    if request.method == "POST":

        ids = request.POST.get(
            "application_ids"
        ).split(",")

        applications = Application.objects.filter(
            id__in=ids
        )

        for application in applications:

            create_notification(
                request.user,
                "Application Deleted",
                f"{application.application_number} - {application.full_name} was deleted.",
                url=""
            )
            log_activity(
                request.user,
                f"Application deleted: {application.application_number}",
                application_id=application.pk
            )

        applications.delete()

        messages.success(
            request,
            "Applications deleted successfully"
        )

    return redirect("applications_list")
@login_required
def customer_bulk_delete(request):

    if request.method == "POST":

        ids = request.POST.get(
            "customer_ids"
        ).split(",")

        customers = Customer.objects.filter(
            id__in=ids
        )

        for customer in customers:

            log_activity(
                request.user,
                f"Customer deleted: {customer.customer_reference}",
                customer_id=customer.pk
            )

            Notification.objects.create(
                user=request.user,
                title="Customer Deleted",
                message=f"{customer.customer_reference} - {customer.full_name} was deleted.",
                url=""
            )

        customers.delete()

        messages.success(
            request,
            "Customers deleted successfully"
        )

    return redirect("customers_list")

def pre_register_success(request):

    language = request.session.pop(
        "application_language",
        "en"
    )

    if request.user.is_authenticated:
        back_url = "/applications/"
    else:
        back_url = "back"

    return render(
        request,
        "core/pre_register_success.html",
        {
            "language": language,
            "back_url": back_url
        }
    )

@login_required
def application_delete(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if request.method == "POST":

        create_notification(
            request.user,
            "Application Deleted",
            f"{application.application_number} - {application.full_name} was deleted.",
            url=""
        )
    
        log_activity(
    request.user,
    f"Application deleted: {application.application_number}",
    application_id=application.pk
)
        application.delete()

        messages.success(
            request,
            "Application deleted successfully"
        )

    return redirect("applications_list")
# ---------------------------
# 2) Customer Summary
# ---------------------------
@never_cache
@login_required
def customer_summary(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    # Use explicit query for related documents to avoid attribute access issues
    documents = CustomerDocument.objects.filter(customer=customer)

    document_summary = Counter(
    document.doc_type
    for document in documents
).items()
    
    from_customer_create = request.session.pop(
        "from_customer_create",
        False
    )
    
    from_customer_edit = request.session.pop(
        "from_customer_edit",
        False
    )

    clear_customer_form=request.session.pop(
            "clear_customer_form",
            False
        )
    
    return render(
        request,
        "core/customer_summary.html",
        {
            "customer": customer,
            "documents": documents,
            "document_summary": document_summary,
            "from_customer_create": from_customer_create,
            "from_customer_edit": from_customer_edit,
             "clear_customer_form":clear_customer_form,

        }
    )

@login_required
def customer_documents_download(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    documents = CustomerDocument.objects.filter(
        customer=customer
    ).order_by("doc_type", "-id")

    grouped_documents = {}

    for document in documents:
        if document.doc_type not in grouped_documents:
            grouped_documents[document.doc_type] = []

        grouped_documents[document.doc_type].append(document)

    document_order = [
        "IC",
        "Passport",
        "Salary Slip",
        "Bank Statement",
        "Utility Bill",
        "Other",
    ]

    sorted_grouped_documents = {}

    for doc_type in document_order:
        if doc_type in grouped_documents:
            sorted_grouped_documents[doc_type] = (
                grouped_documents[doc_type]
            )

    for doc_type, docs in grouped_documents.items():
        if doc_type not in sorted_grouped_documents:
            sorted_grouped_documents[doc_type] = docs

    return render(
        request,
        "core/customer_documents_download.html",
        {
            "customer": customer,
            "grouped_documents": sorted_grouped_documents,
        }
    )


@login_required
def customer_profile_pdf(request, customer_id):

    

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    selected_sections = request.session.get(
        "download_sections",
        []
    )

    

    language = request.session.get("profile_pdf_language","en")

    def t(en, ms):
        if language == "ms":
            return ms
        return en

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Customer_{customer.customer_reference}.pdf"'
    )

    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    def check_page_space():

        nonlocal y

        if y < 140:
            draw_footer()
            p.showPage()


            y = 760

    # Logo centered
    try:
        logo = ImageReader("core/static/core/logo.png")

        p.drawImage(
            logo,
            260,
            755,
            width=70,
            height=55,
            preserveAspectRatio=True,
            mask="auto"
        )

    except:
        pass

    def draw_footer():

        p.setFont("Times-Roman", 9)

        p.drawRightString(
            550,
            25,
            f"{t('Generated At', 'Dijana Pada')}: {timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')}"
)  
    # System name centered
    p.setFont("Times-Bold", 18)
    p.drawCentredString(
        300,
        735,
        "SYSTEM NAME"
    )

    p.setFont("Times-Bold", 14)
    p.drawCentredString(
        300,
        710,
        t("CUSTOMER PROFILE REPORT", "LAPORAN PROFIL PELANGGAN")
    )



    if customer.display_photo:

        try:

            photo = ImageReader(
            customer.display_photo.path
        )
            p.rect(
    415,   # x
    545,   # y
    130,   # width
    110    # height
) 
            photo_x = 420
            photo_y = 550

            p.drawImage(
            photo,
            photo_x,
            photo_y,
            width=120,
            height=100,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto"
        )

        except Exception:

            pass
    # Personal Information
    p.setFont("Times-Bold", 13)
    p.drawString(50,670,t("Personal Information", "Maklumat Peribadi"))
    p.line(50,662,550,662)

    p.setFont("Times-Roman", 11)

    p.drawString(
        50,
        645,
        f"{t('Customer Number', 'Nombor Pelanggan')}: {customer.customer_reference}"
    )

    p.drawString(
        50,
        627,
        f"{t('Generated At', 'Dijana Pada')}: {timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')}"
    )

    p.drawString(
        50,
        609,
        f"{t('Full Name', 'Nama Penuh')}: {customer.full_name}"
    )

    p.drawString(
        50,
        591,
        f"{t('IC/Passport', 'KP/Pasport')}: {customer.ic_number}"
    )

    p.drawString(
        50,
        573,
        f"{t('Phone Number', 'Nombor Telefon')}: {customer.phone}"
    )

    p.drawString(
    50,
    555,
    f"{t('Email', 'Emel')}: {customer.email or '-'}"
    )

    p.drawString(
        50,
        537,
        f"{t('Status', 'Status')}: {t('Active', 'Aktif') if customer.is_active else t('Inactive', 'Tidak Aktif')}"
    )

    p.drawString(
        50,
        519,
        f"{t('Gender', 'Jantina')}: {customer.gender or '-'}"
    )

    p.drawString(
        50,
        501,
        f"{t('Date of Birth', 'Tarikh Lahir')}: {customer.date_of_birth or '-'}"
    )

    p.drawString(
        50,
        483,
        f"{t('Age', 'Umur')}: {customer.age or '-'}"
    )

    p.drawString(
        50,
        465,
        f"{t('Marital Status', 'Status Perkahwinan')}: {customer.marital_status or '-'}"
    )

    y = 430
    check_page_space()
    if "home" in selected_sections:
        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Home Information", "Maklumat Rumah"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)
        p.drawString(50, y, f"{t('Home Address 1','Alamat Rumah 1')}: {customer.home_address_1 or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Home Address 2','Alamat Rumah 2')}: {customer.home_address_2 or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Home Address 3','Alamat Rumah 3')}: {customer.home_address_3 or '-'}")
        y -= 18

        p.drawString(50,y,f"{t('Home Phone Number','Nombor Telefon Rumah')}: {customer.home_phone_number or '-'}")
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Phone Number 2','Nombor Telefon 2')}: {customer.phone_number_2 or '-'}")
        y -= 30

    

    if "employment" in selected_sections:

        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(
            50,
            y,
           t("Employment Information", "Maklumat Pekerjaan")
        )

        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(
            50,
            y,
            f"{t('Working Status','Status Pekerjaan')}:{customer.working_status or '-'}"
        )

        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Employer Name','Nama Majikan')}: {customer.employer_name or '-'}"
        )

        y -= 18

        p.drawString(
        50,
        y,
            f"{t('Employer Address','Alamat Majikan')}: {customer.employer_address or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Office Phone Number','Nombor Telefon Pejabat')}: {customer.office_phone_number or '-'}"
        )

        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Total Working Years','Jumlah Tahun Bekerja')}:{customer.total_working_years or '-'}"
        )

        y -= 30  

    

    if "family" in selected_sections:
        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Family Information", "Maklumat Keluarga"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(50, y, f"{t('Spouse Full Name','Nama Penuh Pasangan')}: {customer.spouse_name or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Spouse IC/Passport','KP/Pasport Pasangan')}: {customer.spouse_ic_number or '-'}")
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Spouse Age','Umur Pasangan')}: {customer.spouse_age or '-'}"
        )
        y -= 18

        p.drawString(50, y, f"{t('Spouse Job','Pekerjaan Pasangan')}: {customer.spouse_job or '-'}")
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Spouse Monthly Income','Pendapatan Bulanan Pasangan')}: RM {customer.spouse_monthly_income or 0}"
        )
        y -= 18

        p.drawString(50, y, f"{t('Number of Children','Bilangan Anak')}: {customer.number_of_children or '-'}")
        y -= 18

        p.drawString(
        50,
        y,
        f"{t('Number of Schooling Children','Bilangan Anak Bersekolah')}: {customer.number_of_schooling_children or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Number of Working Children','Bilangan Anak Bekerja')}: {customer.number_of_working_children or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Working Children Total Income','Jumlah Pendapatan Anak Bekerja')}: RM {customer.working_children_total_income or 0}"
        )
        y -= 30

    

    if "financial" in selected_sections:
        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Financial Information", "Maklumat Kewangan"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(
            50,
            y,
            f"{t('Monthly Net Income','Pendapatan Bersih Bulanan')}: RM {customer.monthly_net_income or 0}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Basic Monthly Salary','Gaji Asas Bulanan')}: RM {customer.basic_monthly_salary or 0}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Other Income Name','Nama Pendapatan Lain')}: {customer.other_income_name or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Other Income Total','Jumlah Pendapatan Lain')}: RM {customer.other_income_total or 0}"
        )
        y -= 18

        p.drawString(
        50,
        y,
        f"{t('Car Monthly Loan','Pinjaman Kereta Bulanan')}: RM {customer.car_loan or 0}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('House Monthly Loan','Pinjaman Rumah Bulanan')}: RM {customer.house_loan or 0}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Motorcycle Monthly Loan','Pinjaman Motosikal Bulanan')}: RM {customer.motorcycle_loan or 0}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Other Loan','Pinjaman Lain')}: RM {customer.other_loan or 0}"
        )
        y -= 18

        p.drawString(50, y, f"{t('House Monthly Rental','Sewa Bulanan Rumah')}: RM {customer.house_monthly_rental or 0}")
        y -= 18
        
        p.drawString(
            50,
            y,
            f"{t('Monthly Loan Total','Jumlah Pinjaman Bulanan')}: RM {customer.monthly_loan_total or 0}"
        )
        y -= 30
      

   

    if "housing" in selected_sections:

        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Housing & Vehicle Information", "Maklumat Perumahan & Kenderaan"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(50, y, f"{t('House Type','Jenis Rumah')}: {customer.house_type or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('House Ownership','Pemilikan Rumah')}: {customer.house_ownership or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Vehicle Type','Jenis Kenderaan')}: {customer.vehicle_type or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Vehicle Name','Nama Kenderaan')}: {customer.vehicle_name or '-'}")
        y -= 18

        p.drawString(50, y, f"{t('Vehicle Registration Number','Nombor Pendaftaran Kenderaan')}: {customer.vehicle_registration_number or '-'}")
        y -= 18

        p.drawString(
        50,
        y,
        f"{t('Vehicle Color','Warna Kenderaan')}: {customer.vehicle_color or '-'}"
        )
        y -= 30

    

    if "payment" in selected_sections:
        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Payment Information", "Maklumat Pembayaran"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(
            50,
            y,
            f"{t('Payment Bank Name','Nama Bank Pembayaran')}: {customer.payment_bank_name or '-'}"
        )
        y -= 18

        if customer.payment_bank_name == "Other":

            p.drawString(
            50,
            y,
            f"{t('Other Payment Bank Name', 'Nama Bank Pembayaran Lain')}: {customer.payment_other_bank_name or '-'}"
        )

            y -= 18

        p.drawString(
            50,
            y,
            f"{t('Balance Transfer Bank','Bank Pemindahan Baki')}: {customer.balance_transfer_bank_name or '-'}"
        )
        y -= 18

        if customer.balance_transfer_bank_name == "Other":

            p.drawString(
                50,
                y,
                f"{t('Other Balance Transfer Bank Name', 'Nama Bank Pemindahan Baki Lain')}: {customer.balance_transfer_other_bank_name or '-'}"
            )

            y -= 18

        p.drawString(
            50,
            y,
            f"{t('Balance Transfer Account Number','Nombor Akaun Pemindahan Baki')}: {customer.balance_transfer_account_number or '-'}"
        )
        y -= 18

        p.drawString(
        50,
        y,
        f"{t('Balance Transfer Account Owner','Pemilik Akaun Pemindahan Baki')}: {customer.balance_transfer_account_owner or '-'}"
        )
        y -= 30

    

    if "other" in selected_sections:
        check_page_space()

        p.setFont("Times-Bold", 13)
        p.drawString(50, y, t("Other Information", "Maklumat Lain"))
        y -= 8
        p.line(50, y, 550, y)
        y -= 18

        p.setFont("Times-Roman", 11)

        p.drawString(
            50,
            y,
            f"{t('Introduced By','Diperkenalkan Oleh')}: {customer.introduced_by or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Introducer IC/Passport','KP/Pasport Pengenal')}: {customer.introducer_ic_number or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Note','Nota')}: {customer.note or '-'}"
        )
        y -= 18

        p.drawString(
            50,
            y,
            f"{t('Internal Note','Nota Dalaman')}: {customer.internal_note or '-'}"
        )
        y -= 30

    check_page_space()
    draw_footer()
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    Notification.objects.create(
    user=request.user,
    title="Customer Profile Downloaded",
    message=f"{customer.full_name} ({customer.customer_reference}) profile downloaded.",
    url=f"/customers/{customer.pk}/"
)

    log_activity(
        request.user,
        f"Customer profile downloaded: {customer.customer_reference}",
        customer_id=customer.pk
    )

    response.write(pdf)
    return response
# ---------------------------
# 3) Applications
# ---------------------------
@login_required
def applications_list(request):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    apps = Application.objects.order_by("-created_at")
    return render(request, "core/applications_list.html", {"apps": apps})

@never_cache
@login_required
def application_detail(request, app_id):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    app = get_object_or_404(Application, id=app_id)

    is_admin = request.user.role in [
        "ADMIN",
        "MASTER_ADMIN"
    ]

    if request.method == "POST":

        support_status = request.POST.get(
            "support_status",
            ""
        ).strip()

        if support_status:

            support_reason = request.POST.get(
                "support_reason",
                ""
            ).strip()

            if support_status == "SUPPORT" and not support_reason:
                messages.error(
                    request,
                    "Support reason is required"
                )

                return redirect(
                    "application_detail",
                    app_id=app.pk
                )
            app.support_status = support_status

            if support_status == "SUPPORT":
                app.support_reason = support_reason
            else:
                app.support_reason = ""

            app.save()

            log_activity(
                request.user,
                f"Application review updated: {support_status}",
                application_id=app.pk
            )

            Notification.objects.create(
                user=request.user,
                title="Application Review Updated",
                message=f"{app.full_name} marked as {support_status}.",
                url=f"/applications/{app.pk}/"
            )
            messages.success(
    request,
    "Review saved successfully"
)
            return redirect(
                "application_detail",
                app_id=app.pk
            )

        if not is_admin:
            return HttpResponseForbidden(
                "Only admin can approve/reject"
            )
        action = request.POST.get("action")

        reason = request.POST.get(
            "rejection_reason",
            ""
        ).strip()

        STATUS_APPROVED = getattr(
            Application,
            "STATUS_APPROVED",
            "APPROVED"
        )

        STATUS_REJECTED = getattr(
            Application,
            "STATUS_REJECTED",
            "REJECTED"
        )

        if action == "approve":

            app.status = STATUS_APPROVED
            app.rejection_reason = ""

            app.save()

            log_activity(
                request.user,
                "Application approved",
                application_id=app.pk
            )

            Notification.objects.create(
                user=request.user,
                title="Application Approved",
                message=f"{app.full_name} application approved",
                url=f"/applications/{app.pk}/"
            )
            messages.success(
    request,
    "Application approved successfully"
)
        elif action == "reject":

            app.status = STATUS_REJECTED

            app.rejection_reason = reason

            app.save()

            log_activity(
                request.user,
                "Application rejected",
                application_id=app.pk,
                reason=app.rejection_reason
            )

            Notification.objects.create(
                user=request.user,
                title="Application Rejected",
                message=f"{app.full_name} application rejected",
                url=f"/applications/{app.pk}/"
            )
            messages.success(
    request,
    "Application rejected successfully"
)

        return redirect(
            "application_detail",
            app_id=app.pk
        )

    return render(
        request,
        "core/application_detail.html",
        {
            "app": app,
            "is_admin": is_admin
        }
    )

@never_cache
@login_required
def convert_to_customer(request, app_id):

    app = get_object_or_404(
        Application,
        id=app_id
    )

    existing_customer = Customer.objects.filter(
        ic_number=app.ic_or_passport_no
    ).first()

    if existing_customer:

        messages.warning(
    request,
    f"Customer already exists: {existing_customer.customer_reference}"
)

        return redirect(
            "customer_summary",
            customer_id=existing_customer.pk
        )

    # Use .pk to be compatible with models that may not expose `id` attribute
    request.session["convert_application_id"] = app.pk
    request.session["customer_prefill"] = {

    "full_name": app.full_name,

    "ic_number": app.ic_or_passport_no,

    "phone": app.phone_number,

    "phone_number_2": app.phone_number_2,

    "home_phone_number": app.home_phone_number,

    "marital_status": app.marital_status or "" ,

    "home_address_1": app.home_address,

    "employer_name": app.employer_name,

    "employer_address": app.employer_address,

    "office_phone_number": app.office_phone_number,

    "total_working_years": app.total_working_years,

    "monthly_net_income": str(
        app.net_salary_after_deductions or ""
    ),

    "other_income_name": app.other_income_name,

    "other_income_total": str(
        app.other_income_amount or ""
    ),

    "spouse_name": app.spouse_full_name,

    "spouse_ic_number": app.spouse_ic_number,

    "spouse_job": app.spouse_job,

    "spouse_monthly_income": str(
        app.spouse_income or ""
    ),

    "number_of_children": app.number_of_children,

    "number_of_working_children": app.number_of_working_children,

    "car_loan": str(
        app.car_loan_commitment or ""
    ),

    "house_loan": str(
        app.house_loan_commitment or ""
    ),
    
    "house_monthly_rental": str(app.house_rental_commitment or ""),

    "motorcycle_loan": str(
        app.motorcycle_commitment or ""
    ),

    "other_income_name": app.other_income_name,

    "introduced_by": app.referred_by,

    "note": app.loan_reason,
}
    
    messages.success(
    request,
    "Application converted to customer form successfully."
)

    create_notification(
        request.user,
        "Application Converted",
        f"{app.full_name} application converted to customer form",
        url=f"/applications/{app.pk}/",
        company_code=None
    )

    log_activity(
    request.user,
    f"Application converted to customer form: {app.application_number}",
    application_id=app.pk
)
    return redirect(
        "customer_create"
    )
@never_cache
@login_required
def agreement_create(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    existing_agreement = Agreement.objects.filter(
    customer=customer
).first()

    if existing_agreement:

        messages.error(
        request,
        "Agreement already exists for this customer"
    )

        return redirect(
        "customer_summary",
        customer_id=customer.pk
    )

    today = timezone.localdate()

    if request.method == "POST":

        agreement = Agreement.objects.create(
            customer=customer,
            agreement_date=request.POST.get("agreement_date"),
            principal_amount_words=request.POST.get(
                "principal_amount_words",
                ""
            ),
            principal_amount=request.POST.get(
                "principal_amount"
            ) or None,
            interest_rate_words=request.POST.get(
                "interest_rate_words",
                ""
            ),
            interest_rate_percentage=request.POST.get(
                "interest_rate_percentage"
            ) or None,
            monthly_repayment_amount=request.POST.get(
                "monthly_repayment_amount"
            ) or None,
            total_repayment_amount=request.POST.get(
                "total_repayment_amount"
            ) or None,

            book=request.POST.get("book", ""),
        )

        request.session["agreement_language"] = request.POST.get(
            "selected_language",
            "en"
        )

        messages.success(
            request,
            "Agreement created successfully"
        )

        Notification.objects.create(
    user=request.user,
    title="Agreement Created",
    message=f"{agreement.agreement_number} created for {customer.full_name}.",
    url=f"/agreements/{agreement.pk}/"
)

        log_activity(
            request.user,
            f"Agreement created: {agreement.agreement_number}",
            customer_id=customer.pk
        )

        request.session["from_agreement_create"] = True
        return redirect(
            "agreement_detail",
            agreement_id=agreement.pk
        )

    return render(
        request,
        "core/agreement_create.html",
        {
            "customer": customer,
            "today": today,
        }
    )


@login_required
def agreement_detail(request, agreement_id):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    agreement = get_object_or_404(Agreement, id=agreement_id)
    from_agreement_create = request.session.pop(
        "from_agreement_create",
        False
    )
    return render(
        request,
        "core/agreement_detail.html",
        {
            "agreement": agreement,
            "from_agreement_create": from_agreement_create,
        }
    )

@login_required
def bulk_delete_agreements(request):

    if request.method == "POST":

        ids = request.POST.get("agreement_ids", "")

        if ids:

            agreements = Agreement.objects.filter(
    id__in=ids.split(",")
)

            for agreement in agreements:

                Notification.objects.create(
        user=request.user,
        title="Agreement Deleted",
        message=f"{agreement.agreement_number} deleted.",
        url="/agreements/"
    )

                log_activity(
        request.user,
        f"Agreement deleted: {agreement.agreement_number}",
        customer_id=agreement.customer.pk
    )

            agreements.delete()

        messages.success(
            request,
            "Agreement(s) deleted successfully"
        )

        

    return redirect("agreement_list")

@login_required
def agreement_list(request):

    query = request.GET.get("q", "")

    agreements = Agreement.objects.select_related(
        "customer"
    ).order_by("-created_at")

    if query:
        agreements = agreements.filter(
            Q(agreement_number__icontains=query) |
            Q(customer__full_name__icontains=query) |
            Q(customer__ic_number__icontains=query)
        )

    return render(
        request,
        "core/agreement_list.html",
        {
            "agreements": agreements,
            "query": query,
        }
    )

@never_cache
@login_required
def agreement_edit(request, agreement_id):

    agreement = get_object_or_404(
        Agreement,
        id=agreement_id
    )

    customer = agreement.customer

    if request.method == "POST":

        agreement.principal_amount_words = request.POST.get(
            "principal_amount_words",
            ""
        )

        agreement.principal_amount = request.POST.get(
            "principal_amount"
        ) or None

        agreement.interest_rate_words = request.POST.get(
            "interest_rate_words",
            ""
        )

        agreement.interest_rate_percentage = request.POST.get(
            "interest_rate_percentage"
        ) or None

        agreement.monthly_repayment_amount = request.POST.get(
            "monthly_repayment_amount"
        ) or None

        agreement.total_repayment_amount = request.POST.get(
            "total_repayment_amount"
        ) or None

        agreement.book = request.POST.get("book", "")
       

        agreement.save()

        messages.success(
            request,
            "Agreement updated successfully"
        )

        Notification.objects.create(
    user=request.user,
    title="Agreement Updated",
    message=f"{agreement.agreement_number} updated.",
    url=f"/agreements/{agreement.pk}/"
)

        log_activity(
            request.user,
            f"Agreement updated: {agreement.agreement_number}",
            customer_id=agreement.customer.pk
        )

        return redirect(
            "agreement_detail",
            agreement_id=agreement.pk
        )

    return render(
        request,
        "core/agreement_edit.html",
        {
            "agreement": agreement,
            "customer": customer,
        }
    )

@login_required
def agreement_pdf(request, agreement_id):

    agreement = get_object_or_404(
        Agreement,
        id=agreement_id
    )

    lang = request.GET.get("lang", "en")

    template = get_template(
        "core/agreement_pdf.html"
    )

    html = template.render({
        "agreement": agreement,
        "lang": lang,
    })

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{agreement.agreement_number}.pdf"'
    )

    pisa.CreatePDF(
        html,
        dest=response
    )

    Notification.objects.create(
    user=request.user,
    title="Agreement Downloaded",
    message=f"{agreement.agreement_number} downloaded.",
    url=f"/agreements/{agreement.pk}/"
)

    log_activity(
    request.user,
    f"Agreement downloaded: {agreement.agreement_number}",
    customer_id=agreement.customer.pk
)

    return response
# ---------------------------
# 5) Payment
# ---------------------------
@login_required
def payment_create(request, agreement_id):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    agreement = get_object_or_404(Agreement, id=agreement_id)

    def dec(v):
        v = (v or "").strip()
        return Decimal(v) if v else Decimal("0.00")

    if request.method == "POST":
        payment_date = request.POST.get("payment_date")
        method = request.POST.get("method")
        ref = request.POST.get("reference_note", "").strip()

        amount_principal = dec(request.POST.get("amount_principal"))
        amount_interest = dec(request.POST.get("amount_interest"))

        reported_principal = dec(request.POST.get("reported_principal"))
        reported_interest = dec(request.POST.get("reported_interest"))

        payment = Payment.objects.create(
            agreement=agreement,
            payment_date=payment_date,
            method=method,
            amount_principal=amount_principal,
            amount_interest=amount_interest,
            reported_principal=reported_principal,
            reported_interest=reported_interest,
            reference_note=ref,
            created_by=request.user,
        )

        InternalLedgerEntry.objects.create(
            agreement=agreement,
            entry_date=payment_date,
            entry_type=InternalLedgerEntry.TYPE_PAYMENT,
            principal_amount=amount_principal,
            interest_amount=amount_interest,
            note=f"Payment: {method} {ref}".strip(),
            created_by=request.user,
        )

        OfficialLedgerRecord.objects.create(
            agreement=agreement,
            record_date=payment_date,
            record_type=OfficialLedgerRecord.TYPE_PAYMENT,
            principal_amount_reported=reported_principal,
            interest_amount_reported=reported_interest,
            note=f"Payment (official): {method} {ref}".strip(),
            created_by=request.user,
        )

        log_activity(
            request.user,
            "Payment recorded",
            payment_id=payment.pk,
            agreement_id=agreement.pk,
            customer_id=agreement.customer.pk,
        )

        create_notification(
    request.user,
    "Payment Recorded",
    f"Payment recorded for {agreement.customer.full_name}.",
    f"/payments/{payment.pk}/",
    company_code=None
)
        return redirect("payment_detail", payment_id=payment.pk)

    return render(request, "core/payment_create.html", {"agreement": agreement})


@login_required
def payment_detail(request, payment_id):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "core/payment_detail.html", {"payment": payment})


# ---------------------------
# 6) Receipt
# ---------------------------
@login_required
def receipt_generate(request, payment_id):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    payment = get_object_or_404(Payment, id=payment_id)

    existing_receipt = Receipt.objects.filter(payment=payment).first()
    if existing_receipt:
        return redirect("receipt_detail", receipt_id=existing_receipt.pk)

    principal = payment.amount_principal
    interest = payment.amount_interest
    total = principal + interest

    receipt = Receipt.objects.create(
        payment=payment,
        agreement=payment.agreement,
        customer=payment.agreement.customer,
        receipt_date=payment.payment_date,
        principal_amount=principal,
        interest_amount=interest,
        total_amount=total,
        method=payment.method,
        reference_note=payment.reference_note,
        created_by=request.user,
    )

    log_activity(
        request.user,
        "Receipt generated",
        receipt_id=receipt.pk,
        payment_id=payment.pk,
        agreement_id=payment.agreement.pk,
        customer_id=receipt.customer.pk,
    )

    create_notification(
    request.user,
    "Receipt Generated",
    f"Receipt {receipt.receipt_number} was generated.",
    f"/receipts/{receipt.pk}/",
    company_code=receipt.agreement.company_code
)
    return redirect("receipt_detail", receipt_id=receipt.pk)


@login_required
def receipt_detail(request, receipt_id):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    receipt = get_object_or_404(Receipt, id=receipt_id)
    return render(request, "core/receipt_detail.html", {"receipt": receipt})


# ---------------------------
# 7) Reports
# ---------------------------
@login_required
def reports_dashboard(request):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    date_from = request.GET.get("from")
    date_to = request.GET.get("to")

    internal = internal_summary(date_from, date_to)
    official = official_summary(date_from, date_to)
    activities = activity_summary(date_from, date_to)[:50]

    return render(
        request,
        "core/reports_dashboard.html",
        {
            "internal": internal,
            "official": official,
            "activities": activities,
            "date_from": date_from,
            "date_to": date_to,
        },
    )


# ---------------------------
# 8) Message Center
# ---------------------------
@login_required
def message_center(request):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    templates = MessageTemplate.objects.filter(
        is_active=True,
        key__in=[
            MessageTemplate.KEY_PRE_REGISTER,
            MessageTemplate.KEY_CUSTOM,
            MessageTemplate.KEY_USER,
        ],
    ).order_by("key", "language", "title")

    customers = Customer.objects.all().order_by("full_name")

    customers_data = [
        {
            "id": customer.pk,
            "name": customer.full_name,
            "ic": customer.ic_number,
            "phone": customer.phone,
        }
        for customer in customers
    ]

    selected_id = request.GET.get("template", "").strip()
    selected = None

    if selected_id:
        selected = get_object_or_404(
            MessageTemplate,
            id=selected_id,
            is_active=True,
        )

    generated = request.GET.get("generate") == "1"

    customer_id = request.GET.get("customer_id", "").strip()
    customer_name = request.GET.get("customer_name", "").strip()
    phone = request.GET.get("phone", "").strip()
    custom_message = request.GET.get("custom_message", "").strip()
    amount = request.GET.get("amount", "").strip()
    due_date = request.GET.get("due_date", "").strip()

    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
        customer_name = customer.full_name
        phone = customer.phone

    pre_register_link = request.build_absolute_uri(
        reverse("pre_register")
    )

    current_date = timezone.localdate().strftime("%d/%m/%Y")
    rendered_message = ""
    whatsapp_link = ""

    if selected and generated:
        errors = []

        if not customer_name:
            errors.append("Name is required")

        if not phone:
            errors.append("Phone number is required")

        if selected.key == MessageTemplate.KEY_CUSTOM and not custom_message:
            errors.append("Custom message is required")

        if "{CUSTOM_MESSAGE}" in selected.body and not custom_message:
            errors.append("Custom message is required")

        if "{AMOUNT}" in selected.body and not amount:
            errors.append("Amount is required")

        if "{DUE_DATE}" in selected.body and not due_date:
            errors.append("Due date is required")

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            rendered_message = selected.body

            replacements = {
                "{DATE}": current_date,
                "{CUSTOMER_NAME}": customer_name,
                "{PHONE}": phone,
                "{LINK}": pre_register_link,
                "{CUSTOM_MESSAGE}": custom_message,
                "{AMOUNT}": amount,
                "{DUE_DATE}": due_date,
            }

            for placeholder, value in replacements.items():
                rendered_message = rendered_message.replace(
                    placeholder,
                    value,
                )

            log_activity(
                request.user,
                f"Generated message: {selected.title}",
            )

            messages.success(
                request,
                "Message generated successfully",
            )

            from urllib.parse import urlencode

            whatsapp_link = reverse(
                "open_whatsapp_message"
            ) + "?" + urlencode({
                "phone": phone,
                "message": rendered_message,
            })

    return render(
        request,
        "core/message_center.html",
        {
            "templates": templates,
            "selected": selected,
            "customers_data": customers_data,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "phone": phone,
            "custom_message": custom_message,
            "amount": amount,
            "due_date": due_date,
            "current_date": current_date,
            "rendered_message": rendered_message,
            "whatsapp_link": whatsapp_link,
        },
    )

@login_required
def message_template_create(request):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        language = request.POST.get("language", "").strip()
        body = request.POST.get("body", "").strip()

        if not title or not language or not body:
            messages.error(
                request,
                "Template name, language, and message body are required."
            )
            return render(
                request,
                "core/message_template_create.html",
                {
                    "title": title,
                    "language": language,
                    "body": body,
                },
            )

        if language not in ["EN", "BM"]:
            messages.error(request, "Please select a valid language.")
            return render(
                request,
                "core/message_template_create.html",
                {
                    "title": title,
                    "language": "",
                    "body": body,
                },
            )
        MessageTemplate.objects.create(
    key=MessageTemplate.KEY_USER,
    title=title,
    language=language,
    body=body,
    is_active=True,
)
        messages.success(request, "Message template created successfully")
        return redirect("message_center")

    return render(request, "core/message_template_create.html")
@login_required
def bulk_delete_message_templates(request):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    if request.method == "POST":
        template_ids = request.POST.get("template_ids", "").strip()

        if template_ids:
            templates = MessageTemplate.objects.filter(
                id__in=template_ids.split(","),
                key=MessageTemplate.KEY_USER,
            )

            deleted_count = templates.count()
            templates.delete()

            if deleted_count:
                messages.success(
                    request,
                    "Message template(s) deleted successfully"
                )
            else:
                messages.error(
                    request,
                    "No deletable templates were selected"
                )

    return redirect("message_center")

@login_required
def open_whatsapp_message(request):
    phone = request.GET.get("phone", "").strip()
    message = request.GET.get("message", "").strip()

    if not phone or not message:
        messages.error(
            request,
            "Phone number and generated message are required"
        )
        return redirect("message_center")

    clean_phone = "".join(
        character for character in phone
        if character.isdigit()
    )

    # Convert Malaysian local format:
    # 0123456789 -> 60123456789
    if clean_phone.startswith("0"):
        clean_phone = "60" + clean_phone[1:]

    from urllib.parse import quote

    whatsapp_url = (
        f"https://wa.me/{clean_phone}"
        f"?text={quote(message, safe='')}"
    )

    return redirect(whatsapp_url)

# ---------------------------
# 9) Dashboard
# ---------------------------
@login_required
def dashboard(request):
    today = timezone.localdate()
    active_company = request.session.get("active_company", "ALL")

    pending_applications_count = Application.objects.filter(
        status="PENDING"
    ).count()

    total_customers_count = Customer.objects.count()

    agreements = Agreement.objects.all()

    if active_company != "ALL":
        agreements = agreements.filter(company_code=active_company)

    agreements_today_count = agreements.filter(
        created_at__date=today
    ).count()

    recent_activities = ActivityLog.objects.order_by("-created_at")[:3]

    notifications = Notification.objects.filter(
    user=request.user
    )
    if active_company != "ALL":
        notifications = notifications.filter(company_code=active_company
    )
    notifications = notifications.order_by("-created_at")[:5]

    unread_notifications_count = Notification.objects.filter(
    user=request.user,
    is_read=False
)   .count()
    

    return render(request, "core/dashboard.html", {
        "pending_applications_count": pending_applications_count,
        "total_customers_count": total_customers_count,
        "agreements_today_count": agreements_today_count,
        "active_company": active_company,
        "recent_activities": recent_activities,
        "notifications": notifications,
        "unread_notifications_count": unread_notifications_count,

        "can_pre_registration": True,
        "can_application_review": True,
        "can_customer_registration": True,
        "can_agreement": True,
        "can_payment": True,
        "can_receipt": True,
        "can_reports": True,
    })

# ---------------------------
# 10) Login / Logout (attempts + Axes lockout)
# ---------------------------
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.messages import get_messages
from datetime import timedelta, datetime

# -------------------------
# Log lock events only (NOT normal login/logout)
# -------------------------
def log_lock_event(request, reason="too_many_attempts"):
    try:
        ip = request.META.get("REMOTE_ADDR")
        username = request.POST.get("username", "").strip()

        log_activity(
            None,
            "Login locked",
            username=username,
            ip_address=ip,
            reason=reason,
        )
    except Exception:
        pass

LOCK_MINUTES = 5

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    # -------------------------
    # A) Check if locked (session-based)
    # -------------------------
    locked_until_str = request.session.get("locked_until")
    is_locked = False
    remaining_seconds = 0

    if locked_until_str:
        try:
            locked_until = datetime.fromisoformat(locked_until_str)
            if locked_until.tzinfo is None:
                locked_until = timezone.make_aware(locked_until)

            if timezone.now() < locked_until:
                is_locked = True
                remaining_seconds = int((locked_until - timezone.now()).total_seconds())
            else:
                request.session.pop("locked_until", None)
        except Exception:
            request.session.pop("locked_until", None)

    # -------------------------
    # B) GET: refresh should clear old UI alerts
    # -------------------------
    if request.method == "GET":
        list(get_messages(request))  # clear Django messages

        # ✅ one-time UI flash (clears on refresh automatically)
        ui = request.session.pop("login_ui", None) or {}

        # If locked, we want lock UI to show even on refresh
        lock_message = "Too many attempts. Try again in 5 minutes." if is_locked else None

        response = render(request, "core/login.html", {
            "show_invalid": ui.get("show_invalid", False),
            "show_forgot": (ui.get("show_forgot", False) or is_locked),  # locked always shows contact admin
            "is_locked": is_locked,
            "lock_message": lock_message,
            "remaining_seconds": remaining_seconds,   # for countdown
        })

        # prevent caching
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response

    # -------------------------
    # C) POST: if locked, redirect back (no render)
    # -------------------------
    if is_locked:
        request.session["login_ui"] = {
            "show_invalid": False,
            "show_forgot": True,
        }
        return redirect("login")

    # -------------------------
    # D) Normal login attempt
    # -------------------------
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")

    user = authenticate(request, username=username, password=password)

    if user:
        request.session["failed_attempts"] = 0
        request.session.pop("locked_until", None)
        request.session.pop("login_ui", None)
        login(request, user)
        return redirect("dashboard")

    # -------------------------
    # E) Wrong credentials -> count + decide messages
    # -------------------------
    failed_attempts = request.session.get("failed_attempts", 0) + 1
    request.session["failed_attempts"] = failed_attempts

    # Rules you wanted:
    # 1-2: invalid only
    # 3: invalid + contact admin
    # 4-5: invalid + contact admin
    show_invalid = True
    show_forgot = failed_attempts >= 3

    # 5th attempt -> lock for 5 minutes
    if failed_attempts >= 5:
        request.session["locked_until"] = (timezone.now() + timedelta(minutes=LOCK_MINUTES)).isoformat()

        log_lock_event(request)
    # ✅ Store UI once then redirect (refresh clears it)
    request.session["login_ui"] = {
        "show_invalid": show_invalid if failed_attempts < 5 else False,  # after lock, we don't want invalid spam
        "show_forgot": True if failed_attempts >= 3 else False,
    }

    return redirect("login")
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def customers_list(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    customers = Customer.objects.order_by(
        "-created_at"
    )

    if query:

        customers = customers.filter(
            Q(full_name__icontains=query) |
            Q(ic_number__icontains=query) |
            Q(phone__icontains=query) 
        )

    return render(
        request,
        "core/customers_list.html",
        {
            "customers": customers,
            "query": query
        }
    )

@never_cache
@login_required
def customer_document_upload(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":

        doc_types = request.POST.getlist("doc_type[]")
        other_doc_types = request.POST.getlist("other_doc_type[]")
        files = request.FILES.getlist("file[]")



        uploaded_count = 0

        for index, file in enumerate(files):

            doc_type = doc_types[index]

            if doc_type == "Other":
                doc_type = other_doc_types[index].strip()

            if file and not doc_type:

                messages.error(
                    request,
                    f"Please select Document Type for Document {index + 1}"
                )

                return redirect(
                    "customer_document_upload",
                    customer_id=customer.pk
                )

            if doc_type and not file:

                messages.error(
                    request,
                    f"Please choose a file for Document {index + 1}"
                )

                return redirect(
                    "customer_document_upload",
                    customer_id=customer.pk
                )

            if not doc_type and not file:
                continue

            document = CustomerDocument.objects.create(
                customer=customer,
                doc_type=doc_type,
                note="",
                file=file,
                
            )

            Notification.objects.create(
                user=request.user,
                title="Document Uploaded",
                message=f"{document.doc_type} uploaded for {customer.full_name}.",
                url=f"/customers/{customer.pk}/"
            )

            log_activity(
                request.user,
                f"Document uploaded: {document.doc_type}",
                customer_id=customer.pk
            )

            uploaded_count += 1

        if uploaded_count == 0:

            messages.error(
                request,
                "Please choose at least one document file"
            )

            return redirect(
                "customer_document_upload",
                customer_id=customer.pk
            )

        messages.success(
            request,
            f"{uploaded_count} document(s) uploaded successfully"
        )

        return redirect(
            "customer_summary",
            customer_id=customer.pk
        )

    return render(request, "core/customer_document_upload.html", {"customer": customer})
@never_cache
@login_required
def customer_create(request):

    if request.method == "POST":

        if (
            not request.POST.get("full_name", "").strip()
            or not request.POST.get("id_type", "").strip()
            or not request.POST.get("ic_number", "").strip()
        ):
            messages.error(request, "Full Name, ID Type and IC Number are required.")
            return redirect("customer_create")
        
        existing_customer = Customer.objects.filter(
    ic_number=request.POST.get("ic_number", "")
).first()

        if existing_customer:

            messages.error(
        request,
        "Customer with this IC number already exists."
    )

            return redirect(
        "customer_create"
    )
    
        application_id = request.session.get(
    "convert_application_id"
)

        application = None

        if application_id:
            application = Application.objects.filter(
                id=application_id
            ).first()
        
        dob = request.POST.get(
    "date_of_birth",
    ""
).strip()

        if dob:
            try:
                dob = datetime.strptime(
                    dob,
                    "%d/%m/%Y"
                ).date()
            except ValueError:
                dob = None
        else:
                dob=None

        customer = Customer.objects.create(

    full_name=request.POST.get(
        "full_name",
        ""
    ),

    ic_number=request.POST.get(
        "ic_number",
        ""
    ),

    phone=request.POST.get(
        "phone",
        ""
    ),

    email=request.POST.get(
        "email",
        ""
    ),

    gender=request.POST.get(
        "gender",
        ""
    ),

    marital_status=request.POST.get(
        "marital_status",
        ""
    ),

    date_of_birth=dob,

    age=request.POST.get(
        "age"
    ) or None,

    home_address_1=request.POST.get(
        "home_address_1",
        ""
    ),

    home_address_2=request.POST.get(
        "home_address_2",
        ""
    ),

    home_address_3=request.POST.get(
        "home_address_3",
        ""
    ),

    home_phone_number=request.POST.get(
        "home_phone_number",
        ""
    ),

    phone_number_2=request.POST.get(
        "phone_number_2",
        ""
    ),

    working_status=request.POST.get(
        "working_status",
        ""
    ),

    employer_name=request.POST.get(
        "employer_name",
        ""
    ),

    employer_address=request.POST.get(
        "employer_address",
        ""
    ),

    office_phone_number=request.POST.get(
        "office_phone_number",
        ""
    ),

    total_working_years=request.POST.get(
        "total_working_years",
        ""
    ),

    spouse_name=request.POST.get(
        "spouse_name",
        ""
    ),

    spouse_ic_number=request.POST.get(
        "spouse_ic_number",
        ""
    ),

    

    spouse_job=request.POST.get(
        "spouse_job",
        ""
    ),

    spouse_age=request.POST.get(
        "spouse_age"
    ) or None,

    spouse_monthly_income=request.POST.get(
        "spouse_monthly_income"
    ) or None,

    number_of_children=request.POST.get(
        "number_of_children"
    ) or None,

    number_of_schooling_children=request.POST.get(
        "number_of_schooling_children"
    ) or None,

    number_of_working_children=request.POST.get(
        "number_of_working_children"
    ) or None,

    working_children_total_income=request.POST.get(
        "working_children_total_income"
    ) or None,

    monthly_net_income=request.POST.get(
        "monthly_net_income"
    ) or None,

    basic_monthly_salary=request.POST.get(
        "basic_monthly_salary"
    ) or None,

    other_income_name=request.POST.get(
        "other_income_name",
        ""
    ),

    other_income_total=request.POST.get(
        "other_income_total"
    ) or None,

    car_loan=request.POST.get(
        "car_loan"
    ) or None,

    house_loan=request.POST.get(
        "house_loan"
    ) or None,

    motorcycle_loan=request.POST.get(
        "motorcycle_loan"
    ) or None,

    other_loan=request.POST.get(
        "other_loan"
    ) or None,

    monthly_loan_total=request.POST.get(
        "monthly_loan_total"
    ) or None,

    house_type=request.POST.get(
        "house_type",
        ""
    ),

    house_ownership=request.POST.get(
        "house_ownership",
        ""
    ),

    house_monthly_rental=request.POST.get(
        "house_monthly_rental"
    ) or None,

    house_monthly_bank_payment=request.POST.get(
        "house_monthly_bank_payment"
    ) or None,

    vehicle_type=request.POST.get(
        "vehicle_type",
        ""
    ),

    vehicle_name=request.POST.get(
        "vehicle_name",
        ""
    ),

       id_type=request.POST.get(
        "id_type",
        ""
    ),

    vehicle_registration_number=request.POST.get(
        "vehicle_registration_number",
        ""
    ),

    vehicle_color=request.POST.get(
        "vehicle_color",
        ""
    ),

    vehicle_monthly_bank_payment=request.POST.get(
        "vehicle_monthly_bank_payment"
    ) or None,

    payment_bank_name=request.POST.get(
        "payment_bank_name",
        ""
    ),

    payment_other_bank_name=request.POST.get(
        "payment_other_bank_name",
        ""
    ),

    balance_transfer_bank_name=request.POST.get(
        "balance_transfer_bank_name",
        ""
    ),

    balance_transfer_other_bank_name=request.POST.get(
        "balance_transfer_other_bank_name",
        ""
    ),

    balance_transfer_account_number=request.POST.get(
        "balance_transfer_account_number",
        ""
    ),

    balance_transfer_account_owner=request.POST.get(
        "balance_transfer_account_owner",
        ""
    ),

    introduced_by=request.POST.get(
        "introduced_by",
        ""
    ),

    introducer_ic_number=request.POST.get(
        "introducer_ic_number",
        ""
    ),

    note=request.POST.get(
        "note",
        ""
    ),

    internal_note=request.POST.get(
        "internal_note",
        ""
    ),


    customer_photo=request.FILES.get(
        "customer_photo"
    ),

    mykad_photo=request.FILES.get(
        "mykad_photo"
    ),
    application=application,
)
        
        create_notification(
    request.user,
    "Customer Created",
    f"{customer.full_name} customer profile created",
    url=f"/customers/{customer.pk}/",
    company_code=None
)
        
        log_activity(
    request.user,
    f"Customer created: {customer.customer_reference} - {customer.full_name}",
    customer_id=customer.pk
)
        
     
        if application:

            application.is_converted_to_customer = True
            if hasattr(application, "status"):
                application.status = Application.STATUS_APPROVED
            application.save()


            request.session.pop(
        "convert_application_id",
        None
             )

            request.session.pop(
        "customer_prefill",
        None
            )

        customer.is_active = (
        request.POST.get("is_active")
        == "True"
    )
        customer.save()

        messages.success(
    request,
    "Customer created successfully."
)
        
        request.session["from_customer_create"] = True

        return redirect(
    "customer_summary",
    customer_id=customer.pk
)

    prefill = request.session.get(
    "customer_prefill",
    {
    "full_name": "",
    "ic_number": "",
    "phone": "",
    "home_address_1": "",
    "home_phone_number": "",
    "phone_number_2": "",
    "marital_status": "",
    "employer_name": "",
    "employer_address": "",
    "office_phone_number": "",
    "total_working_years": "",
    "spouse_name": "",
    "spouse_ic_number": "",
    "spouse_job": "",
    "spouse_monthly_income": "",
    "number_of_children": "",
    "number_of_working_children": "",
    "monthly_net_income": "",
    "other_income_name": "",
    "other_income_total": "",
    "car_loan": "",
    "house_loan": "",
    "motorcycle_loan": "",
    "introduced_by": "",
}
)
    request.session.pop(
        "customer_prefill",
        None
    )

    return render(
    request,
    "core/customer_form.html",
    {
        "prefill": prefill
    }
)
@never_cache
@login_required
def customer_edit(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == "POST":

        customer.full_name = request.POST.get(
            "full_name",
            ""
        )

        new_ic_number = request.POST.get(
            "ic_number",
            ""
        ).strip()

        existing_customer = Customer.objects.filter(
            ic_number=new_ic_number
        ).exclude(
            id=customer.pk
        ).first()

        if existing_customer:

            messages.error(
                request,
                "Customer with this IC number already exists."
            )

            return redirect(
                "customer_edit",
                customer_id=customer.pk
            )

        customer.ic_number = new_ic_number

        customer.phone = request.POST.get(
            "phone",
           ""
        ) 

        customer.email = request.POST.get(
            "email",
            ""
        )

        customer.gender = request.POST.get(
            "gender",
            ""
        )

        dob = request.POST.get(
            "date_of_birth",
            ""
        ).strip()

        if dob:
            try:
                customer.date_of_birth = datetime.strptime(
                    dob,
                    "%d/%m/%Y"
                ).date()
            except ValueError:
                customer.date_of_birth = None
        else:
            customer.date_of_birth = None

        customer.age = request.POST.get(
            "age"
        ) or None



        customer.marital_status = request.POST.get(
            "marital_status",
            ""
        )

        customer.home_address_1 = request.POST.get(
            "home_address_1",
            ""
        )

        customer.home_address_2 = request.POST.get(
            "home_address_2",
            ""
        )

        customer.home_address_3 = request.POST.get(
            "home_address_3",
            ""
        )

        customer.home_phone_number = request.POST.get(
            "home_phone_number",
    ""
        ) 

        customer.phone_number_2 = request.POST.get(
            "phone_number_2",
            ""
        ) 

        customer.working_status = request.POST.get(
            "working_status",
            ""
        )

        customer.employer_name = request.POST.get(
            "employer_name",
            ""
        )
        customer.employer_address = request.POST.get(
            "employer_address",
            ""
        )

        customer.office_phone_number = request.POST.get(
            "office_phone_number",
        ""
        ) 

        customer.total_working_years = request.POST.get(
            "total_working_years",
            ""
        ) 

        customer.spouse_name = request.POST.get(
            "spouse_name",
            ""
        )

        customer.spouse_ic_number = request.POST.get(
            "spouse_ic_number",
            ""
        )

        customer.spouse_job = request.POST.get(
            "spouse_job",
            ""
        )

        customer.introduced_by = request.POST.get(
            "introduced_by",
            ""
        )

        customer.introducer_ic_number = request.POST.get(
            "introducer_ic_number",
            ""
        )

        customer.note = request.POST.get(
            "note",
            ""
        )

        customer.internal_note = request.POST.get(
            "internal_note",
            ""
        )

        customer.is_active = (
    request.POST.get("is_active") == "True"
        )

        customer.spouse_monthly_income = request.POST.get(
            "spouse_monthly_income"
        ) or None

        customer.working_children_total_income = request.POST.get(
            "working_children_total_income"
        ) or None

        customer.number_of_children = request.POST.get(
            "number_of_children"
        ) or None

        customer.monthly_net_income = request.POST.get(
            "monthly_net_income"
        ) or None

        customer.basic_monthly_salary = request.POST.get(
            "basic_monthly_salary"
        ) or None

        customer.other_income_name = request.POST.get(
            "other_income_name",
            ""
        )

        customer.other_income_total = request.POST.get(
            "other_income_total"
        ) or None

        customer.car_loan = request.POST.get(
            "car_loan"
        ) or None

        customer.house_loan = request.POST.get(
            "house_loan"
        ) or None

        customer.motorcycle_loan = request.POST.get(
            "motorcycle_loan"
        ) or None

        customer.other_loan = request.POST.get(
            "other_loan"
        ) or None

        customer.house_monthly_rental = request.POST.get(
            "house_monthly_rental"
        ) or None

        customer.monthly_loan_total = request.POST.get(
            "monthly_loan_total"
        ) or None

        customer.vehicle_name = request.POST.get(
            "vehicle_name",
            ""
        )

        customer.payment_bank_name = request.POST.get(
            "payment_bank_name",
            ""
        )

        customer.payment_other_bank_name = request.POST.get(
    "payment_other_bank_name",
    ""
)

        customer.balance_transfer_other_bank_name = request.POST.get(
            "balance_transfer_other_bank_name",
            ""
        )

        customer.balance_transfer_bank_name = request.POST.get(
            "balance_transfer_bank_name",
            ""
        )

        customer.balance_transfer_account_number = request.POST.get(
            "balance_transfer_account_number",
            ""
        ) 

        customer.balance_transfer_account_owner = request.POST.get(
            "balance_transfer_account_owner",
            ""
        )

        customer.vehicle_registration_number = request.POST.get(
            "vehicle_registration_number",
            ""
        ) 

        customer.vehicle_color = request.POST.get(
            "vehicle_color",
            ""
        )

        customer.vehicle_type = request.POST.get(
    "vehicle_type",
    ""
)
        customer.working_status = request.POST.get(
    "working_status",
    ""
)

        customer.house_type = request.POST.get(
            "house_type",
            ""
        )

        customer.spouse_age = request.POST.get(
            "spouse_age"
        
        ) or None

        customer.house_ownership = request.POST.get(
            "house_ownership",
            ""
        )

        customer.number_of_schooling_children = request.POST.get(
            "number_of_schooling_children"
        ) or None

        customer.number_of_working_children = request.POST.get(
            "number_of_working_children"
        ) or None
        customer.id_type = request.POST.get(
            "id_type",
            ""
        )
        if request.FILES.get("customer_photo"):
            customer.customer_photo = request.FILES.get(
                "customer_photo"
            )

        if request.FILES.get("mykad_photo"):
            customer.mykad_photo = request.FILES.get(
                "mykad_photo"
            )

        customer.save()

        create_notification(
    request.user,
    "Customer Updated",
    f"{customer.full_name} customer profile updated",
    url=f"/customers/{customer.pk}/",
    company_code=None
)
        log_activity(
    request.user,
    f"Customer updated: {customer.customer_reference} - {customer.full_name}",
    customer_id=customer.pk
)

        messages.success(
    request,
    "Customer updated successfully."
)

        request.session["from_customer_edit"]=True
        request.session["clear_customer_form"]=True

        return redirect(
    "customer_summary",
    customer_id=customer.pk
)
    

    return render(
        request,
        "core/customer_form.html",
        {
           
            "customer": customer,
            "prefill": {
    "full_name": "",
    "ic_number": "",
    "phone": "",
    "phone_number_2": "",
    "home_phone_number": "",
    "marital_status": "",
    "home_address_1": "",
    "employer_name": "",
    "employer_address": "",
    "office_phone_number": "",
    "total_working_years": "",
    "monthly_net_income": "",
    "other_income_name": "",
    "other_income_total": "",
    "spouse_name": "",
    "spouse_ic_number": "",
    "spouse_job": "",
    "spouse_monthly_income": "",
    "number_of_children": "",
    "number_of_working_children": "",
    "car_loan": "",
    "house_loan": "",
    "motorcycle_loan": "",
    "introduced_by": "",
    "note": "",
}
        }
    )
@never_cache
@login_required
def customer_download_options(request, customer_id):

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    language = request.GET.get("lang", "en")

    if request.method == "POST":



        selected_sections = request.POST.getlist(
            "sections"
        )

        request.session["download_sections"] = (
            selected_sections
        )

        request.session["profile_pdf_language"] = request.GET.get(
    "lang",
    "en"
)

        request.session["download_type"] = (
    request.POST.get(
        "download_type",
        "pdf"
    )
)

        if request.session["download_type"] == "word":

            return redirect(
        "customer_profile_word",
        customer_id=customer.pk
    )
    

        return redirect(
    "customer_profile_pdf",
    customer_id=customer.pk
)


    return render(
        request,
        "core/customer_download_options.html",
        {
            "customer": customer,
            "language": language,
        }
    )



@login_required
def payment_list(request):
    if not require_steps_8_10(request.user):
        return HttpResponseForbidden("Access Denied")

    payments = Payment.objects.select_related(
        "agreement", "agreement__customer"
    ).order_by("-created_at")

    return render(request, "core/payment_list.html", {"payments": payments})


@login_required
def receipt_list(request):
    if not require_steps_5_7(request.user):
        return HttpResponseForbidden("Access Denied")

    receipts = Receipt.objects.select_related("customer", "agreement").order_by("-created_at")
    return render(request, "core/receipt_list.html", {"receipts": receipts})

@login_required
def open_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    url = notification.url
    notification.delete()

    if url:
        return redirect(url)

    return redirect("dashboard")

@login_required
def clear_notifications(request):

    Notification.objects.filter(
        user=request.user
    ).delete()

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

@login_required
def delete_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.delete()

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

@login_required
def live_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    activities = ActivityLog.objects.all().order_by(
        "-created_at"
    )[:5]

    return JsonResponse({
        "unread_count": Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count(),

        "notifications": [
            {
                "title": n.title,
                "message": n.message,
                "url": n.url,
                "created_at": n.created_at.strftime("%d %b %Y, %I:%M %p")
            }
            for n in notifications
        ],

        "activities": [
            {
                "action": a.action,
                "created_at": a.created_at.strftime("%d %b %Y, %I:%M %p"),
                "user": a.user.username if a.user else "System"
            }
            for a in activities
        ]
    })

@login_required
def notifications_api(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:10]

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    html = ""

    if notifications:
        for n in notifications:
            html += f"""
            <a class="notif-item" href="/notifications/{n.pk}/open/">
                <div class="notif-title">{n.title}</div>
                <div class="notif-message">{n.message}</div>
                <div class="notif-time">{timesince(n.created_at)}ago</div>
            </a>
            """
    else:
        html = """
        <div class="notif-empty">
            No notifications
        </div>
        """

    return JsonResponse({
        "unread_count": unread_count,
        "html": html
    })

from django.http import JsonResponse

@login_required
def recent_activity_api(request):

    activities = ActivityLog.objects.order_by(
        "-created_at"
    )[:3]

    html = ""

    for activity in activities:

        user_text = ""

        if activity.user:
            user_text = (
                activity.user.full_name
                if hasattr(activity.user, "full_name")
                else activity.user.username
            )

        html += f"""
        <div class="activity-item">
            <div class="activity-title">
                {activity.action}
            </div>

            <div class="activity-meta">
               {timezone.localtime(activity.created_at).strftime('%d %b %Y • %I:%M %p')}
                {f' • {user_text}' if user_text else ''}
            </div>
        </div>
        """

    return JsonResponse({
        "html": html
    })

@login_required
def global_search(request):

    q = request.GET.get("q", "").strip()

    results = []

    if len(q) < 2:
        return JsonResponse({
            "results": results
        })

    applications = Application.objects.filter(
        Q(full_name__icontains=q) |
        Q(ic_or_passport_no__icontains=q) |
        Q(phone_number__icontains=q) |
        Q(status__icontains=q)
    )[:10]

    for app in applications:

        results.append({
            "type": "Application",
            "title": app.full_name,
            "subtitle": f"{app.ic_or_passport_no} • {app.status}",
            "url": f"/applications/{app.pk}/"
        })
    customers = Customer.objects.filter(
        Q(full_name__icontains=q)
    )[:5]

    for customer in customers:

        results.append({
            "type": "Customer",
            "title": customer.full_name,
            "subtitle": "Customer Record",
            "url": f"/customers/{customer.pk}/"
        })
    agreements = Agreement.objects.filter(
        Q(agreement_number__icontains=q) |
        Q(customer__full_name__icontains=q)
    ).select_related("customer")[:5]

    for agreement in agreements:

        results.append({
            "type": "Agreement",
            "title": agreement.agreement_number,
            "subtitle": f"{agreement.customer.full_name}",
            "url": f"/agreements/{agreement.pk}/"
        })
    payments = Payment.objects.filter(
        Q(agreement__agreement_number__icontains=q) |
        Q(agreement__customer__full_name__icontains=q) |
        Q(method__icontains=q) |
        Q(reference_note__icontains=q)
    ).select_related(
        "agreement",
        "agreement__customer"
    )[:5]

    for payment in payments:

        results.append({
            "type": "Payment",
            "title": f"Payment #{payment.pk}",
            "subtitle": f"{payment.agreement.customer.full_name} • {payment.payment_date}",
            "url": f"/payments/{payment.pk}/"
        })
    receipts = Receipt.objects.filter(
        Q(receipt_number__icontains=q) |
        Q(customer__full_name__icontains=q)
    ).select_related("customer")[:5]

    for receipt in receipts:

        results.append({
            "type": "Receipt",
            "title": receipt.receipt_number,
            "subtitle": receipt.customer.full_name,
            "url": f"/receipts/{receipt.pk}/"
        })

    return JsonResponse({
        "results": results
    })

@login_required
def switch_company(request, company_code):
    request.session["active_company"] = company_code
    return redirect("dashboard")
@never_cache
@login_required
def application_full_detail(request, app_id):
    if not require_steps_1_4(request.user):
        return HttpResponseForbidden("Access Denied")

    app = get_object_or_404(Application, id=app_id)

    return render(
        request,
        "core/application_full_detail.html",
        {
            "app": app
        }
    )