import bpy
from bpy.types import Panel

class LazyMDLExporter_Panel(Panel):
    bl_idname = "VIEW3D_PT_lazy_mdl_exporter"
    bl_label = "Lazy MDL Exporter v2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'POGO'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.Hakuinputs
        
        # Check if we're in a valid mode
        valid_mode = (context.mode == "OBJECT" or
                     (context.active_object and context.active_object.mode == "EDIT"))
        
        if not valid_mode:
            layout.label(text="You are not in object or edit mode.")
            return
        
        # File naming section
        name_box = layout.box()
        name_box.label(text="File Naming:")
        name_box.prop(props, "export_use_object_name")
        
        if not props.export_use_object_name:
            name_box.prop(props, "export_name")
        
        name_box.prop(props, "export_prefix")
        
        # Export path section
        path_box = layout.box()
        path_box.label(text="Export Path:")
        path_box.prop(props, "export_path")
        
        # Export settings
        layout.prop(props, "export_scale")
        layout.prop(props, "export_selection_only")
        layout.prop(props, "export_all_skins")
        layout.prop(props, "export_center")
        
        # Individual export options (only show when relevant)
        if props.export_use_object_name and props.export_selection_only:
            layout.prop(props, "export_individually")
            
            if props.export_individually:
                indent = layout.column(align=True)
                indent.prop(props, "export_force_origin")
                
                if props.export_force_origin:
                    indent.prop(props, "export_force_rotation")
        
        # Export button
        export_row = layout.row()
        export_row.scale_y = 2
        export_row.operator("lazy_mdl_exporter.export_mdl", text="Export as MDL", icon="EXPORT")
        
        # Edge split section
        edge_box = layout.box()
        edge_box.prop(props, "edge_split_angle")
        edge_box.operator("lazy_mdl_exporter.edge_split", text="Edge Split Modifier", icon="MODIFIER")

def menu_func_export_mdl(self, context):
    """Add MDL export to File > Export menu"""
    self.layout.operator("lazy_mdl_exporter.export_mdl", text="Export as MDL", icon="EXPORT")