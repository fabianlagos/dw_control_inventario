def registros_inventario():
    consulta = (db.logs_inventario.id_inventario == db.inventario.id) & (db.inventario.id_producto == db.producto.id)
    fields = [db.logs_inventario.id_user, db.producto.nombre, db.logs_inventario.fecha, db.logs_inventario.descripcion]
    grid = SQLFORM.grid(db.logs_inventario, fields=fields, create=False, editable=False, deletable=False, details=False)
    return dict(grid=grid)

def registros_productos():

    return dict()
