from django.urls import path
from core import views
from core.views import clear_notifications, customers_list, open_notification, pre_register, customer_summary
from core.views import applications_list
from core.views import application_detail
from core.views import convert_to_customer
from core.views import agreement_create, agreement_detail
from core.views import payment_create, payment_detail, payment_list
from core.views import receipt_generate, receipt_detail, receipt_list
from core.views import reports_dashboard
from core.views import message_center
from core.views import dashboard
from core.views import login_view, logout_view
from core.views import customer_document_upload, delete_notification
from core.views import customer_create 
from core.views import customer_edit
from core.views import customer_download_options
from core.views import customer_profile_pdf
from core.views import customer_documents_download



urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("pre-register/", pre_register, name="pre_register"),
    path("applications/", applications_list, name="applications_list"),
    path("applications/<int:app_id>/", application_detail, name="application_detail"),
    path("applications/<int:application_id>/delete/",views.application_delete,name="application_delete"),
    path(
    "applications/bulk-delete/",
    views.application_bulk_delete,
    name="application_bulk_delete"
),
path(
    "customers/bulk-delete/",
    views.customer_bulk_delete,
    name="customer_bulk_delete"
),
path(
    "customers/documents/<int:document_id>/download/",
    views.customer_document_file_download,
    name="customer_document_file_download"
),
path(
    "customers/documents/<int:document_id>/delete/",
    views.customer_document_delete,
    name="customer_document_delete"
),
    path("applications/<int:app_id>/convert/", views.convert_to_customer, name="convert_to_customer"),
    path("customers/", customers_list, name="customers_list"),
    path("customers/new/",customer_create,name="customer_create"),
    path("customers/<int:customer_id>/", customer_summary, name="customer_summary"),
    path("customers/<int:customer_id>/edit/", customer_edit, name="customer_edit"),
    path("customers/<int:customer_id>/download/",customer_download_options,name="customer_download_options"),
    path("customers/<int:customer_id>/download/pdf/",customer_profile_pdf,name="customer_profile_pdf"),
    path("customers/<int:customer_id>/documents/download/",customer_documents_download,name="customer_documents_download"),
    path("customers/<int:customer_id>/documents/upload/", customer_document_upload, name="customer_document_upload"),
    path("customers/<int:customer_id>/agreements/new/", agreement_create, name="agreement_create"),
    path("agreements/<int:agreement_id>/", agreement_detail, name="agreement_detail"),
    path("agreements/<int:agreement_id>/payments/new/", payment_create, name="payment_create"),
    path("payments/", payment_list, name="payment_list"),
    path("payments/<int:payment_id>/", payment_detail, name="payment_detail"),
    path("payments/<int:payment_id>/receipt/generate/", receipt_generate, name="receipt_generate"),
    path(
    "live-notifications/",
    views.live_notifications,
    name="live_notifications"
),
    path(
    "customers/<int:customer_id>/agreements/new/",
    views.agreement_create,
    name="agreement_create"
),
path(
    "agreements/<int:agreement_id>/download/",
    views.agreement_pdf,
    name="agreement_pdf",
),
path(
    "agreements/bulk-delete/",
    views.bulk_delete_agreements,
    name="bulk_delete_agreements",
),
path("messages/open-whatsapp/", views.open_whatsapp_message, name="open_whatsapp_message"),
path(
    "agreements/<int:agreement_id>/edit/",
    views.agreement_edit,
    name="agreement_edit",
),
    path("receipts/", receipt_list, name="receipt_list"),
    path(
    "notifications/api/",
    views.notifications_api,
    name="notifications_api"
),
    path("receipts/<int:receipt_id>/", receipt_detail, name="receipt_detail"),
    path(
    "activity/api/",
    views.recent_activity_api,
    name="recent_activity_api"
),
path(
    "messages/create-template/",
    views.message_template_create,
    name="message_template_create",
),
path(
    "messages/templates/bulk-delete/",
    views.bulk_delete_message_templates,
    name="bulk_delete_message_templates",
),
    path("reports/", reports_dashboard, name="reports_dashboard"),
    path("messages/", message_center, name="message_center"),
    path("notifications/<int:notification_id>/open/", open_notification, name="open_notification"),
    path("notifications/clear/", clear_notifications, name="clear_notifications"),
    path("notifications/<int:notification_id>/delete/", delete_notification, name="delete_notification"),
    path("global-search/", views.global_search, name="global_search"),
    path("switch-company/<str:company_code>/", views.switch_company, name="switch_company"),
    path("pre-register/success/",views.pre_register_success,name="pre_register_success"),
    path("applications/<int:app_id>/full/",views.application_full_detail,name="application_full_detail"),
            path(
    "agreements/",
    views.agreement_list,
    name="agreement_list",
),

]
