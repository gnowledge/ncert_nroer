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


# This project incorporates work covered by the following copyright and permission notice:  

#    Copyright (c) 2009, Julien Fache
#    All rights reserved.

#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:

#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#    * Neither the name of the author nor the names of other
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.

#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE.

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



"""Views for Gstudio nodetypes search"""
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from gstudio.models import Nodetype
from gstudio.settings import PAGINATION

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *

def nodetype_search(request):
    """Search nodetypes matching with a pattern"""
    error = None
    pattern = None
    nodetypes_dic = ""
    nodetypes = Nodetype.published.none()

    if request.GET:
        pattern = request.GET.get('pattern', '')
        if len(pattern) < 3:
            error = _('The pattern is too short')
        else:
            nodetypes_dic =GetSearchdic(pattern)
    else:
        error = _('No pattern to search found')

    variables = RequestContext(request,{"object_dic":nodetypes_dic,'error': error,'pattern': pattern})
    template  =	'gstudio/nodetype_search.html'
    return render_to_response(template, variables)  			    
    # return object_list(request, queryset=nodetypes,
    #                    paginate_by=PAGINATION,
    #                    template_name='gstudio/nodetype_search.html',
    #                    extra_context={'error': error,
    #                                   'pattern': pattern})
	


def GetSearchdic(pattern):
	a=Nodetype.published.search(pattern).exclude(title__icontains="page box of").exclude(title__icontains="message box of")
	lstimg=[]
	lstvid=[]
	lstpg=[]
	lstdoc=[]
	lstoth=[]
	lstcol=[]
	lstimgcol=[]
	lstdoccol=[]
	dic={}
	for each in a:
	   if 'type' not in each.reftype:	
                obj=each.ref.objecttypes.all()
                if obj:	
                     	if(obj[0].title=="Image"):
                            	lstimg.append(each)
                     	elif(obj[0].title=="Document"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Audio"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Graphics"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Multimedia"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Presentation"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="PDF"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Spreadsheet"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Html"):
                              	lstdoc.append(each)
                     	elif(obj[0].title=="Video"):            
                               	lstvid.append(each)
		     	else:
			       	lstoth.append(each)	
                else:
		   check=System.objects.filter(id=each.id)
		   if check:			                  
                   	obj=each.ref.system.systemtypes.all()
		   	if obj:	
		      		if(len(obj)>1):
					obj.exclude(title__icontains="Wikipage")
					if(obj[0].title=="Collection"):
                        	       		lstcol.append(each)
				else:
                     			if(obj[0].title=="Wikipage"):
                        		      	lstpg.append(each)
					elif(obj[0].title=="Imagecollection"):
                        		       	lstimgcol.append(each)
					elif(obj[0].title=="Documentcollection"):
                        		      	lstdoccol.append(each)
		     			else:
					      	lstoth.append(each)
	dic["Image"]=lstimg
	dic["Document"]=lstdoc
	dic["Page"]=lstpg
	dic["Video"]=lstvid
	dic["others"]=lstoth
	dic["Collection"]=lstcol
	dic["DocCollection"]=lstdoccol
	dic["ImgCollection"]=lstimgcol
        return dic         
