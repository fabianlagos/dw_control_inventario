
def lista_usuarios():


    query = ((db.auth_membership.group_id == auth.id_group('user_basic')) & (db.auth_user.id == db.auth_membership.user_id) & (db.auth_group.id == db.auth_membership.group_id))
    fields = [db.auth_user.first_name, db.auth_user.last_name, db.auth_user.username, db.auth_user.email, db.auth_group.role ]
    grid = SQLFORM.grid(query, create=False, details=False, csv=False, fields=fields)

    #grid = SQLFORM.grid(query, create=False, details=False)

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
