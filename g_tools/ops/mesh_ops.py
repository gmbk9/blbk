#importdefs
import bpy
from g_tools.bpy_itfc_funcs import mesh_fs
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty 
from bpy.types import Operator

#fdef


#opdef
class w_mirror_op(bpy.types.Operator):
    """ウェイトの鏡像化"""
    bl_idname = "mesh.w_mirror"
    bl_label = "Weight mirror"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    scale = bpy.props.FloatProperty(default=1.0)
    precision = bpy.props.IntProperty(default=4)
    target_shape_key_index = bpy.props.IntProperty(default=0)
    use_active_shape_key = bpy.props.BoolProperty(default=False)
    do_clear = bpy.props.BoolProperty(description = "Clear original weights on mirror targets",default=True)
    '''
    type = EnumProperty(
            name="Mirroring type",
            description="Choose mirroring type",
            items=(('l>r', "Left to right", "Mirror from left to right"),
                   ('l<r', "Right to left", "Mirror from right to left"),
                   ('both', "Both", "Mirror across both sides")),
            default='both',
            )
    '''

    def execute(self, context):
        mesh_fs.mirror_weights_exec(scale = self.scale, precision = self.precision, do_clear = self.do_clear, target_shape_key_index = self.target_shape_key_index, use_active_shape_key = self.use_active_shape_key,oper = self)
        return {'FINISHED'}

class mirror_sel_op(bpy.types.Operator):
    """機能が拡張（？）された頂点の鏡像選択"""
    bl_idname = "mesh.mirror_sel"
    bl_label = "Alternative mirror select"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    extend = bpy.props.BoolProperty(default=True)
    basis = bpy.props.BoolProperty(default=True)
    target_shape_key_index = bpy.props.IntProperty(default=0)
    use_active_shape_key = bpy.props.BoolProperty(default=False)
    cutoff = bpy.props.FloatProperty(description = "Middle cutoff",default=0.001)
    scale = bpy.props.FloatProperty(default=1.0)
    precision = bpy.props.IntProperty(default=4)
    type = EnumProperty(
            name="Mirroring type",
            description="Choose mirroring type",
            items=(('l>r', "Left to right", "Mirror from left to right"),
                   ('l<r', "Right to left", "Mirror from right to left"),
                   ('both', "Both", "Mirror across both sides")),
            default='both',
            )

    def execute(self, context):
        mesh_fs.mirror_sel(cutoff = self.cutoff, scale = self.scale, precision = self.precision, type = self.type, extend = self.extend, target_shape_key_index = self.target_shape_key_index, use_active_shape_key = self.use_active_shape_key)
        return {'FINISHED'}

#opdef
class clean_vertex_groups_op(bpy.types.Operator):
    """頂点グループ欄を見やすくする為にウェイト情報がない頂点グループをメッシュから削除する"""
    bl_idname = "mesh.sclean_vertex_groups"
    bl_label = "Clean vertex groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        mesh_fs.clean_vertex_groups()
        return {'FINISHED'}

#opdef
class parts_to_vgroups_op(bpy.types.Operator):
    """メッシュのパーツそれぞれを頂点グループとして登録する"""
    bl_idname = "mesh.parts_to_vgroups"
    bl_label = "Parts to vertex groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'UNDO', 'REGISTER'}

    vg_name = bpy.props.StringProperty(default="part_group_")

    def execute(self, context):
        mesh_fs.parts_to_vgroups(vg_name = self.vg_name)
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
        row = layout.row()
        row.operator("mesh.w_mirror")

        #rowdefs
        row = layout.row()
        row.operator("mesh.mirror_sel")

        #rowdefs
        row = layout.row()
        row.operator("mesh.sclean_vertex_groups")
        #rowdefs
        row = layout.row()
        row.operator("mesh.parts_to_vgroups")

def register():
    #regdef
    bpy.utils.register_class(w_mirror_op)
    bpy.utils.register_class(mirror_sel_op)
    bpy.utils.register_class(clean_vertex_groups_op)
    bpy.utils.register_class(parts_to_vgroups_op)
    bpy.utils.register_class(GMeshPanel)

def unregister():
    #unregdef
    bpy.utils.unregister_class(w_mirror_op)
    bpy.utils.unregister_class(mirror_sel_op)
    bpy.utils.register_class(clean_vertex_groups_op)
    bpy.utils.register_class(parts_to_vgroups_op)
    bpy.utils.unregister_class(GMeshPanel)
    
    