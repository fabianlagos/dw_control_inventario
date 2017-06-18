def registros_inventario():
    consulta = db.logs_inventario
    fields = [db.logs_inventario.username, db.logs_inventario.nombre_producto, db.logs_inventario.fecha, db.logs_inventario.descripcion]
    maxtextlength = {'logs_inventario.descripcion' : 50}
    grid = SQLFORM.grid(consulta, orderby=~db.logs_inventario.fecha, fields=fields, create=False, editable=False, deletable=False, details=False, maxtextlength=maxtextlength)
    return dict(grid=grid)

def registros_productos():
    consulta = db.logs_producto
    fields = [db.logs_producto.username, db.logs_producto.nombre_producto, db.logs_producto.fecha, db.logs_producto.descripcion]
    maxtextlength = {'logs_producto.descripcion' : 50}
    grid = SQLFORM.grid(consulta, orderby=~db.logs_producto.fecha, fields=fields, create=False, editable=False, deletable=False, details=False, maxtextlength=maxtextlength)
    return dict(grid=grid)
