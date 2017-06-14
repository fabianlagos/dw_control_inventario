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

#Funcion que prestar productos en el inventario
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

def inventario():

    estado = (db.inventario.disponible == True)

    links = [lambda row: A('Solicitar', callback=URL('gestion_inventario', 'solicitar_producto',
    vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]
    grid = SQLFORM.grid(estado, details=False, csv=False, links=links)

    return dict(grid=grid)

def solicitar_producto():

    import inventario
    #retrieve value
    id_producto_solicitado = request.vars['id']

    print id_producto_solicitado

    response.flash = PrestarInventario(id_producto_solicitado, auth.user.id)

    #db(db.inventario.id == id_producto_solicitado).update(disponible = False)

    #aquí van los insert a prestaciones

    estado = (db.inventario.disponible == True)

    links = [lambda row: A('Solicitar', callback=URL('gestion_inventario', 'solicitar_producto', vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(estado, details=False, csv=False, links=links)

    return grid

#Esta funcion la pueden ver el Administrador y Supervisor
def productos_prestados():

    prestado = (db.inventario.disponible == False)

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver_producto', vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(prestado, details=False, csv=False, links=links)

    return dict(grid=grid)

def devolver_producto():

    import inventario

    #retrieve value
    id_producto_solicitado = request.vars['id']

    print id_producto_solicitado

    #db(db.inventario.id == id_producto_solicitado).update(disponible = True)
    response.flash = DevolverInventario(id_producto_solicitado, auth.user.id)

    #aquí van los insert a prestaciones

    prestado = (db.inventario.disponible == False)

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver_producto', vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(prestado, details=False, csv=False, links=links)

    return grid
