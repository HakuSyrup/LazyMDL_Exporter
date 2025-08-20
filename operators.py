import bpy
import math
from bpy.types import Operator
from . import utils


class LazyMDLExporter_EdgeSplit(Operator):
    bl_idname = "lazy_mdl_exporter.edge_split"
    bl_label = "Edge Split"
    
    def execute(self, context):
        """Apply edge split modifier to selected mesh objects"""
        angle_rad = math.radians(context.scene.Hakuinputs.edge_split_angle)
        
        # Get selected mesh objects
        original_active = context.view_layer.objects.active
        mesh_objects = [obj for obj in context.view_layer.objects.selected if obj.type == 'MESH']
        
        if not mesh_objects:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'FINISHED'}
        
        # Apply smooth shading first
        bpy.ops.object.shade_smooth()
        bpy.ops.object.select_all(action='DESELECT')
        
        try:
            for obj in mesh_objects:
                context.view_layer.objects.active = obj
                obj.select_set(True)
                
                # Remove existing modifier if present
                if "Haku ES MDL" in obj.modifiers:
                    obj.modifiers.remove(obj.modifiers["Haku ES MDL"])
                
                # Configure auto smooth
                obj.data.use_auto_smooth = True
                obj.data.auto_smooth_angle = angle_rad
                
                # Add edge split modifier
                modifier = obj.modifiers.new(name="Haku ES MDL", type='EDGE_SPLIT')
                modifier.split_angle = angle_rad
                modifier.use_edge_sharp = True
                
                obj.select_set(False)
                
        finally:
            # Restore selection
            for obj in mesh_objects:
                obj.select_set(True)
            context.view_layer.objects.active = original_active
            
        return {'FINISHED'}


class LazyMDLExporter_Export(Operator):
    bl_idname = "lazy_mdl_exporter.export_mdl"
    bl_label = "Export as MDL"
  
    def execute(self, context):
        
        if not context.active_object:
            self.report({'ERROR'}, "No active object selected.")
            return {'FINISHED'}
        
        props = context.scene.Hakuinputs
        active_obj = context.active_object
        
        # Handle edit mode
        was_edit_mode = active_obj.mode == "EDIT"
        if was_edit_mode:
            bpy.ops.object.mode_set(mode='OBJECT')
        
        if context.mode != "OBJECT":
            self.report({'INFO'}, "You are not in object or edit mode.")
            return {'FINISHED'}
        
        # Store original transform if needed
        original_location = None
        original_rotation = None
        
        if props.export_force_origin:
            original_location = active_obj.location.copy()
            active_obj.location = (0, 0, 0)
            
            if props.export_force_rotation:
                original_rotation = active_obj.rotation_euler.copy()
                active_obj.rotation_euler = (0, 0, 0)
        
        try:
            # Export logic
            should_export_individually = (
                props.export_use_object_name and
                props.export_individually and
                props.export_selection_only
            )
            
            if should_export_individually:
                self._export_individually(context)
            else:
                utils.execute_Export(self, context)
                
        finally:
            # Restore original transform
            if original_location is not None:
                active_obj.location = original_location
            if original_rotation is not None:
                active_obj.rotation_euler = original_rotation
            
            # Restore edit mode
            if was_edit_mode:
                bpy.ops.object.mode_set(mode='EDIT')
        
        # Report results
        self.report({'INFO'}, "Export completed.")
        
        return {'FINISHED'}
    
    def _export_individually(self, context):
        """Export each selected object individually"""
        self.report({'INFO'}, "Exporting individually")
        
        original_active = context.view_layer.objects.active
        selected_objects = [obj for obj in context.view_layer.objects.selected]
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        try:
            for obj in selected_objects:
                context.view_layer.objects.active = obj
                obj.select_set(True)
                utils.execute_Export(self, context)
                obj.select_set(False)
        finally:
            # Restore selection
            for obj in selected_objects:
                obj.select_set(True)
            context.view_layer.objects.active = original_active