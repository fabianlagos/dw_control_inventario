# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B('ITsec'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    if auth.has_membership(1):
        response.menu += [
            (T('Inventario'), False, URL('inventario')),
            (T('Productos'), False, URL('productos')),
            (T('Productos prestados'), False, URL('productos_prestados')),
            (T('Gestion de usuarios'), False, URL('gestion_usuarios'))


        ]
    if auth.has_membership(2):
        response.menu += [
            (T('Inventario'), False, URL('inventario')),
            (T('Devolver producto'), False, URL('devolver_productos')),
            (T('Productos prestados'), False, URL('productos_prestados')),

        ]
    if auth.has_membership(3):
        response.menu += [
            (T('Inventario'), False, URL('inventario')),
            (T('Productos prestados'), False, URL('productos_prestados')),
        ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
