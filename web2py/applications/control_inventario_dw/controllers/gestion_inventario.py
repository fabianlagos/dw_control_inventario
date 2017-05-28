def inventario():

    estado = (db.inventario.disponible == True)

    links = [lambda row: A('Solicitar',_href=URL("default","inventario",args=[row.id]), _class='button')]

    grid = SQLFORM.grid(estado, links=links, csv=False)


    return dict(grid=grid)

#Esta funcion la pueden ver el Administrador y Supervisor
def productos_prestados():

    prestado = (db.inventario.disponible != True)

    grid = SQLFORM.grid(prestado, csv=False)

    return dict(grid=grid)
