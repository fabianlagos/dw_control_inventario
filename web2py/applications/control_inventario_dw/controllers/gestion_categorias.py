def categorias():
    consulta = db.categoria
    fields = [db.categoria.nombre, db.categoria.descripcion]
    links = [lambda row: A(' Productos asociados',_href=URL("categoria_productos", vars={'id': row.id}), _class="btn btn-default" )]
    grid = SQLFORM.grid(consulta, details=False, csv=False, fields=fields, links=links)

    return dict(grid=grid)

def categoria_productos():
    id_categoria = request.vars['id']
    nombre_categoria = db(db.categoria.id == id_categoria).select(db.categoria.nombre)[0].get('nombre')
    consulta = (db.categoria_producto.id_categoria == id_categoria) & (db.categoria_producto.id_producto == db.producto.id)
    fields = [db.producto.nombre, db.producto.modelo, db.producto.marca]

    grid = SQLFORM.grid(consulta, fields=fields, create=False, editable=False, deletable=False, details=False, csv=False)

    return dict(grid=grid, nombre_categoria=nombre_categoria)
