# -*- coding: utf-8 -*-
import bpy
from .. import gtls
from g_tools.gtls import defac,defac2,set_mode,set_ac
from g_tools.nbf import *

@defac
def make_point_arm_mod(name,obj = None,sobj = None):
    mod = make_mod(name,"ARMATURE",obj = obj,)
    props = {"use_vertex_groups":False,"use_bone_envelopes":True,"object":sobj,"show_in_editmode":True,"use_apply_on_spline":True}
    prop_copy(mod,props)
    return mod
    
@defac
def make_mod(name,type,obj = None):
    return obj.modifiers.new(name = name,type = type)
    
@defac
def make_modifier_shapes(obj = None,target_mod = "Armature"):
    ctx = bpy.context
    scn = ctx.scene
    objs = scn.objects
    cf = scn.frame_current
    
    mods = obj.modifiers
    arm_mod = tuple((m for m in mods if m.name == target_mod))[0]
    mname = arm_mod.name
    
    fs = scn.frame_start
    fe = scn.frame_end
    fr_range = range(fs,fe)
    
    for x in (fr_range):
        scn.frame_set(x)
        bpy.ops.object.modifier_copy(modifier = mname)
        bpy.ops.object.modifier_apply(modifier = mods[-1].name, apply_as='SHAPE')
    
    scn.frame_set(cf)