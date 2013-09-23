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
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.settings import *
from gstudio.models import *
from objectapp.models import *
import os
from gstudio.methods import *
from PIL import Image
import glob, os
import hashlib
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.template import Context
from gstudio.methods import getimages,check_collection
from django.http import Http404
from gstudio.views.ajaxviews import notifyuserimg
from django.shortcuts import render


def dashboard(request):
    allObject = []
    if request.user.is_superuser:
        systype = Systemtype.objects.get(title="Wikipage")
        for each in systype.member_systems.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,'type':"Concept Page",'date':each.creation_date,'view':"/gstudio/page/gnowsys-page/"+str(each.id)})

        imgtype = Objecttype.objects.get(title="Image")
        for each in imgtype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,'type':"Image",'date':each.creation_date,'view':"/gstudio/resources/images/show/"+str(each.id)})

        videotype = Objecttype.objects.get(title="Video")
        for each in videotype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,'type':"Video",'date':each.creation_date,'view':"/gstudio/resources/videos/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Document")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Document",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})    

        allObjecttype = Objecttype.objects.get(title="Audio")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Audio",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Graphics")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Graphics",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Multimedia")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Multimedia",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Presentation")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Presentation",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="PDF")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"PDF",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Spreadsheet")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Spreadsheet",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        allObjecttype = Objecttype.objects.get(title="Html")
        for each in allObjecttype.member_objects.filter(status=1):
            author = ""
            if each.authors.all():
                author = each.authors.all()[0].username
            allObject.append({'title':each.title,'id':each.id,'authors':author,"type":"Html",'date':each.creation_date,'view':"/gstudio/resources/documents/show/"+str(each.id)})

        
    vars=RequestContext(request,{'allObject':allObject})
    template="gstudio/dashboard.html"
    return render_to_response(template, vars)
