Instalation
+++++++++++++++
Install the library
======================
You can install the library using pip, poetry or pipx.
pip
---
Run ``pip install django-oauth-client``

Poetry
------
Run ``poetry add django-oauth-client``

Pipx
----
Run ``pipx install django-oauth-client``

Manual
------
Download the source code from https://https://github.com/3h04m1/django-oauth-client
and run ``python setup.py install``

Add to Django
==================================================================
#. Add ``oauth_client`` to your ``INSTALLED_APPS`` setting like this.
    .. code-block:: python

        INSTALLED_APPS = [
            ...
            'oauth_client',
        ]
#. Include the oauth_client URLconf in your project urls.py like this.
    .. code-block:: python

        url(r'^oauth/', include('oauth_client.urls')),

#. Run ``python manage.py makemigrations oauth_client`` to create the oauth_client models.
#. Run ``python manage.py migrate oauth_client`` to create the oauth_client models.



