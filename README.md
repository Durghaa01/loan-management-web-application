# Custom Loan Management Web Application

A custom Django-based loan management web application developed for a real business client.

> **Note:** Client data, credentials, production configuration, and confidential business files are not included in this repository.

## Overview

The system centralizes customer onboarding, loan agreements, payments, ledger records, receipts, reporting, staff access, and operational activity in one web application.

## Key Features

- Customer pre-registration and application review
- Customer profile and document management
- Loan / agreement management
- Payment recording and receipt generation
- Separate internal and official ledger workflows
- Reports and PDF/document generation
- Role-based staff access and authentication
- Activity logging, notifications, and global search
- Multi-company / business-context switching
- Message templates and WhatsApp-related workflow support

## Tech Stack

- **Backend:** Python, Django 6
- **Frontend:** Django Templates, HTML, CSS, JavaScript
- **Database:** SQLite for the development/demo configuration
- **Security:** Django authentication, role-based permissions, django-axes
- **Documents / Reports:** ReportLab, WeasyPrint, xhtml2pdf, python-docx

## Architecture

![System Architecture](docs/Loan%20Management%20system-architecture.png)

## Documentation

📄 [Project Notes](docs/project-notes.md)

## Local Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and replace the sample values.
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a local admin account if needed:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Context

- **Role:** Independent / Freelance Full-Stack Developer
- **Project Type:** Paid real-world client project
- **Development Period:** December 2025 – Present

This repository contains the project source and technical documentation without client production data or confidential operational information.
