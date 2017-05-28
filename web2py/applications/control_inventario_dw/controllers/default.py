# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Bienvenido al Inventario de ITsec'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

#Esta funcion solo la puede ver el tipo de usuario Administrador
def productos():
    #Esto es un SELECT * FROM db.producto
    consulta = db.producto

    grid = SQLFORM.grid(consulta, csv=False)

    return dict(grid=grid)

#Esta funcion la puede ver todos los usuarios
def devolver_productos():

    return dict()


def inventario():

    estado = (db.inventario.disponible == True)

    links = [lambda row: A('Solicitar',_href=URL("default","inventario",args=[row.id]), _class='button')]

    grid = SQLFORM.grid(estado, links=links, csv=False)


    return dict(grid=grid)

#Esta funcion la pueden ver el Administrador y Supervisor
def productos_prestados():

<<<<<<< HEAD
    prestado = (db.inventario.disponible != True)

    grid = SQLFORM.grid(prestado, csv=False)
=======
    query = (db.inventario.disponible == False)

    grid = SQLFORM.grid(query)
>>>>>>> develop

    return dict(grid=grid)
