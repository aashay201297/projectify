# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application

## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    rows2=db().select(db.project.ALL, orderby=~db.project.downloads)
    rows1=db().select(db.d.ALL, orderby=db.d.time_stamp)
    rows=db().select(db.project.ALL, orderby=~db.project.rating)
    response.flash = T("Welcome to Projectify!")
    return dict(message=T('Welcome to web2py!'),rows1=rows1,rows2=rows2,rows=rows)
def sort():
	ans=[];
	return dict()
def sortbydow():
	rows1=db().select(db.project.ALL, orderby=~db.project.downloads)
	return dict(rows1=rows1)
def sortbycon():
	rows1=db().select(db.auth_user.ALL, orderby=~db.auth_user.uploads)
	return dict(rows1=rows1)
def sortbyadd():
    	rows1=db().select(db.project.ALL, orderby=db.project.time_of_upload)
	return dict(rows1=rows1)
def sortbyrat():
    	rows1=db().select(db.project.ALL, orderby=~db.project.rating)
	return dict(rows1=rows1)


auth.requires_login()
def allprofiles():
	users=db().select(db.auth_user.ALL)
	return dict(users=users)
def profile():
        rec = db.auth_user(request.args(0,cast=int))
        i=request.args(0,cast=int)
        recid=request.args(0,cast=int) or redirect(URL('allprofiles'))
        pubpro=db(db.project.author_name==rec.id).select()
        return dict(i=i,rec=rec,recid=recid,pubpro=pubpro)


@auth.requires_login()
def upload():
	x=auth.user.id
	y=db(db.auth_user.id==x).select().first()
	z=y.user_type
	if z=='Developer':
		import datetime
		now=datetime.datetime.now()
		db.project.author_name.readable=db.project.author_name.writable= False
		upform=SQLFORM(db.project)
#	form1=SQLFORM(db.cat)
		#form2=SQLFORM(db.subcat)
		if upform.process().accepted:
			cur=upform.vars.id
			row = db(db.project.id==cur).select().first()
        		row.update_record(author_name=auth.user.id)
        		row.update_record(time_of_upload=now)
			us=db(db.auth_user.id==auth.user.id).select().first()
			up=int(us.uploads)
			us.update_record(uploads=up)
        		db.conti.insert(contributor=auth.user.id,project_id=cur)
        		response.flash = "1 record inserted"
        		redirect(URL('category()',args=cur))
 	   	elif upform.errors:
        		response.flash = "Errors"
		else:
        		response.flash = "Please fill the form"
	else:
		redirect(URL('needd'))
	return dict(upform=upform)
def needd():
	return locals()

@auth.requires_login()
def category():
	form=SQLFORM(db.subcat)
	cur=request.args[1]
	print 'cur=',cur[1]
	if form.process().accepted:
		curcat=int(form.vars.id)
		catrow=db(db.subcat.id==curcat).select().first()
		row= db(db.project.id==cur).select().first()
                x=db(db.cat.id==catrow.category).select().first()
                print 'row=',row
                row.update_record(category=x.category)
		#print "catrow=",catrow.category
		#row.update_record(category=catrow.category)
		#print row
		response.flash = "categorised"
		redirect(URL('projects'))
	elif form.errors:
		response.flash="Errors"
	else:
		response.flash="Please fill the form"
	return dict(form=form)
@auth.requires_login()
def projects():
	if len(request.args):
		print "if"
		page=int(request.args[0])
	else: 
		page=0
	items_per_page=5
	limitby=(page*items_per_page,(page+1)*items_per_page+1)
	rows=db().select(db.project.ALL, limitby=limitby, orderby=~db.project.time_of_upload)
	return dict(rows=rows,page=page,items_per_page=items_per_page)
    
@auth.requires_login()
def show():
	rec = db.project(request.args(0,cast=int))
        i=request.args(0,cast=int)
        recid=request.args(0,cast=int) or redirect(URL('projects'))
        cons=db(db.conti.project_id==recid).select()
        x=0
        for con in cons:
                if auth.user.id==con.contributor:
                        x=1
                        break
        if x==1 or rec.type_of_project=='public':
                cos=db(db.conti.project_id==recid).select()
                con_list=[] 
                for con in cos:
                    c=int(con.contributor)
                    print c
                    if c not in con_list:
                        con_list.append(int(c))
                        print "pepepe",c
                like_str=str(db(db.project.id==request.args[0]).select(db.project.likes))
                vot=(like_str.split())
                votes=len(vot)
#row = db(db.project.id==request.args[0]).select().first()
#	row.update_record(like_count=votes-1)
                if vot[1]=='""':
                    votes=1
                form = FORM(BUTTON('Like / Unlike',_type='submit'),
                            _action=URL('default','like',args=recid))
                db.post1.project_id.default=rec.id
                db.post1.project_id.writable=db.post1.project_id.readable=False
                db.post1.author.writable=db.post1.author.readable=False
                form1=SQLFORM(db.post1)
                if form1.process().accepted:
                        cur=form1.vars.id
                        q=str(db(db.auth_user.id==auth.user.id).select(db.auth_user.first_name))
                        a=q.split()
                        row = db(db.post1.id==cur).select().first()
                        row.update_record(author=a[1])
                        response.flash = 'your comment is posted'
                comments = db(db.post1.project_id==rec.id).select()
                return dict(rec=rec,recid=recid,form=form, votes=votes,comments=comments,form1=form1,x=1,con_list=con_list)
        else:
                return dict(rec=rec,recid=recid, x=0)
def rating():
        i=int(request.args[0])
        r=str(db(db.rate.project_id==i).select(db.rate.rater))
        r=r.split()
        del r[0]
        print r
        x=0
        for o in r:
                print "o=",o,"r=",r
                if int(o)==int(auth.user.id):
                        print "yes"
                        x=1
        form=SQLFORM(db.rate)
        if form.process().accepted:
                response.flash = "1 record inserted"
                cur=form.vars.id
                row=db(db.rate.id==cur).select().first()
                row.update_record(rater=auth.user.id)
                row.update_record(project_id=i)
                pro_row=db(db.project.id==i).select().first()
                r=float(pro_row.rating)
                n=float(pro_row.num)
                print r,n
                r=r*n+float(row.rating)
                n=n+1
                r=float(r)/float(n)
                pro_row.update_record(rating=r)
                pro_row.update_record(num=n)
                redirect(URL('show',args=i))
        elif form.errors:
                response.flash = "Errors"
        else:
                response.flash = "Please fill the form"
        return dict(form=form,x=x)
def edit():
    	update=int(request.args[0])
    	db.project.author_name.writable=False;
    	db.project.author_name.readable=False;
    	db.project.id.writable=False;
    	db.project.id.readable=False;
    	db.project.type_of_project.writable=False;
    	db.project.type_of_project.readable=False;
    	form=SQLFORM(db.project,update)
	if form.process().accepted:
                response.flash = "1 record inserted"
        	redirect(URL('category()',args=update))
		
        elif form.errors:
                response.flash = "Errors"
        else:
                response.flash = "Please fill the form"
        return dict(form=form)
def likes():
	var = db().select(db.project.ALL, orderby=db.project.project_title)
	return dict(var=var)
def add_contributor():
        db.conti.project_id.writable=db.conti.project_id.readable=False
        addform=SQLFORM(db.conti)
        recid=request.args[0]
        if addform.process().accepted:
                cur=addform.vars.id
                row = db(db.conti.id==cur).select().first()
                row.update_record(project_id=recid)
                response.flash=T('contributor added')
                redirect(URL('show',args=recid))
                response.flash("a contributor added successfully")
        return dict(addform=addform)
        #return dict(rec=rec,recid=recid,)



@auth.requires_login()
def like():
	from re import match
	recid=request.args[0]
	like_str=str(db(db.project.id==request.args[0]).select(db.project.likes))
	row = db(db.project.id==request.args[0]).select().first()
	likes=int(row.like_count)
	like_list=[x for x in like_str.split() if match('^[0-9]*$',x)]
	if str(auth.user.id) not in like_list:
		like_list.append(str(auth.user.id))
		db(db.project.id==request.args[0]).update(likes=(' ').join(like_list))
#row = db(db.project.id==request.args[0]).select().first()
		row.update_record(like_count=likes+1)
	else:
	        like_list.remove(str(auth.user.id))
	        db(db.project.id==request.args[0]).update(likes=(' ').join(like_list))
#likes=int(row.like_count)
#likes=likes-1
#print "likes=",likes-1,request.args[0]
		row.update_record(like_count=likes-1)
	return dict(l=like_list,recid=recid)
@auth.requires_login()
def myprofile():
#        rec = db.auth_user(request.args(0,cast=int))
#	print rec
#        i=request.args(0,cast=int)
#        recid=request.args(0,cast=int) or redirect(URL('allprofiles'))
#	pubpro=db(db.project.author_name==auth.user.id).select()
	redirect(URL('profile',args=auth.user.id))
	return dict(pubpro=pubpro)
@auth.requires_login()
def searchbytitle():
	form=FORM(INPUT(_type="string",_name="title",_placeholder="a piece of string in title",requires=IS_NOT_EMPTY()))
	ans=[];
	if form.process().accepted:
		response.flash="Required search is applied"
	elif form.errors:
		response.flash="Please fill the form COMPLETELY"
	else:
		response.flash="Fill this form completely to search"
	if len(request.vars) != 0:
		s=request.vars["title"]
		ans=db(db.project.project_title.like("%"+s+"%")).select()
	return dict(ans=ans,form=form)
@auth.requires_login()
def search():
	a=10
	return dict(a=a);

@auth.requires_login()
def searchbyperson():
	form=FORM(INPUT(_type="string",_name="person",_placeholder="a piece of string in name of person",requires=IS_NOT_EMPTY()))
	ans=[];
	if form.process().accepted:
		response.flash="Required search is applied"
	elif form.errors:
		response.flash="Please fill the form COMPLETELY"
	else:
		response.flash="Fill this form completely to search"
	if len(request.vars) != 0:
		s=request.vars["person"]
		ans=db(db.project.author_name.like("%"+s+"%")).select()
        print "amana=",ans,len(ans)

	return locals()
	
@auth.requires_login()
def searchbycat():
	form=FORM(INPUT(_type="string",_name="category",requires=IS_IN_SET(['Programming language','Mathematics','Web development','App development'])))
	ans=[];
	var=0;
	if form.process().accepted:
		response.flash="Required search is applied"
	elif form.errors:
		var=1;
		response.flash="Please fill the form COMPLETELY"
	else:
		response.flash="Fill this form completely to search"
	if len(request.vars) != 0:
		s=request.vars["category"]
        print "amancat=",ans,len(ans)
	return locals()
def show_cat():

    query=db.project.category.like("%"+s+"%")
    users = db(query).select(orderby=db.project.category)
    links = [A(p.project_title, _href=URL('show',args=p.id)) for p in users]
    return DIV(*[DIV(k,  _onmouseover="this.style.backgroundColor='yellow'", _onmouseout="this.style.backgroundColor='white'")for k in links])

    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def red():
    s=db(db.project.id>0).select(db.project.ALL)	
    return locals();
def download_a():
#print request.args
    file_id=request.args[0]
#print "FILE==",file1
    row = db(db.project.id==file_id).select().first()
    down =row.downloads 
    down=down+1
    row.update_record(downloads=down)
    import datetime
    now=datetime.datetime.now()
    db.d.insert(project_id=row.id,time_stamp=now,author=auth.user.id)
    redirect(URL('download',args=row.folder))
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db) 

def search2():
    return dict(form1=FORM(INPUT(_id='keyword1',_name='keyword1', _onkeyup="ajax('callback2', ['keyword1'], 'target1');")),target_div1=DIV(_id='target1'),form2=FORM(INPUT(_id='keyword2',_name='keyword2', _onkeyup="ajax('callback3', ['keyword2'], 'target2');")),target_div2=DIV(_id='target2'),form3=FORM(INPUT(_id='keyword3',_name='keyword3', _onkeyup="ajax('callbackcomb', ['keyword3'], 'target3');")),target_div3=DIV(_id='target3'),form4=FORM(INPUT(_id='keyword4',_name='keyword4', _onkeyup="ajax('callback4', ['keyword4'], 'target4');")),target_div4=DIV(_id='target4'))

def callback2():
    if not request.vars.keyword1: return ''
    query = db.project.project_title.contains(request.vars.keyword1)
    images = db(query).select(orderby=db.project.project_title)
    links = [A(p.project_title, _href=URL('show',args=p.id)) for p in images]
    return DIV(*[DIV(k,  _onmouseover="this.style.backgroundColor='yellow'", _onmouseout="this.style.backgroundColor='white'")for k in links])

def callback3():
    if not request.vars.keyword2: return ''
    query = db.auth_user.first_name.contains(request.vars.keyword2)
    users = db(query).select(orderby=db.auth_user.first_name)
    links = [A(p.first_name, _href=URL('profile',args=p.id)) for p in users]
    return DIV(*[DIV(k,  _onmouseover="this.style.backgroundColor='yellow'", _onmouseout="this.style.backgroundColor='white'")for k in links])
def callback4():
    if not request.vars.keyword4: return ''
    query = db.project.category.contains(request.vars.keyword4)
    users = db(query).select(orderby=db.project.category)
    links = [A(p.project_title, _href=URL('show',args=p.id)) for p in users]
    return DIV(*[DIV(k,  _onmouseover="this.style.backgroundColor='yellow'", _onmouseout="this.style.backgroundColor='white'")for k in links])
def callbackcomb():
    if not request.vars.keyword3: return ''
    query1 = db.project.project_title.contains(request.vars.keyword3)
    images = db(query1).select(orderby=db.project.project_title)
    links1 = [A(p.project_title + " (project)", _href=URL('show',args=p.id)) for p in images]
    query = db.auth_user.first_name.contains(request.vars.keyword3)
    users = db(query).select(orderby=db.auth_user.first_name)
    links = [A(p.first_name+" (user)", _href=URL('profile',args=p.id)) for p in users]
    links=links+links1
    return DIV(*[DIV(k,  _onmouseover="this.style.backgroundColor='yellow'", _onmouseout="this.style.backgroundColor='white'")for k in links])


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
