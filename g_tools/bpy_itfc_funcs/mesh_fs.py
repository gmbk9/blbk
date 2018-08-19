# -*- coding: utf-8 -*-
import bpy
from g_tools.nbf import *
from g_tools.gtls import defac,get_ac,set_ac,set_mode,moderate,get_sel_obj,get_sel_objs
from .. import gtls

#########################################################デコレーター/decorators
def bm_install(f):
    def bm_installerated(obj = None,bm = None,*args,**kwargs):
        do_clean = False
        if bm == None:
            do_clean = True
            bm = get_bmesh(obj = obj)
        res = f(obj = obj,bm = bm,*args,**kwargs)
        if do_clean:
            bm.free()
        return res
    return bm_installerated

#########################################################選択関連/selection
@defac
def sel_verts(targets,obj = None,state = True,all = False):
    """
    頂点の選択状態をstateに変更する
    :param targets: 頂点オブジェクトまたはインデックスを渡して選択状態をstateに変更する
    :param all: Trueだととりあえず頂点の選択状態ををstateに変更する
    :param obj: defac用
    :return: None
    """
    verts = obj.data.vertices
    if all:
        for v in verts:
            v.select = state
    elif len(targets) == 0:
        return
    elif type(targets[0]) == int:
        for vidx in targets:
            verts[v].select = state
    else:
        for v in targets:
            v.select = state

@defac
def sel_items(targets,obj = None,state = True,all = False,collection = "vertices"):
    """
    何かの選択状態をstateに変更する
    :param targets: 複数オブジェクトまたはインデックスを渡して選択状態をstateに変更する
    :param all: Trueだと、とりあえず複数オブジェクトの選択状態ををstateに変更する
    :param collection: リストのproperty名
    :param obj: defac用
    :return: None
    """
    coll = getattr(obj.data,collection)
    if all:
        targets = coll
    elif len(coll) == 0:
        return
    elif type(targets[0]) == int:
        for i in coll:
            coll[i].select = state
    else:
        for i in targets:
            i.select = state

#########################################################bmesh関連/bmesh related
def get_bmesh(obj = None):
    mesh = bpy.data.objects[obj.name].data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    return bm

@defac
def make_hull(do_link=False, name="hull_obj",obj = None):

    tobj = gtls.make_obj(do_link=do_link, obj_name=name, obj_type="MESH")
    bm = get_bmesh(obj=obj)

    mesh = obj.data
    verts = bm.verts
    opres = bmesh.ops.convex_hull(bm, input=verts)

    bm.to_mesh(tobj.data)
    bm.free()

@bm_install
@defac
def get_separated_parts(obj =  None,bm = None):
    objs = bpy.context.scene.objects
    mesh = (obj.data)
    verts = mesh.vertices
    
    vidxs = range(len(verts))
    
    emem = {}
    vmem = {}
    rem = {v:1 for v in vidxs}
    
    def fnc(es,vmem = None,emem = None,rem = None,res = None):
        if res == None:
            res = []
        for e in es:    
            eidx = e.index
            if try_key(emem,eidx):continue
                
            for v in e.verts:
                vidx = v.index
                try:
                    vmem[vidx]
                    continue
                except:
                    vmem[vidx] = 1
                    res.append(vidx)
                    es = v.link_edges
                    fnc(es,vmem = vmem,emem = emem,rem = rem,res = res)
        return res
    
    vs = list(bm.verts)
    res = []
    
    #using a dictionary to keep track of ungrouped vertices,
    #iterate over all vertices until edges are found for all vertices
    #will probably break if there are floating vertices
    while len(rem) > 0:
        for i in rem:
            es = vs[i].link_edges
            break
        r = fnc(es,vmem = vmem, emem = emem, rem = rem)
        res.append(r)
        for vidx in r:
            rem.pop(vidx)
        
    return res

@bm_install
@defac
def find_doubles_bm(obj=None, bm=None, to_mesh=True, dist=0.0001):
    res = bmesh.ops.find_doubles(bm, verts=bm.verts, dist=dist)
    if to_mesh:
        mesh = obj.data
        bm.to_mesh(mesh)
    return res

@bm_install
@defac
def remove_doubles_bm(obj=None, bm=None, to_mesh=True, dist=0.0001):
    res = bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    dissolve_verts = bm.verts[1:-1]
    # for x in range(len(dissolve_verts)-1,0,-15):
    # dissolve_verts.pop(x)
    # res = bmesh.ops.dissolve_verts(bm,verts = dissolve_verts)
    if to_mesh:
        mesh = obj.data
        bm.to_mesh(mesh)
    return res

@defac
def map_boundary_verts(obj=None, bm=None):
    do_clean = False
    if bm == None:
        do_clean = True
        bm = get_bmesh(obj=obj)
    vidxmap = tmap(lambda v: v.is_boundary, bm.verts)
    if do_clean:
        bm.free()
    return vidxmap

@defac
def get_boundary_verts(obj=None, bm=None):
    do_clean = False
    if bm == None:
        do_clean = True
        bm = get_bmesh(obj=obj)
    vidxmap = map_boundary_verts(obj=obj, bm=bm)
    vidxs = tuple(compress(rlen(bm.verts), vidxmap))
    if do_clean:
        bm.free()
    return vidxs

@defac
def bm_map(obj=None, bm=None, prop="is_manifold"):
    do_clean = False
    if bm == None:
        do_clean = True
        bm = get_bmesh(obj=obj)
    vidxmap = tmap(lambda v: v.is_boundary, bm.verts)
    if do_clean:
        bm.free()
    return vidxmap

@defac
def bm_filter(obj=None, bm=None, prop="is_manifold"):
    do_clean = False
    if bm == None:
        do_clean = True
        bm = get_bmesh(obj=obj)
    vidxmap = bm_map(obj=obj, bm=bm, prop=prop)
    vidxs = tuple(compress(rlen(bm.verts), vidxmap))
    if do_clean:
        bm.free()
    return vidxs

@defac
def get_nmf_verts(obj=None, bm=None):
    return bm_filter(obj=obj, bm=bm, prop="is_manifold")


#########################################################シェープキー（つまりモーフ）関連/shape key related
@defac
def choose_verts(obj=None, type="mesh"):
    mesh = bpy.data.objects[obj.name].data.name
    verts = bpy.data.meshes[mesh].vertices
    sks = obj.data.shape_keys
    if sks == None:
        bss = obj.shape_key_add(name="Basis")
    keys = skeys.key_blocks

    if type == "basis":
        res = keys[0]
    elif type == "active":
        res = obj.active_shape_key
    else:
        res = verts

    return res

@defac
def apply_blends(group = True,
                all = True,
                blendval = 0,
                set_basis_active_key = False,
                set_active_group = False,
                obj = None):
    ct = bpy.context
    scn = ct.scene
    data = bpy.data
    objs = scn.objects
    obj = objs.active
    mods = obj.modifiers
    keys = obj.data.shape_keys.key_blocks

    #newkey = obj.shape_key_add(name = "temp",from_mix = True)
    askidx = obj.active_shape_key_index
    obj.active_shape_key_index = len(keys)
    asgidx = obj.vertex_groups.active_index

    shapevals = []
    shapenames = []
    for m in mods:
        if m.type == "ARMATURE":
            mod = m
            armshow = m.show_viewport
            if armshow == True:
                m.show_viewport = False

    for k in keys:
        shapevals.append(k.value)
        shapenames.append(k.name)
        k.value = blendval
    keys2 = keys[:][::-1]
    if not group:
        if all:
            r = range(len(keys)-1)
        else:
            r = range(askidx,askidx+1)
        for kidx in r:
            k = keys[kidx]
            val = k.value
            if set_basis_active_key:
                k.relative_key = keys[askidx]
            if k.relative_key != keys[0]:
                k.value = 1
                newkey = obj.shape_key_add(name = "temp",from_mix = True)
                for coord in range(len(newkey.data)):
                    k.data[coord].co = newkey.data[coord].co
                k.relative_key = keys[0]
            k.value = shapevals[kidx]
            obj.shape_key_remove(key = keys[len(keys) - 1])

    else:
        dupliobj = gtls.dupli_obj()
        dupliobj.data = obj.data.copy()
        duplikeys = dupliobj.data.shape_keys.key_blocks
        c=len(keys)-1
        for k in keys2:
            if set_active_group:
                k.vertex_group = obj.vertex_groups[asgidx].name
            if k.vertex_group != "":
                duplikeys[c].value = 1
                newkey = dupliobj.shape_key_add(name = "temp",from_mix = True)
                cv = 0
                for v in k.data:
                    v.co = newkey.data[cv].co
                    cv+=1
                duplikeys[c].value = 0
                k.vertex_group = ""
            c-=1
        c = 0
        for k in keys:
            k.value = shapevals[c]
            c+=1

        objs.unlink(dupliobj)
    obj.active_shape_key_index = askidx
    mod.show_viewport = armshow

@defac
def create_modified_duplicate2(apply_count = 0,obj_name = "modified",mesh_mod_clear = False,shape_apply = True,obj = None):
    ac = set_ac(obj)
    modified = obj.copy()
    if mesh_mod_clear:
        rem_types = ["MIRROR"]
        for m in modified.modifiers[:][::-1]:
            if (not m.show_viewport) or (m.type in rem_types):
                print(m)
                modified.modifiers.remove(m)
    if shape_apply:
        bpy.ops.object.shape_key_add(from_mix=True)
        for kidx,k in enumerate(modified.data.shape_keys.key_blocks[-1].data):
            modified.data.vertices[kidx].co = k.co
    modified.name = obj_name
    modmesh = modified.data.name
    modmeshdup = bpy.data.meshes[modmesh].copy()
    modified.data = modmeshdup
    modkeys = None
    try:
        modkeys = modified.data.shape_keys.key_blocks
    except:
        pass

    modmods = modified.modifiers
    bpy.context.scene.objects.link(modified)
    bpy.context.scene.objects.active = modified
    bpy.context.scene.update()
    oselect = obj.select
    modified.select = True
    obj.select = False
    bpy.context.scene.objects.active = modified

    if modkeys:
        bpy.ops.object.shape_key_remove(all=True)

    nummods = len(modmods)
    for m in range(nummods):
        '''
        #if apply_count > 0:
            #if m > apply_count:
                #break
        '''
        bpy.ops.object.modifier_apply(apply_as='DATA',modifier = modmods[0].name)
    obj.select = oselect
    set_ac(ac)
    return modified

#########################################################鏡像関連
@defac
def mesh_part_separate(obj = None,invert = False):
    
    parts = get_separated_parts(obj = obj)
    nobjs = tuple(gtls.dupli_obj(obj = obj) for i in parts)
    nobj_bms = tuple(get_bmesh(obj = o) for o in nobjs)
    
    for bmidx,bm in enumerate(nobj_bms):
        bmverts = tuple(bm.verts)
        for pidx,part in enumerate(parts):
            if cnegate(pidx == bmidx,condition = invert):
                continue
            else: 
                for vidx in part:
                    bm.verts.remove(bmverts[vidx])

    for o,bm in zip(nobjs,nobj_bms):
        bm.to_mesh(o.data)
        bm.free()
    
    return nobjs

########################################################頂点グループ像関連
@defac
def parts_to_vgroups(obj = None,parts = None,vg_name = "part_group_"):
    if parts == None:
        parts = get_separated_parts(obj = obj)
    vgroups = obj.vertex_groups
    vgs = tuple(vgroups.new(vg_name + str(p[0])) for p in enumerate(parts))
    
    for part,vg in zip(parts,vgs):
        vg.add(part,1,"ADD")
    
    return vgs

#########################################################鏡像関連
@defac
def find_mirror(cutoff=.001, type="both", extend=True, scale=1, basis=True, active_key=False, prec=4, obj=None):
    mesh = bpy.data.objects[obj.name].data.name
    verts = bpy.data.meshes[mesh].vertices
    sks = obj.data.shape_keys
    if sks == None:
        bss = obj.shape_key_add(name="Basis")
        sks = obj.data.shape_keys
    keys = sks.key_blocks

    selvertsR = []
    selvertsL = []

    vcodictL = {}
    vcodictR = {}

    if basis == True:
        vertsx = keys[0].data
    elif active_key == True:
        vertsx = obj.active_shape_key.data
    else:
        vertsx = verts

    for vidx, v in enumerate(vertsx):
        if v.co[0] > 0:
            vco = roundtuple(tuple(v.co), prec, scale=scale)
            if verts[vidx].select == True:
                selvertsL.append((vco, vidx))
            try:
                vcodictL[vco].append(vidx)
            except:
                vcodictL.update({vco: [vidx]})
        elif v.co[0] < 0:
            vco = roundtuple(tuple((abs(v.co[0]),*v.co[1::])), prec, scale=scale)
            if verts[vidx].select == True:
                selvertsR.append((vco, vidx))
            try:
                vcodictR[vco].append(vidx)
            except:
                vcodictR.update({vco: [vidx]})

    return selvertsL, vcodictL, selvertsR, vcodictR

def mirror_selector(mirror_verts, mirror_dict, obj=None):
    mode = set_mode('OBJECT')
    obj = bpy.context.scene.objects.active
    mesh = bpy.data.objects[obj.name].data.name
    verts = bpy.data.meshes[mesh].vertices
    errs = []
    for v in mirror_verts:
        vco, vindex = v
        try:
            for vert in mirror_dict[vco]:
                verts[vert].select = True
        except Exception as e:
            errs.append(e, vindex)
    set_mode(mode)
    return errs

@defac
def mirror_sel(vdata=None, cutoff=.001, type="both", extend=True, scale=1, basis=True, active_key=False, prec=4,
               obj=None):
    locs = dict(locals())
    locs.pop("vdata")

    mode = set_mode('OBJECT')
    if vdata == None:
        vdata = find_mirror(**locs)
    selvertsL, vcodictL, selvertsR, vcodictR = vdata

    tdict = {"l>r": ((selvertsL, vcodictR),), "r>l": ((selvertsL, vcodictR),),
             "both": ((selvertsL, vcodictR), (selvertsR, vcodictL),)}
    for vs, vdict in tdict[type]:
        mirror_selector(vs, vdict, obj=obj)

    set_mode(mode)
    return vdata

@defac
def mirror_weight(vdata=None, cutoff=.001, type="both", scale=1, basis=True, active_key=False, prec=4,
               obj=None):
    pass

#########################################################その他
@bm_install
@defac
def first_weld(obj=None, bm=None):
    mesh = obj.data
    verts = mesh.vertices

    parts = get_separated_parts(obj=obj)
    for p in range(1, len(parts)):
        verts[parts[p - 1][1]].co = verts[parts[p][0]].co

    return bm
