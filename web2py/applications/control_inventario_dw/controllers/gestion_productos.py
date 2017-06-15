def productos():
    #Esto es un SELECT * FROM db.producto
    consulta = db.producto

    grid = SQLFORM.grid(consulta, csv=False, links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.id]), _class="btn btn-default glyphicon glyphicon-plus")])

    return dict(grid=grid)


def agregarainventario():

    form1 = SQLFORM(db.inventario, db.categoria, fields=['n_serie', 'descripcion', 'disponible'])
    form2 = SQLFORM(db.categoria, fields=['nombre'])
    idproducto=request.args[0]
    cantidad=1
    if form1.validate():
        while cantidad>0:
            #db.inventario.insert(id_producto='idproducto',n_serie="f", descripcion="x", disponible= "true")
            db.inventario.insert(id_producto=idproducto, n_serie=form.vars.n_serie, descripcion=form.vars.descripcion, disponible=form.vars.disponible)
                     #**db.inventario._filter_fields(form.vars))
            #db.inventario.insert(id_producto=idproducto,**(form.vars))
            cantidad=cantidad-1
        redirect(URL("gestion_inventario", "inventario"))
    return dict(form1=form1, form2=form2)

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
        response.flash = 'form accepted'
        session.your_name = form.vars.your_name
        session.your_image = form.vars.your_image
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
