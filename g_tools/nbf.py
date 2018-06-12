# -*- coding: utf-8 -*-
#便利？関数集。ぶっちゃけ罪です
import re
from itertools import *
from functools import *
from mathutils import Vector,Euler,Quaternion,Matrix
from math import floor,sqrt,sin,cos,tan,asin,acos,atan,atan2,pi
from string import ascii_letters,whitespace
from random import random,randrange

gen = type((z for z in ()))
    
    
#########################################################decorators
def inverterate(f):
    """
    関数の真偽と見た戻り値を反転する
    ex:
        inverterate(lambda: 5)() = False
    大体map用
    """
    def inverted(*args,**kwargs):
        return not f(*args,**kwargs)
    return inverted
    
def oneverterate(f):
    def oneverted(*args,**kwargs):
        return 1 - f(*args,**kwargs)
    return oneverted
    
def negaterate(f):
    def negated(*args,**kwargs):
        return -1*f(*args,**kwargs)
    return negated
    
def argreorder(f,new_order,*args):
    def f2():
        return f(*tuple(reorder(args,new_order)),**kwargs)
    return f2
    
def tuplize(f):
    def tuplized(*args,**kwargs):
        return tuple(f(*args,**kwargs))
    return tuplized
    
    
#########################################################fp
def cons(a,b):
    return (a,b)
    
def delay(exp):
    def expret():
        return exp
    return expret
    
def force(exp):
    return exp()    
    
def mapcan(lst1,lst2):
    return zip(lst1,lst2)
    
def pair_up(lst,pairnum = 2,unpairable_check = True,cut_unpairable = True):
    """
    Zip an iterable into an iterable of tuples of length pairnum.
    Ex: Zips (1,2,3,4,5,6) into ((1,2),(3,4),(5,6)) with the argument pairnum as 2.
    Args:
        lst: 
            some iterable
        pairnum:
            number of items to zip together
    Keyword args:
        unpairable_check:
            Check if the items will fit evenly into the list.
        cut_unpairable:
            If they won't, cut the last set.
    """
    paired = tuple((lst[i:i+pairnum]) for i in range(0,len(lst),pairnum))
    if unpairable_check:
        ratio = len(lst)/pairnum
        required = len(lst)%pairnum
        is_fully_pairable = required ==  0
        if not is_fully_pairable:
            if cut_unpairable:
                paired = paired[0:-(pairnum-required)]
            else:
                raise ValueError
    return paired
    
def chain_up(lst,):
    return zip_longest(lst,lst_shift(lst))
    
def by_x(lst,step):
    return (lst[n:step+n] for n in range(0,int(len(lst)),step))
    
def andmap(f,c):
    if len(c) == 0:
        return True
    for i in c:
        res = f(i)
        if not res:
            return False
    return res
    
def ormap(f,c):
    if len(c) == 0:
        return False
    for i in c:
        res = f(i)
        if not res:
            continue
        else:
            return res
    return False
    
def passmap(*args,**kwargs):
    for x in map(*args,**kwargs): 
        pass
        
def anymap(*args,**kwargs):
    return any(map(*args,**kwargs))

def allmap(*args,**kwargs):
    return all(map(*args,**kwargs))
    
def id_func(x):
    return x
    
def edict(i):
    """
    enumからdictを作成。iはiterableでなきゃならない。
    """
    return {item[1]:item[0] for item in enumerate(i)}
    
def edict2(*args):
    """
    複数の因数からdictを作成。iはiterableでなきゃならない。
    """
    return {i[1]:i[0] for i in enumerate(args)}
    
def edict3(**kwargs):
    """
    複数のキーワード因数からdictを作成。
    """
    return {i:kwargs[i] for i in kwargs}
    
def attrmap(coll,prop,val):
    return any(map(lambda x:setattr(x,prop,val),coll))

def accmap(coll,prop,val):
    return any(map(lambda x:setattr(acc(x),prop,acc(val),coll)))
    
def gattrmap(prop,coll):
    return any(map(lambda x:getattr(x,prop),coll))

def fmap(f,coll,*args,**kwargs):
    return any(map(lambda x: f(x,*args,**kwargs),coll))

def lenconv(x):
    try:
        l = len(x)
    except:
        return (x,)
    
def rec_unmap(x,unpack_hint = None,use_try = False,tuplize = False):
    if tuplize:
        return tuple(rec_unmap(x,unpack_hint = unpack_hint,use_try = use_try,tuplize = False))
    for y in x:
        if type(y) == map:
            for z in rec_unmap(y):
                yield z
        else:
            yield y
            
def sreduce(f,c,*init_args,init_func = None,**init_kwargs):
    if init_func == None:
        def init_func(*args,**kwargs):
            return ()
    return reduce(f,(init_func(*init_args,**init_kwargs),*c))
    
def sreduce_offset(start_indices,strings,offset_end = 1,offset_start = 0):
    return reduce(lambda x,y: (*x,start_indices[x+1]-x[-1]) ,((start_indices[offset_start:offset]),*start_indices[offset::]))
    
def sreduce_wrap(start_indices,strings,offset_end = 1,offset_start = 0):
    return reduce(lambda x,y: (*x,start_indices[x+1]-x[-1]) ,(*(start_indices[offset_start:offset]),*start_indices[offset::]))
    
def reduce_wrap(f,lst,offset_end = 1,offset_start = 0):
    return reduce(f,lstwrap(lst,offset_start,offset_end))
    
def lstwrap(lst,offset_start,offset_end,match_type = True,rev = False):
    if rev:
        lst = lst[::1]
    res = tuple((*lst[offset_start:offset_end],*lst[offset_end::],*lst[0:offset_start]))
    if match_type:
        res = type_match(lst,res)
    return res
    
def format_squeeze(start_indices,strings):
    space = reduce(lambda x,y: (*x,start_indices[x+1]-x[-1]) ,((start_indices[0]),*start_indices[1::]))
    
def frange(f,*args):
    return (f(i) for i in range(*args))
    
@tuplize
def tfrange(f,*args):
    return (f(i) for i in range(*args))
    
#########################################################collection filtering/gathering
def unpack(l):
    """King of king."""
    return reduce(lambda x,y: (*x,*y),l)
    
def filter_by_prop(coll,propname,propval,mode = 0,checkfunc = None):
    if mode != 0:
        return filter_by_prop_iter(coll,propname,propval,checkfunc = checkfunc)
    if checkfunc == None:
        def checkfunc(x):
            return getattr(x,propname) == propval
    return tuple(filter(checkfunc,coll))
    
def filter_by_name(target_name,lst,pref = "",suf = "",extract = False,name_prop = "name",getf = getattr,do_negate = False):
    if extract:
        lst = (getf(i,name_prop) for i in lst)
    return filter(lambda iname: cnegate(re.search(pref+target_name+suf,iname[1]),condition = do_negate),enumerate(lst))
    

#########################################################geometry
def get_midpoint(a,b):
    return lerp(a,b,.5)
    
def get_angle(co,d):
    if (co[0] > 0):
        return pi + (pi - acos(d))
    else:
        return acos(d)

def get_rad(vec,axis = (0,1,0)):
    axis = Vector(axis)
    c = vec.normalized()
    d = c.dot(axis)
    a = get_angle(-c,d)
    return a
    
def get_deg(vec,axis = (0,1,0)):
    return degrees(get_rad(vec,axis = axis))
    
def unrotate(vec,idx_order = (0,1)):
    """これは酷い、助けて、死にたい"""
    idmat = ((1,0,0),(0,1,0),(0,0,1))
    idmat = Matrix(idmat)
    zv = Vector((0,0,0))
    eus = []
    op_vec = vec.copy()
    for i in idx_order:
        dotaxis = (i+1)%3
        rotaxis = (dotaxis+1)%3
        v2 = zv.copy()
        v6 = (*op_vec,*op_vec)
        n = Vector(v6[i:i+2]).normalized()
        for x in range(2):
            v2[((i+x)%3)] = n[x]
        
        r = get_rad(v2,axis = idmat[dotaxis])
        euler_rot = Euler((idmat[rotaxis])*r)
        eus.append(euler_rot)
        op_vec.rotate(euler_rot)
    
    eus = (*eus,Euler((0,radians(90),0)),)
    return eus
    
#########################################################assignment
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

def prop_copy(pyobj,prop_source,excludes = None):
    if type(prop_source) == dict:
        property_dictionary = prop_source
    else:
        property_dictionary = prop_dict(prop_source)
    
    errs = [property_dictionary[i] for i in property_dictionary]
    
    if excludes != None:
        for i in excludes:
            property_dictionary.pop(i)
    for idx,x in enumerate(property_dictionary):
        try:
            item = property_dictionary[x]
            if item == "#_GET_ERR":
                continue
            setattr(pyobj,x,item)
        except Exception as e:
            errs[idx] = e
    return errs
    
#########################################################iterable関連
def lst_shift(lst,count = 1):
    for x in range(count):
        lst.append(lst.pop(0))
    return lst
    
def lst_shift_ex(lst,count = 1):
    lst_new = lst[count:len(lst)]+lst[0:count]
    lst.clear()
    lst += lst_new
    return lst
    
#########################################################数学？
def saturate(chk_val,max = 1, min = 0):
    if chk_val > max:
        chk_val = max
    if chk_val < min:
        chk_val = min
    return chk_val
    
def normalize(vec):
    s = sum(vec)
    return tuple(i/s for i in vec)
    
def lnormalize(vec):
    s = sum(vec)
    return tuple(i/s for i in vec)
    
#for working with mathutils objects
def dot2(x,y):
    return x.dot(y)    
    
def cross2(x,y):
    return x.cross(y)
    
#########################numerical analysis
def even(n):
    return n%2 == 0
    
def odd(n):
    return n%2 != 0

def is_prime(n):
    if n == 2:
        return n
    elif n < 2:
        return False
    elif even(n):
        return False

    sqrt_n = int(floor(sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def prime_range(target_count):
    l = ()
    c = 1
    while len(l) < target_count:
        if is_prime(c):
            l = postjoin(c,l)
        c+=1
    return l
    
def pi_range(res):
    return (0,*tuple((pi/res)*r for r in range(1,res)))
def tau_range(res):
    tau = pi*2
    return (0,*tuple((tau/res)*r for r in range(1,res)))
#########################set analysis

def even_length(res):
    return even(len(res))

def odd_length(res):
    return odd(len(res))
    
#########################set creation
def expand(f,v,*args,**kwargs):
    return map(id_func,f(v,*args,**kwargs))
    
#########################boolean関連
def bool_to_negpos(b):
    return (-1+b*2)

def check_prev_exists(idx,lencoll):
    if lencoll < 2:
        return 0
    return idx > 0

def check_next_exists(idx,lencoll):
    if lencoll < 2:
        return 0
    return idx < (lencoll-1)
    
#########################################################ごみでしょう。いい子は真似しない#########################################################

def rlen(x,*args):
    defaults = (0,0,1)
    start,sub,step = default_fill(args,defaults)
    end = len(x)-sub
    return range(start,end,step)
    
def argize(*args):
    return args
    
def kwargize(**kwargs):
    return kwargs
    
def exclude(l,targets):
    return list(x for x in l if x not in targets)
    
def multisplit(target_string,targets):
    return re.split(r'['+''.join(targets)+']',target_string)
    
#########################################################arg analysis
def split_signature(sig):
    arglist = str(sig)[1:-1].split(",")
    argtypes = [0 for a in arglist]
    kwdict = {}
    arglist2 = []
    for a in range(len(arglist)):
        v = arglist[a].split("=")        
        if len(v) > 1:
            kwdict.update({v[0]:eval(v[1])})
            argtypes[a] = 1
        else:
            arglist2.append(v[0])
    return (kwdict,arglist2,argtypes)
    
def argfill(expected,*args):
    diff = (expected-len(args))
    return (*args,*(None for x in range(diff*int(diff>0))))

def default_fill(args,defaults):
    args = argfill(len(defaults),*args)
    return tuple(args[a] if not none_test(args[a]) else defaults[a] for a in range(3))
    