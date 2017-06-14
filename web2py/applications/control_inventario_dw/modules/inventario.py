from gluon import *

def PrestarInventario(id_producto_solicitado, id_user):
    from datetime import datetime
    #Cambiar el estado a no disponible del producto en el inventario
    db(db.inventario.id == id_producto_solicitado).update(disponible = False)
    #Insertar la transaccion en prestaciones(registro)
    db.prestaciones.insert( id_user = id_user,
                            id_inventario = id_producto_solicitado,
                            fecha_prestacion = datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    print "Prestacion valida"
