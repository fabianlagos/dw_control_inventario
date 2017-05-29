def inventario():

    estado = (db.inventario.disponible == True)

    links = [lambda row: A('Solicitar', callback=URL('gestion_inventario', 'solicitar_producto', vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]
    grid = SQLFORM.grid(estado, details=False, csv=False, links=links)

    return dict(grid=grid)

def solicitar_producto():
    #retrieve value
    id_producto_solicitado = request.vars['id']

    print id_producto_solicitado

    db(db.inventario.id == id_producto_solicitado).update(disponible = False)

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
    #retrieve value
    id_producto_solicitado = request.vars['id']

    print id_producto_solicitado

    db(db.inventario.id == id_producto_solicitado).update(disponible = True)

    #aquí van los insert a prestaciones

    prestado = (db.inventario.disponible == False)

    links = [lambda row: A('Devolver', callback=URL('gestion_inventario', 'devolver_producto', vars={'id' : row.id }), target='t', _class="btn btn-default btn-md glyphicon-ok-sign")]

    grid = SQLFORM.grid(prestado, details=False, csv=False, links=links)

    return grid
