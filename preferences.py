import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
)
from bpy.types import AddonPreferences

class LazyMDLExporter_Preferences(AddonPreferences):
    bl_idname = __name__.rpartition('.')[0]
    
    export_path: StringProperty(
        name="Export Path",
        subtype='FILE_PATH',
        description="Default export path for MDL files",
        default=""
    )
    
    export_name: StringProperty(
        name="File Name",
        description="Default MDL file name",
        default="Object"
    )
    
    export_prefix: StringProperty(
        name="Prefix",
        description="Default prefix for MDL file names",
        default=""
    )
    
    export_scale: FloatProperty(
        name="Scale Multiplier",
        description="Default scale multiplier for export",
        min=0.0, max=1000.0,
        default=1000.0
    )
    
    export_selection_only: BoolProperty(
        name="Export Selection Only",
        description="Export selected objects only by default",
        default=True
    )

    export_all_skins: BoolProperty(
        name="Export All Skins",
        description="Export additional skins by default",
        default=False
    )
    
    export_center: BoolProperty(
        name="Center model (aligned to 32 units)",
        description="Center model alignment by default",
        default=True
    )
    
    export_use_object_name: BoolProperty(
        name="Use Object Name",
        description="Use object name for export by default",
        default=True
    )
    
    export_individually: BoolProperty(
        name="Export Individually",
        description="Export each object individually by default",
        default=True
    )
    
    export_force_origin: BoolProperty(
        name="Force Origin as Object Location",
        description="Force origin to object location by default",
        default=True
    )
        
    export_force_rotation: BoolProperty(
        name="Reset Object Rotation",
        description="Reset object rotation during export by default",
        default=False
    )
    
    edge_split_angle: FloatProperty(
        name="Edge Split Angle",
        description="Default edge split angle",
        min=0.0, max=180.0,
        default=30.0
    )
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Default Settings:")
        
        col = layout.column(align=True)
        col.prop(self, "export_use_object_name")
        col.prop(self, "export_name")
        col.prop(self, "export_prefix")
        col.prop(self, "export_path")
        
        col.separator()
        col.prop(self, "export_scale")
        col.prop(self, "export_selection_only")
        col.prop(self, "export_all_skins")
        col.prop(self, "export_center")
        col.prop(self, "export_individually")
        
        col.separator()
        col.prop(self, "export_force_origin")
        col.prop(self, "export_force_rotation")
        col.prop(self, "edge_split_angle")