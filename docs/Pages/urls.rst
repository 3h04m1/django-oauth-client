Urls
++++

Default Urls
=============

For each ``provider`` there are 2 default urls:

Login url
------------
``/<provider_name>/login/`` - login url wich maps to :ref:`Login view`

url's ``name`` is ``{provider_name}_login``

Callback url
----------------
``/<provider_name>/callback/`` - callback url wich maps to :ref:`Callback view`
    
url's ``name`` is ``{provider_name}_callback``

.. important:: All the urls are generated based on ``OAUTH_PROVIDERS`` settings.
    The ``provider_name`` is the key of the provider in ``OAUTH_PROVIDERS``

Custom Urls
============
For custom urls visit :ref:`Customization` or :ref:`How To` section