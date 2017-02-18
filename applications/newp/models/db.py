# -*- coding: utf-8 -*-


from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)

response.generic_patterns = ['*'] if request.is_local else []
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

db.define_table(
		auth.settings.table_user_name,
		Field('first_name', length=128, default=''),
		Field('last_name', length=128, default=''),
		Field('username',length=128, unique=True),
		Field('email', length=128, default='', unique=True), # required
		Field('password', 'password', length=512,            # required
			readable=False, label='Password'),
		Field('phone'),
		Field('profile_picture','upload'),
		Field('registration_key', length=512,                # required
			 writable=False, readable=False, default=''),
		Field('reset_password_key', length=512,              # required
		     writable=False, readable=False, default=''),
		Field('registration_id', length=512,                 # required
			 writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.username.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=8, special=1, upper=1), CRYPT()]
custom_auth_table.email.requires = [
IS_EMAIL(error_message=auth.messages.invalid_email),
IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.define_tables(username=True, signature=False)
auth.settings.table_user=custom_auth_table

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True



"""
db=DAL("sqlite://storage.sqlite")

from gluon.tools import Auth
auth = Auth(db)
auth.define_tables(username=True)
"""


db.define_table('image',
    Field('title', 'string',length=255,required=True,unique=True),
    Field('author_id', 'reference auth_user'),
    Field('upload_date'),
    Field('description','text'),
    Field('image', 'upload'),
    Field('like1','integer',default=0),
    Field('like2','integer',default=0),
    Field('like3','integer',default=0),
    Field('like4','integer',default=0),
    Field('like5','integer',default=0),
    Field('total','integer',default=0),
    Field('taglist','list:integer',default=[]),
    format = '%(id)s'
    #number of comments also
)

db.image.image.requires=[IS_IMAGE(extensions=('jpeg','png','gif'))]
db.image.description.requires = IS_NOT_EMPTY(error_message='Add a brief description')
db.image.author_id.requires=IS_IN_DB(db, db.auth_user, '%(title)s')
db.image.like1.writable=db.image.like1.readable=False
db.image.like2.writable=db.image.like2.readable=False
db.image.like3.writable=db.image.like3.readable=False
db.image.like4.writable=db.image.like4.readable=False
db.image.like5.writable=db.image.like5.readable=False
db.image.total.writable=db.image.total.readable=False
db.image.taglist.writable=db.image.taglist.readable=False

db.image.author_id.writable=db.image.author_id.readable=False
db.image.upload_date.writable=db.image.upload_date.readable=False
db.image.id.writable=db.image.id.readable=False

db.define_table('post',
    Field('image_id', 'reference image'),
    Field('author_id', 'reference auth_user'),
    Field('body', 'text')
)

db.post.author_id.writable=db.post.author_id.readable=False
db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.post.image_id.writable=db.post.image_id.readable=False
db.post.author_id.requires=IS_IN_DB(db, db.auth_user, '%(title)s')
db.post.body.requires=IS_NOT_EMPTY(error_message='Please type comment')

db.define_table('likes',
    Field('imageid', 'reference image'),
    Field('score','integer'),
    auth.signature
)

db.define_table('tags',
    Field('name','text'),
    Field('imglist','list:integer',default=[]),
    auth.signature
)
db.tags.imglist.writable=db.tags.imglist.readable=False
