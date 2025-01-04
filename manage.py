#!/usr/bin/env python

# Minimal manage.py script. Can be used to create migrations.

import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line

settings.configure(
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        # "django.contrib.sessions",
        "django.contrib.messages",
        # "django.contrib.staticfiles",
        "mneia_backend",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],
    MIDDLEWARE=[
        # "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        # "django.middleware.common.CommonMiddleware",
        # "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        # Keep this after django.contrib.auth.middleware.AuthenticationMiddleware because AuthenticationMiddleware adds
        # the user to the request and MneiaLoginRequiredMiddleware requires it:
        # "mneia_project.middleware.MneiaLoginRequiredMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        # "django.middleware.clickjacking.XFrameOptionsMiddleware",
        # "corsheaders.middleware.CorsMiddleware",
    ],
)
django.setup()
execute_from_command_line(sys.argv)
