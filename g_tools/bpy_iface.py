import bpy

def defac(f):
    def defactived(*args,obj = None,**kwargs):
        if obj == None:
            obj = bpy.context.scene.objects.active
        return f(*args,obj = obj,**kwargs,)
    return defactived

def moderate(mode):
    mode = mode.upper()
    def moderator(f):
        def moderated(*args,**kwargs):
            original_mode = set_mode(mode)
            res = f(*args,**kwargs)
            set_mode(original_mode)
            return res
        return moderated
    return moderator
    
def set_ac(obj):
    ac = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = obj
    return ac
    
def set_mode(new_mode):
    mode = bpy.context.scene.objects.active.mode
    bpy.ops.object.mode_set(mode=new_mode)
    return mode
	
