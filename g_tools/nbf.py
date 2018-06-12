# -*- coding: utf-8 -*-
#便利？関数集。ぶっちゃけ罪です
import re
from itertools import *
from functools import *
from mathutils import Vector,Euler,Quaternion,Matrix
from math import floor,sqrt,sin,cos,tan,asin,acos,atan,atan2,pi

gentype = type((z for z in ()))

#########################################################decorators
def inverterate(f):
    def inverted(*args,**kwargs):
        return not f(*args,**kwargs)
    return inverted
    
def setvec(i,idx,val):
    i[idx] = val[idx]
    return None
    
def getidx(i,idx):
    return i[idx]
    
def setidx(i,idx,val):
    i[idx] = val
    return None
    
def setattr2(i,prop,val):
    """
    setattr, but if passed an integer set the value of the index i.
    Will fail on immutable data.
    """
    if type(prop == int):
        setidx(i,prop,val)
    else:
        setattr(i,prop,val)
        
def try_setattr(i,prop,val):
    try:
        return setattr2(i,prop,val)
    except:
        return 0
        
def dict2attr(obj,attrdict):
    return any(map(lambda attr: try_setattr(obj,attr,attrdict[attr]),attrdict.keys()))
    