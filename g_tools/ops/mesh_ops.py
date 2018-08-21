#importdefs
import bpy
from g_tools.bpy_itfc_funcs import mesh_fs
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty 
from bpy.types import Operator

#fdef


#opdef
class w_mirror_op(bpy.types.Operator):
    """NODESC"""
    bl_idname = "mesh.w_mirror"
    bl_label = "Weight mirror"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    selected_only = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        mesh_fs.mirror_weight()
        return {'FINISHED'}


class mirror_sel_op(bpy.types.Operator):
    """NODESC"""
    bl_idname = "mesh.mirror_sel"
    bl_label = "Alternative mirror select"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    extend = bpy.props.BoolProperty(default=True)
    basis = bpy.props.BoolProperty(default=True)
    active_key = bpy.props.BoolProperty(default=True)
    cutoff = bpy.props.FloatProperty(default=0.001)
    scale = bpy.props.FloatProperty(default=1.0)
    prec = bpy.props.IntProperty(default=4)
    type = EnumProperty(
            name="Mirroring type",
            description="Choose mirroring type",
            items=(('l>r', "Left to right", "Mirror from left to right"),
                   ('l<r', "Right to left", "Mirror from right to left"),
                   ('both', "Both", "Mirror across both sides")),
            default='both',
            )

    def execute(self, context):
        mesh_fs.mirror_sel(cutoff = self.cutoff, scale = self.scale, prec = self.prec, type = self.type, extend = self.extend)
        return {'FINISHED'}


class GMeshPanel(bpy.types.Panel):
    """Creates a Panel in the 3D View"""
    bl_label = "GMesh"    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "G Tools"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        #rowdefs
        #row = layout.row()
        #row.operator("mesh.w_mirror")

        #rowdefs
        row = layout.row()
        row.operator("mesh.mirror_sel")
        
def register():
    #regdef
    #bpy.utils.register_class(w_mirror_op)
    bpy.utils.register_class(mirror_sel_op)
    bpy.utils.register_class(GMeshPanel)

def unregister():
    #unregdef
    #bpy.utils.unregister_class(w_mirror_op)
    bpy.utils.unregister_class(mirror_sel_op)
    bpy.utils.unregister_class(GMeshPanel)
    
    