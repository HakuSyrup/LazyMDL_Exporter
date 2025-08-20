import os
import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
)
from bpy.types import PropertyGroup
from bpy_extras.io_utils import ExportHelper

def execute_Export(self, context):
    props = context.scene.Hakuinputs
    
    # Validate inputs
    if not props.export_name:
        self.report({'ERROR'}, "Enter MDL file name.")
        return {'FINISHED'}
    
    if not props.export_path:
        self.report({'ERROR'}, "Enter Export Path.")
        return {'FINISHED'}
    
    if not os.path.exists(props.export_path):
        self.report({'ERROR'}, 'This Export Path does not exist.')
        return {'FINISHED'}
    
    if not os.path.isabs(props.export_path):
        self.report({'ERROR'}, 'Export Path must be absolute path.')
        return {'FINISHED'}
    
    # Normalize path
    export_path = props.export_path
    if not export_path.endswith("\\"):
        export_path += "\\"
    
    # Determine file name
    if props.export_use_object_name:
        file_name = bpy.context.object.name
    else:
        file_name = props.export_name
    
    # Add prefix if specified
    if props.export_prefix and props.export_prefix.strip():
        file_name = props.export_prefix.strip() + "_" + file_name
    
    # Validate file name
    if len(file_name) > 29:
        self.report({'ERROR'}, 'Object name must be less than 29 characters.')
        return {'FINISHED'}
    
    if '\\' in file_name or '/' in file_name:
        self.report({'ERROR'}, 'Do not use "Backslash" or "Slash" in object name')
        return {'FINISHED'}
    
    # Execute export
    bpy.ops.export_mdl.some_data(
        exportScale=props.export_scale,
        use_setting=props.export_selection_only,
        export_skin2=props.export_all_skins,
        export_center=props.export_center,
        filepath=export_path + file_name + ".mdl",
    )
    
    # Export completed successfully
    return {'FINISHED'}


def get_addon_prefs():
    """Get addon preferences safely"""
    try:
        addon_name = __name__.rpartition('.')[0]
        return bpy.context.preferences.addons[addon_name].preferences
    except (KeyError, AttributeError):
        return None


def sync_props_with_prefs(props):
    """Sync properties with preferences if available"""
    prefs = get_addon_prefs()
    if not prefs:
        return
    
    # Map of property names to preference names
    prop_mapping = {
        'export_path': 'export_path',
        'export_name': 'export_name',
        'export_prefix': 'export_prefix',
        'export_scale': 'export_scale',
        'export_selection_only': 'export_selection_only',
        'export_all_skins': 'export_all_skins',
        'export_center': 'export_center',
        'export_use_object_name': 'export_use_object_name',
        'export_individually': 'export_individually',
        'export_force_origin': 'export_force_origin',
        'export_force_rotation': 'export_force_rotation',
        'edge_split_angle': 'edge_split_angle'
    }
    
    for prop_name, pref_name in prop_mapping.items():
        if hasattr(prefs, pref_name):
            setattr(props, prop_name, getattr(prefs, pref_name))


class LazyMDLExporter_Props(PropertyGroup, ExportHelper):
    def get_default_value(self, attr_name, fallback):
        """Get default value from preferences or fallback"""
        prefs = get_addon_prefs()
        if prefs and hasattr(prefs, attr_name):
            return getattr(prefs, attr_name)
        return fallback
    
    export_path: StringProperty(
        name="Export Path",
        description="Path for Export MDL",
        subtype='FILE_PATH',
        default=""
    )
    
    export_name: StringProperty(
        name="File Name",
        description="MDL file name",
        default="Object"
    )
    
    export_prefix: StringProperty(
        name="Prefix",
        description="Prefix for MDL file name",
        default=""
    )
    
    export_scale: FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0, max=1000.0,
        default=1000.0
    )
    
    export_selection_only: BoolProperty(
        name="Export Selection Only",
        description="Uncheck to export all objects",
        default=True
    )
    
    export_all_skins: BoolProperty(
        name="Export All Skins",
        description="Export additional skins",
        default=False
    )
    
    export_center: BoolProperty(
        name="Center model (aligned to 32 units)",
        description="Center model alignment",
        default=True
    )
    
    export_use_object_name: BoolProperty(
        name="Use Object Name",
        description="Use object name for export",
        default=True
    )
    
    export_individually: BoolProperty(
        name="Export individually",
        description="Export each object individually by its name",
        default=True
    )
    
    export_force_origin: BoolProperty(
        name="Force origin as object location",
        description="Force origin to object location",
        default=True
    )
    
    export_force_rotation: BoolProperty(
        name="Reset object rotation",
        description="Reset object rotation during export",
        default=False
    )
    
    edge_split_angle: FloatProperty(
        name="Edge Split Angle",
        description="Edge Split Angle",
        min=0.0, max=180.0,
        default=30.0
    )