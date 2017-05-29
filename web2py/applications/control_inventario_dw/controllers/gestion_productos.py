def productos():
    #Esto es un SELECT * FROM db.producto
    consulta = db.producto

    grid = SQLFORM.grid(consulta, csv=False, links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.id]), _class="btn btn-info glyphicon glyphicon-signal")])

    return dict(grid=grid)


def agregarainventario():
    form = SQLFORM(db.inventario, fields=['n_serie', 'descripcion', 'disponible'])
    idproducto=request.args[0]
    cantidad=1
    if form.validate():
        while cantidad>0:
            #db.inventario.insert(id_producto='idproducto',n_serie="f", descripcion="x", disponible= "true")
            db.inventario.insert(id_producto=idproducto, n_serie=form.vars.n_serie, descripcion=form.vars.descripcion, disponible=form.vars.disponible)
                     #**db.inventario._filter_fields(form.vars))
            #db.inventario.insert(id_producto=idproducto,**(form.vars))
            cantidad=cantidad-1
        redirect(URL("default", "inventario"))
    return dict(form=form)
