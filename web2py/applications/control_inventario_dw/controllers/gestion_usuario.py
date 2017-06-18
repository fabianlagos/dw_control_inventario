
def lista_usuarios():

    query = ((db.auth_membership.group_id >= auth.id_group('supervisor')) & (db.auth_user.id == db.auth_membership.user_id) & (db.auth_group.id == db.auth_membership.group_id))
    fields = [db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_user.email, db.auth_group.role]
    db.auth_user.id.writable = False
    links = [lambda row: A(' Cambiar Privilegio', _href=URL('gestion_usuario', 'cambiar_privilegios', vars={ 'id' : row.auth_user.id }), _class='btn btn-default glyphicon glyphicon-eye-open')]
    grid = SQLFORM.grid(query, create=False, details=False, csv=False, fields=fields, links=links)

    #grid = SQLFORM.grid(query, create=False, details=False)
    #links = [lambda row: A(' Change status', callback=URL("default","change_status", vars={'id': row.id, 'id_zone': request.vars['id_zone']}), target='callback_listrecords',_class="btn btn-danger glyphicon glyphicon-edit")]
    return dict(grid=grid)

def crear_usuario():

    form = SQLFORM(db.auth_user, showid=True)

    if form.process().accepted:
       auth.add_membership(auth.id_group('user_basic'), form.vars.id)
       response.flash = 'form accepted'
       redirect(URL('gestion_usuario','lista_usuarios'))
    elif form.errors:
       response.flash = 'form has errors'

    return dict(form=form)

def cambiar_privilegios():

    s = auth.has_membership(auth.id_group('supervisor'), request.vars['id'])

    username = db(db.auth_user.id == request.vars['id']).select(db.auth_user.username)[0].get('username')

    form = SQLFORM.factory(Field('Supervisor', 'boolean', default=s) )

    if form.process().accepted:

        if form.vars.Supervisor:
            auth.del_membership(auth.id_group('user_basic'), request.vars['id'])
            auth.add_membership(auth.id_group('supervisor'), request.vars['id'])
        else:
            auth.add_membership(auth.id_group('user_basic'), request.vars['id'])
            auth.del_membership(auth.id_group('supervisor'), request.vars['id'])
            
        response.flash = "Los privilegios han sido cambiado con exito"
        redirect(URL('lista_usuarios'))



    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form, username=username)

    """

    if auth.has_membership(auth.id_group('user_basic'), request.vars['id']):
        auth.del_membership(auth.id_group('user_basic'), request.vars['id'])
        auth.add_membership(auth.id_group('supervisor'), request.vars['id'])
    else:
        auth.add_membership(auth.id_group('user_basic'), request.vars['id'])
        auth.del_membership(auth.id_group('supervisor'), request.vars['id'])


    query = ((db.auth_membership.group_id >= auth.id_group('supervisor')) & (db.auth_user.id == db.auth_membership.user_id) & (db.auth_group.id == db.auth_membership.group_id))
    fields = [db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_user.email, db.auth_group.role]
    db.auth_user.id.writable = False
    links = [lambda row: A(' Cambiar Privilegio', callback=URL('gestion_usuario', 'cambiar_privilegios', vars={ 'id' : row.auth_user.id }), target='callback-lista_usuarios', _class='btn btn-default glyphicon glyphicon-eye-open',_onclick="return confirm('Estas seguro que desea cambiar privilegios?');")]

    grid = SQLFORM.grid(query, create=False, details=False, csv=False, fields=fields, links=links)
    """
