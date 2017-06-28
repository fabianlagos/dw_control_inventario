#Funcion que prestar productos en el inventario
def PrestarInventario(id_producto_solicitado, id_user):

    from datetime import datetime

    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    nombre_producto = db((db.inventario.id == id_producto_solicitado) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    try:
        #Insertar la transaccion en prestaciones(registro)
        db.prestacion.insert( id_user = id_user,
                            id_inventario = id_producto_solicitado,
                            fecha_prestacion = fecha_actual,
                            devolucion_pendiente = False)

        #Cambiar el estado a no disponible del producto en el inventario
        db(db.inventario.id == id_producto_solicitado).update(disponible = False)


    except:
         db.logs_inventario.insert(id_user=id_user,
                                    username=auth.user.username,
                                    id_inventario=id_producto_solicitado,
                                    nombre_producto=nombre_producto,
                                    fecha=fecha_actual,
                                    descripcion="Error: No se puedo registrar el producto prestado")

         return "Hubo un error, comunicate con el administrador"

    db.logs_inventario.insert(id_user=id_user,
                               username=auth.user.username,
                               id_inventario=id_producto_solicitado,
                               nombre_producto=nombre_producto,
                               fecha=fecha_actual,
                               descripcion="Se registra el producto prestado")

    return "Tu producto ha sido prestado correctamente"

#Funcion que presta productos en el inventario
def DevolverInventario(id_producto_solicitado, id_user):
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    nombre_producto = db((db.inventario.id == id_producto_solicitado) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    try:
        #Cambia el estado a devolucion_pendiente en prestacion. estado = True
        db((db.prestacion.id_inventario == id_producto_solicitado) & (db.prestacion.fecha_devolucion == None)).update(devolucion_pendiente = True)

        #Cambiar el estado a no disponible del producto en el inventario
        db(db.inventario.id == id_producto_solicitado).update(disponible = False)

    except:
        db.logs_inventario.insert(id_user=id_user,
                                   username=auth.user.username,
                                   id_inventario=id_producto_solicitado,
                                   nombre_producto=nombre_producto,
                                   fecha=fecha_actual,
                                   descripcion="Error: Producto no devuelto")

        return "Hubo un error, comunicate con el administrador."

    db.logs_inventario.insert(id_user=id_user,
                               username=auth.user.username,
                               id_inventario=id_producto_solicitado,
                               nombre_producto=nombre_producto,
                               fecha=fecha_actual,
                               descripcion="Producto devuelto, esperado aprobacion")

    return "Tu producto ha sido devuelto correctamente y queda a la espera de aprobación de un administrador."

def AprobarInventario(id_prestacion, id_producto_solicitado, id_user):
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    nombre_producto = db((db.inventario.id == id_producto_solicitado) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    try:
        #Cambia el estado del producto en prestaciones a Falso, con lo que se cumplen las condiciones de
        #disponibilidad del producto (aprobacion_pendiente y devolucion_pendiente = False)
        db(db.prestacion.id == id_prestacion).update( devolucion_pendiente = False,
                                                                 fecha_devolucion = datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

        #Cambia el estado del producto en el inventario y lo marca como disponible.
        db(db.inventario.id == id_producto_solicitado).update(disponible = True)

    except:
        db.logs_inventario.insert(id_user=id_user,
                                   username=auth.user.username,
                                   id_inventario=id_producto_solicitado,
                                   nombre_producto=nombre_producto,
                                   fecha=fecha_actual,
                                   descripcion="Error: Devolucion fallida")

        return "Hubo un error, comunicate con el administrador."

    db.logs_inventario.insert(id_user=id_user,
                               username=auth.user.username,
                               id_inventario=id_producto_solicitado,
                               nombre_producto=nombre_producto,
                               fecha=fecha_actual,
                               descripcion="Devolucion aprobada, producto añadido al inventario")

    return "El producto ha sido devuelto al inventario correctamente."

def RechazarInventario(id_prestacion, id_producto_solicitado, id_user, user_involucrado, razon):
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    nombre_producto = db((db.inventario.id == id_producto_solicitado) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    try:
            #Solo se agrega la fecha de devolucion en el caso de rechazo
        db(db.prestacion.id == id_prestacion).update(fecha_devolucion = datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))


    except:
        db.logs_inventario.insert(id_user=id_user,
                                   username=auth.user.username,
                                   id_inventario=id_producto_solicitado,
                                   nombre_producto=nombre_producto,
                                   fecha=fecha_actual,
                                   descripcion="Error al rechazar producto")

        return "Hubo un error, comunicate con el administrador."

    db.logs_inventario.insert(id_user=id_user,
                               username=auth.user.username,
                               id_inventario=id_producto_solicitado,
                               nombre_producto=nombre_producto,
                               fecha=fecha_actual,
                               descripcion="Se rechaza la devolucion del usuario: " + user_involucrado + '. Razon: ' + razon )

    return "El producto ha sido rechazado"

def RetirarInventario(id_inventario, id_user, razon):
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    nombre_producto = db((db.inventario.id == id_inventario) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    try:

        db(db.inventario.id == id_inventario).delete()

    except:
        db.logs_inventario.insert(id_user=id_user,
                                   username=auth.user.username,
                                   id_inventario=id_inventario,
                                   nombre_producto=nombre_producto,
                                   fecha=fecha_actual,
                                   descripcion="Error al retirar el producto del inventario")

        return "Hubo un error, comunicate con el administrador."

    db.logs_inventario.insert(id_user=id_user,
                               username=auth.user.username,
                               id_inventario=id_inventario,
                               nombre_producto=nombre_producto,
                               fecha=fecha_actual,
                               descripcion="Se retira el producto del inventario. Razon:"  + razon )

    return "El producto ha sido retirado del inventario"



#Esta es la vista Inventario
@auth.requires_login()
def inventario():

    if request.vars['id_inventario'] != None:
        if db(db.inventario.id == request.vars['id_inventario']).select(db.inventario.disponible)[0].get('disponible'):
            response.flash = PrestarInventario(request.vars['id_inventario'], auth.user.id)

    #SELECT producto.nombre, inventario.n_serie, inventario.descripcion FROM producto, inventario
        #WHERE producto.id = inventario.id_producto AND inventario.disponible = True

    #Falta agregar la categoria a los campos, para mostrarlos en la vista
    consulta = ((db.inventario.id_producto == db.producto.id) & (db.inventario.disponible == True))


    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo]

    maxtextlength = {'inventario.descripcion' : 50}

    db.inventario.id.readable = False


    links = [lambda row: A('Solicitar', _href=URL('gestion_inventario', 'solicitar_producto',
             vars={'id' : row.inventario.id }), _class="btn btn-default glyphicon glyphicon-plus"),
             lambda row: A('Informacion', _href=URL('informacion_inventario', vars={'id' : row.inventario.id}),  _class="btn btn-default glyphicon glyphicon-plus" )  ]

    #grid = SQLFORM.grid(consulta, fields=campos, editable=False, deletable=False, details=False, csv=False)
    if auth.has_membership(group_id='admin'):
        links = [lambda row: A('Informacion', _href=URL('informacion_inventario', vars={'id' : row.inventario.id}), _class="btn btn-default glyphicon glyphicon-plus"),
                 lambda row: A('Retirar', _href=URL('retirar_inventario', vars={'id_inventario' : row.inventario.id}), _class="btn btn-default 	glyphicon glyphicon-minus"),
                 lambda row: A('Editar', _href=URL('editar_inventario', vars={'id_inventario': row.inventario.id}), _class="btn btn-default glyphicon glyphicon-pencil")]
        grid = SQLFORM.grid(consulta, fields=campos, create=False, details=False, csv=False, deletable=False, editable=False, links=links, maxtextlength=maxtextlength)

    else:
        grid = SQLFORM.grid(consulta, fields=campos, create=False, details=False, csv=False, deletable=False, editable=False, links=links, maxtextlength=maxtextlength)

    return dict(grid=grid)

#ajax para solicitar producto (botón)
def solicitar_producto():

    id_inventario = request.vars['id']

    query = db((db.inventario.id == id_inventario) & (db.inventario.id_producto == db.producto.id)).select(db.inventario.ALL, db.producto.ALL)[0]

    hay_imagen = True
    if query.inventario['imagen'] == None:
        hay_imagen=False


    return dict(query=query, hay_imagen=hay_imagen, id_inventario=id_inventario)

#Esta funcion la pueden ver el Supervisor y usuarios
def devolver_productos():

    consulta = ((auth.user.id == db.prestacion.id_user)
              & (db.prestacion.fecha_devolucion == None)
              & (db.prestacion.devolucion_pendiente == False)
              & (db.inventario.disponible == False)
              & (db.prestacion.id_inventario == db.inventario.id)
              & (db.inventario.id_producto == db.producto.id) )

    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo ]

    """

    consulta = (db.prestacion.fecha_devolucion == None) & (db.prestacion.id_user == auth.user.id)

    campos = [db.prestacion.id]

    """
    db.inventario.id.readable = False

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
    vars={'id' : row.inventario.id }),_onclick="confirm('Estas seguro que deseas pedir este producto?')" , target='t', _class="btn btn-default glyphicon glyphicon-minus")]

    grid = SQLFORM.grid(consulta, fields=campos, create=False, editable=False, deletable=False, details=False, csv=False, links=links)
    #grid = SQLFORM.grid(consulta, fields=campos, create=False, details=False, csv=False, links=links)

    return dict(grid=grid)

#Ajax de la vista devolver productos
def devolver():

    import inventario

    #retrieve value
    id_producto_solicitado = request.vars['id']

    #db(db.inventario.id == id_producto_solicitado).update(disponible = True)
    response.flash = DevolverInventario(id_producto_solicitado, auth.user.id)

    #aquí van los insert a prestaciones

    consulta = ((auth.user.id == db.prestacion.id_user)
              & (db.prestacion.fecha_devolucion == None)
              & (db.prestacion.devolucion_pendiente == False)
              & (db.inventario.disponible == False)
              & (db.prestacion.id_inventario == db.inventario.id)
              & (db.inventario.id_producto == db.producto.id) )

    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo]

    db.inventario.id.readable = False

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
    vars={'id' : row.inventario.id }), _onclick="confirm('Estas seguro que deseas pedir este producto?')" , target='t', _class="btn btn-default glyphicon glyphicon-minus")]

    grid = SQLFORM.grid(consulta, fields=campos, create=False, editable=False, deletable=False, details=False, csv=False, links=links)

    return grid

#Vista de productos prestados (Administrador y Supervisor pueden ver esto)
def productos_prestados():

    consulta = ((db.inventario.id_producto == db.producto.id)
              & (db.auth_user.id == db.prestacion.id_user)
              & (db.prestacion.fecha_devolucion == None)
              & (db.prestacion.devolucion_pendiente == False)
              & (db.inventario.disponible == False))

    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo,
              db.auth_user.username ]

    db.inventario.id.readable = False

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
             vars={'id' : row.inventario.id }), target='t', _class="btn btn-default glyphicon glyphicon-minus")]

    grid = SQLFORM.grid(consulta, fields=campos, editable=False, deletable=False, details=False, csv=False)
    #grid = SQLFORM.grid(consulta, fields=campos, create=False, details=False, csv=False, links=links)
    return dict(grid=grid)

def devolucion_pendiente():

    consulta = ((db.prestacion.id_inventario == db.inventario.id)
                & (db.inventario.id_producto == db.producto.id)
                & (db.auth_user.id == db.prestacion.id_user)
                & (db.inventario.disponible == False)
                & (db.prestacion.devolucion_pendiente == True)
                & (db.prestacion.fecha_devolucion == None))

    links = [lambda row: A('Aprobacion', callback=URL('gestion_inventario', 'aprobacion',
             vars={'id' : row.prestacion.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign"),
             lambda row: A('Rechazar', _href=URL('gestion_inventario', 'rechazar', vars={'id_prestacion' : row.prestacion.id }), _class="btn btn-default btn-md glyphicon-ok-sign")]

    campos = [db.prestacion.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo,
              db.auth_user.username,
              db.prestacion.fecha_prestacion ]

    db.prestacion.id.readable = False

    grid = SQLFORM.grid(consulta, fields=campos, create=False, editable=False, deletable=False, details=False, csv=False, links=links)

    return dict(grid=grid)

def aprobacion():

    id_prestacion_solicitada = request.vars['id']

    id_producto_solicitado = db(db.prestacion.id == id_prestacion_solicitada).select(db.prestacion.id_inventario)[0].get('id_inventario')

    #db(db.inventario.id == id_producto_solicitado).update(disponible = True)
    response.flash = AprobarInventario(id_prestacion_solicitada, id_producto_solicitado, auth.user.id)

    consulta = ((db.prestacion.id_inventario == db.inventario.id)
                & (db.inventario.id_producto == db.producto.id)
                & (db.auth_user.id == db.prestacion.id_user)
                & (db.inventario.disponible == False)
                & (db.prestacion.devolucion_pendiente == True)
                & (db.prestacion.fecha_devolucion == None))

    campos = [db.prestacion.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo,
              db.auth_user.username,
              db.prestacion.fecha_prestacion ]

    db.prestacion.id.readable = False

    links = [lambda row: A('Aprobacion', callback=URL('gestion_inventario', 'aprobacion',
             vars={'id' : row.prestacion.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign"),
             lambda row: A('Rechazar', _href=URL('gestion_inventario', 'rechazar', vars={'id_prestacion' : row.prestacion.id }), _class="btn btn-default btn-md glyphicon-ok-sign")]


    grid = SQLFORM.grid(consulta, fields=campos, create=False, editable=False, deletable=False, details=False, csv=False, links=links)

    return grid

def retirar_inventario():

    id_inventario = request.vars['id_inventario']

    nombre_producto = db((db.inventario.id == id_inventario) & (db.inventario.id_producto == db.producto.id)).select(db.producto.nombre)[0].get('nombre')

    form = SQLFORM.factory( Field('Razon', 'text', requires=IS_NOT_EMPTY() ) )
    strings = form.elements(_class='col-sm-9')
    for s in strings:
        s['_class'] = 'col-sm-7'


    if form.process().accepted:

        session.flash = RetirarInventario(id_inventario, auth.user.id, form.vars.Razon)

        redirect(URL('inventario'))

    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'

    return dict(form=form, nombre_producto=nombre_producto )

def rechazar():

    id_prestacion = request.vars['id_prestacion']

    query = db((db.prestacion.id == id_prestacion) & (db.prestacion.id_inventario == db.inventario.id) & (db.producto.id == db.inventario.id_producto) & (db.auth_user.id == db.prestacion.id_user)).select(db.auth_user.username, db.inventario.id ,db.producto.nombre)[0]

    form = SQLFORM.factory( Field('Razon', 'text', requires=IS_NOT_EMPTY() ) )
    strings = form.elements(_class='col-sm-9')


    for s in strings:
        s['_class'] = 'col-sm-7'


    if form.process().accepted:

        session.flash = RechazarInventario(id_prestacion, query.inventario['id'], auth.user.id, query.auth_user['username'], form.vars.Razon)

        redirect(URL('devolucion_pendiente'))

    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'


    return dict(form=form, query=query)

def informacion_inventario():

    id_inventario = request.vars['id']

    query = db((db.inventario.id == id_inventario) & (db.inventario.id_producto == db.producto.id)).select(db.inventario.ALL, db.producto.ALL)[0]

    hay_imagen = True
    if query.inventario['imagen'] == None:
        hay_imagen=False


    return dict(query=query, hay_imagen=hay_imagen)

def editar_inventario():

    record = db.inventario(request.vars['id_inventario']) or redirect(URL('inventario'))
    nombre = db(db.producto.id == record.id_producto).select(db.producto.nombre)[0].get('nombre')
    form = SQLFORM(db.inventario, record, fields=['n_serie', 'descripcion'], showid=False)

    if form.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('inventario'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, nombre=nombre)
