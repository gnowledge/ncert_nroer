from gstudio.methods import *

def con_script():
    wiki_st=Systemtype.objects.get(title='Wikipage')
    all_sys=System.objects.all()
    all_wikis=[]
    fp=open("../demo/concept_with_relns.csv","a")
    for each in all_sys:
        if not 'page box of' in each.title:
            if wiki_st in each.systemtypes.all():
                all_wikis.append(each)
    fp.write("subject-id,subject-name,relation-name,object-name,object-title,subject-title")
    for eachwiki in all_wikis:
        line="\n"+eachwiki.id.__str__()+","+eachwiki.title.encode('utf8')+","
        relns=eachwiki.get_relations_for_view()
        for key,value in relns.items():
            if not (key=="has_video" or key =="has_image" or key == "has_html" or key == "has_multimedia" or key == "has_audio"):
                for eachval in value:
                    reln=Relation.objects.get(id=eachval['id'])
                    oburl=str(eachval['url']).split("/")
                    objid=oburl[len(oburl)-1]
                    if str(reln.left_subject_id).strip() == str(objid).strip():
                        inv_name=reln.relationtype.title.encode('utf8')
                    else:
                        inv_name=reln.relationtype.inverse.encode('utf8')
                    lpline=key.encode('utf8')+","+str(objid)+","+eachval['title'].encode('utf8')+","+inv_name+","+eachwiki.title.encode('utf\
8')
                    fline=line+lpline
                    fp.write(fline)
    fp.close()
    return

