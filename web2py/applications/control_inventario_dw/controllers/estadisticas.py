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

def HistorialUsuario():

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'

    import pygal
    import calendar

    #aqui va la consulta
    #count = db.producto.id.count()
    #consulta = db((db.inventario.id == db.prestacion.id_inventario) &
    #               (db.producto.id == db.inventario.id_producto)).select(db.prestacion.id, db.inventario.id, db.producto.id, db.producto.nombre, count, groupby=db.producto.nombre, orderby=~count)


    consulta = db(db.prestacion.id_user == auth.user.id).select(db.prestacion.ALL)
    labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    prestacion = [0,0,0,0,0,0,0,0,0,0,0,0]
    devolucion = [0,0,0,0,0,0,0,0,0,0,0,0]

    for i in consulta:
        prestacion[i.fecha_prestacion.month-1] = prestacion[i.fecha_prestacion.month-1] + 1
        if i.fecha_devolucion != None:
            devolucion[i.fecha_devolucion.month-1] = devolucion[i.fecha_devolucion.month-1] + 1



    line_chart = pygal.Bar(width=800, height=400, x_label_rotation=50)



    line_chart.x_labels = labels
    line_chart.add('Total prestaciones', prestacion)
    line_chart.add('Total devoluciones', devolucion)
    line_chart.title = "Historial Usuario"




    return line_chart.render()

@auth.requires_login()
def estadisticas():



    ProductosMasPedidos = URL('estadisticas', 'ProductosMasPedidos')

    UsuariosMasPrestaciones = URL('estadisticas', 'UsuariosMasPrestaciones')

    HistorialUsuario = URL('estadisticas', 'HistorialUsuario')

    TotalUsuarios =  db(db.auth_user.id > 0).count()

    TotalProductos =  db(db.producto.id > 0).count()

    TotalInventarioDisponibles = db((db.inventario.id > 0) & (db.inventario.disponible == True)).count()

    TotalInventarioPrestado = db((db.inventario.id > 0) & (db.inventario.disponible == False)).count()

    TotalPrestaciones = db(db.prestacion.id > 0).count()

    TotalDevoluciones = db((db.prestacion.id > 0) & (db.prestacion.fecha_devolucion != None)).count()

    pTotalPeticiones = db((db.prestacion.id > 0) & (db.prestacion.id_user == auth.user.id) & (db.prestacion.fecha_devolucion == None)).count()

    pTotalDevoluciones =  db((db.prestacion.id > 0) & (db.prestacion.id_user == auth.user.id) & (db.prestacion.fecha_devolucion != None)).count()

    pTotalPrestaciones = db((db.prestacion.id > 0) & (db.prestacion.id_user == auth.user.id)).count()

    consulta = ((db.prestacion.id_user == auth.user.id) &
               (db.prestacion.id_inventario == db.inventario.id) &
                (db.inventario.id_producto == db.producto.id))

    fields = [db.producto.nombre, db.producto.marca, db.producto.modelo, db.inventario.n_serie, db.prestacion.fecha_prestacion, db.prestacion.fecha_devolucion]
    grid = SQLFORM.grid(consulta, fields=fields, create=False, editable=False, deletable=False, details=False)

    return dict(ProductosMasPedidos=ProductosMasPedidos,
                UsuariosMasPrestaciones=UsuariosMasPrestaciones,
                TotalUsuarios=TotalUsuarios,
                TotalProductos=TotalProductos,
                TotalInventarioDisponibles=TotalInventarioDisponibles,
                TotalInventarioPrestado=TotalInventarioPrestado,
                TotalPrestaciones=TotalPrestaciones,
                TotalDevoluciones=TotalDevoluciones,
                pTotalPeticiones=pTotalPeticiones,
                pTotalDevoluciones=pTotalDevoluciones,
                pTotalPrestaciones=pTotalPrestaciones,
                HistorialUsuario=HistorialUsuario,
                grid=grid)

def crear_recomendacion():

    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    form = SQLFORM(db.recomendacion, fields=['titulo', 'mensaje'])
    if form.validate():
    ### deal with uploads explicitly
        form.vars.id = db.recomendacion.insert(id_user=auth.user.id, username=auth.user.username, titulo=form.vars.titulo, mensaje=form.vars.mensaje, fecha=fecha_actual)
        session.flash = "Tu recomendacion sera analizada por el administrador, muchas gracias!"
        redirect(URL('default','index'))
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form)

def lista_recomendacion():

    consulta = db.recomendacion

    fields = [db.recomendacion.username, db.recomendacion.titulo, db.recomendacion.activa]

    grid = SQLFORM.grid(consulta, deletable=False, editable=auth.has_membership('admin'), create=False, fields=fields)

    return dict(grid=grid)
