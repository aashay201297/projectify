# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
## if NOT running on Google App Engine use SQLite or other DB
	db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
## connect to Google BigTable (optional 'google:datastore://namespace')
	db = DAL('google:datastore+ndb')
## store sessions and tickets there
	session.connect(request, response, db=db)
## or store session in Memcache, Redis, etc.
## from gluon.contrib.memdb import MEMDB
## from google.appengine.api.memcache import Client
## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
	response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
	response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
	response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()
db.define_table(auth.settings.table_user_name,
		Field('first_name', length=128, default=''),
		Field('last_name', length=128, default=''),
		Field('email', length=128, default='', unique=True), # required
		Field('password', 'password', length=512,            # required
			readable=False, label='Password'),
		Field('phone'),
		Field('Profile_pic','upload',requires=IS_IMAGE(extensions=('jpg','jpeg','png'))),
		Field('profession',requires=IS_IN_SET(['Student(Undergrad)','Professor','MS','PHD','others'])),
		Field('user_type',requires=IS_IN_SET(['Developer','Viewer'])),
		Field('registration_key', length=512,                # required
			writable=False, readable=False, default=''),
		Field('reset_password_key', length=512,              # required
			writable=False, readable=False, default=''),
		Field('registration_id', length=512,                 # required
			writable=False, readable=False, default=''),
		Field('uploads',default=0))
## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =   IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.email.requires = [
	IS_EMAIL(error_message=auth.messages.invalid_email),
	IS_NOT_IN_DB(db, custom_auth_table.email)]
auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)
## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')
## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(dbdb.define_table('project',

db.define_table('project',
		Field('project_title',type='string'),
		Field('time_of_upload','string',readable=False,writable=False),
		Field('folder','upload',autodelete=True),
		Field('author_name'),
		Field('project_manual',type='upload'),
		Field('description',type='text'),
		Field('likes','string',default='',readable=False,writable=False),
		Field('like_count',default=0,readable=False,writable=False),
		Field('category'),
		Field('type_of_project'),
                Field('downloads','integer',default=0,readable=False,writable=False),
		Field('rating',default=0,readable=False,writable=False,requires=IS_IN_SET(['1','2','3','4','5'])),
                Field('num',default=0,readable=False,writable=False),
			format = '%(project_title)s')
db.define_table('post1',
		Field('project_id','reference project'),
		Field('author'),
		Field('post','text'))
db.define_table('cat',
		Field('category'),
		format='%(category)s')	
db.define_table('subcat',
		Field('category',db.cat),
		Field('sub_category'),
			format=	'%(sub_category)s')	
db.define_table('d',
		Field('project_id'),
                Field('time_stamp'),
                Field('author'))	
if db(db.cat.id>0).count() == 0:
	db.cat.truncate()
	db.subcat.truncate()
	db.cat.insert(category='Texas')
	db.cat.insert(category='Illinois')
	db.cat.insert(category='California')
	db.subcat.insert(sub_category='Austin',category=1)
	db.subcat.insert(sub_category='Dallas',category=1)
	db.subcat.insert(sub_category='Chicago',category=2)
	db.subcat.insert(sub_category='Aurora',category=2)
	db.subcat.insert(sub_category='Los Angeles',category=3)
	db.subcat.insert(sub_category='San Diego',category=3)	 
db.define_table('conti',
                Field('contributor','reference auth_user'),
                Field('project_id'))
db.define_table('rate',
                Field('rater',readable=False,writable=False),
                Field('review','text'),
                Field('rating',requires=IS_IN_SET(['1','2','3','4','5'])),
                Field('project_id',readable=False,writable=False))
#db.define_table('post',
#		Field('project_id','reference project'),
#		Field('author'),
#		Field('body','text'))
db.conti.contributor.requires=IS_IN_DB(db,db.auth_user,'%(first_name)s')
db.post1.project_id.requires = IS_IN_DB(db, db.project.id, '%(project_title)s')
db.post1.author.requires = IS_NOT_EMPTY()
db.post1.project_id.writable = db.post1.project_id.readable = False
db.project.category.writable = db.project.category.readable = False
#db.project.folder.requires = IS_NOT_EMPTY()
db.project.project_title.requires = IS_NOT_EMPTY()
db.project.description.requires = IS_NOT_EMPTY()
#db.project.project_manual.requires = IS_NOT_EMPTY()
db.post1.author.requires = IS_NOT_EMPTY()
db.project.type_of_project.requires=IS_IN_SET(['private','psuedo-private','public'])



"""class CascadingSelect(object):
	def __init__(self, *tables):
		self.tables = tables 
		self.prompt = lambda table:str(table)   
	def widget(self,f,v):
		import uuid
		uid = str(uuid.uuid4())[:8]
	d_id = "cascade-" + uid
	wrapper = TABLE(_id=d_id)
	parent = None; parent_format = None; 
	fn =  '' 
	vr = 'var dd%s = [];var oi%s = [];\n' % (uid,uid)
	prompt = [self.prompt(table) for table in self.tables]
	vr += 'var pr%s = ["' % uid + '","'.join([str(p) for p in prompt]) + '"];\n' 
	f_inp = SQLFORM.widgets.string.widget(f,v)
	f_id = f_inp['_id']
	f_inp['_type'] = "hidden"
        for tc, table in enumerate(self.tables):             
		db = table._db     
		format = table._format            
		options = db(table['id']>0).select()
		id = str(table) + '_' + format[2:-2]             
		opts = [OPTION(format % opt,_value=opt.id,
				_parent=opt[str(parent)] if parent else '0') \
				for opt in options]
	opts.insert(0, OPTION(prompt[tc],_value=0))
	inp = SELECT(opts ,_parent=str(parent) + \
			 "_" + str(parent_format),
			 _id=id,_name=id,
			 _disabled="disabled" if parent else None)
	wrapper.append(TR(inp))
	next = str(tc + 1)
	vr += 'var p%s = jQuery("#%s #%s"); dd%s.push(p%s);\n' % (tc,d_id,id,uid,tc)            
	vr += 'var i%s = jQuery("option",p%s).clone(); oi%s.push(i%s);\n' % (tc,tc,uid,tc)
	fn_in = 'for (i=%s;i<%s;i+=1){dd%s[i].find("option").remove();'\
		'dd%s[i].append(\'<option value="0">\' + pr%s[i] + \'</option>\');'\
		'dd%s[i].attr("disabled","disabled");}\n' % \
			 (next,len(self.tables),uid,uid,uid,uid)
	fn_in +='oi%s[%s].each(function(i){'
	'if (jQuery(this).attr("parent") == dd%s[%s].val()){'\
		'dd%s[%s].append(this);}});' % (uid,next,uid,tc,uid,next)            
	fn_in += 'dd%s[%s].removeAttr("disabled");\n' % (uid,next)
	fn_in += 'jQuery("#%s").val("");' % f_id
	if (tc < len(self.tables)-1):		
		fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in) 
	else:
		fn_in = 'jQuery("#%s").val(jQuery(this).val());' % f_id
		fn += 'dd%s[%s].change(function(){%s});\n' % (uid,tc,fn_in)
		if v:
			 fn += 'dd%s[%s].val(%s);' % (uid,tc,v)                       
	parent = table
	parent_format = format[2:-2]

	wrapper.append(f_inp)
	wrapper.append(SCRIPT(vr,fn))
	return wrapper"""
