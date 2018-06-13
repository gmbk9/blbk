from gsrc import *
import os
import operator
import re
import inspect
import time
from string import ascii_letters,whitespace
from random import random,randrange
from itertools import *
from functools import *
from mathutils import Vector,Euler,Quaternion,Matrix
from math import floor,sqrt,sin,cos,tan,asin,acos,atan,atan2,pi
tau = pi*2
from what import *
from m.n_anlys import *
DEFAULT_HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
DEFAULT_DRIVE = "C"
SYS_PTH = DEFAULT_DRIVE + r":\\Windows\\System32"
gentype = type((z for z in ()))
stime = time.clock()
ptime = [time.clock()]
tt = tuple
ts = list
tx = set
ee = enumerate
#macro tag
mtag = "#@^"
#null tag
ntag = "#!@"
def inf(c=0):
    while True:
        yield c
        c+=1

class IO_MODE_ERR(Exception):
    pass

#########################################################decorators

def mode_error(acceptable_modes = ("r","rb"),default = "r"):
    def f1(f):
        def f2(fpath,*args,**kwargs):
            #if passed more than one argument, assume the second is a mode
            if len(args):
                mode = args[0]
            else:
                mode = default
            if mode not in ('r','rb'):
                raise IO_MODE_ERR
            return f(fpath,mode,*args,**kwargs)
        return f2
    return f1

def mode_check(mode,acceptable_modes = ("r","rb")):
    if mode not in acceptable_modes:
        raise IO_MODE_ERR
    return mode

def delta_getterate(coll,props):    
    def delta_getterator(f):
        def delta_getterated(*args,**kwargs):
            def getterator(i):
                accer = partial(acc,i)
                return tuple(map(accer,props))
            coll_before = tuple(map(getterator,coll))
            res = f(*args,**kwargs)
            coll_after = tuple(map(getterator,coll))
            return res,coll_before,call_after
        return delta_getterated
    return delta_getterator

def inverterate(f):
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
    
def argreverse(f,*args,**kwargs):
    def reversed():
        return f(*args[::-1],**kwargs)
    return reversed

def argreorder(f,new_order,*args):
    def f2():
        return f(*tuple(reorder(args,new_order)),**kwargs)
    return f2
#the finest decorator
def r(f):
    print('r')
    
def kwargs_to_props(f):
    def kwargs_to_propped(*args,**kwargs):
        print(args,kwargs,f)
        kwdict,*a = get_arg_data(f)
        pass_kwargs = {kw:kwargs[kw] for kw in kwargs if kw in kwdict}
                
        res = f(*args,**pass_kwargs)
        for i in kwargs:
            if i not in kwdict:
                setattr(res,i,kwargs[i])
        return res
    return kwargs_to_propped
    
def id_dec(f):
    return id_func(f)

def aliasate(gs,*names):
    def aliasator(f):
        def aliasated(*args,**kwargs):
            return f(*args,**kwargs)
        gs.update({n:aliasated for n in names})
        return aliasated
    return aliasator
 
def tag_fn(fn,tag = "_OUT"):
    spl = fn.split(".")
    return ".".join((*spl[0:-1],tag,spl[-1]))
    
def collection_versionate(env,collection_types,base_name = "",delim = "_",name_list = ()):
    def wrapper(f):
        _fdict = {}
        def subwrapper(t,*args,**kwargs):
            return t(wrapped(*args,**kwargs))
        def wrapped(*args,**kwargs):
            return f(*args,**kwargs)
        #prioritize a base name
        if base_name == "":
            base_name_list = tuple(f.__name__ + "_" for t in collection_types)
        #if no base name was provided and name_list is nil, append the type function as a string to the given function's registered("magic method") name
        elif name_list == ():
            base_name_list = tuple(f.__name__ + "_" for t in collection_types) 
        else:
            base_name_list = name_list
        
        print("BNL",base_name_list)
        _fdict = {base_name_list[tidx] + str(t).split("'")[1]:partial(subwrapper,t) for tidx,t in enumerate(collection_types)}
        print(_fdict)
        
        env.update(_fdict)
        
        return f
    return wrapper
#testing decorator splitting... my deepest apologies
def ctx_exec(ctx,null_cases,f,*args,ret = None,**kwargs):
    if any(context_test(ctx,null_cases)):
        return None
    return f(*args,**kwargs)
def ctx_exec_d1(ctx,null_cases,f,ret = None,):
    return partial(ctx_exec,ctx,null_cases,f,ret = ret)
def ctx_exec_d2(ctx,null_cases,ret = None):
    '''
    Inputs:
        ctx: Context dictionary; a hash table relating strings to
            the result of case tests done elsewhere.
        null_cases:
            Cases in which to cancel execution.
        ret:
            Cancelled return value.
    Determine whether to execute function f by doing hash table lookups.
    Return ret(default None) upon cancelled execution.
    EX: If the case represented by string "IS_MY_CODE" is registered as True, cancel execution, returning ret.
    '''
    return partial(ctx_exec_d1,ctx,null_cases,ret=ret)
    
def tuplize(f):
    def tuplized(*args,**kwargs):
        return tuple(f(*args,**kwargs))
    return tuplized
    
def tuplize_input(f):
    def altered(*args,**kwargs):
        return f(tuple(tuple(a) for a in args),**kwargs)

def anyize(f):
    def anyized(*args,**kwargs):
        return any(f(*args,**kwargs))
    
def allize(f):
    def allized(*args,**kwargs):
        return all(f(*args,**kwargs))    

def capturate(f):
    '''Detect a side-effect change in collection coll as a result of executing some function'''
    def capturated(coll,*args,**kwargs):
        return capture(coll,f,*args,**kwargs)
    return capturated

def decoratorate(f1):
    def decoratorated():
        def decorated(*args,**kwargs):
            return f1(*args,**kwargs)
        return decorated
    return decoratorated

#if defined iteratively(i.e. without star unpacking) could be used for creating a function with partial parameters depending on external state?
#gorrible
def partialize(f,*args,**kwargs):
    def partialized(*args2,**kwargs2):
        return f(*args,*args2,**kwargs,**kwargs2)
    return partialized

def has_depth(item):
    try:
        for i in item:
            return True
    except:
        return False
    
    
def has_nested_depth(lst):
    for i in lst:
        try:
            for i2 in i:
                return True
        except:
            continue
    return False
    
def garbageize(f,args = None,kwargs = None):
    arglist = tuple(a for a in args)
    kwarglist = {kwargs[kw] for k in kwargs}
    def garbageized(args2 = None,kwargs2 = None):
        arglist2 = tuple(a for a in args2)
        kwarglist2 = {kwargs2[kw] for k in kwargs2}
        arglist = reduce(lambda x,y: (*x,*y),((a for a in args),(a for a in args2)))
        #update AND overwrite
        kwarglist.update(kwarglist2)
        return f(*arglist,**kwarglist1)
    return garbageize
    
def garbageize2(f,args = None,kwargs = None):
    def garbageized2(args2 = None,kwargs2 = None):
        arglist = reduce(lambda x,y: (*x,*y),((a for a in args),(a for a in args2)))
        return f(*arglist,**({kwargs[kw] for k in kwargs}.update({kwargs2[kw] for k in kwargs2})))
    return garbageize
    
#########################################################file nonsense        
def fdir(fpath):
    return "\\".join(fpath.split("\\")[0:-1])
        
def fdirexists(fpath):
    from os.path import exists
    return exists(fdir(fpath))
    
        
def fexists(fpath):
    from os.path import exists
    return exists(fpath)
        
def ftest(fpath):
    from os.path import isfile,isdir
    if isfile(fpath):
        return 1
    elif isdir(fpath):
        return 2
    return 0

def fcreate(fpath,encoding = "utf-8"):
    if not fdirexists(fpath):
        os.mkdir(fdir(fpath))
    fwrite(fpath,"","w",encoding = encoding)
    
def fread(fpath,mode = 'r',encoding = "utf-8"):
    if 'w' in mode:
        raise ValueError
    elif mode != 'rb':
        with open(fpath,mode,encoding = encoding) as e: return e.read()
    with open(fpath,mode) as e: return e.read()
def fsplit(fpath,mode,encoding = "utf-8",nl = "\n"):
    with open(fpath,mode,encoding = encoding) as e: return e.read().split(nl)
    
def fwrite(fpath,target_data,mode,encoding = "utf-8"):
    with open(fpath,mode,encoding = encoding) as e: return e.write(target_data)

def fappend(fpath,target_data,encoding = "utf-8"):
    with open(fpath,'a',encoding = encoding) as e: return e.write(target_data)

def finsert(fpath,foutpath,data,mode = 's',line_pos = -1,string_pos = 0):
    fstrs = fsplit(fpath,mode='r')
    target_line = fstrs.pop(line_pos)
    insert_point = (target_line[0:string_pos],target_line[string_pos::])
    inserted = (insert_point[0],*data,insert_point[1])
    fstrs.insert(pos,"".join(inserted))
    fwrite(foutpath,fstrs,mode = 'w')

def fscan(fil,sterm,start_pos = 0):
    def _getline(l,_fil):
        l[0] = _fil.readline()
        return l[0] != ''
    for line in fil:
        pass
    fend = fil.tell()
    fil.seek(start_pos)
    c = 0
    line = [""]
    fpos = 0
    while _getline(line,fil):
        if sterm in line[0]:
            break
        elif c > fend:
            break
        c+=1
        fpos = fil.tell()
    
    fil.seek(fpos)
    return (fil,c,fpos)

def idx_select(c,idx):
    return tuple(item[idx] for item in tuple(c))
def ifilter(c1,c2):
    res = tmap(lambda idx: c2[idx],filter(lambda i:c1[i],rlen(c2)))
    print(len(res),len(c2))
    return res

def f2dict(fpath,mode = "r"):
    """
    Convert a file into a dictionary intepreting lines as repeating key,value pairs
    """
    return {l[0]:l[1] for l in by_x(fsplit(fpath,mode),2)}

def csvdict(fpath,mode = "r",delim = ","):
    """
    Convert a csv file into a dictionary intepreting delimiters as repeating key,value pairs
    """
    return {l[0]:l[1] for l in by_x(fread(fpath,mode).split(delim),2)}
    
def fresult_hash(f,*args,**kwargs):
    return {fdict[f.__name__]:f(*args,**kwargs)}
    
def fresult_dict(fs,arglists,kwarglists):
    fdict = {}
    result_hashes = tmap(lambda i: fresult_hash(fs[i],*arglists[i],**kwarglists[i]),rlen(fs))
    reduce(lambda x,y: fdict.update(y),((),*result_hashes))
    return fdict
    
def ws_test(s):
    return re.search(r"[^\s]",s)        
def ws_filter(coll):
    return filter(ws_test,coll)
def tws_filter(coll):
    return tuple(filter(ws_test,coll))
def tfilter(f,c):
    return tuple(filter(f,c))
    
def mem_install(init = None,mem = None):
    if mem == None:
        mem = [init]
    def mem_installer(f):
        def mem_installed(*args,**kwargs):
            return f(mem = mem,*args,**kwargs)
        return mem_installed
    return mem_installer
    
def etime():
    return time.clock() - stime 

@mem_install(init = time.clock())
def dtime(mem = None):
    """Given a global timer, return the time difference between now and the last call to self."""
    mem[0] = time.clock() - mem[0]
    return mem[0]
    
def fpack(f,*args,**kwargs):
    """
    Pack a function and its arguments into the format:
    Tuple#2:
        f
        Tuple#2:
            arguments,keyword arguments
    """
    return (f,args,kwargs)

'''
def fpack2(f,*args,**kwargs):
    """
    Pack a function and its arguments into the format:
    Tuple#1xy:
        f, x arguments, y keyword arguments
    """
    return (f,*args,**kwargs)
'''
    
def funpack(fpack):
    """
    Execute a function, packed arguments pair.
    """
    return fpack[0](*fpack[1],**fpack[2])

def nullf():
    pass

def cforce(y):
    if type(y) == type(nullf):
        return y()
    return y

def cforce_rec(y):
    if type(y) == type(nullf):
        return cforce_rec(y())
    return y

def wrapmap(x,y):
    def wrapped(*args,**kwargs):
        return y(cforce(x))
    return wrapped
def wrapmap2(x,y):
    def wrapped(*args,**kwargs):
        return y(x)
    return wrapped
    
def wreduce(f,c):
    """
    Wrap the first element of a generator or collection in functional form and reduce it.
    For when you want to apply one function of two arguments that unconditionally calls the first... I guess.
    """
    #if the collection is a stream
    if type(c) not in (list,tuple,set):
        for x in c:
            y = lambda *args,**kwargs:c[0]
            break
        c2 = (y,c)
    #if it's an immediate collection
    else:
        c2 = (lambda *args,**kwargs: c[0],*c[1::])
    return reduce(f,c2)
    
##try multiple different encodings before returning None if all fail
##if try_all == True:
##   return file stream upon success
##if test_idx != None:
##   tries the encoding matching the index only
def enc_open(fpath,mode = 'r',encs = ('ascii','utf-8','shift-jis'),test_idx = None,try_all = False):
    def tr(fpath,mode = 'r',encoding = None):
        try:
            return open(fpath,mode,encoding = enc)
        except:
            pass
        return None
    if test_idx:
        test_range = range(test_idx,test_idx+1)
    else:   
        test_range = rlen(encs)
        
    for idx in rlen(encs):
        e = encs[idx]
        attempt = tr(fpath,mode=mode,encoding=e)
        if attempt:
            return attempt
    return None

def lstfill(required,args):
    arglen = len(args)
    diff = (required-arglen)
    return (*args,*(None for x in range(diff*int(diff>0))))
    
    '''
    arglen = len(args)
    if arglen == 1:
        args == args[0]
        arglen = len(args)
    diff = (expected-arglen)
    return (*args,*(None for x in range(diff*int(diff>0))))
    '''
    
def setidx(i,idx,val):
    i[idx] = val
    return None
    
def setvec(i,idx,val):
    i[idx] = val[idx]
    return None

def getidx(i,idx):
    return i[idx]
    
def none_test(x):
    """
    A test for Noneality.
    """
    if x == None:
        return 1
    return 0
    
def getattr2(i,prop):
    """
    getattr, but if passed an integer get the value fo the index i.
    may have unintended effects if there's an occasion where integers are actually used as a property.
    """
    if type(prop == int):
        return getidx(i,prop)
    
def setattr2(i,prop,val):
    """
    setattr, but if passed an integer set the value of the index i.
    will fail on immutable data.
    """
    if type(prop == int):
        setidx(i,prop,val)

def retpoint(f,*args,**kwargs):
    def delayed():            
        try:
            return f(*args,**kwargs)
        except Exception as e:
            return e
    return delayed
    
def try_wrap(f):
    def try_wrapped(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except:
            return "#@!TRYWRAP_EXEC_ERR"
    return try_wrapped
    
def try_f(f,*args,**kwargs):
    try:
        return f(*args,**kwargs)
    except:
        return "#@!TRYWRAP_EXEC_ERR"
    
def try_wrap2(f1,f2,a1 = None,kw1 = None,a2 = None,kw2 = None):
    if a1 == None:
        a1 = ()
    if kw1 == None:
        kw1 = {}
    if a2 == None:
        a2 = ()
    if kw2 == None:
        kw2 = {}
        
    try:
        return f1(*a1,**kw1)
    except:
        return f2(*a2,**kw2) 
trywrap = try_wrap

def trap(i):
    return (i,)

def trygetattr(prop,val):
    try:
        return getattr2(prop,val)
    except:
        return "@#TRYGETATTR_ERR!"
        
def trysetattr(i,prop,val):
    try:
        return setattr2(i,prop,val)
    except:
        return 0
        
def get_fn(fpath):
    return fpath.split("\\")[-1].split(".")[0]
    
def dual_prop_filter(coll,prop1 = "select",val1 = True,prop2 = "lock",val2 = True):
    """
    For when they provide that selection feature but not information about the most current selection.
    """
    sel1 = tuple(filter_by_prop(coll,prop1,val1))
    if len(sel1) < 2:
        raise ValueError("Did not detect enough items with property: ",prop1, " as ",val1)
    sel2 = tuple(filter_by_prop(sel1,prop2,val2))
    if len(sel2) == 0:
        raise ValueError("Did not detect enough items with property: ",prop2, " as ",val2)

    res1 = locked_tracks[0]
    res2 = tfilter(lambda i: i != res1,sel1)[0]
    return res1,res2   
    
#########################################################data,numbers,etc
def rangerator(data,fanc):
    return fanc(range(*data))

def strange():
    return fanc(range(*data))
    
def type_match(x,y):
    print(x,y)
    return (type(x))(y)
    
def recsplit(split_targets,s):
    def splitterate(x,y):
        if type(x) != str:
            return map(lambda item: splitterate(item,y),x)
        else:
            return x.split(y)
    return reduce(splitterate,([s,],*split_targets))

#########################################################folder searching

#old
def scan_folder(filepath):
    empt = []
    try:
        folder = os.listdir(filepath)
        #name of the current folder we're searching
        for file in folder:
            if "." in file:
                if "keaw" in file.lower():
                    txtxt.write(file +nl)
                    txtxt.write(filepath+nl)
                    #print(file,"              ",filepath.split("\\")[-1])
                pyfiles.append(filepath + r'''\\''' + file)
            else:
                #print(fold)
                folpath = filepath + r'''\\''' + file
                empt.append(folpath)
    #except Exception as e:
    except:
        pass
        #p(str(e))
    return empt

####################byte-related
def get_byte_length(filepath,size):
    """Open filepath and return its size in bytes"""
    with open(filepath,'rb') as binfil: return len(binfil.read())
def pretest_byte_length(filepath,size):
    """Open a filepath and check if it is at least as long as size argument"""
    with open(filepath,'rb') as binfil:
        c=0
        while binfil.read(size) != b'':
            c+=1
    return c

####################oct

####################dec

####################hex
    
####################bit
def bincheck(n):
    zero_str = '00000000'
    if n:
        binrep = bin(n)[2::]
        binrep = zero_str[0:(8-(len(binrep)))]+binrep
        return binrep
    else:
        return zero_str

#########################################################data tagging/encoding
def __tag(item,tag):
    return (item,tag)
    
def append_tag(i,tag):
    return (*i,tag)
    
def iter_tag(i,tag):
    def item_tag(item):
        return __tag(item,tag)
    return map(item_tag,i)

def dict_tag(i,tag):
    i[tag] = (tag,tag)
    
def dict_tag(i,tag_key,tag):
    i[tag_key] = tag
    
def dict_val_tag():
    def item_tag(item):
        i[item] = (i[item],tag)
    return map(item_tag,i)
    
#append a tag to some function's return result; the result is packed into a tuple with the tag
def f_tag(tag,f,*args,**kwargs):
    return (f(*args,**kwargs),tag)

def op_taggerate(tag,tag_op = None):
    '''Append a tag to some function's return result as a decorator; defaults to the + operator'''
    if tag_op == None:
        def tag_op(a,b):
            return a+b
    def tagger(f):
        def tagged(*args,**kwargs):
            return tag_op(f(*args,**kwargs),tag)
        return tagged
    return tagger
    
def taggerate(tag):
    '''Append a tag to some function's return result as a decorator; the result is packed into a tuple with the tag'''
    def tagger(f):
        def tagged(*args,**kwargs):
            return (f(*args,**kwargs),tag)
        return tagged
    return tagger
    
def xor_enc(a,b):
    """
    XOR "encode"
    """
    return a^b
def xor_dec(b,a):
    """
    Not really necessary but seeing it jogs memory.
    """
    return b^a
    
    
#########################################################string formatting
def strcap(s,reqlen):
    len_s = len(s)
    if len_s < reqlen:
        s += " "*(reqlen-len_s)
    return s

def sfit(data,target_positions,auto_length = False,spacing_size = -1,spacing = "    ",filler = "...",dbg = 1):
    #if passed a list of str,int elements, reorganize the list for compatibility
    fmt_spec_mode = (type(data[0]) == str and type(data[1]) == str)
    if fmt_spec_mode == 0:
        data,target_positions = (tuple(data[i] for i in range(0,len(data),2)),tuple(data[i] for i in range(1,len(data),2)))

    lenfill = len(filler)
    
    #determine the largest length between any two position elements to use as a basis
    target_pos = target_positions
    deltas = reduce(lambda x,y: (*x,target_pos[y+1]-target_pos[y]),((),*range(0,len(target_positions)-1)))
    deltas = (*deltas,len(data[-1])+len(spacing))
    max_delta = max(deltas)
    if auto_length:
        md = tuple(max_delta for i in data)
    elif spacing_size > -1:
        md = tuple(spacing_size for i in data)
    else:
        md = deltas
    print(deltas)
    print(md,'hoo')
    #subtract the largest element distance from the filler length to get the fill position
    maxlen = max_delta-len(filler)
    maxlens = tuple(delta-lenfill for delta in md)

    #convert all data to string
    strings = tmap(lambda d: str(d),data)

    #space-fill any data that are less than spacing distance
    #cut and fill any that are longer than the spacing distance
    strings = tmap(lambda d: strcap(strings[d],md[d]) if len(strings[d])<md[d] else strings[d][0:maxlens[d]]+filler,rlen(strings,1))

    #append the spacing element to all strings
    strings = tmap(lambda d: d+spacing,strings)

    #output
    if dbg:
        print("".join(strings))
    return strings
    
#########################################################arg analysis
def argfill(expected,*args):
    diff = (expected-len(args))
    return (*args,*(None for x in range(diff*int(diff>0))))

def default_fill(args,defaults):
    args = argfill(len(defaults),*args)
    return tuple(args[a] if not none_test(args[a]) else defaults[a] for a in range(3))
    
def argfeed(f,a):
    """
    An attempted functional equivalent at calling a function with an argument.
    """
    return partial(f,a)
    
def kwargfeed(f,k):
    """
    An attempted functional equivalent at calling a function with a keyword argument.
    """
    return partial(f,**k)
    
def argprep(f,*args):
    return reduce(argfeed,(f,*args))
    
def kwargprep(f,**kwargs):
    kws = ({kw:kwargs[kw]} for kw in kwargs)
    return reduce(kwargfeed,(f,*kws))
    
def callprep(f,*args,**kwargs):
    return kwargprep(argprep(f,*args),**kwargs)
    
def slowcall(f,*args,**kwargs):
    return callprep(f,*args,**kwargs)()
    
def maybe_try(f,*args):
    try:
        return f(*args,**kwargs)
    except Exception as e:
        pass
    return "{... famished...}"
    
def actually_try(f,*args):
    for i in combinations(args):
        try:
            f(*i)
        except:
            pass
def really_try(f,*args):
    for i in combinations(args):
        try:
            f(*i)
        except:
            pass

def really_really_try(f,*args):
    for i in permutations_rr(args,len(args)+1):
        try:
            return f(*i)
        except Exception as e:
            print(i,e)
            
def argmax(f,*args,**kwargs):
    f2 = partial(f,**kwargs)
    return max(map(f2,*args))
'''            
def permutations_r2(coll,c):
       return (i.send(None) for i in map(lambda x: (i for i in x),map(lambda combs: ((i2 for i2 in (permutations(combs,c)))),
                combinations_with_replacement(coll,c))))
'''
    
def arg_check(data):
    return type(data[1]) == dict
    
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
    
def pass_kwarg_filter(f,local_kwargs):
    kwdict,arglist2,argtypes = get_arg_data(f)
    return {kw:local_kwargs[kw] for kw in local_kwargs if kw in kwdict}
    
def get_arg_data(f):
    argdata = inspect.signature(f)
    kwdict,arglist2,argtypes = split_signature(argdata)
    return kwdict,arglist2,argtypes

#########################################################function composition/scheduling
def compose(f1,f2):
    return f2(f1)
def compose_result(f1,f2,args1 = None,kwargs1 = None,args2 = None,kwargs2 = None,):
    return f2(*args1,**kwargs1)(f1(*args2,**kwargs2))
def compose_argpass(f1,f2,args1 = None,kwargs1 = None,args2 = None,kwargs2 = None,):
    return f2(f1,args1,kwargs1,*args2,**kwargs2,)
def compose_argcall(f1,f2,args1 = None,kwargs1 = None,args2 = None,kwargs2 = None,):
    return f2(f1(*args1,**kwargs1),*args2,**kwargs2,)
def dualize(f1,f2,args1 = None,kwargs1 = None,args2 = None,kwargs2 = None,):
    return f1(*args1,**kwargs1),f2(*args2,**kwargs2)

def f0call(data):
    return data[0]()
    
def f1call(data):
    if arg_check(data):
        return data[0](**data[1])
    return data[0](*data[1])

def f2call(data):
    return data[0](*data[1],**data[2])

def fcall(data):
    types = (None,f0call,f1call,f2call,)
    return types[len(data)](data)
    
def fcall_s(a,b):
    return f(a,b)
    
def fcall_s_inv(a,b):
    return f(b,a)
    
def zeroize(t):
    tdict = {tuple:(),list:[],str:"",int:0,float:0,bool:0,type(None):None,}
    return tdict[t]
    
def meta_invalidate(fdict,*args,**kwargs):
    def meta_invalidator(f):
        if fdict[f] == None:
            return
        def meta_invalidated(*args,**kwargs):
            res = f(*args,**kwargs)
            if fdict[f]:
                try:
                    lenres = len(res)
                    
                except:
                    return zeroize(type)

#########################################################what the fuck is this shit? seriously? who the fuck writes this garbage?
def gt_trans(x):
    if x == 1:
        return ">"
    return "<"
def _gt(a,b):
    return a > b
def _lt(a,b):
    return a < b
def _gte(a,b):
    return a >= b
def _lte(a,b):
    return a <= b
    
def _add(a,b):
    return a+b
def _sub(a,b):
    return a-b
def _pow(a,b):
    return a**b
def _sqrt(a,b):
    return sqrt_n(a,b)
def _log(a,b):
    return log(a,b)
def _ln(a,b):
    return ln(a,b)
def _mult(a,b):
    return a*b
def _div(a,b):
    return a/b

def invert_test(i,c):
    return _gt(_add(i,c))
def invert_test_pair(a,b,inverted = False):
    return ((a,b)[invert_test(inverted,x)] for x in (0,1))

#Functional description of a number of potential python function application patterns.
def fapply(f,x):
    """
    Assume an argument pair: function,arg.
    """
    return f(x)
def fapply_s(q):
    """
    Assume a single, paired argument: q is a function,arg pair.
    """
    return q[0](q[1])
def fapply_args(*args):
    """
    Assume an unknown number of arguments: Assume first is a function.
    """
    f = partial(fapply,args[0])
    return reduce(f,args)
def fapply_args(*args):
    """
    Assume an unknown number of arguments.
    Assume a function f is defined.
    """
    return reduce(f,args)
def fapply_pargs(*args):
    """
    Assume an unknown number of function,argument pairs.
    """
    return reduce(fapply_s,pair_up(args))
def fapply_pargs_inv(*args):
    """
    Assume an unknown number of argument,function pairs.
    """
    return reduce(fapply_s_inv,pair_up(args))
def choose(a,b,c = 0,inverted = 0):
    """
    Choose between A or B by interpreting a boolean value c as an index.
    """
    return (a,b)[invert_test(inverted,c)]
def do_ifin(a,b,f,c = 0):
    if a in b:
        fapply(f,choose(a,b,c))
def do_trex(a,f):
    try:
        fapply(f,a)
    except:
        pass
def knock_knock(f,*args,**kwargs):
    """
    Try to execute f.
    On failure try again anyway.
    Just in case you have to try twice.
    """
    try:
        f(*args,**kwargs)
    except:
        return f(*args,**kwargs)
def knock_knock_e(f,*args,**kwargs):
    """
    Knock_knock but actually properly throw an error.
    """
    tryex_wrap(knock_knock)(f,*args,**kwargs)
def resolve_env(env = None):
    """
    Resolve the operating environment/context.
    """
    if env == None:
        globs = dict(globals())
        return globs.update(locals())
    
def env_check(sterm,env = None,):
    if env == None:
        locs = locals()
        if sterm in locs:
            env = locs
        globs = globals()
        if sterm in globs:
            env = globs
    map()
    return env

def incheck(a,b):
    return a in b

def flookup(f,env = None,tag = "inv",delim = "_"):
    _errsig = nulltag + "FLOOKUP_ERR"
    sterm = f.__name__ + delim + tag
    locs = locals()
    candidates = (env,globals,locals)
    envs = tuple(map(lambda e: e() if e != None else {},candidates))
    tests = tmap(incheck(sterm,e),envs)
    results = map(lambda testidx: envs[sterm] if tests[tidx] else _errsig,rlen(tests))
    
def getf_inv(f,env):
    return flookup(f,env = env)

def fapply_inv(x,f):
    return f(x)
def fapply_s_inv(q):
    """
    Assume q is a arg,function pair.
    """
    return q[1](q[0])
def fapply_s_inv(q):
    """
    Same as the above but uses the fapply_s instead of applying on its own.
    Would probably only a make a difference in memory/ipointer addresses involved.
    """
    return fapply_s((q[1],q[0]))
def fapply_dk(q):
    """
    Q should be a keyword,hash table pair.
    Assumes the keyword is associated to a function.
    """
    return (q[0])(q[1])(q[1])
def fapply_te(f,x):
    try:
        test = x[0]        
        f = partial(fapply,f)
        reduce(f,args)
    except:
        return f(x)
def fapply_args(f,*args):
    f = partial(fapply,f)
    reduce(f,args)
def fapply_args_inv(arg,*fs):
    reduce(fapply_s,zip((arg for arg in fs),fs))
def fapply_kwargs(f,**kwargs):
    f = partial(fapply_kw,f)
    reduce(f,kwargs)
def gt_len_comp(a,b):
    return len(a) > len(b)

def tryex_test(f,*args,**kwargs):
    """
    Test to see if a function is executable without error using the passed arguments.
    Leap before you leap.
    """
    try:
        f(*args,**kwargs)
        return 1
    except:
        return 0
        
def fdet(a,fs = None,test_all = False):
    """
    Determine function to use on an argument using try/except.
    Assuming a represents a member of a set of elements that all share some property/functionality which allows the comparison,
    (such as: they have length)
    should return a function that will work on other elements.
    Or at least, it's intended for use when you know for sure that is the case and want to
    dynamically pre-compute a function to use from a list of possibilities.
    """
    if fs == None:
        fs = (gt_comp,gt_len_comp)
    
    fsched = map(tryex_test(f),fs)
    return map(fapply_s,zip(fs,(a for a in fs)))
        
def versionate(gs,*names,version_args = (),version_keywords = {},version_funcs = ()):
    def versionator(f):
        def versionated(*args,**kwargs):
            return f(*args,**kwargs)
        lencomp = gt_comp(version_funcs,names)
        if len(version_funcs) != len(names):
            raise Exception("Num funcs "+gt_trans()+" num names")
        gs.update({n:partial(versionated,*version_args,**version_keywords) for n in names})
        return versionated
    return versionator

def _type(x):
    pass

def kw_access(d,i,inverted = False):
    d,i = invert_test_pair(d,i)
    return d[i]
def dmap(f,c,inverted = False):
    return map(lambda i: {kw_access(f,i,inverted = inverted)},c)

def negate(x):
    return not x
def cnegate(x,condition = False):
    if not condition:
        return x
    return not x

#########################################################regex stuff

def s_tagger(span,target,tag = "#@GAT!"):
    """
    Take a regex tag result and return the second argument(intended to be a regex target) between its span with a tag and encapsulated in parentheses.
    """
    return target[0:span[0]] + tag + "(" + target[span[0]:span[1]] + ")" + target[span[1]::]
    
def rgx_sub_tag(rgxer,target,tag = "#@GAT!"):
    def tagger(x):
        """
        Take a regex tag result and return the second argument(intended to be a regex target) between its span with a tag and encapsulated in parentheses.
        """
        s = x.span()
        return tag + "(" + target[s[0]:s[1]] + ")"
    return re.sub(rgxer,tagger,target)


@mode_error()
@tuplize
def tokenize_f(fpath,*args,enc = 'utf-8'):
    from tokenize import tokenize
    from io import BytesIO
    
    fstr = fread(fpath,mode)
    byio = BytesIO(fstr.encode(enc)).readline
    tkn = tokenize(byio)
    return tkn

@tuplize
def tokenize_s(s,enc = 'utf-8'):
    from tokenize import tokenize
    from io import BytesIO

    byio = BytesIO(s.encode(enc)).readline
    tkn = tokenize(byio)
    return tkn
    
#########################################################interface
#class to generalize iterables/iterators
class ap():
    def __init__(self,f,use_cache = True):
        self.original = f
        self.original_type = type(f)
        self.__gen__ = map(self.id_func,f)
        self.cache = None
        self.cacher = self.id_func
        if use_cache:
            self.cache = []
            self.cacher = self.cachex
        self.idx_current = 0
    def __getitem__(self,item):
        return self.cache[item]
    def next(self,):
        res = self.cacher(self.__gen__.__next__())
        self.idx_current += 1
        return res
    def id_func(self,x):
        return x    
    def cachex(self,x):
        if type(self.cache) == list:
            self.cache.append(x)
        return x
    def advance(self,):
        self.cacher(self.__gen__.__next__())
    def advance_ignore(self):
        self.__gen__.__next__()
        
def normalize():
    s = sum(vec)
    return (i/s for i in vec)
    
def mormalize(vec):  
    l = sqrt(reduce(lambda x,y: x+y**2),(0,*vec))
    return (i/l for i in vec)
    
def mu_normalize(v):
    return v.normalized()
    
def mu_dot(x,y):
    return x.dot(y)
    
def mu_cross(x,y):
    return x.cross(y)

def ex_class(cls):
    class ncls(cls):
        def __init__(*args,**kwargs):
            self.inner = cls(*args,**kwargs)
            self.initialized_with = (args,kwargs)
        def __getattr__(self,*args,**kwargs):
            return self.inner.__getattr__(self.inner,*args,**kwargs)
        def __setattr__(self,*args,**kwargs):
            return self.inner.__getattr__(self.inner,*args,**kwargs)
        
    
    return ncls

def dict_update(d1,d2):
    for k in d2:
        d1[k] = d2[k]

def acc_idx(x,y):
    '''Access index y of x'''
    return x[y]
        
def indicize(py_obj):
    def getv(v):
        return getattr(py_obj,v)
    return map(getv,dir(py_obj))

def akmap(f,coll,*args,**kwargs):
    def fwrapped(i):
        return f(i,*args,**kwargs)
    return map(fwrapped,coll)

def amap(f,coll,*args):
    def fwrapped(i):
        return f(i,*args)
    return map(fwrapped,coll)

def kmap(f,coll,**kwargs):
    def fwrapped(i):
        return f(i,**kwargs)
    return map(fwrapped,coll)

def rnt(i,iname,propname,names):
    reinterfacer = namedtuple(iname,names)
    return reinterfacer(*(getattr(i,propname) for n in names))

def quasi_parallelize(a,b):
    z = zip(a,b)
    for a2,b2 in z:
        yield (a2,b2)
        
def gen_idx(target,idx):
    for x in range(idx):
        target.next()
#########################################################fresult proc

####analysis
def nullf():
    return None
def nulltagf():
    return "#!@NO_RESULT"

#nyi
def detect_changed_prop(o,f,recursive = False):
    original = prop_dict(o)
    
    return original
    
####gathering
def capture(coll,f,*args,**kwargs):
    original = set(coll)
    f_res = f(*args,**kwargs)
    res = set(coll) - original
    return res,f_res

def size_changed(coll,f,*args,**kwargs):
    original = len(coll)
    f_res = f(*args,**kwargs)
    res = len(coll) - original
    return f_res,original>res,original,res,
    
def context_test(ctx,cases):
    for s in cases:
        if ctx[s]:
            yield True
    

####modification
    
    
#########################################################collection filtering/gathering
def unpack(l):
    """King of king."""
    return reduce(lambda x,y: (*x,*y),l)
    
def recursive_splitter(f = lambda x: x,fcond = lambda x: tuple(x) == (),target = (None,None)):
    '''
    Recursively run a function f on a list of arguments x.
    By default, expires when x is exhausted.
    
    '''
    x = unpack(target)
    if fcond(x):
        return ()
    yield map(recursive_splitter,target = x)
    
def inner_range(lst,x):
    return range(x,len(lst)-x)

def lmap(f,c,*args,**kwargs):
    return map(lambda i: f(i,*args,*kwargs),c)
    
def ltmap(f,c,*args,**kwargs):
    return tuple(map(lambda i: f(i,*args,*kwargs),c))
    
def inner(lst,x):
    return tmap(lambda i: lst[i],inner_range(lst,x))
    
def pnmap(lst,x = 1,none_val = (None,None,None),none_fill = True,wrap = False):
    '''Return a set of tuples containing the n-xth,nth, and n+xth items in lst
    Corresponds to a list of previous, current, next data
    
    Ends of the list are considered undefined if wrap is not enabled
    If none_fill is enabled, preserves the indices of the original list by appending none_val for the ends if they're undefined'''
    fill_range = ()
    if none_fill:
        fill_range = tuple(range(x))
        filler = tuple(none_val for n in fill_range)
    def get_pn(idx,x = 0,lst = (0,1,2)):
        return (lst[idx-x],lst[idx],lst[idx+x])
    get_pn = partial(get_pn,x=x,lst=lst)
    r = range(x,len(lst)-x)
    return (*filler,*reduce(get_pn,r),*filler)
    
def none_if_nil(x,idx = 0):
    return None if x == () else x[idx]

def nil_convert(x):
    if x == None: return ()
    elif x == (): return None
    
def false_cycle(x):
    if x == False: return 0
    elif x == 0: return None
    elif x == None: return ()
    elif x == (): return -1
    elif x == -1: return False
    
    

def name_filter(coll,names):
    return tuple(filter(lambda i:any(map(lambda n: n in getattr(i,"name"),names)),coll))
    
def dict_roll(ds):
    return reduce(dict_update,*ds)

def roll(ts):
    return reduce(lambda x,y: (*x,*y),*ts)

def filter_objects_by_prop_o(propname,propval,checkfunc):
    return lambda x: list(filter(getattr(x,propname) == propval))
    
def filter_objects_by_prop(coll,propname,propval,checkfunc = None):
    if checkfunc == None:
        def checkfunc(x):
            return getattr(x,propname) == propval
    return lambda: tuple(filter(checkfunc,coll))

def filter_by_prop_rec(coll,propname,propval,checkfunc = None):
    '''Filter objects by property values.
    Returns items in the order given by the value list.
    Inputs:
        propname: Name of attribute to check.
        propval: An iterable values to check for.
        coll: Collection
        '''
    return tmap(none_if_nil,tmap(lambda t: filter_by_prop(coll,"type",t,checkfunc = checkfunc),propval))
    
def filter_by_prop_iter(coll,propname,propval,checkfunc = None):
    if checkfunc == None:
        def checkfunc(x,val):
            return getattr(x,propname) == val
    return tuple(map(lambda val: unpack_r(filter(lambda item: checkfunc(item,val),coll)),propval))
    
def filter_by_prop(coll,propname,propval,mode = 0,checkfunc = None):
    if mode != 0:
        return filter_by_prop_iter(coll,propname,propval,checkfunc = checkfunc)
    if checkfunc == None:
        def checkfunc(x):
            return getattr(x,propname) == propval
    return tuple(filter(checkfunc,coll))
    
def collect_object_by_type(coll,searchterm,searchprop,ret = 'o'):
    ret_types = ['o','i','n']
    ret_type = ret_types.index(ret)
    
    res = []
    for oidx,o in enumerate(coll):
        target_prop = getattr(o,searchprop)
        if re.search(searchterm,target_prop):
            rets = tuple((o,oidx,o.name))
            res.append((rets[ret_type],o))    
                    
    
    return res
    
def exclude_consecutive(tar_string,roll_char):
    return reduce(lambda s,c: s + c if not (s[-1] == roll_char and c == roll_char) else s,tar_string)
#########################################################elmap paradigm

def elmappo_inter(f,c):
    """
    Map based on the stupid idea that you can treat multiple
    elements and single elements of a type in the same way by
    wrapping singular inputs into a 1-length tuple.
    """
    try:
        len(c)
        target = c
    except:
        target = ()
    return map(f,c)

def exmap(f,c):
    """
    Map based on the stupid idea that you can treat multiple
    elements and single elements of a type in the same way by
    wrapping singular inputs into a 1-length tuple.
    """
    try:
        len(c)
        target = c
    except:
        target = (c,)
    return map(f,c)


#########################################################get>gather>check>filter paradigm(?)
def get_prop_tag(i,taglen = 3,prop = "name",is_suffix = True,tag_region = None):
    return getattr(i,prop)[0:taglen]
    
def gather_prop_tags(coll,taglen = 3,prop = "name",is_suffix = True,tag_region = None):
    return (get_prop_tag(i,prop = prop,taglen = taglen,is_suffix = is_suffix) for i in coll)

@tuplize
def check_prop_tags(coll,prop = "name",target_tag = "kV_",tags = None,is_suffix = True,tag_region = None):
    taglen = len(target_tag)
    #if passed a list of tags use it
    if tags == None:
        tags = gather_prop_tags(coll,taglen = taglen,prop = prop,is_suffix = is_suffix,tag_region = tag_region)
    tag_checks = filter(lambda m: m[1] == target_tag,enumerate(tags))
    return map(lambda m: m[0],tag_checks)

@tuplize
def filter_prop_tags(coll,prop = "name",target_tag = "kV_",tags = None,is_suffix = True,tag_region = None):
    #pass args to check
    tag_checks = check_prop_tags(**locals())
    
    return map(lambda i: coll[i],tag_checks)

#decorator that raises an error if called without an argument
#no, uh, it does, but its porpoise is to dynamically create required keyword arguments for functions that normally accept variable kwargs
#that's needed functionality, right?
#ex:
'''
#if f is called without "arg" as a keyword argument, it will raise an error.
@defargerate({"arg":"value"})
def f(*args,**kwargs):
    print("fn")
'''
#########################################################time
def timerate_test(count_limit):
    '''On this computer, 5 seconds is about 11111111'''
    t = time.clock()
    for x in range(count_limit):
        crnt = time.clock()-t
        if (int(crnt+1)%5)-1 == 0:
            print(crnt)
def timerate(time_limit,*args,count_limit = None,f = nullf,**kwargs):
    '''On this computer, 5 seconds is about 11111111'''
    t = time.clock()
    c=0
    res = "#!@NO_RESULT"
    while True:
        if count_limit != None:
            if c > count_limit:
                break
        crnt = time.clock()-t
        res = f(*args,**kwargs)
        if crnt>=time_limit:
            break
    return res
#########################################################randomtivity


def ransize(size,signed = True):
    return random()*size-((size/2)*int(signed))

@tuplize
def ranvecs(c_size = 3,s_size = 3,normalize = False):
    return (ranvec(s_size = s_size,normalize = normalize) for i in range(c_size))
    
def ranvec(s_size = 3,normalize = False):
    if normalize:
        normalize = mu_normalize
    else:
        normalize = id_func
    return normalize(Vector(((random()-.5)*2 for x in range(s_size))))
    
def ranchar(char_set = ascii_letters,n = None):
    if n == None:
        n = len(char_set)
    return char_set[int(random()*n)]
    
def ranstr(s_size = 8,char_set = ascii_letters):
    return "".join(ranchar(char_set = char_set) for r in range(s_size))

def _ranpos(size):
    return randrange(0,size)
    
def ranpos(coll):
    return _ranpos(len(coll))
    
def smungerate(x):
    n = ranpos(x)
    return x[0:n] + ranchar() + x[(n+1)::]

#########################################################garbage

def sextract(s,a,b):
    return s[s.index(a):s.index(b)]

def switch(x,case_result_pairs,default = None,cmpf = None):
    """
    switch(5,
    #case-result pairs
    ((3,2),
    (5,1),),
    #since 5 == 5 the second item is returned
    ) = 1
    Does not evaluate lazily.
    """
    cases = idx_select(case_result_pairs,0)
    results = idx_select(case_result_pairs,1)
    #default to simple equality comparison
    if cmpf == None:
        def cmpf(case):
            return x == case
    for cidx,c in enumerate(cases):
        if cmpf(c):
            return results[cidx]
    return default
    
    
def delim_strip(s,delim = ","):
    s_len = len(s)
    pos = -1
    if s[pos] != delim:
        return s
    while s[pos] == delim and (abs(pos) < s_len):
        pos -= 1
    if abs(pos) >= s_len:
        return s
    return s[0:pos]
    
def create_if_nonexist(coll,existing_names,itype,item):
    if item == -1:
        return -1
    try:
        if type(existing_names) in (list,tuple):
            return existing_names.index(item)
        else:
            return existing_names[item]
    except:
        new = itype()
        new.name = item
        
        if type(coll) == list:
            coll.append(new)
        if type(existing_names) == list:
            existing_names.append(item)
        return len(coll)-1
    
def create_if_nonexist2(coll,existing_names,itype,item):
    if item == -1:
        return -1
    try:
        return existing_names[item]
    except:
        new = itype()
        new.name = item
        
        coll.append(new)
        existing_names.append(item)
        return len(coll)-1
        
def enumdiff(lst,max_count = 1000):
    cnt = 0
    lenlst = len(lst)
    while True:
        m = cnt%lenlst
        yield lst[m]-m 
        cnt+=1
        if max_count != None:
            if cnt>=max_count:
                return None
def naxt(target):
    if type(target) == map:
        return target.__next__()
    else:
        return target.send(None)
def gen_idx(target,idx):
    for x in range(idx):
        target.next()
def quasi_parallelize(a,b):
    z = zip(a,b)
    for a2,b2 in z:
        yield (a2,b2)
def sum_map(a,b):
    z = zip(a,b)
    for a2,b2 in z:
        yield a2+b2 
    
def repeat_pattern(pattern,n):
    return sum_map(enumdiff(pattern,max_count = n),range(n))

def lerp(min,max,percent):
    if type(min) not in (float,int,bool):
        if type(min) in (Vector,list,tuple,set):
            return type(min)((lerp(min[x],max[x],percent) for x in range(len(min))))
    return ((max-min)*percent)+min
    
def option_filter(i,default = True,option = True,prop = "select"):
    return getattr(i,prop) if option else default
    
def option_filterf(option = True):
    return partial(option_filter,option = option)
    
def sseek(target,sses,first_only = True,testf = lambda x,y: (x[2::] in y) and ("@#" not in y)):
    def searcher(s):
        return testf(target,s[1])
    res = filter(searcher,enumerate(sses))
    if first_only:
        return res.__next__()
    else:
        return res
    return nsgnl
    
def recursive_finderate(s,rgxers,):
    #initialize by taking the length of the list
    s_count = len(s)
    def recursive_finderator(start_index,rgx_index):
        while start_index < s_count:
            res = re.search(rgxers[rgx_index],s[start_index])
            start_index+=1
            if res != None:
                #if the final rgx has been found, raise to exit loop
                if(len(rgxers) < 2):
                    raise Exception(start_index,res,)
                #else try until the end
                return recursive_finderator(start_index,rgx_index + 1)
        #if the target has been exhausted, return the length of the list and None as a failure signal
        return (start_index,None)
    return recursive_finderator

def sequential_finderate(s,rgxers,start_index = 0):
    #initialize a search with the passed list and rgx expressions
    recursive_finderator = recursive_finderate(s,rgxers)
    try:
        res = recursive_finderator(start_index,0)
        return res
    except Exception as e:
        return e.args

    
def file_char_replace(fpath,target,rep = "    "):
    fstr = fread(fpath,'r')
    fstr = fstr.replace(target,rep)
    fwrite(fstr)
    
def tab_replace(fpath,):
    """Simple function to replace tabs with 4-spaces; relevant because Python"""
    return file_char_replace(fpath,"\t","    ")
    
def sequals(a,b):
    return str(a) == str(b)
    
def swrap(s1,s2):
    return s1+s2+s1

def try_new_name(name,max_tries = 1000):
    gs = globals()
    if name == None:
        for n in range(max_tries):
            name = "mated" + ranstr(s_size = 5)
            if name in gs:
                continue
            else:
                break
    return name

def argize(*args):
    return args
    
def kwargize(**kwargs):
    return kwargs
    
def setattrate(___itarget1,dbg = False,**kwargs):
    if dbg:
        print(___itarget1)
        for kw in kwargs:
            print("Key:",kw)
            print("Value:",kwargs[kw])
    if ___itarget1 == None:
        return kwargs
    anymap(lambda kw: setattr(___itarget1,kw,kwargs[kw]),kwargs)
    return kwargs

#remove fractional part, operate,add fractional part
def cancellate_frac(f,vals,base_val):
    map(f(val-((val%base_val))) + (val%base_val),range(len(vals)))

def group_op(target_group,f,*args,**kwargs):
    return map(partial(f,*args,**kwargs),target_group.objects)
    
def tmap(f,c):
    return tuple(map(f,c))
    
def tfil(f,c):
    return tuple(filter(f,c))

def to_gen(f):
    def to_genned(*args,**kwargs):
        for x in f(*args,**kwargs):
            yield x
    return to_genned
    
@to_gen
def gmap(*args,**kwargs):
    return map(*args,**kwargs)

@to_gen
def gfil(*args,**kwargs):
    return filter(*args,**kwargs)
    
def stop_gen(f):
    def stop_genned(*args,**kwargs):
        for x in f(*args,**kwargs):
            yield x
        yield None
    return stop_genned

def passmap(*args,**kwargs):
    for x in map(*args,**kwargs): pass
    
def anymap(*args,**kwargs):
    return any(map(*args,**kwargs))
    
def allmap(*args,**kwargs):
    return all(map(*args,**kwargs))
    
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
    
def untilv(f,coll,*args,**kwargs):
    for x in coll:
        res = f(x,*args,**kwargs)
        if res:
            return res
    
    
def enumsplit(enum_list):
    return (i[0] for i in enum_list),(i[1] for i in enum_list)

def enumsort(c,key,):
    c = enumerate(c)
    c.sort(key = lambda x: key(x[1]))
    return enumsplit(c)

def closest_value(vals,target):
    return min((enumerate(abs(v-target) for v in vals)),key = lambda x: x[1])

def falloff_collect(vals,target):
    return min((enumerate(abs(v-target) for v in vals)),key = lambda x: x[1])

def analyze_closest(vals,target,falloff):
    mapped = map(lambda v: abs(v-target) < falloff,vals)
    for x in mapped:
        yield x

def split_at_closest(vals,target,falloff):
    m = analyze_closest(vals,target,falloff)
    return (i2[0] for i2 in filter(lambda i: i[1] == 1,enumerate(m)))

def id_closest(vals,target,falloff):
    m = analyze_closest(vals,target,falloff)
    for x in (i2[0] for i2 in filter(lambda i: i[1] == 1,enumerate(m))):
        yield x

def counted_split_at_closest(vals,target,falloff,split_count):
    numvals = len(vals)
    split_length = int(numvals/split_count)
    m = analyze_closest(vals,target,falloff)
    return (i2[0] for i2 in filter(lambda i: i[1] == 1,enumerate(m)))

        
def sin_split(vals,split_count):
    splitrange = tuple(range(0,len(vals),split_count))
    list_split = tuple(map(lambda i: vals[i:(i+split_count)],splitrange))

    splitsums = tuple(map(lambda s: sum(s),list_split))

    lsplit_normalized = tuple(
    map(lambda val_list_idx: normalize_range(
    tmap(lambda val_idx: (list_split[val_list_idx][val_idx])/(splitsums[val_list_idx]),
    range(len(list_split[val_list_idx])))),
    range(len(list_split))))
    nrange = map(lambda s: tuple(round(sin(v*pi),4) for v in s),lsplit_normalized)
    
    for x in nrange:
        yield x

def id_func(x):
    return x

def closest_value(vals,target): 
    return min(tuple(enumerate(abs(v-target) for v in vals)),key = lambda x: x[1])
    
def sin_split2(vals,split_count, f = None,key = None):
    if f == None:
        f = id_func
    if key == None:
        key = id_func
    splitrange = tuple(range(0,len(vals),split_count))
    list_split = tuple(map(lambda i: vals[i:(i+split_count)],f(splitrange)))

    splitsums = tuple(map(lambda s: sum(s),(key(item) for item in list_split)))

    lsplit_normalized = tuple(
    map(lambda val_list_idx: normalize_range(
    tmap(lambda val_idx: (key(list_split[val_list_idx][val_idx]))/(splitsums[val_list_idx]),
    range(len(list_split[val_list_idx])))),
    range(len(list_split))))
    nrange = map(lambda s: tuple((v,round(sin((key(v))*pi),4)) for v in s),lsplit_normalized)
    
    for x in nrange:
        yield x
        
@tuplize
def sinsmooth_range(vals):
    vals = (v-.5 for v in vals)
    for v in ((((sin(v*2*pi+(.5*pi))/2)+.5)) for v in vals): yield v
    
def normalize_range(vals):
    minimum = min(vals)
    res = tuple(v-minimum for v in vals)
    res_max = max(res)
    if res_max == 0:
        unscale_factor = 0
    else:
        unscale_factor = 1/res_max
    mapped = map(lambda v: v*unscale_factor,res)
    for x in mapped:
        yield x
        
def itempair(items,cnt):
    return tuple(reduce(lambda x,y: (*x,y,y+1),((),*range(len(items)-1) )))

def mapitalize(words,delim = "_",fill_delim = " ",cap_idx = 0):
    return map(lambda word: fill_delim.join((word[cap_idx].upper() + word[(cap_idx+1)::],words.split(delim))))

#i should be an iteratable
def edict(i):
    return {item[1]:item[0] for item in enumerate(i)}

#to digest an iteratable use spread syntax
def edict2(*args):
    return {i[1]:i[0] for i in enumerate(args)}
    
#to digest an iteratable use spread syntax
def edict3(**kwargs):
    return {i:kwargs[i] for i in kwargs}

def defargerate(kwargdict):
    def defargerator(f):
        def defargerated(*args,**kwargs):
            missing_kwargs = tuple(kw for kw in kwargdict if kw not in kwargs)
            if len(missing_kwargs)>0:
                raise ValueError("Function",f,"missing keyword arguments:",','.join(missing_kwargs))
            else:
                f(*args,**kwargs)
        return defargerated
    return defargerator
    
##assumes: 
#simple . path strings 
#ending in indexed collection
def prop_by_path_dot(target,collpath = "data.vertices"):
    collpath_split = collpath.split('.')
    prop = target
    for p in collpath_split:
        prop = getattr(prop,p)
    return (target,prop,collpath_split,p)


#selective unpack
#add_bones = reduce(lambda x,y: (*x,y) if type(y[0]) != tuple else (*x,*y),((),*add_bones))

#add_bones =tuple(reduce(lambda x,y: (*x,y) if y[1] == 0 else (*x,*((x,0) for x in vfb.get_lr_name(y[0],'jp'))),((),*add_bones)))
def get_boolprop_idx(coll,prop):
    return tuple(v for v in rlen(coll) if getattr(coll[v],prop))
    
def get_sobjs_selverts(targets):
    colls = map(prop_by_path_dot,targets)
    return tuple(map(lambda x: get_boolprop_idx(x[1],"select"),colls))

def get_sobjs_selparts(targets,part_name):
    colls = map(lambda x: prop_by_path_dot(x,collpath = "data."+part_name),targets)
    return tuple(map(lambda x: get_boolprop_idx(x[1],"select"),colls))

def get_sobjs_props(targets,base_path = "data.",part_name = "vertices",prop_name = "select",):
    colls = map(lambda x: prop_by_path_dot(x,collpath = base_path+part_name),targets)
    return tuple(map(lambda x: get_boolprop_idx(x[1],prop_name),colls))

def get_objs_props(targets,base_path = "data.",part_name = "vertices",prop_name = "select",obj_prop_path = "select"):
    colls = map(lambda x: prop_by_path_dot(x,collpath = base_path+part_name),filter(lambda x:prop_by_path_dot(x,collpath = obj_prop_path)[1],targets))
    return tuple(map(lambda x: get_boolprop_idx(x[1],prop_name),colls))

def multisplit(target_string,targets):
    return re.split(r'['+''.join(targets)+']',target_string)
    
class bpy_data_text():
    def __init__(self,name,coll,stream):
        pass
        self.name = name
        self.coll = coll
        self.stream = stream
    def write(self,data):
        with open(self.stream,'a') as write_stream:
            write_stream.write(data)
            
def exclude(l,targets):
    return list(x for x in l if x not in targets)

    
#likely horribly inefficient
def permutations_r(coll,n):
    coll = list(coll)*n
    return permutations(coll,n)
    
#likely horribly inefficient
def permutations_r(coll,n):
    coll = unpack(coll for x in range(n))
    return permutations(coll,n)
    
def permutations_rr(coll,*rd):
    """
    Args:
    coll: Some collection.
    rd: range data.
        start index, end index, step.
    """
    def ltz(x):
        return x > 0
    r = filter(ltz,range(*rd))
    for x in r:
        for i in permutations_r(coll,x):
            yield i
            
def fmapx(prop,coll,val):
    def fmap2(f):
        return f(map(lambda x:setattr(x,prop,val),coll))
    return fmap2

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
    
def rattrmap(coll,prop,coll2,target_range = None,getf = None,setf = None,use_try = False):
    if target_range == None:
        target_range = range(len(coll2))
    q = (n for n in ())
    if type(coll) == type(q):
        coll = tuple(coll)
    elif type(coll2) == type(q):
        coll2 = tuple(coll2)
    
    if use_try:
        if setf == None:
            setf = trysetattr
    if setf == None:
        setf = setattr
    if use_try:
        if getf == None:
            getf = trygetattr
    if getf == None:
        getf = getattr
        
    return any(map(lambda x:setf(coll[x],prop,(lambda y:getf(y,prop))(coll2[x])),target_range))

def rmap(coll,coll2,target_range = None,):
    if target_range == None:
        target_range = range(len(coll2))
    q = (n for n in ())
    if type(coll) == type(q):
        coll = tuple(coll)
    elif type(coll2) == type(q):
        coll2 = tuple(coll2)
    
    try:
        len(coll2[0])
        return passmap(lambda i: rmap(coll[i],coll2[i],target_range = target_range,),rlen(coll2))
    except:
        return any(map(lambda x:setidx(coll,x,getidx(coll2,x)),rlen(coll2)))


class bpy_data_texts():
    def __init__(self):
        self.names = {}
        self.texts = []
        self.nameref = {}
        pass
    def new(self,name):
        ntxt = bpy_data_text(name,self)
        self.texts.append(ntxt)
        self.names.append(name)
        self.nameref[name] = ntxt
    
    

#probably really really bad
def vec_avg(vecs):
    for v in vecs:
        if type(v) == Vector:
            return Vector((a/len(vecs) for a in reduce(lambda x,y: x+y,vecs)))
        break
    vecrange = range(len(vecs[0]))
    res = [0 for a in vecrange]
    for v in range(len(vecs)):
        for i in vecrange:
            res[i] += vecs[v][i]
    for i in vecrange:
        res[i] /= v+1
    return Vector(res)
    
def arg_inspect(f,arglist = None,kwargdict = None,*args,**kwargs):
    def arg_inspector(f,):
        if arglist != None:
            for x in range(len(arglist)):
                if arglist[x] != args[x]:
                    args[x] = arglist[x]
        if kwargdict != None:
            for x in kwargdict:
                kwargdict_items = kwargdict.items()
                kwargs_items = kwargs.items()
                if kwargdict[x] != kwargs[x]:
                    kwargs[x] = kwargdict[x]
                    
        #call function with updated args/kwargs
        def arg_inspected(*args,**kwargs):
            return f(*args,**kwargs)
        return arg_inspect
    return arg_inspector
        
def kwarg_inspect(f,kwarg_funcs_dict = None,kwarg_dict = None,*args,**kwargs):
    def kwarg_inspector(f,):
        if kwarg_dict != None:
            for x in kwarg_dict:
                if kwarg_dict[x] != kwargs[x]:
                    kwargs[x] = kwarg_funcs_dict[x]()
                    
        #call function with updated args/kwargs
        def kwarg_inspected(*args,**kwargs):
            return f(*args,**kwargs)
        return kwarg_inspected
    return kwarg_inspector
        


def tryex_wrap(f,*args,**kwargs):
    def argpass1(f):
        def wrapped(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except Exception as e:
                return None
        return wrapped
    return argpass1(f)
    
def dict2prop(obj,obj_data):
    for prop in obj_data:
        setattr(obj,prop,obj_data[prop])

def pair2dict(pair_tuple):
    return dict({pair_tuple[0]:pair_tuple[1]})

def csv2dict(csvstr):
    return (pair2dict(i.split(":")) for i in (csvstr.split(",")))
    
def print_fails(good_fails,failmsg,print_divider = True,div = "\n########################################################\n",always = False):
    if not always:
        if not len(good_fails)>0:
            return
    if print_divider:
        failmsg = div + failmsg + div + '\n'
    print(failmsg)

def slice(i,s,e):
    return i[s:e]
    
def save_py_item(pyitem):
    #if returnvdl == "LIST":
    proplist = []
    for prop in dir(pyitem):
        val = getattr(pyitem,prop,)
        proplist.append([prop,val])
    '''
    if returnvdl == "DICT":
        proplist = {}
        for prop in dir(pyitem):
            val = getattr(pyitem,prop,)
            proplist.update({prop:val})
    '''
    
    return proplist

def copy_py_item_from_list(pyitemplist,target_item):
    for v in pyitemplist:
        prop,val = v
        try:
            setattr(target_item,prop,val,)
        except:
            pass

def copy_py_item(pyitemp1,pyitem2):
    pyitemplist = save_pyitem(pyitemp1)
    copy_pyitem_from_list(pyitemplist,pyitem2)

#only guaranteed to work for immediate values like int, float, string, etc.
def setattr_immediate_copy(pyobj,pydict):
    errs = ["#_NOERR" for i in pydict]
    for idx,x in enumerate(pydict):
        try:
            setattr(pyobj,x,pydict[x])
        except Exception as e:
            errs[idx] = e
    return errs

def truef(*args,**kwargs):
    return True
   
def prop_dict(obj,filter_func = truef,result_filter = truef,targets = None):
    cdir = tuple(filter(filter_func,dir(obj)))
    def gattrate(obj,i):
        try:
            return getattr(obj,i)
        except:
            return "#_GET_ERR"
    if targets != None:
        cdir = targets
    proplist = ((i,gattrate(obj,cdir[i])) for i in range(len(cdir)))
    proplist = filter(lambda i: result_filter(i[1]),proplist)
    return {cdir[i[0]]:i[1] for i in proplist}

    
def point_copy(verts,coords):
    return rmap(list(verts),coords,)
    
#only guaranteed to work for immediate values like int, float, string, etc.
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
   
def lstchain(lsts,ret="t"):
    res = reduce(lambda x,y:x+y,lsts)
    if ret=="t":
        return tuple(res)
    elif ret=="l":
        return list(res)
    elif ret=="g":
        return res
    else:
        raise ValueError
        
#probably useless
def complete_idxlist(idxlist,startnum = None,lastnum = None):
    sidx = idxlist[0]
    eidx = idxlist[-1]
    if startnum:
        sidx = startnum
    if lastnum:
        eidx = lastnum
    return(tuple(range(sidx,eidx)))
    
def find_missing_indices(idxlist,startnum = None,lastnum = None,fill = False):
    missingnos = []
    if fill:
        sidx = idxlist[0]
        eidx = idxlist[-1]
        if startnum:
            sidx = startnum
        if lastnum:
            eidx = lastnum
        return(tuple(range(sidx,eidx)))
    if startnum:
        if idxlist[0] > startnum:
            diff = idxlist[0] - startnum
            for x in range(diff):
                missingnos.append(x+1)
            
                
    for x in range(len(idxlist)-1):
        next = idxlist[x+1]
        current = idxlist[x]
        diff = next - current
        if diff > 1:
            for x in range(diff-1):
                missingnos.append(current+x+1)
                
    if lastnum:
        if idxlist[-1] < lastnum:
            diff = lastnum - idxlist[-1]
            for x in range(diff):
                missingnos.append(idxlist[-1]+x+1)
    return missingnos
    
def get_other(pair,current_item,*args,**kwargs):
    return tuple(i for i in pair if i != current_item)[0]
    
def get_sel(coll,prop = "select"):
    return tuple(filter(lambda x:(getattr(coll[x],prop)),range(len(coll))))

def arg_discard(f):
    def arg_discarding(num):
        def fanc(*args,**kwargs):
            return f(*args[num::],**kwargs)
        return fanc
    return arg_discarding
    
def arg_discard_r(f):
    def arg_discarding(num1,num2):
        def fanc(*args,**kwargs):
            return f(*args[num1:num2],**kwargs)
        return fanc
    return arg_discarding
    
def print_pmx_csv_header(header,numbered = True,split_header = False):
    if split_header:
        headersplit = header.split(",")
    else:    
        headersplit = header
    for i in range(len(headersplit)):
        if numbered:
            print(i,headersplit[i])
        else:
            print(headersplit[i])

def unpack_list(item):
    unpackerated = []
    unpackerate(item,unpackerated)
    return unpackerated

def unpackerate(item,target):
    if "__len__" in dir(item[0]):
        for i in item:
            unpackerate(i,target)
    else:
        for i in item:
            target.append(i)

def unpack_r(l):
    return reduce(lambda x,y: (*x,*y),l)
    
def unpack_r2(l):
    pass
    #return reduce(lambda x,y: (*x,*y) if all("__len__" in dir(x),"__len__" in dir(y)),l)
  
def print_dict_formatted(target,quotize1 = False,quotize2 = False):
    for i in target:
        b = target[i]
        if quotize1:
            i = quotize(i)
        if quotize2:
            b = quotize(b)
        print(i,":",b + ",")
        
def arg_seek(f):
    def argseek(self,*args,**kwargs):
        locs = f(self,a = 1)
        for a in locs:
            print(a)
            if locs[a] == None:
                locs.update({a:getattr(self,a)})
        locs["a"] = 0
        kwargs.update(locs)
        return f(*args,**kwargs)
    return argseek
    
def strip_nl(line):
    return line.replace("\n","")

def prop_filterate(coll,prop):
    return filter(lambda y: getattr(y,prop),coll)
    
#converts a number to a string with a specified number of digits;
#digits representing values larger than the number itself are output as leading 0s
#ex:10,3563 = 0000003523
#if the number won't fit in the specified digit length, a message is printed and an error is raised
def num_str(digit_count,num):
    n = str(num)
    lennum = len(n)
    if lennum > digit_count:
        print("Size of number exceeds specified digit count.")
        raise ValueError
    n = "0"*(digit_count - lennum)+n
    return n
    
def prop_above_limit(v,propname,f):
    def limcheck(target):
        return f(getattr(target,propname)) > v
    return limcheck
    
def zero_func(*args,**kwargs):
    return (*args,dict(**kwargs))
    
def check_prev_exists(idx,lencoll):
    if lencoll < 2:
        return 0
    return idx > 0

def check_next_exists(idx,lencoll):
    if lencoll < 2:
        return 0
    return idx < (lencoll-1)
    
        
def dict2attr(obj,attrdict):
    itin = anymap(lambda attr: trysetattr(obj,attr,attrdict[attr]),attrdict.keys())
    return itin
    
def check_inbounds(idx,lencoll):
    return check_prev_exists(idx,lencoll) and check_next_exists(idx,lencoll)

def bool_to_negpos(b):
    return (-1+b*2)
    
def rlen(x,*args):
    defaults = (0,0,1)
    start,sub,step = default_fill(args,defaults)
    end = len(x)-sub
    return range(start,end,step)
    
def rlen2(x,rev):
    rev = bool(rev)
    lenx = tuple((0,len(x)))
    return range(lenx[0-rev]-rev,lenx[1-rev]-rev,bool_to_negpos(not rev))
    

def get_named(coll,target_name,multi_res = False):
    if multi_res:
        return tuple(filter(lambda x:x.name == target_name,coll,))
    return tuple(filter(lambda x:x.name == target_name,coll,))[0]
    

def clean_by_tag(coll,tag,f):
    taglen = len(tag)
    for item in coll:
        if len(item.name)<(taglen+2):
            continue
        if (item.name[0:(taglen)] == tag) and (item.name[taglen] == "_"):
            f(coll,item)
            
def quotize(s):
    return "\""+ s + "\""

#########################################################dict stuff
class vdict(dict):
    def __init__():
        pass
        
def revdict(d):
    return {d[i]:i for i in d}
    
def d2l(d):
    return [(i,d[i]) for i in d]
    
def d2t(d):
    return tuple((i,d[i]) for i in d)
    
def filter_dict_comp(d1,d2):
    for i in d1:
        if not i in d2:
            d2.pop(i)
            
def dict_xor(d1,d2):
    for i in d1:
        if not i in d2:
            d2.pop(i)
            
def dict_and(d1,d2):
    for i in d1:
        if not i in d2:
            d2.pop(i)
            
def dict_or(d1,d2):
    for i in d1:
        if not i in d2:
            d2.pop(i)
            
def dict_sub(d1,d2):
    failed = []
    d1keys = set(d1.keys())
    d2keys = set(d2.keys())
    keydiff = tuple(d2keys - d1keys)
    return {k:d2[k] for k in keydiff}
    
def dict_add(d,key,val):
    d[key] = val
    return 0
    
def dictmap(d,f1 = id_func,f2 = id_func):
    keys = d.keys()
    return reduce(lambda x,y: dict_add(x,f1(y),f2(d[y])),({},*keys))
        
def dict_not(d1):
    return dictmap(lambda x: not x,d1)

def append_update(d,i,v):
    try:
        d[i].append(v)
    except:
        d.update({i:[v]})
        
def list_dict(lst1,lst2):
    d = {}
    updater = partial(append_update,d)
    tmap(lambda i: updater(*i),zip(lst1,lst2))
    
    return d
'''
#might be faster than the above depending on the size of the item?
def filter_dict_comp(d1,d2):
    for i in d1:
        try:
            d2[i]
        except:
            d2.pop(i) 
            
#slower than the above
def filter_dict_comp(d1,d2):
    filterdict = {i:d2[i] for i in d1}
    return filterdict
    #sd1 = set(d1.keys())
    #sd2 = set(d2.keys())
    #sdf = sd2 - sd1
    #sd2 = sd2 - sdf
    #print(sdf)
    

#slower than the above
def filter_dict_compset(d1,d2):
    d2s = set(d2)
    sd2 = (d2s - set(d1)) - d2s
    
    filterdict = {i:d2[i] for i in sd2}
    
    return filterdict
'''
 
def qstr(o):
    return "\"" + str(o) + "\""
    
def sstr(o):
    return str(o).replace("\n","\\n").replace("\"","\\\"")

def save_obj_state(o,tarprop = None,tempwrite = False,tempwritepath = "",propfunc = lambda x: x,strproc = lambda x: x):
    datstr = ""
    if tarprop:
        datstr = strproc(str(propfunc(getattr(o,tarprop))))
    else:
        for i in dir(o):
            datstr += strproc(str(propfunc(i)))
    return datstr

def save_obj_state_dict(o):
    tempf= open(path1 + "\\pytmp\\temp_ostate" + ".pytmp",'w')
    tempf.write("{\n")
    
    datstr = save_obj_state(o,propfunc = lambda x,y = o: "\""+str(x)+"\":\"" + sstr(getattr(y,x)) + "\",\n")
    tempf.write(datstr)
    tempf.write("\n}")
    tempf.close()
    #record types; eval is not reliable
    
    tempf= open(path1 + "\\pytmp\\temp_ostate_types" + ".pytmp",'w')
    tempf.write("{\n")
    
    datstr = save_obj_state(o,propfunc = lambda x,y = o: "\""+str(x)+"\":\"" + sstr(type(getattr(y,x))) + "\",\n")
    tempf.write(datstr)
    tempf.write("\n}")
    tempf.close()
    return datstr

def load_obj_state():
    #delegating definition for later work; laziness at its finest
    parsedict = eval
    tpath = path1 + "\\pytmp\\temp_ostate" + ".pytmp"
    os.chdir(path1)
    tempf= open(tpath,'r')
    datstr = tempf.read()
    tempf.close()
    
    t = eval(datstr)
    return t

#filter evaluatable saved values
#example: 1 will evaluate, <class 'str'> will not
#pretty fucking unsafe... probably, use with caution if at all,
#why am i programming this
def filter_evaluated_dict(evdict):
    
    newdict = {}
    
    for i in evdict:
        try:
            evi = eval(evdict[i])
            newdict.update({i,evi})
        except:
            pass
    return newdict

def load_obj_state_checktype():
    #delegating definition for later work; laziness at its finest
    parsedict = eval
    tpath = path1 + "\\pytmp\\temp_ostate" + ".pytmp"
    os.chdir(path1)
    tempf= open(tpath,'r')
    datstr = tempf.read()
    tempf.close()
    vals = eval(datstr)
    
    tpath = path1 + "\\pytmp\\temp_ostate_types" + ".pytmp"
    os.chdir(path1)
    tempf= open(tpath,'r')
    datstr = tempf.read()
    tempf.close()
    types = eval(datstr)
    
    vals = filter_evaluated_dict(vals)
    for item in types:
        try:
            vals[item]
        except:
            types.remove(item)
    return (vals,types_filter)
    
def save_obj_state(o,tarprop,propfunc = lambda x: x,strproc = lambda x: x):
    #tempsav = open(path1 + "\\temp_ostate" + ".pytmp",'w')
    datstr = strproc(str(propfunc(getattr(o,tarprop))))
    return datstr
        
def load_obj_state(o,tarprop,propfunc = lambda x: x,strproc = lambda x: x):
    #delegating definition for later work; laziness at its finest
    parsedict = eval
    
    tempf= open(path1 + "\\temp_ostate" + ".pytmp",'w')
    os.chdir(path1)
    return datstr
        
def test_length_bytes(filepath,size):
    

    binfil = open(filepath,'rb')
    c=0
    while binfil.read(size) != b'':
        c+=1
    return c

def write_footer(filbase,newfil):
    for line in filbase:
        newfil.write(line)
            
def fappend_str(ifil,ofil,astr,sterm,finish = False):
    current_pos = ifil.tell()
    ifil,linecount,fpos = fscan(ifil,sterm,start_pos = current_pos)
    ifil.seek(current_pos)
    for l in range(linecount+1):
            ofil.write(ifil.readline())
    ofil.write(astr)
    if finish:
        for l in ifil:
                ofil.write(l)
            
def backup_file(fp,append = "_backup"):

    fil = open(fp,'rb')
    bckpath = ""
    bckname = ""
    if fil:
        fpsplit = fp.split("\\")
        fnsplit = fpsplit[-1].split(".")
        fn_base = ".".join(fnsplit[0:-1])
        fp_base = "\\".join(fpsplit[0:-1])
        fn_type = fnsplit[-1]
        bckpath = fp_base + "\\"
        bckname = fn_base + append + "." + fn_type
        backup = open(bckpath+bckname,'wb')
        if backup:
            for l in fil:
                backup.write(l)
            
        backup.close()
    fil.close()
    return (bckpath,bckname)
    
def split_fname(fn,delim = "\\"):
    fnsplit = fn.split(".")
    fname = ".".join(fnsplit[0:-1])
    ext = fnsplit[-1]
    return (fname,ext)
    
def get_ext(fpath):
    return fpath.split(".")[-1]
    
def enumdict(target):
    return {idx:i for idx,i in enumerate(target)}
    
def enumdictr(target):
    return {i:idx for idx,i in enumerate(target)}

def split_at_first(delim,target):
    delimidx = target.index(delim)
    return (target[0:delimidx],target[(delimidx+1):len(target)])
    
def split_fpath(fn,delim = "\\",mode = 0):
    if mode != 0:
        return split_fullpath(fn,delim = delim)
    fpsplit = fn.split(delim)
    base_pth = delim.join(fpsplit[0:-1])
    #return the filename
    return (base_pth,fpsplit[-1])
fpath_split = split_fpath

#just an alias
def split_fullpath(fn,delim = "\\"):
    if "." not in fn:
        return 0
    fpsplit = fn.split(delim)
    base_pth = delim.join(fpsplit[0:-1])
    fnsplit = fpsplit[-1].split(".")
    fname = ".".join(fnsplit[0:-1])
    ext = fnsplit[-1]
    return (base_pth,fname,ext)
    
def build_fpath(ext,*args):
    return "\\".join(args) + "." + ext

def fns_from_glob(fpath,g):
    return tuple(s.replace(fpath+"\\","") for s in g)

def globberate(fpath):
    """
    Given a full path to a file, return a string that can be passed to the glob function that will find 
    files in the same folder with the same extension.
    In other words, just replace the file's name with *.
    """
    fpsplit = split_fpath(fpath,mode = 1)
    res = fpsplit[0] + "\\*." + fpsplit[1]
    return res
    
def try_unique_fn(fpath,lim = 100,appendn = "STT"):
    pth,fn,ext = split_fullpath(fpath)
    if os.path.exists(fpath):
        for x in range(lim):
            testexistname = pth + "\\" + fn + "_"+str(x)+appendn +"."+ ext
            if os.path.exists(testexistname):
                pass
            else:
                return testexistname
    else:
        return fpath

def default_outpath(fpath,delim = "\\"):
    basepath,fn,ext = split_fullpath(fpath)
    newpath = basepath + "\\" + fn + "_OUT." + ext
    return try_unique_fn(newpath)
    
get_out_name = default_outpath
    
def try_unique_fpath(fpath,lim = 100,appendn = "STT"):
    pth,fol = split_fpath(fpath)
    if os.path.exists(fpath):
        for x in range(lim):
            testexistname = pth + "\\" + fol + "_"+str(x)+appendn
            if os.path.exists(testexistname):
                pass
            else:
                return testexistname
    else:
        return fpath
        
def io_path(fp,fn,ext,out_tag = "_OUT"):
    fn_o = fn + out_tag
    fn = fn + ext
    fullpath = fp + "\\" + fn
    fullpath_out = fp + "\\" + fn_o

    return(fullpath,fullpath_out,(fp,fn,fn_o,ext,out_tag))
    
def get_vpds(filepath):
    vpds = []
    folders = []
    def checkfolder(folderpath,type):
        typelen = len(type)
        print("HOOOOOOOOOOOOWAWA2!?",folderpath)
        vpdfolder = os.listdir(folderpath)
        for f in vpdfolder:
            if f[-typelen::] == ".vpd":
                vpds.append(folderpath+"\\"+f)
                
            #if the file is not of the specified type
            elif "." in f:
                pass
            else:
                folders.append(folderpath+"\\"+f)

    #run an initial check
    checkfolder(filepath,'.vpd')

    checkedfolders = []
    #
    uncheckedfolders = True
    c=0
    while uncheckedfolders == True:
        flen = len(folders)
        for f in range(flen):
            if not os.path.isdir(folders[f]):
                continue
            checkfolder(folders[f],'.vpd')
            checkedfolders.append(folders[f])
        folders = folders[flen::]
        if len(folders) == 0:
            uncheckedfolders = False
            break
        c+=1
        if c>5000:
            break
    return vpds
    


#parses a list of property/index access commands
#currently takes a string of python accessor commands delimited by @
#returns a series of functions which access an object's propert(ies) as directed,
#followed by a tuple containing their packed arguments
#
#the command delimiter, base_delim, is set to "@"
#so write commands in chains of @ before each access operator
#like:
#
#cmdizzle = "foo@.bar@[\"shoo\"]@.shaw@($\"hoo\",\"ha\",#that=\"thehooha\",)"
#cmdizzler = r"foo@.bar@[\"shoo\"]@.shaw@($\"hoo\",\"ha\",#that=\"thehooha\",)"
#
#using literal(r-prefixed) strings is probably for the best
#but that's TODO because i'm dumb
def accessor_breakdown(accsrcmd,base_delim = "@"):
    cmd = accsrcmd.split(base_delim)
    tar_item = cmd[0]
    cmd = cmd[1::]
    seq = []
    for c in cmd:
        #print(c)
        #key or index access
        if c[0] == "[":
            acc_key = c[1:-1]
            q = (acc_key.count("\"")) + (acc_key.count("\'"))
            
            #temporary fix to allow keys to be passed as strings
            #without stripping afterwards they become double quoted and unusable
            #maybe start using r strings instead, dummy
            if q > 0:
                acc_key = ";"+acc_key
            #seq.append(lambda x:x[acc_key])
            seq.append((lambda x,y:x[y],tuple((acc_key,))))   

        #function call
        elif c[0] == "(":
            acc_args,acc_kwargs = c.split("#")
            
            #if a comma exists at the end of the list, as is common in python,
            #it causes an unneeded extra null character to be produced in the list
            #which can mess up argument count.
            #so we'll strip it. 
            if acc_args[-1] == ",":
                acc_args = acc_args[0:-1]
            
            #split the list of args and keyword arguments into a list
            #currently will encounter problems if part of some argument
            #actually contains a comma; need some sort of escape to differentiate?
            acc_args = tuple(acc_args[2::].split(","))
            acc_kwargs = acc_kwargs[0:-2].split(",")
            
            #pack the list of kwargs into a dictionary
            kwargs = {}
            for item in acc_kwargs:
                isplit = item.split("=")
                kwargs.update({isplit[0]:isplit[1]})
            
            #seq.append(lambda x:x(*args,**kwargs))
            
            #if you simply directly append a lambda function,
            #it seems the passed variable will be tied to later executions of the loop,
            #so pass the arguments separately to make sure we can pass the
            #variable in its current state
            seq.append((lambda x,y,z:x(*y,**z),tuple((acc_args,kwargs))))    
        
        #class-based .accessor
        elif c[0] == ".":
            acc_token = c[1::] 
            #seq.append(lambda x:getattr(x,acc_token))
            seq.append((lambda x,y:getattr(x,y),tuple((acc_token,))))    
    return seq

#function which accesses a python item using a sequence of 
#functions produced by the above function
def accessor_sequence_exec(seq,base):
    res = base
    for s in seq:
        f,args = s
        arglist = []
        for a in range(len(args)):
            arg = args[a]
            if (type(arg) == str) and (arg[0] == ";"):
                    arglist.append(arg[2:-1])
            else:
                arglist.append(arg)
        res = f(res,*arglist)
    return res

def accessr(acc_cmd,target):
    bd = accessor_breakdown(acc_cmd)
    return accessor_sequence_exec(bd,target)

def acc(o,instrs,):
    """
    Parse an accessor string into a series of getattr statements.
    """

    instrs = acc_instparse(instrs)
    #For the case in which the instructions contain no accessors; skip the loop and return o.
    if instrs == ():
        return o
    
    return accrate(o,instrs,0)

def accrate(o,instrs,parse_index):
    if parse_index == len(instrs):
        return o
    ftype,i = instrs[parse_index]
    #Loop over the instructions.
    if ftype:
        g = lambda x,y: x.__getitem__(y)
        if "\"" in i:
            i = i.replace("\"","")
        else:
            i = int(i)
    else:
        g = getattr
    return accrate(g(o,i),instrs,parse_index + 1)

def accset(o,instrs,val):
    """
    Parse an accessor string into a series of getattr statements.
    """

    instrs = acc_instparse(instrs)
    #For the case in which the instructions contain no accessors; skip the loop and return o.
    if instrs == ():
        return o
    
    return accsetrate(o,instrs,val,0)

def accsetrate(o,instrs,val,parse_index):
    if parse_index == len(instrs)-1:
        return setattr(o,instrs[-1][-1],val)
    ftype,i = instrs[parse_index]
    #Loop over the instructions.
    if ftype:
        g = lambda x,y: x.__getitem__(y)
        if "\"" in i:
            i = i.replace("\"","")
        else:
            i = int(i)
    else:
        g = getattr
    return accsetrate(g(o,i),instrs,val,parse_index + 1)
    
def acc_instparse(i,accdict = {'.':'0','[':'1','(':'2'}):
    def clip_initial(inst,accdict = {'.':'0','[':'1','(':'2'}):
        for i in range(len(inst)):
            if inst[i] in "([.":
                return accdict[inst[i]] + inst[(i+1)::]
    rgxer = r'[.[(]'
    parse_res = clip_initial(i)
    if parse_res == None:
        return ()
    elif len(parse_res) == 1:
        raise ValueError("Malformed accessor string")
    inst = parse_res.replace(".",".0").replace("[","[1").replace("(","(2").replace(")","").replace("]","")
    return tuple(map(lambda x: (bool(int(x[0])),x[1::]),re.split(rgxer,inst)))

def prop_switch(o,prop,new_val = True):
    init_val = acc(o,prop)
    c = 0
    while True:
        is_even = even(c)
        if is_even:
            accset(o,prop,new_val)
        else:
            accset(o,prop,init_val)
        yield is_even
        c+=1
    
#old version
'''
def acc(o,instrs,do_parse = True):
    if do_parse:
        instrs = acc_instparse(instrs)
    for ftype,i in instrs:
        if ftype:
            g = lambda x,y: x.__getitem__(y)
            if "\"" in i:
                i = i.replace("\"","")
            else:
                i = int(i)
        else:
            g = getattr
        return acc(g(o,i),instrs[1::],do_parse = False)
    return o

def acc_instparse(i):
    def clip_initial(inst):
        accdict = {'.':'0','[':'1','(':'2'}
        for i in range(len(inst)):
            if inst[i] in "([.":
                return accdict[inst[i]] + inst[(i+1)::]

    rgxer = r'[.[(]'
    inst = clip_initial(i).replace(".",".0").replace("[","[1").replace("(","(2").replace(")","").replace("]","")
    
    return tuple(map(lambda x: (bool(int(x[0])),x[1::]),re.split(rgxer,inst)))
'''

def avg(x):
    assert(len(x)!=0)
    return sum(x)/len(x)
    
def seqinsert(seq,target_val,insert_val):
    pass
    
class st_range():
    def __init__(self,s,e,step):
        self.range = range(s,e,step)
        
        pass
    def __add__(self,other,):
        pass
        
#determine how to restore an item by looking up its type
#in a dictionary
#the dictionary must contain:
    #a method of getting the item from whatever contains it using getattr
    #function used to access the immediate value
    #the container of the item as a string parsable using the accessr function
def restore_item(i,retrieval_dict):
    prop,get_type,dp = retrieval_dict[type(i)](i)
    acc_cmd = "@.".join(dp.split("."))
    parent_item = accessr(acc_cmd,bpy)
    return getattr(parent_item,get_type)(prop)
    
def dot_old(vec1,vec2):
    return vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2]

def dot(vec1,vec2):
    sum(map(operator.mul, vec1, vec2))
    
def dot_n(vec1,vec2):
    if (len(vec1) < len(vec2)):
        print("Length of second vector must gequal to first")
        raise ValueError
    res = 0
    while v < len(vec1):
        res += vec1[v]*vec2[v]
        v+=1
    return res
    
def cross(vec1,vec2):
    res = tuple(vec1[x]*vec2[(x+1)%lenvec]-vec1[(x+1)%lenvec]*vec2[x] for x in vecrange)
    return tuple(
                    (
                        vec1[1]*vec2[2]-vec1[2]*vec2[1],
                        vec1[2]*vec2[0]-vec1[0]*vec2[2],
                        vec1[0]*vec2[1]-vec1[1]*vec2[0]
                    )
                )
            
def cross_n(vec1,vec2):
    if (len(vec1) < len(vec2)):
        print("Length of second vector must gequal to first")
        raise ValueError
    res = 0
    lenvec = len(vec1)
    vecrange = (lenvec-2,lenvec-1,*(range(lenvec-2)))
    #cross_idxes = tuple(tuple((x,(x+1)%lenvec,(x+1)%lenvec,x)) for x in vecrange)
    v = lenvec-2
    print(vecrange)
    res = tuple(vec1[x]*vec2[(x+1)%lenvec]-vec1[(x+1)%lenvec]*vec2[x] for x in vecrange)
    return res

def tail(arg):
    return arg[-1]
    
def nested_tail(arg):
    try:
        #test if arg is a pair or more
        len(arg)
        return supernested_tail(arg[-1])
        #test if arg's tail is a pair or more
    except:
        return arg
        
        

    
        
def cond(*cond_clauses):
    clause_p1 = tmap(lambda c: c[0] == "else",cond_clauses)
    clause_p2 = tmap(lambda c: True and c[0],cond_clauses)
    clause_lens = tmap(lambda c: try_wrap(len)(c),cond_clauses)
    
    return
    clause_count = len(cond_clauses)
    if len(cond_clauses) == 0:
        return None
    for caseidx in range(clause_count):
        case = cond_clauses[caseidx]
        if case[0] == "else":
            if caseidx != clause_count:
                raise ValueError
            test_expr = case[-1]
            then_expr = then_bodies[-1]
            if (test_expr[0])(*test_expr[1],**test_expr[2]):
                pass
        if len(case) == 1:
            lambda d = case[0](): 1
        if 1:
            return t
    #return results of evaluated expressions; v is some value, f is a procedure which takes one argument, n is None for else
    fs = ["v","v_f","v_v","n_f","else"]
    pass
    
    
#############################lispish

def assoc(item, lst, key = None,test = None):
    if key == None:
        key = id_func
    if cndf == None:
        def cndf(x):
            return key(x[0]) == item
    return andmap(cndf,lst)
    
def conjoin(targets,fs):
    pass
    
def disjoin(targets,fs):
    pass
    
def curry(f,a):
    def nf(*args):
        return f(a,*args)
        pass
    return nf

def rcurry(f,a):
    def nf(*args):
        return f(*args,a)
        pass
    return nf
    
def postjoin(i,lst):
    return (*lst,i)
    
def adjoin(i,lst):
    for item in lst:
        if item == i:
            return lst
    return (i,*lst)

def every(f,lsts):
    return all(map(f,zip(lsts)))

def some(f,lsts):
    return any(map(f,zip(lsts)))

def eql(a,b):
    return a == b

def y_combinator(x):
    return x(x)
    
def car(a):
        return a[0]

def cdr(b):
        return b[1]

def cprp(s):
    if s[0] == "c": return s[1:-1]
    else: return s[1:-1]

def cpr_fgen(s):
    return map(lambda x: car if x == 'a' else cdr,(cprp(s)))

#parse a silly car/cdr string
def cpr(s,a):
    return reduce(lambda x,y: y(x),((a),*cpr_fgen(s)))
    
def cons(a,b):
    return (a,b)
    
def fcons(a,b,c=0):
    def f():
        c = not c
        return (a,b)[c]
    return f
    
def delay(exp):
    def expret():
        return exp
    return expret
    
def force(exp):
    return exp()    
    
def saturate(chk_val,max = 1, min = 0):
    if chk_val > max:
        chk_val = max
    if chk_val < min:
        chk_val = min
    return chk_val

def ob_search(ob,sterm):
    res = []
    for o in ob:
        #rgxres = re.search(sterm,str(o),)
        #if rgxres:
        if sterm in str(o):
            res.append(o)
    return res

def lst_shift(lst,count = 1):
    for x in range(count):
        lst.append(lst.pop(0))
    return lst
    
def lst_shift_ex(lst,count = 1):
    lst_new = lst[count:len(lst)]+lst[0:count]
    lst.clear()
    lst += lst_new
    return lst

def item_insert(target,data,insert_point):
    """
    (target,data,insert_point)
    args: 
        target: 
            some tuple
        data: 
            some tuple; if you want to insert a single data item, pack it into a 1-item tuple
        insert point: 
            point to insert the data at
    """
    return (*target[0:insert_point],*data,*target[insert_point::])

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

def getidx(lst,*args):
    return tuple(lst[i] for i in args)
    
def order_list_by_list(lst1,lst2,sort_prop = "name"):
    idict = {getattr(i,sort_prop):i for i in lst1}
    ordered_list = []
    for i in lst2:
        try:
            ordered_list.append(idict[i])
        except Exception as e:
            #print(str(e),)
            pass
    for i in lst1:
        if i not in ordered_list:
            ordered_list.append(i)
    return ordered_list

def filter_strings_by_tag(str_list,target_parent = 3,tag = r"親",is_indexed = True,count_relevant = 0):
    if is_indexed:
        rgxer = r"(" + tag + r"\d+)"
    else:
        rgxer = "(" + tag + ")"
    res = map(lambda i: None if not ((len(str_list[i]) > 2)) else re.search(rgxer,str_list[i][(len(tag)+int(is_indexed))+count_relevant::]) != None,range(len(str_list)))
    return tuple(res)
    
#not working
def range_split(iter,split_indices):
    offset = min(split_indices)
    step = max(split_indices) - offset
    end = len(iter)
    last_split = split_indices[len(split_indices)-1]
    print(last_split,end-step+last_split)
    if end > (end-step+last_split):
        end = end - last_split
    r = range(offset,end,step)
    print(tuple(r))
    return map(lambda x: (iter[x+i] for i in split_indices),r)

 
def chain_up(lst,):
    return zip_longest(lst,lst_shift(lst))

def by_x(lst,step):
    return (lst[n:step+n] for n in range(0,int(len(lst)),step))
    
def dumb_ichk(i,lim):
    item = i
    indexable = True
    depth=0
    while indexable:
        try:
            item = item[0]
        except:
            break
        if depth>lim:
            break
        depth+=1
    return depth
    
def dumb_ichk2(i,lim = 10):
    item = i
    indexable = True
    depth=0
    while True:
        if "__len__" in dir(item):
            item = item[0]
        else:
            break
        if depth>lim:
            break
        depth+=1
    return (item,depth)

#for working with mathutils objects
def dot2(x,y):
    return x.dot(y)    
def cross2(x,y):
    return x.cross(y)
    
def combit():
    pass
    
def base_combit():
    pass

def filter_by_name(target_name,lst,pref = "",suf = "",extract = False,name_prop = "name",getf = getattr,do_negate = False):
    if extract:
        lst = (getf(i,name_prop) for i in lst)
    return filter(lambda iname: cnegate(re.search(pref+target_name+suf,iname[1]),condition = do_negate),enumerate(lst))

def get_lr_name(name,lang = "jp"):
    lrdict = {
    "jp":(("右","左"),lambda x,lr: lr + x),
    "en":(("_L","_R"),lambda x,lr: x + lr),
    "en.":((".L",".R"),lambda x,lr: x + lr),
    }

    lrtype = lrdict[lang]
    names = []
    for t in lrtype[0]:
        names.append(lrtype[1](name,t))
    return names
    
def lr_fill(name_list):
    lrized = tuple(get_lr_name(i) for i in name_list)
    return tuple((lr[0]) for lr in lrized),tuple((lr[1]) for lr in lrized)
    
class idxiter():
    def __init__(self,iterable):
        self.iterable = iterable

    def __getitem__(self,idx):
        return nth(self.iterable,idx)

def rec_unmap(x,unpack_hint = None,use_try = False,tuplize = False):
    if tuplize:
        return tuple(rec_unmap(x,unpack_hint = unpack_hint,use_try = use_try,tuplize = False))
    for y in x:
        if type(y) == map:
            for z in rec_unmap(y):
                yield z
        else:
            yield y

@tuplize
def trec_unmap(x,unpack_hint = None,use_try = False):
    for y in x:
        if type(y) == map:
            for z in rec_unmap(y):
                yield z
        else:
            yield y

            
def rec_unmap2(x,c,unpack_hint = None,use_try = False):
    for y in x:
        t = type(y)
        if t in (map,gentype,range):
            for z in rec_unmap2(y,c+1,unpack_hint = unpack_hint,use_try = use_try):
                yield z
        elif t in (list,tuple,set):
            if unpack_hint[c]:
                for z in rec_unmap2(y,c+1,unpack_hint = unpack_hint,use_try = use_try):
                    yield z
            else:
                yield y
        else:
            yield y
            
def rec_unmap3(x,c,unpack_hint = None,unpack_instrs = None,use_try = False):
    for y in x:
        t = type(y)
        #if the next unpack step requires property accessing, do the access and continue on the result
        if unpack_hint[c] == 2:
            y = acc(y,unpack_instrs[c])
        if t in (map,gentype,range):
            for z in rec_unmap2(y,c+1,unpack_hint = unpack_hint,use_try = use_try):
                yield z
        elif t in (list,tuple,set):
            if unpack_hint[c]:
                for z in rec_unmap2(y,c+1,unpack_hint = unpack_hint,use_try = use_try):
                    yield z
            else:
                yield y
        else:
            yield y
            
def cycler(coll,target,coll_accessor = "bpy.data.textures",prop = ""):
    dc = acc(coll,coll_accessor)
    icount = len(dc)
    idx = dc[:].index(getattr(target,prop))
    next_item = dc[(idx+1)%icount]
    setattr(target,prop,next_item)
#dynamic decorate
def dyndec(dec,f,*args,**kwargs):
    newf = dec(f,*args,**kwargs)
    def decced(*args2,**kwargs2):
        return newf(*args2,**kwargs2)
    return decced
    
def reorder(new_order,c):
    return tmap(lambda x: c[x],type(new_order)(new_order))

#vector map return retrieve example
#q = map(lambda x: (lambda v: ((v).rotate(Euler((30,90,20))),v))(Vector(x))[1],cos)
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
    
    

##############################################################################WHO IS RESPONSIBLE FOR THIS
#unpacks a tuple into several data interpretation items:
#by index,
    #data:
        #data to apply functions to
    #functions:
        #functions to apply to data ranges
    #ranges of data:
        #correspond to which functions to apply to which ranges
        #one function for each n preceding this
    #-1 location of data and range boundary


def modulator(coll):
    def modulated(x):
        return x%len(coll)
    return modulated

def frange(f,*args):
    return (f(i) for i in range(*args))
    
@tuplize
def tfrange(f,*args):
    return (f(i) for i in range(*args))


class srange():
    """A class for representing stupidity in compact form."""
    def __init__(self,s,*args,proc = None,coll = None):
        self.s,self.e,self.step = argfill(3,s,*args,)
        if self.step == None:
            self.step = 1
        self.eidx = None
        self.sidx = None
        self.length = len(coll)
        self.modulator = None
        self.modulus = None
        if proc == None:
            self.proc = id_func
        else:
            self.proc = proc
        if self.e == None:
            self.eidx = self.length-1
        if coll == None:
            self.modulus = 10
            self.range = range(s,*args)
        else:
            self.modulator = modulator(coll)
            for x in range(self.length):
                if coll[x] == self.s:
                    self.sidx = x
                elif coll[x] == self.e:
                    self.eidx = x
                
                if all(map(none_test,(self.sidx,self.eidx))):
                    print("brakken like the kraken")
                    break
            self.modulus = self.length
        self.coll = coll
        self.cidx = self.sidx
        self.range = range(*filter(inverterate(none_test),(self.sidx,self.eidx,self.step)))
    def __add__(self,other):
        return (self,other)
        pass
    def __call__(self,s,*args):
        if all(map(lambda i: type(i) == int,(s,*args))):
            r = range(s,*args)
        else:
            raise ValueError
    def __iter__(self,):
        self.cidx = self.sidx
        return (self.proc(self.coll[i]) for i in self.range)
    def __next__(self,):
        n = self.range[self.cidx]
        self.cidx = (self.cidx+1)%self.modulus
        return n
    def __getitem__(self,item):
        return [self.coll[i] for i in self.range[item]]
    def __str__(self,):
        print(self.sidx,self.eidx)
        return "srange("+str(self.coll[self.sidx])+", "+str(self.coll[self.eidx])+")"
    def __len__(self,):
        return len(self.coll)

def similarity_unpack(packed):
    item_length = len(packed)
    range_data = len(packed)-packed[-1] - 1
    ranges = packed[range_data:-1]
    fcount = len(ranges) 
    range_range = tuple(range(fcount))
    fidx = sum(ranges)
    frange = tuple(range(fidx,item_length-fcount-1))
    ranges_starts = reduce(lambda x,y: (*x,x[-1]+y,),((0,),*ranges))
    data_ranges = tmap(lambda r: (ranges_starts[r],ranges_starts[r+1]),range_range)
    def item_pull(coll,idx):
        return coll[idx]
    def iter_pull(coll,r):
        def pull(idx):
            return coll[idx]
        return map(pull,range(*r))
    def argcall(f,a):
        def argcalled(*args,**kwargs):
            return f(a,*args,**kwargs)
        return argcalled
    ipull = argcall(item_pull,packed)
    itpull = argcall(iter_pull,packed)
    
    #fs = tuple(map(ipull,frange))
    #data = tuple(map(itpull,data_ranges))
    #return tmap(lambda i: (data[i],fs[i]),range_range)
    fs = map(ipull,frange)
    data = map(itpull,data_ranges)
    return map(lambda i: (data.__next__(),fs.__next__()),range_range)


def similarity_pack(cases,handling_funcs,handling_ranges):
    def f(i):
        return i
    range_count = len(handling_ranges)
    if range_count < len(handling_funcs):
        raise ValueError("Not enough ranges to handle handlers: Number of ranges,number of functions = ",range_count,len(handling_funcs))
    res = (*cases,*handling_funcs,*handling_ranges,range_count)
    return res

def similarity_exec(unpackerated):
    return map(lambda i: map(i[1],i[0]),unpackerated)
'''
if __name__ != "__main__":
    done

fs = (lambda i: 2, lambda i: i+4)
data = (3,6,7,3,2,4,6,7,4,32,5,7,8,9,4,32,3,6,4,3,22,)

lendata = len(data)
w = tuple(expand(lambda d: (d,lendata-d),int(lendata/2)))
packerated = similarity_pack(data,fs,w)
unpackerated = similarity_unpack(packerated)

x = similarity_exec(unpackerated)
print(tuple(rec_unmap(x)))
'''

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
    
def unrotatehack(vec,idx_order = (0,1)):
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
    
#creates an identity vector generator in n dimensional space
#d: dimensionality
def dgen(rd):
    return (Vector((rd[y] == x for y in rd)) for x in rd)
def nvec(d):
    return dgen(tuple(range(d)))
#creates an identity vector in n dimensional space
#axis: axis to create
def dvec(axis,dimensionality,ret = 't'):
    if ret == 't':
        return tuple(map(lambda a: float(a == axis),range(dimensionality)))
    return map(lambda a: float(a == axis),range(dimensionality))

def make_circ(s,r,t,res):
    yield translate_g(*rotate_g(*scale_g(vectorize_g(*d_append(circ(res))),s),r),t)
    
def circ(res,slen = 0, elen = 1):
    fac = (2*pi)/(res)
    start = (0 for n in range(slen))
    end = (0 for n in range(elen))
    for x in range(res):
        c = fac*x
        yield (*start,sin(c),cos(c),*end)

    
def d_append(gen):
        yield map(lambda c: (*c,0),gen)
    
def vectorize_g(gen):
    yield map(lambda coordinate_array: Vector(coordinate_array),gen)

def translate_g(gen,t):
    yield map(lambda vec_obj: vec_obj+t,gen)

def rotate_g(gen,e):
    yield map(lambda vec_obj: (vec_obj.rotate(e),vec_obj)[1],gen)

def scale_g(gen,s):
    yield map(lambda vec_obj: vec_obj*s,*gen)