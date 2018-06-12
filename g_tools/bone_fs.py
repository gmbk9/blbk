# -*- coding: utf-8 -*-
import bpy
from g_tools.nbf import *
from . import gtls
from g_tools.gtls import defac,set_mode,set_ac
from mathutils import Vector,Euler,Quaternion,Matrix

@defac
def set_minimum_envelopes(obj = None):
    ac = set_ac(obj)
    mode = set_mode("EDIT")
    for b in obj.data.edit_bones:
        b.envelope_distance = 0
        b.head_radius = .0001
        b.tail_radius = .0001
    set_mode(mode)
    set_ac(ac)

def bone_exists(bname,bones):
    try:
        b = bones[bname]
    except:
        return 0
    return 1

def init_new_bone(ebones):
    newbone = ebones.new(name = "temp")
    newbone.head = Vector((0,0,0))
    newbone.tail = Vector((0,1,0))
    newbone.roll = 0
    return newbone
    
@defac
def make_bone(name = "Bone",obj = None,autoswitch = True,loc = None,dir = None,scale = .05,parent = None,props = {}):
    if loc == None:
        loc = (0,0,0)
    if dir == None:
        dir = (0,1,0)
    if autoswitch:
        ac = set_ac(obj)
        mode = set_mode("EDIT")
        ebones = obj.data.edit_bones
        newbone = init_new_bone(ebones)
        newbone.name = name
    else:
        ebones = obj.data.edit_bones
        newbone = init_new_bone(ebones)
        newbone.name = name
        
    if loc != None:
        newbone.head = loc
        newbone.tail = Vector(loc) + Vector(dir)*scale
    if parent:
        newbone.parent = parent
    prop_copy(newbone,props)
    set_mode(mode)
    set_ac(ac)
    return newbone
