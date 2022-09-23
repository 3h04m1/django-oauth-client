Configuration
+++++++++++++++

Configure settings.py for the desired OAuth providers.
=======================================================
.. code-block:: python

    OAUTH_PROVIDERS = {
        # First provider
        "{provider_name}": 
            {
            "client_id": "{your_client_id}",
            "client_secret": "{your_client_secret}",
            "authorize_url": "{your_authorize_url}",
        },
        # Second provider
        "{provider_name}": 
            {
            "client_id": "{your_client_id}",
            "client_secret": "{your_client_secret}",
            "authorize_url": "{your_authorize_url}",
        },
        # ...
    } 

.. important:: 
    For custom providers the ``{provider_name}`` must be the same as the ``OAuth2Provider.name`` or provider class ``name`` atribute .