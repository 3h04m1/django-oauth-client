Views
++++

Default Views
=====

There are 2 default views that are created when you install the module. These views are:

Login view
----------

``login`` - Thist view only redirect the user to the ``provider_authorize_url`` from ``settings.py``or the ``authorize_url`` atribute from the **Custom Provider** model.
   .. code-block:: python

        def login(request: HttpRequest,provider:OAuth2Provider) -> HttpResponseRedirect:
            return redirect(provider.authorize_url)

Callback view
-------------

``callback`` - This view is the callback view that is called by the provider after the user has
   authorized the application. This view will create a new user if the user does not exist in the
   database. If the user exists, the view will update the user's information. The view will then
   redirect the user to the root of the site.
    .. code-block:: python
        
        def callback(request :HttpRequest,provider:OAuth2Provider) -> HttpResponseRedirect:
            provider.authorize(request)
            return redirect(to='/')

Custom Views
=============
For custom views visit the :ref:`Customization` section.
