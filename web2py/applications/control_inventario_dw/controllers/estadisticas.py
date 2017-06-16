def ProductosMasPedidos():

    response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
    response.headers['Content-Type']='image/svg+xml'

    import pygal
    import requests

    #aqui va la consulta
    count = db.producto.id.count()
    consulta = db((db.inventario.id == db.prestacion.id_inventario) &
               (db.producto.id == db.inventario.id_producto)).select(db.prestacion.id, db.inventario.id, db.producto.id, db.producto.nombre, count, groupby=db.producto.nombre, orderby=count)



    counts = []
    labels = []

    line_chart = pygal.Line(width=800, height=400, x_label_rotation=50)


    for i in consulta:
        labels.append(i.producto.nombre)
        counts.append(i._extra.get('COUNT(producto.id)'))


    line_chart.x_labels = labels
    line_chart.add('Prestaciones', counts)
    line_chart.title = "Productos prestados"




    return line_chart.render()

def estadisticas():



    ProductosMasPedidos = URL('estadisticas', 'ProductosMasPedidos')

    return dict(ProductosMasPedidos=ProductosMasPedidos)
