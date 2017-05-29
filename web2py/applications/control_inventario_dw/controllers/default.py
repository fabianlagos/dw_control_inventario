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

    grid = SQLFORM.grid(consulta, csv=False, links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.id]), _class="btn btn-info glyphicon glyphicon-signal")])

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

def agregarainventario():
    form = SQLFORM(db.inventario, fields=['n_serie', 'descripcion', 'disponible'])
    idproducto=request.args[0]
    cantidad=1
    if form.validate():
        while cantidad>0:
            #db.inventario.insert(id_producto='idproducto',n_serie="f", descripcion="x", disponible= "true")
            db.inventario.insert(id_producto=idproducto, n_serie=form.vars.n_serie, descripcion=form.vars.descripcion, disponible=form.vars.disponible)
                     #**db.inventario._filter_fields(form.vars))
            #db.inventario.insert(id_producto=idproducto,**(form.vars))
            cantidad=cantidad-1
        redirect(URL("default", "inventario"))
    return dict(form=form)
