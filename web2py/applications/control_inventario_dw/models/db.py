# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('mysql://inventario:inventario@localhost/db_inventario', db_codec='UTF-8')
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=True, signature=False)
auth.settings.create_user_groups = None
auth.settings.everybody_group_id = 3

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled.append('register')

#Falta el required en los atributos por definir

db.define_table('producto',
                Field('nombre', 'string'),
                Field('marca', 'string'),
                Field('modelo', 'string'))

db.define_table('inventario',
                Field('id_producto', db.producto),
                Field('n_serie', 'string'),
                Field('descripcion', 'string'),
                Field('disponible', 'boolean', default=True),
                Field('imagen', 'upload'))

db.define_table('categoria',
                Field('nombre', 'string'),
                Field('descripcion', 'string'))

db.define_table('categoria_producto',
                Field('id_producto', db.producto, unique=True),
                Field('id_categoria', db.categoria))

db.define_table('prestacion',
                Field('id_user', db.auth_user),
                Field('id_inventario', db.inventario),
                Field('fecha_prestacion', 'datetime'),
                Field('fecha_devolucion', 'datetime'),
                Field('devolucion_pendiente', 'boolean', default=False)) #Prestado pero aun sin aprobacion

db.define_table('logs_inventario',
                Field('id_user'),
                Field('username'),
                Field('id_inventario'),
                Field('nombre_producto', 'string'),
                Field('fecha', 'datetime'),
                Field('descripcion'))

db.define_table('logs_producto',
                Field('id_user'),
                Field('username' , 'string'),
                Field('id_producto'),
                Field('nombre_producto', 'string'),
                Field('fecha', 'datetime'),
                Field('descripcion'))

db.define_table('recomendacion',
                Field('id_user'),
                Field('username'),
                Field('titulo', 'string'),
                Field('mensaje', 'text'),
                Field('fecha', 'datetime'),
                Field('activa', 'boolean', default=True))

if (db(db.auth_group).isempty()):
    auth.add_group('admin', 'admin')
    auth.add_group('supervisor', 'supervisor')
    auth.add_group('user_basic', 'user_basic')


#Revisar esto
if not db().select(db.auth_user.ALL).first():
    id_user = db.auth_user.insert(
        username = 'admin',
        password = db.auth_user.password.validate('admin')[0],
        email = 'null@null.com',
        first_name = 'admin',
        last_name = 'Administrator',
    )
    auth.del_membership(auth.id_group('user_basic'), id_user)
    auth.add_membership(auth.id_group('admin'), id_user)

    id_user = db.auth_user.insert(
        username = 'supervisor',
        password = db.auth_user.password.validate('supervisor')[0],
        email = 'null@null.com',
        first_name = 'supervior',
        last_name = 'Supervisor',
    )
    auth.del_membership(auth.id_group('user_basic'), id_user)
    auth.add_membership(auth.id_group('supervisor'), id_user)
