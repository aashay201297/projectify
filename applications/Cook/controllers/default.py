# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

@auth.requires_membership('Admins')
def manage():
	grid=SQLFORM.grid(db.recipes,paginate=10)
	return locals()

def find():
	 form=FORM(INPUT(_type="number",_name="min",_placeholder="Minimum ID",requires=IS_NOT_EMPTY()),
		INPUT(_type="number",_name="max",_placeholder="Maximum ID",requires=IS_NOT_EMPTY()),
		INPUT(_type="string",_name="fi",requires=[IS_IN_SET(['Veg','Non-veg','only Egg'],error_message='invalid dish type'),IS_NOT_EMPTY()],_placeholder="Dish type"),
		INPUT(_type="number",_name="la",_placeholder="Minimum likes",requires=IS_NOT_EMPTY()),
		INPUT(_type="submit",_value="Search"),    
		_id="search-form")
	 ans=0
	 if form.process().accepted:
		 response.flash="Required search is applied"
	 elif form.errors:
		 response.flash="Please fill the form COMPLETELY"
	 else:
		 response.flash="Fill this form completely to search"
	 if len(request.vars) != 0:
	        l=request.vars["min"]
	 	r=request.vars["max"]
                arr=request.vars["fi"]
		arr2=request.vars["la"]
		ans=db(((db.recipes.id>=l) & (len(l))) & ((db.recipes.id<=r) & (len(r))) & ((db.recipes.veg_or_not==arr) & (len(arr))) & ((db.recipes.likes>=arr2) & (len(arr2)))).select()
         return locals()


@auth.requires_login()
def index():
    if len(request.args): page=int(request.args[0])
    else: page=0
    recent_cooks=5
    limitby=(page*recent_cooks,(page+1)*recent_cooks+1)
    rows=db().select(db.recipes.ALL, limitby=limitby, orderby=~db.recipes.Time_of_upload)
    return dict(rows=rows,page=page,recent_cooks=recent_cooks)

import datetime
now=datetime.datetime.now()

@auth.requires_login()
def upload():
        db.recipes.Author.writable=False
        db.recipes.Author.readable=False
        db.recipes.Time_of_upload.writable=False
        db.recipes.Time_of_upload.readable=False
	'''
	fields=[field for field in db.recipes]
	fields+=[
	Field('reeegee1','string',label=T('extra_field_1')),
	Field('ere2','string',label=T('extra_field_2'))
	]
	form1=SQLFORM.factory(
	*fields,
	formstyle='bootstrap',
	_class='random form-horizontal',
	table_name='random'
	)
	 '''
	form1=SQLFORM(db.recipes)
        if form1.process().accepted:
                cur=form1.vars.id
                row = db(db.recipes.id==cur).select().first()
                row.update_record(Author=auth.user.id)
                row.update_record(Time_of_upload=now)
                response.flash = "Another delicious dish added"
        elif form1.errors:
                response.flash = " Form has Errors"
        else:
                response.flash = "Please fill the form"
        return dict(form1=form1)

@auth.requires_login()
def edit():
        update= int(request.args[0])
        db.recipes.Author.writable=False
        db.recipes.Author.readable=False
        db.recipes.Time_of_upload.writable=False
        db.recipes.Time_of_upload.readable=False
        db.recipes.id.readable=False
        db.recipes.id.writable=False
	form = SQLFORM(db.recipes, update)

# form = SQLFORM(db.recipes, update)
        if form.process().accepted:
                response.flash = "1 record inserted"
        elif form.errors:
                response.flash = "Errors"
        else:
                response.flash = "Please fill the form"
        return dict(form=form)
    
def user():
   return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
@auth.requires_login()
def show():
	rec = db.recipes(request.args(0,cast=int))
	i=request.args(0,cast=int)
	recid=request.args(0,cast=int) or redirect(URL('index'))
	like_str=str(db(db.recipes.id==request.args[0]).select(db.recipes.likes))
	vot=(like_str.split())
	votes=len(vot)
	print "no. of votes are",vot
	if votes==1 or (vot[1]=='""' and votes>=2):
		votes=1
		print "done"
	form=FORM(BUTTON('LIKE / UNLIKE',_type='submit'),
		_action=URL('default','like',args=recid))
	temp=db.recipes(request.args(0,cast=int))
	db.post.dish_id.default=temp.id
	form5 = SQLFORM(db.post)
	if form5.process().accepted:
		response.flash='Comment posted successfully!'
	tem= db(db.post.dish_id==temp.id).select()
	return dict(i=i,rec=rec,recid=recid,tem=tem,form5=form5,votes=votes,form=form)

'''	db.post.image_id.default =rec.id
	db.post.image_id.writeble=False
	db.post.image_id.readable=False
	form2 = SQLFORM(db.post)
	if form2.process().accepted:
		p=form2.vars.id
		q=str(db(db.auth_user.id==auth.user.id).select(db.auth_user.first_name))
		r=q.split()
		row=db(db.post.id==p).select().first()
		row.update_record(commentor=r[1])
	        response.flash = 'your comment is posted'
	comments = db(db.post.image_id==rec.id).select()
	'''
@auth.requires_login()
def show2():
	rec = db.recipes(request.args(0,cast=int))
	i=request.args(0,cast=int)
	recid=request.args(0,cast=int) or redirect(URL('index'))
	like_str=str(db(db.recipes.id==request.args[0]).select(db.recipes.likes))
	vot=(like_str.split())
	votes=len(vot)
	print "no. of votes are",vot
	if votes==1 or (vot[1]=='""' and votes>=2):
		votes=1
		print "done"
	form=FORM(BUTTON('LIKE / UNLIKE',_type='submit'),
		_action=URL('default','like2',args=recid))
	return dict(recid=recid,rec=rec,votes=votes,form=form)
def like():
	from re import match
	recid=request.args[0]
	like_str=str(db(db.recipes.id==request.args[0]).select(db.recipes.likes))
	like_list = [x for x in like_str.split() if match('^[0-9]*$',x)]
	if str(auth.user.id) not in like_list:
		like_list.append(str(auth.user.id))
		db(db.recipes.id==request.args[0]).update(likes=(' ').join(like_list))
	else:
		like_list.remove(str(auth.user.id))
		db(db.recipes.id==request.args[0]).update(likes=(' ').join(like_list))
	return dict(like_list=like_list,recid=recid)
def like2():
	from re import match
	recid=request.args[0]
	like_str=str(db(db.recipes.id==request.args[0]).select(db.recipes.likes))
	like_list = [x for x in like_str.split() if match('^[0-9]*$',x)]
	if str(auth.user.id) not in like_list:
		like_list.append(str(auth.user.id))
		db(db.recipes.id==request.args[0]).update(likes=(' ').join(like_list))
	else:
		like_list.remove(str(auth.user.id))
		db(db.recipes.id==request.args[0]).update(likes=(' ').join(like_list))
	return dict(like_list=like_list,recid=recid)
def user_recipe():
    if len(request.args): page=int(request.args[0])
    else: page=0
    recent_cooks=5
    limitby=(page*recent_cooks,(page+1)*recent_cooks+1)
#for chronoogical order: year 2015 will come before 2016
    rows=db(db.recipes.Author==auth.user.id).select(db.recipes.ALL, limitby=limitby, orderby=db.recipes.Time_of_upload)
    return dict(rows=rows,page=page,recent_cooks=recent_cooks)
