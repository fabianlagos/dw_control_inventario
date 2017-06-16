def productos():
    #Esto es un SELECT * FROM db.producto
    consulta = db.producto

    db.producto.id.readable = False

    grid = SQLFORM.grid(consulta, create=False, csv=False, links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.id]), _class="btn btn-default glyphicon glyphicon-plus")])

    return dict(grid=grid)


def agregarainventario():

    form = SQLFORM(db.inventario, fields=['n_serie', 'descripcion'])

    idproducto=request.args[0]
    nombre_producto = db(db.producto.id == idproducto).select(db.producto.nombre)[0].get('nombre')
    cantidad=1
    if form.validate():
        while cantidad>0:
            #db.inventario.insert(id_producto='idproducto',n_serie="f", descripcion="x", disponible= "true")
            db.inventario.insert(id_producto=idproducto, n_serie=form.vars.n_serie, descripcion=form.vars.descripcion)
                     #**db.inventario._filter_fields(form.vars))
            #db.inventario.insert(id_producto=idproducto,**(form.vars))
            cantidad=cantidad-1
        redirect(URL("gestion_inventario", "inventario"))
    return dict(form=form, nombre_producto=nombre_producto)

def crear_producto():

    categorias = []
    for row in db().select(db.categoria.ALL):
        categorias.append(row.nombre)
    #categorias = db().select(db.categoria.nombre)

    print categorias

    form = SQLFORM.factory(
        db.producto,
        Field('Categoria', requires=IS_IN_SET(categorias)) )
    if form.process().accepted:
        id_producto = db.producto.insert(**db.producto._filter_fields(form.vars))
        id_categoria = db(db.categoria.nombre == form.vars.Categoria).select(db.categoria.id)[0].get('id')
        db.categoria_producto.insert(id_producto=id_producto, id_categoria=id_categoria)
        redirect(URL('productos'))

        response.flash = "Producto agregado correctamente"

    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
