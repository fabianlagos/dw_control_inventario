#Funcion que prestar productos en el inventario
def PrestarInventario(id_producto_solicitado, id_user):
    from datetime import datetime

    try:
        #Insertar la transaccion en prestaciones(registro)
        db.prestacion.insert( id_user = id_user,
                            id_inventario = id_producto_solicitado,
                            fecha_prestacion = datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
                            devolucion_pendiente = True)

        #Cambiar el estado a no disponible del producto en el inventario
        db(db.inventario.id == id_producto_solicitado).update(disponible = False)


    except:
         return "Hubo un error, comunicate con el administrador"

    return "Tu producto ha sido prestado correctamente"

#Funcion que presta productos en el inventario
def DevolverInventario(id_producto_solicitado, id_user):
    from datetime import datetime

    try:
        #Cambiar el estado a disponible del producto en el inventario
        db(db.inventario.id == id_producto_solicitado).update(disponible = True)

        #Cambiar el estado a devolucion_pendiente en prestacion. Se devuelve => estado = False
        db(db.prestacion.id_inventario == id_producto_solicitado).update( devolucion_pendiente = False,
                                                                          fecha_devolucion = datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))

    except:
         return "Hubo un error, comunicate con el administrador"

    return "Tu producto ha sido devuelto correctamente"

#Esta es la vista Inventario
def inventario():

    #SELECT producto.nombre, inventario.n_serie, inventario.descripcion FROM producto, inventario
        #WHERE producto.id = inventario.id_producto AND inventario.disponible = True

    #Falta agregar la categoria a los campos, para mostrarlos en la vista
    consulta = ( db.inventario.id_producto == db.producto.id ) & (db.inventario.disponible == True)
    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo]

    db.inventario.id.readable = False

    links = [lambda row: A('Solicitar', callback=URL('gestion_inventario', 'solicitar_producto',
    vars={'id' : row.inventario.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    #grid = SQLFORM.grid(consulta, fields=campos, editable=False, deletable=False, details=False, csv=False)
    grid = SQLFORM.grid(consulta, fields=campos, details=False, csv=False, links=links)

    return dict(grid=grid)

#ajax para solicitar producto (botón)
def solicitar_producto():

    import inventario
    #Retrieve value
    id_producto_solicitado = request.vars['id']

    #db(db.inventario.id == id_producto_solicitado).update(disponible = False)
    response.flash = PrestarInventario(id_producto_solicitado, auth.user.id)

    #¿aquí van los insert a prestaciones?

    consulta = ( db.inventario.id_producto == db.producto.id ) & (db.inventario.disponible == True)
    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo]

    db.inventario.id.readable = False

    links = [lambda row: A('Solicitar', callback=URL('gestion_inventario', 'solicitar_producto',
             vars={'id' : row.inventario.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(consulta, fields=campos, details=False, csv=False, links=links)

    return grid

#Esta funcion la pueden ver el Supervisor y usuarios
def devolver_productos():

    prestado = (db.inventario.disponible == False)

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
             vars={'id' : row.inventario.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    #grid = SQLFORM.grid(consulta, fields=campos, editable=False, deletable=False, details=False, csv=False)
    grid = SQLFORM.grid(consulta, fields=campos, details=False, csv=False, links=links)

    return dict(grid=grid)

#Ajax de la vista devolver productos
def devolver():

    import inventario

    #retrieve value
    id_producto_solicitado = request.vars['id']

    #db(db.inventario.id == id_producto_solicitado).update(disponible = True)
    response.flash = DevolverInventario(id_producto_solicitado, auth.user.id)

    #aquí van los insert a prestaciones

    consulta = ( db.inventario.id_producto == db.producto.id ) & (db.inventario.disponible == False)
    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo ]

    db.inventario.id.readable = False

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
             vars={'id' : row.inventario.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(consulta, fields=campos, details=False, csv=False, links=links)

    return grid

#Vista de productos prestados (Administrador y Supervisor pueden ver esto)
def productos_prestados():

    consulta = ( db.inventario.id_producto == db.producto.id ) & (db.inventario.disponible == False)
    campos = [db.inventario.id,
              db.producto.nombre,
              db.inventario.n_serie,
              db.inventario.descripcion,
              db.producto.marca,
              db.producto.modelo ]

    db.inventario.id.readable = False

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver',
             vars={'id' : row.inventario.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    #grid = SQLFORM.grid(consulta, fields=campos, editable=False, deletable=False, details=False, csv=False)
    grid = SQLFORM.grid(consulta, fields=campos, details=False, csv=False, links=links)
    return dict(grid=grid)
