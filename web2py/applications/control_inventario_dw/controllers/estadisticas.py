def ProductosMasPedidos():

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'

    import pygal
    import requests

    #aqui va la consulta
    count = db.producto.id.count()
    consulta = db((db.inventario.id == db.prestacion.id_inventario) &
               (db.producto.id == db.inventario.id_producto)).select(db.prestacion.id, db.inventario.id, db.producto.id, db.producto.nombre, count, groupby=db.producto.nombre, orderby=~count)



    counts = []
    labels = []

    line_chart = pygal.Bar(width=800, height=400, x_label_rotation=50)


    for i in consulta:
        labels.append(i.producto.nombre)
        counts.append(i._extra.get('COUNT(producto.id)'))


    line_chart.x_labels = labels
    line_chart.add('Prestaciones', counts)
    line_chart.title = "Productos mas pedidos"




    return line_chart.render()

def UsuariosMasPrestaciones():

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'

    import pygal
    import requests

    #aqui va la consulta
    count = db.auth_user.id.count()
    consulta = db(db.auth_user.id == db.prestacion.id_user).select(db.auth_user.username, count, groupby=db.auth_user.username, orderby=~count)



    counts = []
    labels = []

    line_chart = pygal.Bar(width=800, height=400, x_label_rotation=50)


    for i in consulta:
        labels.append(i.auth_user.username)
        counts.append(i._extra.get('COUNT(auth_user.id)'))


    line_chart.x_labels = labels
    line_chart.add('Prestaciones', counts)
    line_chart.title = "Usuarios con mas prestaciones"




    return line_chart.render()

def estadisticas():

    ProductosMasPedidos = URL('estadisticas', 'ProductosMasPedidos')

    UsuariosMasPrestaciones = URL('estadisticas', 'UsuariosMasPrestaciones')

    TotalUsuarios =  db(db.auth_user.id > 0).count()

    TotalProductos =  db(db.producto.id > 0).count()

    TotalInventarioDisponibles = db((db.inventario.id > 0) & (db.inventario.disponible == True)).count()

    TotalInventarioPrestado = db((db.inventario.id > 0) & (db.inventario.disponible == False)).count()

    TotalPrestaciones = db(db.prestacion.id > 0).count()

    TotalDevoluciones = db((db.prestacion.id > 0) & (db.prestacion.fecha_devolucion != None)).count()

    return dict(ProductosMasPedidos=ProductosMasPedidos,
                UsuariosMasPrestaciones=UsuariosMasPrestaciones,
                TotalUsuarios=TotalUsuarios,
                TotalProductos=TotalProductos,
                TotalInventarioDisponibles=TotalInventarioDisponibles,
                TotalInventarioPrestado=TotalInventarioPrestado,
                TotalPrestaciones=TotalPrestaciones,
                TotalDevoluciones=TotalDevoluciones)
