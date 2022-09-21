====================
Django OAuth Client
====================

Polls is a Django app to conduct web-based polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "oauth_client" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'oauth_client',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('oauth_client.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/