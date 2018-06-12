# -*- coding: utf-8 -*-
import bpy
from g_tools.nbf import *

############bpy object manipulation

def get_obj_type_args(obj_name,obj_type,sub_type):
    """これは酷い。見なかったことにしてください。"""
    default_lst = ('meshes','new',)
    tlst = (
    "EMPTY",
    "MESH",
    "ARMATURE",
    "CURVE",
    "METABALL",
    "LATTICE",
    "LAMP",)
    if obj_type not in tlst:
        raise ValueError("Specified object type is invalid")
    def pluralize(s):
        return s + "s" if s[-1] in 'aeioulpt' else s + "es" 
    
    fdict = {t:[pluralize(t.lower()),'new',[obj_name]] for t in tlst}
    
    subtype_dict = {
    "CURVE":["CURVE","SURFACE","FONT"],
    "LAMP":["POINT","SUN","SPOT","HEMI","AREA"]
    }
    

    fdict["LAMP"][2].append("AREA")
    fdict["CURVE"][2].append("CURVE")
    
    if sub_type != "":
        sub_type_idx = subtype_dict[obj_type].index(sub_type)
        sub_type = subtype_dict[obj_type][sub_type_idx]
        fdict[obj_type][2][-1] = sub_type
        
    return fdict[obj_type]

def make_obj(name = "new_obj",type = "MESH",subtype = "",do_link = True):
    """
    オブジェクトの作成を補助してくれる関数
    """
    dat = bpy.data
    dobjs = bpy.data.objects
    objs = bpy.context.scene.objects
    
    coll_name,create_func_name,create_func_args = get_obj_type_args(name,type,subtype)
    if type == "EMPTY":
        ndata = None
    else:
        ndata = getattr(getattr(dat,coll_name),create_func_name)(*create_func_args)
    nobj = dobjs.new(name = name,object_data = ndata)
    
    if do_link:
        objs.link(nobj)
    return nobj
	
def make_objs(coords,scale = 1,name = "",count = -1,type = "EMPTY"):
    """Creates things at coordinates.
    Pass a count > 0 with the coords to only create some of the coordinates.
    Pass None and a count to create without coordinate setting."""
    if name == "":
        name = "new_" + type
    if count > 0:
        if coords == None:
            return tmap(lambda x: make_obj(name = name,obj_type = type),range(count))
        else:
            return tmap(lambda x: make_obj(coords = coords[x],obj_type = type,obj_name = name),range(count))
    return from_coords(coords,name=name,obj_type = type,**{"scale":scale})
    
def from_coords(coords,name = "new_obj",obj_type = "EMPTY",prop_name = "location",*args,**kwargs):
    '''
    Make a series of objects from given coordinates.
    **Kwargs treated as property arguments.
    '''
    res = list(map(lambda x: make_obj(obj_type = obj_type,obj_name = name),coords))
    any(map(lambda r: setattr(res[r],prop_name,coords[r]),rlen(res)))
    any(map(lambda r: dict2attr(kwargs,r),res))
    return res
    