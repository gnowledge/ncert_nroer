
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



from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.template.defaultfilters import slugify
from unidecode import unidecode
from gstudio.methods import *

@user_passes_test(lambda u: u.is_superuser)
def translate(request):
    wikipage = Systemtype.objects.get(title="Wikipage")
    wikipage_member = wikipage.member_systems.all()
    vars=RequestContext(request,{'no_of_concept':len(wikipage_member)})
    template="gstudio/translate.html"
    return render_to_response(template, vars)

def concept_request(request):
    data = []
    start = request.GET['start']
    end = request.GET['end']
    wikipage = Systemtype.objects.get(title="Wikipage")
    wikipage_member = wikipage.member_systems.all()[start:end]
    for each in wikipage_member:
	rt = []
    	relation = ""
   	conceptObjectTitle = ""
	conceptObjectId = ""
	if each.get_relations():
		for eachrelation in each.get_relations():
			rt.append(eachrelation)
		if "hindipage" in rt:
			conceptObjectTitle = each.get_relations()["hindipage"][0].right_subject.title
			conceptObjectId = each.get_relations()["hindipage"][0].right_subject.id
			relation = "yes"
	if not "englishpage" in rt:
	        data.append({"id":each.id, "title":each.title, "relation":relation, "conceptObjectTitle":conceptObjectTitle, "conceptObjectId":conceptObjectId})
    return HttpResponse(json.dumps(data))

def concept_search(request):
    data = []
    text_search = request.GET['text_concept']
    wikipage = Systemtype.objects.get(title="Wikipage")
    wikipage_member = wikipage.member_systems.all()
    wikipage_filter = wikipage_member.filter(title__icontains=text_search)
    for each in wikipage_filter:
	rt = []
    	relation = ""
   	conceptObjectTitle = ""
	conceptObjectId = ""
	if each.get_relations():
		for eachrelation in each.get_relations():
			rt.append(eachrelation)
		if "hindipage" in rt:
			conceptObjectTitle = each.get_relations()["hindipage"][0].right_subject.title
			conceptObjectId = each.get_relations()["hindipage"][0].right_subject.id
			relation = "yes"
		if not "englishpage" in rt:
		        data.append({"id":each.id, "title":each.title, "relation":relation, "conceptObjectTitle":conceptObjectTitle, "conceptObjectId":conceptObjectId})
    return HttpResponse(json.dumps(data))

	

    
@user_passes_test(lambda u: u.is_superuser)
def translate_to_hindi(request):
    '''
	create relation between eng and hi page
    '''
    if request.is_ajax() and request.method =="POST":
    	conceptid = request.POST['conceptid']
	concept_to_hindi = request.POST['concept_to_hindi']
	content_org = ""
        relation_list=[]
	collection = ""
	list1 = ""
	newconceptid = ""
	exitconcept = System.objects.filter(title=concept_to_hindi)
	try:
		if not exitconcept :
			newconceptid = create_wikipage(concept_to_hindi,request.user.id,content_org,request.user.username,collection,list1)
		else :
			newconceptid = System.objects.get(title=concept_to_hindi).id
		if newconceptid:
			rt=Relationtype.objects.filter(title="hindipage")
			if not rt :
				newrt = Relationtype()
				newrt.title = "hindipage"
				newrt.inverse = "englishpage"
				newrt.slug = slugify("hindipage")
			        newrt.left_subjecttype = NID.objects.get(title='Wikipage')
			        newrt.left_applicable_nodetypes = unicode('ST')
			        newrt.right_subjecttype = NID.objects.get(title='Wikipage')
			        newrt.right_applicable_nodetypes = unicode('ST')
			        newrt.save()
				newrt.authors.add(Author.objects.get(id=request.user.id))
                        parent_id=System.objects.get(id=conceptid)
                        for k,v in parent_id.get_relations().items():
                            for each in v :
                                dict = {}
                                if parent_id.id == each.right_subject_id:
                                    dict['right'] = newconceptid
                                else :
                                    dict['right'] = each.right_subject_id
                                if parent_id.id == each.left_subject_id:
                                    dict['left'] = newconceptid
                                else :
                                    dict['left'] = each.left_subject_id
                                dict['rt'] = each.relationtype.id
                                relation_list.append(dict) 
                        print relation_list
                        for each in relation_list:
                            rt=Relation()
                            rt.right_subject_id=each['right']
                            rt.left_subject_id=each['left']
                            rt.relationtype_id=each['rt']
                            rt.save()

                        rt=Relationtype.objects.get(title="hindipage")
			newrelation=Relation()
	        	newrelation.left_subject = System.objects.get(id=conceptid)
	                newrelation.relationtype = rt
		        newrelation.right_subject=System.objects.get(id=newconceptid)
                       	newrelation.save()

		data = {"id":newconceptid,"title":System.objects.get(id=newconceptid).title,"status":"ok"}
	except Exception as e:
                delnew=System.objects.get(id=newconceptid)
                delnew.delete()
		data = {"status":"failed","error":str(e)}
    		return HttpResponse(json.dumps(data))	

	
    else :
	data = {"status":"failed"}
    return HttpResponse(json.dumps(data))	

