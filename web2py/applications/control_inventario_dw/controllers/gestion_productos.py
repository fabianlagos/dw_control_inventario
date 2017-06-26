def AgregarInventario(id_producto, n_serie, descripcion, id_user, imagen):

    from datetime import datetime

    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    nombre_producto = db(db.producto.id == id_producto).select(db.producto.nombre)[0].get('nombre')

    try:
        db.inventario.insert(id_producto=id_producto, n_serie=n_serie, descripcion=descripcion, imagen=imagen)

    except:
        db.logs_producto.insert(id_user=id_user,
                                username=auth.user.username,
                                id_producto=id_producto,
                                nombre_producto=nombre_producto,
                                fecha=fecha_actual,
                                descripcion="Error: No se pudo agregar el producto al inventario")

    db.logs_producto.insert(id_user=id_user,
                            username=auth.user.username,
                            id_producto=id_producto,
                            nombre_producto=nombre_producto,
                            fecha=fecha_actual,
                            descripcion="Se agrega producto al inventario")

    return "Producto agregado al inventario"

def CrearProducto(id_producto, id_user, estado):
    from datetime import datetime

    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    nombre_producto = db(db.producto.id == id_producto).select(db.producto.nombre)[0].get('nombre')

    if estado:
        db.logs_producto.insert(id_user=id_user,
                                username=auth.user.username,
                                id_producto=id_producto,
                                nombre_producto=nombre_producto,
                                fecha=fecha_actual,
                                descripcion="Producto creado")

        return "Producto creado"

    return "Error: No se pudo crear el producto"


def OnDelete(table, id_producto):
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    if (db(db.inventario.id_producto == id_producto).isempty()):
        nombre_producto = db(db.producto.id == id_producto).select(db.producto.nombre)[0].get('nombre')
        db.logs_producto.insert(id_user=auth.user.id,
                                username=auth.user.username,
                                id_producto=id_producto,
                                nombre_producto=nombre_producto,
                                fecha=fecha_actual,
                                descripcion="Producto eliminado")

    else:
        #session.flash = "ASDSADASD"
        raise NameError("Error")




def productos():
    #Esto es un SELECT * FROM db.producto
    consulta = (db.producto.id == db.categoria_producto.id_producto) & (db.categoria.id == db.categoria_producto.id_categoria)

    fields = [db.producto.nombre, db.producto.marca, db.producto.modelo, db.categoria.nombre]
    db.producto.id.readable = False

    headers = {'categoria.nombre': 'Categoria' }

    if auth.has_membership(group_id='admin'):
        links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.producto.id]), _class="btn btn-default glyphicon glyphicon-plus")]

        grid = SQLFORM.grid(consulta, create=False, headers=headers, fields=fields, csv=False, ondelete=OnDelete, links=links, details=auth.has_membership('admin'), editable=auth.has_membership('admin'), deletable=auth.has_membership('admin'))

    else:
        links = [lambda row: A(' agregar a inventario',_href=URL("agregarainventario",args=[row.producto.id]), _class="btn btn-default glyphicon glyphicon-plus")]

        grid = SQLFORM.grid(consulta, create=False, headers=headers, fields=fields, csv=False, ondelete=OnDelete, details=False, editable=False, deletable=False)

    return dict(grid=grid)


def agregarainventario():

    form = SQLFORM(db.inventario, fields=['n_serie', 'descripcion', 'imagen'])

    idproducto=request.args[0]
    nombre_producto = db(db.producto.id == idproducto).select(db.producto.nombre)[0].get('nombre')
    #cantidad=1
    if form.validate():
        #while cantidad>0:
        mensaje = AgregarInventario(idproducto, form.vars.n_serie, form.vars.descripcion, auth.user.id, form.vars.imagen)
            #db.inventario.insert(id_producto=idproducto, n_serie=form.vars.n_serie, descripcion=form.vars.descripcion)
        session.flash = mensaje
        #    cantidad=cantidad-1
        redirect(URL("gestion_inventario", "inventario"))
    return dict(form=form, nombre_producto=nombre_producto)

def crear_producto():

    categorias = []
    for row in db().select(db.categoria.ALL):
        categorias.append(row.nombre)
    #categorias = db().select(db.categoria.nombre)


    form = SQLFORM.factory(
        db.producto,
        Field('Categoria', requires=IS_IN_SET(categorias)) )
    if form.process().accepted:

        id_producto = db.producto.insert(**db.producto._filter_fields(form.vars))
        id_categoria = db(db.categoria.nombre == form.vars.Categoria).select(db.categoria.id)[0].get('id')
        db.categoria_producto.insert(id_producto=id_producto, id_categoria=id_categoria)
        mensaje = CrearProducto(id_producto, auth.user.id, True)
        session.flash = mensaje
        redirect(URL('productos'))



    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)
