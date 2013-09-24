# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.



from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
from demo.settings import *
from gstudio.models import *
from objectapp.models import *
from gstudio.methods import *
import hashlib
from django.template.defaultfilters import slugify
import os
import mimetypes
from django.http import Http404
from django.shortcuts import get_object_or_404
from itertools import chain
from operator import attrgetter
import subprocess
from gstudio.views.ajaxviews import *
report = "true"


def docu(request):
	p=Objecttype.objects.get(title="Document")
	q=p.get_nbh['contains_members']
	q = q.filter(status=2)
        documents=getdocuments()
        htmlot=Objecttype.objects.get(title='Html')
        html=htmlot.member_objects.all()
        audioot=Objecttype.objects.get(title='Audio')
        audio=audioot.member_objects.all()
	if request.method=="POST":
		title = request.POST.get("title1","")
		user = request.POST.get("user","")
		content= unicode(request.POST.get("contenttext",""))
		sdoc = request.POST.get("sdoc","")
		dn = request.POST.get("dn","")
		sub3 = request.POST.get("mydropdown","")
		rating = request.POST.get("star1","")
		docid = request.POST.get("docid","")
		delete = request.POST.get("delete","")
		addtags = request.POST.get("addtags","")
		texttags = unicode(request.POST.get("texttags",""))
		contenttext = request.POST.get("commenttext","")
		fav=request.POST.get("fav","")
		if rating :
        	 	rate_it(int(docid),request,int(rating))

		if fav != "" :
			list1=[]
			t=Gbobject.objects.filter(title=user+"document")
                        
			if t:
			    t=Gbobject.objects.get(title=user+"document")
			    if t.get_relations():
				    for each in t.get_nbh['has_favourite']:
					    d=each.right_subject_id
					    x=Gbobject.objects.get(id=d)
					    list1.append(x)
                        variables = RequestContext(request,{'documents':list1,'fav':fav,'test1':documents})
			template = "gstudio/docu.html"
			return render_to_response(template, variables)	
	

		if delete != "":
			each=q.get(id=dn)
			each.delete()
			ti=each.title
			os.system("rm -f "+MEDIA_ROOTNEW+'/'+ti)
			p=Objecttype.objects.get(title="Document")
			q=p.get_nbh['contains_members']
                        vars=RequestContext(request,{'documents':q,'val':sdoc,'test1':documents})
			template="gstudio/docu.html"
			return render_to_response(template, vars)
		if sub3 != "":
			if sdoc != "":
				vidon = Objecttype.objects.get(title="Document")
				vido_new = vidon.get_nbh['contains_members']
                                vido = vido_new.filter(title__contains=sdoc).filter(status=2)
                                htmls=html.filter(title__contains=sdoc)
				vido2 = vido.order_by(sub3)
                                audios=audio.filter(title__contains=sdoc)
                                vido2=list(chain(vido2,htmls,audios))
                                variables = RequestContext(request,{'documents':vido2,'val':sdoc,'test1':documents})
				template = "gstudio/docu.html"
				return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Document")
				vido_new = vidon.get_nbh['contains_members']
				vido_new = vido_new.filter(status=2)
				vido=vido_new.order_by(sub3)
                                vido=list(chain(vido,html,audio))
                                variables = RequestContext(request,{'documents':vido,'val':sdoc,'test1':documents})
				template = "gstudio/docu.html"
				return render_to_response(template, variables)
	
		if addtags != "":
			i=Gbobject.objects.get(id=docid)
			i.tags = i.tags+ ","+(texttags)
			i.save()

		if contenttext !="":
			print contenttext,"content"
	                edit_description(docid,contenttext,str(request.user))


		a=[]
		reportid=''
		for each in request.FILES.getlist("doc[]",""):
			a.append(each)
		if a != "":
			for f in a:
				report,imageeachid = save_file(f)
				if report == "false":
					reportid = imageeachid
				else:
					create_object(f,user,content,str(request.user),title)
                        vars=RequestContext(request,{'documents':q,'reportid':reportid,'test1':documents})
			template="gstudio/docu.html"
			return render_to_response(template, vars)	
	s=Nodetype.objects.get(title="Document")
#	t=s.get_nbh['contains_members']
        q=list(sorted(chain(q,html,audio),key=attrgetter('creation_date')))
        q.reverse()
	vars=RequestContext(request,{'documents':q,'docomment':s,'test1':documents})
	template="gstudio/docu.html"
	return render_to_response(template, vars)

def save_file(file, path=""):
	report = "true"
	imageeachid = ''
	filename = file._get_name()
	slugfile = str(filename)
	slugfile=slugfile.replace(' ','_')
	fd = open('%s/%s' % (MEDIA_ROOTNEW2, str(path) + str(slugfile)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()
	global md5_checksum
	md5_checksum = md5Checksum(MEDIA_ROOTNEW2+"/"+str(slugfile))
	attype = Attributetype.objects.get(title="md5_checksum_document")
	att = Attribute.objects.all()
	flag = 0
	for each in att:
		if each.attributetype.id == attype.id:
			if each.svalue == md5_checksum :
				flag = 1
				imageeachid = each.subject.id
	if flag == 1:
		report = "false"
	
        #code to convert mp3 file to ogg file                                                                                       
        file1=MEDIA_ROOTNEW2+"/"+str(slugfile)
        filetype = mimetypes.guess_type(MEDIA_ROOTNEW2+"/"+str(slugfile))[0]
        if file1.endswith(".mp3"):
                if not filetype == None:
                        if "audio" in filetype:
                                subprocess.call(["ffmpeg2theora",file1])
        #end code     
        return report,imageeachid


def create_object(file,log,content,usr,title):
	p=Gbobject()
	filename=file._get_name()
	slugfile = str(filename)
	slugfile=slugfile.replace(' ','_')
	p.title = title
	p.altnames = slugfile
	#p.rurl= #MEDIA_ROOTNEW2+"p.title"
	final = ''
	fname=slugify(p.title)+"-"+usr
	for each1 in p.title:
		if each1==".":
			final=final+'-'
		elif each1==" ":
			final=final+'-'
		else:
			final = final+each1	
	p.slug=slugify(final)
	contorg=unicode(content)
	p.content_org=contorg.encode('utf8')
	p.status=2
	p.save()
	p.slug = p.slug + "-" + str(p.id)
	p.sites.add(Site.objects.get_current())
	p.save()
	s=Author.objects.get(username=log)
	if s.is_superuser == True:
		p.status=2
	else:
		p.status=1	

	p.authors.add(s)
	p.save()
	filetype = mimetypes.guess_type(MEDIA_ROOTNEW2+"/"+str(slugfile))[0]
	if not filetype == None:
		if "audio" in filetype:
			p.objecttypes.add(Objecttype.objects.get(title="Audio"))
		elif "image" in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="Graphics"))
	        elif "video" in filetype or "flash" in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="Multimedia"))
         	elif "presentation"  in filetype or "powerpoint" in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="Presentation"))
         	elif "pdf"  in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="PDF"))
         	elif "spreadsheet"  in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="Spreadsheet"))
         	elif "html"  in filetype:                              
			p.objecttypes.add(Objecttype.objects.get(title="Html"))
	        else :
			p.objecttypes.add(Objecttype.objects.get(title="Document"))
	else:
		p.objecttypes.add(Objecttype.objects.get(title="Document"))							
	p.save()
	new_ob = content
	ext='.org'
 	html='.html'
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 	myfile.write(p.content_org)
 	myfile.close()
 	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
        rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)
 	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 	myfile.write("\n#+TITLE: ")
 	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 	output = stdout.read()
 	data = open(os.path.join(FILE_URL,fname+html))
 	data1 = data.readlines()
        
 	data2 = data1[107:]
        dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'

	data3 = data2[:-6]	
 	newdata=""
 	for line in data3:
        	newdata += line.lstrip()
 	p.content = newdata
 	p.save()	
	a=Attribute()
	a.attributetype=Attributetype.objects.get(title="md5_checksum_document")
	a.subject=p
	a.svalue=md5_checksum  
	a.save()
        #code to notify admin about document upload
        response_content="Uploaded Document :"+p.title
        notifyUpdate(p.id,usr,response_content)
        #end code

def rate_it(topic_id,request,rating):
	ob = Gbobject.objects.get(id=topic_id)
	ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
	return True

def show(request,documentid):
	if request.method=="POST":
		rating = request.POST.get("star1","")
		docid = request.POST.get("docid","")
		addtags = request.POST.get("addtags","")
		texttags = unicode(request.POST.get("texttags",""))
		contenttext = unicode(request.POST.get("contenttext",""))
		favid=request.POST.get("favid","")
		favusr=request.POST.get("favusr","")
		removefavid = request.POST.get("removefavid","")
		titlecontenttext = request.POST.get("titlecontenttext","")
		if rating :
	       	 	rate_it(int(docid),request,int(rating))
		if addtags != "":
			i=Gbobject.objects.get(id=docid)
			i.tags = i.tags+ ","+(texttags)
			i.save()
		if contenttext !="":
			 edit_description(docid,contenttext,str(request.user))

		if favid!="":
                        e=0
                        r = Objecttype.objects.get(title="user")
                        for each in r.get_nbh['contains_members']:
                                if favusr+"document" == each.title:
                                    e=1
                        if e==0 :
				t=Gbobject()
                                t.title=favusr+"document"
                                t.slug=favusr+"document"
                                t.content=' '
                                t.status=2
                                t.save()
                                t.objecttypes.add(Objecttype.objects.get(title="user"))
                                t.save()
                        t=Gbobject.objects.get(title=favusr+"document")
                        rel=Relation()
                        rt=Relationtype.objects.get(title="has_favourite")
                        rel.relationtype_id=rt.id
                        f1=Gbobject.objects.get(id=favid)
                        rel.left_subject_id=t.id
                        rel.right_subject_id=f1.id
                        rel.save()
			t.save()
		if removefavid !="":
			objects = Gbobject.objects.get(id=removefavid)
			objects.get_relations()['is_favourite_of'][0].delete()

	gbobject = Gbobject.objects.filter(id=documentid)
        if gbobject:
            gbobject = Gbobject.objects.get(id=documentid)
	    relation = ""
	    if gbobject.get_relations():
		    if 'is_favourite_of' in gbobject.get_relations():
			    rel = gbobject.get_relations()['is_favourite_of'][0]
			    reluser = rel._left_subject_cache.title
			    if str(reluser) == str(request.user)+str("document"):
				    relation = "rel"
	    vars=RequestContext(request,{'doc':gbobject,'relation':relation})
	    template="gstudio/fulldocument.html"
	    return render_to_response(template,vars)
        else:
		raise Http404



def edit_description(sec_id,title,usr):
	new_ob = Gbobject.objects.get(id=int(sec_id))
	contorg=unicode(title)
	new_ob.content_org=contorg.encode('utf8')
	ssid=new_ob.get_ssid.pop()
	fname=str(ssid)+"-"+usr
	ext='.org'
	html='.html'
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 	myfile.write(new_ob.content_org)
 	myfile.close()
 	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)

 	#myfile.readline()
 	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 	myfile.write("\n#+TITLE: ")
 	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 	output = stdout.read()
 	data = open(os.path.join(FILE_URL,fname+html))
	data1 = data.readlines()
	data2 = data1[107:]
        dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'

	data3 = data2[:-6]
	newdata=""
	for line in data3:
		newdata += line.lstrip()
	new_ob.content = newdata
	new_ob.save()
	return True

def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def createcolln(request):
    listcl=request.GET["listofcollns"]
    print "listdoccl=",listcl
    coltitle=request.GET["coltitle"]
    editcoln=request.GET["editcoln"]
    colid=request.GET["colid"]
    if editcoln=='1':
        print "inside doceditcol"
        col=System.objects.get(id=colid)
        col.gbobject_set.clear()
        i=0
        if listcl != "null":
                listcl=listcl+","
                listcl=eval(listcl)
                while i < len(listcl):
                        objs=Gbobject.objects.get(id=listcl[i])
                        print "objs",objs
                        col.gbobject_set.add(objs)
                        i=i+1
        col.save()
        p=col.gbobject_set.all()
        print "complelst",p
        t=get_template('gstudio/estngdoccollns.html')
        html = t.render(Context({'doc':col,'user':request.user}))
        return HttpResponse(html)
    else:
        syscol=Systemtype.objects.get(title='Documentcollection')
        col=System()
        col.title=coltitle
        col.slug=slugify(coltitle)
        col.save()
        col.systemtypes.add(syscol)
        t='gstudio/doccollns.html'
        if listcl != "" and listcl != "null":
                i=0
                listcl=listcl+","
                listcl=eval(listcl)
                while i < len(listcl):
                        objs=Gbobject.objects.get(id=listcl[i])
                        col.gbobject_set.add(objs)
                        i=i+1
                col.save()
        return render_to_response(t,RequestContext(request))
