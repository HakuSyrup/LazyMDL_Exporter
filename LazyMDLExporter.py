bl_info = {
    "name": "Lazy MDL Exporter ",
    "author": "HakuShiro",
    "version": (0, 0, 10),
    "blender": (3, 3, 1),
    "location": "View3D > Toolshelf(T)",
    "description": "Lazy MDL Exporter",
    "warning": "",
    "support": 'OFFICIAL',
    "category": "3D View",
}

import os
import bpy

from bpy.props import (
        StringProperty,
        EnumProperty,
        BoolProperty,
        PointerProperty,
        FloatProperty,
        IntProperty,
        )
from bpy.types import Operator, AddonPreferences
from bpy_extras.io_utils import ExportHelper
from pathlib import Path
import numpy as np

class Haku_Addon_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    Haku_Export_Path: StringProperty(
        name="Export Path",
        subtype = 'FILE_PATH',
        description="Export Path",
        default=""
    )
    exportMDL_NAME_Haku: StringProperty(
          name = "Name",
          description = "FILE_NAME",
          default="Object"
          )
    exportScale_Haku: FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0, max=1000.0,
        default=1000.0,
    )
    
    use_setting_Haku: BoolProperty(
        name="Export Selection Only",
        description="Uncheck to export all objects",
        default=True,
    )

    export_skin2_Haku: BoolProperty(
        name="Export All Skins",
        description="Export additional skins",
        default=False,
    )
    export_center_Haku: BoolProperty(
        name="Center model (aligned to 32 units)",
        description="See above",
        default=True,
    )
    export_UseObjectName_Haku: BoolProperty(
        name="Use object name",
        description="Use object name",
        default=True,
    )
    export_individually_Haku: BoolProperty(
        name="Export individually",
        description="Export individually by its name.",
        default=True,
    )
    
    export_ForceOrigin: BoolProperty(
        name="Force origin as object location",
        description="",
        default=True,
    )
        
    export_ForceRotation: BoolProperty(
        name="Reset object rotation",
        description="",
        default=False,
    )
    
    
    export_ES_Angle: FloatProperty(
        name="Edge Split Angle",
        description="Edge Split Angle",
        min=0.0, max=180.0,
        default=30.0,
    )
    def draw(self, context):
        self.layout.label(text="Default Settings:")
        self.layout.prop(self, "export_UseObjectName_Haku")
        self.layout.prop(self, "exportMDL_NAME_Haku")
        self.layout.prop(self, "Haku_Export_Path")
        self.layout.prop(self, "exportScale_Haku")
        self.layout.prop(self, "use_setting_Haku")
        self.layout.prop(self, "export_skin2_Haku")
        self.layout.prop(self, "export_center_Haku")
        self.layout.prop(self, "export_individually_Haku")
        self.layout.prop(self, "export_ForceOrigin")
        self.layout.prop(self, "export_ForceRotation")
        self.layout.prop(self, "export_ES_Angle")
        
        

def execute_Export(self,context):
        if context.scene.Hakuinputs.exportMDL_NAME_Haku == "":
            self.report({'ERROR'},"Enter MDL file name.")
            return{'FINISHED'}
        elif context.scene.Hakuinputs.exportMDL_path_Haku == "":
            self.report({'ERROR'},"Enter Export Path.")
            return{'FINISHED'}
        elif not(os.path.exists(str(context.scene.Hakuinputs.exportMDL_path_Haku))):
            self.report({'ERROR'}, 'This Export Path does not exist.')
            return{'FINISHED'}
        elif not(os.path.isabs(str(context.scene.Hakuinputs.exportMDL_path_Haku))):
            self.report({'ERROR'}, 'Export Path must be absolute path.')
            return{'FINISHED'}
        
        if str(context.scene.Hakuinputs.exportMDL_path_Haku).endswith("\\"):     
            Haku_MDL_Path=str(context.scene.Hakuinputs.exportMDL_path_Haku)
        else:
            Haku_MDL_Path=str(context.scene.Hakuinputs.exportMDL_path_Haku+"\\")
            
        if bool(context.scene.Hakuinputs.export_UseObjectName_Haku):
            Haku_MDL_Name= bpy.context.object.name
        else:
            Haku_MDL_Name=context.scene.Hakuinputs.exportMDL_NAME_Haku
        
        if len(Haku_MDL_Name)>29:
            self.report({'ERROR'}, 'Object name must less than 29 characters.')
            return{'FINISHED'}
        if '\\' in Haku_MDL_Name or '/' in Haku_MDL_Name:
            self.report({'ERROR'}, 'Do not use "Backslash" or "Slash"to object name')
            return{'FINISHED'}
        
        bpy.ops.export_mdl.some_data(exportScale=float(context.scene.Hakuinputs.exportScale_Haku),
        use_setting=bool(context.scene.Hakuinputs.use_setting_Haku),
        export_skin2=bool(context.scene.Hakuinputs.export_skin2_Haku),
        export_center=bool(context.scene.Hakuinputs.export_center_Haku),
        filepath=str(Haku_MDL_Path + Haku_MDL_Name+".mdl" ),
        )
        global export_sum
        export_sum += 1
        return{'FINISHED'}
    
class HakuEdgeSplitExecuteButton(bpy.types.Operator):
    bl_idname = "edgesplit.hakuaddon"
    bl_label = "Edge Split."
    def execute(self, context):
        bpy.ops.object.shade_smooth()
        ob_active=bpy.context.view_layer.objects.active
        obs = [o for o in bpy.context.view_layer.objects.selected if o.type=='MESH']
        bpy.ops.object.select_all(action='DESELECT')
        for ob in obs:
            bpy.context.view_layer.objects.active = ob
            ob.select_set(True)
            bpy.ops.object.modifier_remove(modifier="Haku ES MDL")
            bpy.context.object.data.use_auto_smooth = True
            bpy.ops.object.modifier_add(type='EDGE_SPLIT')
            bpy.context.object.modifiers["EdgeSplit"].name = "Haku ES MDL"
            bpy.context.object.modifiers["Haku ES MDL"].split_angle = context.scene.Hakuinputs.export_ES_Angle*np.pi/180
            bpy.context.object.data.auto_smooth_angle=context.scene.Hakuinputs.export_ES_Angle*np.pi/180
            bpy.context.object.modifiers["Haku ES MDL"].use_edge_sharp = True
            ob.select_set(False)
        for ob in obs:    
            ob.select_set(True)
        bpy.context.view_layer.objects.active=ob_active
        return{'FINISHED'}


class HakuMDLExecuteButton(bpy.types.Operator):
    bl_idname = "exportmdl.hakuaddon"
    bl_label = "Export as MDL"
  
    def execute(self, context):
        global export_sum
        export_sum=0
        if context.active_object != None:
            if bpy.context.active_object.mode== "EDIT":
                bpy.ops.object.mode_set(mode = 'OBJECT')
                IsEditmode=True
            else:
                IsEditmode=False
                
            if bpy.context.mode== "OBJECT":
                if context.scene.Hakuinputs.export_UseObjectName_Haku and context.scene.Hakuinputs.export_individually_Haku and context.scene.Hakuinputs.use_setting_Haku: 
                ##export individually
                
                    if context.scene.Hakuinputs.export_ForceOrigin:
                        
                        Object_Position=[
                        bpy.context.active_object.location.x,
                        bpy.context.active_object.location.y,
                        bpy.context.active_object.location.z
                        ]
                        bpy.context.active_object.location.xyz=(0,0,0)
                        context.scene.Hakuinputs.export_center_Haku=False
                        if context.scene.Hakuinputs.export_ForceRotation:
                            Object_Rotation=[
                            bpy.context.active_object.rotation_euler.x,
                            bpy.context.active_object.rotation_euler.y,
                            bpy.context.active_object.rotation_euler.z
                            ]
                            bpy.context.active_object.rotation_euler.x=0
                            bpy.context.active_object.rotation_euler.y=0
                            bpy.context.active_object.rotation_euler.z=0
                        
                
                
                    ob_active=bpy.context.view_layer.objects.active
                    obs = [o for o in bpy.context.view_layer.objects.selected]
                    bpy.ops.object.select_all(action='DESELECT')  
                    for ob in obs:
                        bpy.context.view_layer.objects.active = ob
                        ob.select_set(True)
                        execute_Export(self,context)    
                        ob.select_set(False)
                    for ob in obs:    
                        ob.select_set(True)
                    bpy.context.view_layer.objects.active=ob_active
                else:    
                    execute_Export(self,context)
                    
                if IsEditmode:
                    bpy.ops.object.mode_set(mode = 'EDIT')
                if context.scene.Hakuinputs.export_ForceOrigin:
                    bpy.context.active_object.location.xyz=Object_Position
                    if context.scene.Hakuinputs.export_ForceRotation:
                        bpy.context.active_object.rotation_euler.x=Object_Rotation[0]
                        bpy.context.active_object.rotation_euler.y=Object_Rotation[1]
                        bpy.context.active_object.rotation_euler.z=Object_Rotation[2]
                if export_sum>0:
                    self.report({'INFO'},str(export_sum)+" object(s) has been exported as MDL.")
            else:
                self.report({'INFO'},"You are not in object or edit mode.") 
            
        return{'FINISHED'}

bpy.utils.register_class(Haku_Addon_Preferences)
class HakuProps(bpy.types.PropertyGroup,ExportHelper): 
    
    
    try:
        prefs = bpy.context.preferences.addons[__name__].preferences 
        exportMDL_path_Haku: StringProperty(
          name = "",
          description = "Path for Export MDL",
          subtype = 'FILE_PATH',
          default=str(prefs.Haku_Export_Path)
          )
        exportMDL_NAME_Haku: StringProperty(
          name = "",
          description = "FILE_NAME",
          default=str(prefs.exportMDL_NAME_Haku)
          )
        exportScale_Haku: FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=1000.0,
            default=prefs.exportScale_Haku
        )
        use_setting_Haku: BoolProperty(
            name="Export Selection Only",
            description="Uncheck to export all objects",
            default=bool(prefs.use_setting_Haku),
        )

        export_skin2_Haku: BoolProperty(
            name="Export All Skins",
            description="Export additional skins",
            default=bool(prefs.export_skin2_Haku),
        )
        export_center_Haku: BoolProperty(
            name="Center model (aligned to 32 units)",
            description="See above",
            default=bool(prefs.export_center_Haku),
        )
        export_UseObjectName_Haku: BoolProperty(
            name="Use Object Name",
            description="Use Object Name",
            default=bool(prefs.export_UseObjectName_Haku),
        )
        export_individually_Haku: BoolProperty(
            name="Export individually",
            description="Export individually by its name.",
            default=bool(prefs.export_individually_Haku),
        )
        
        export_ForceOrigin: BoolProperty(
            name="Force origin as object location",
            description="",
            default=bool(prefs.export_ForceOrigin),
        )
        
        export_ForceRotation: BoolProperty(
            name="Reset object rotation",
            description="",
            default=bool(prefs.export_ForceRotation),
        )
        
        
        
        export_ES_Angle: FloatProperty(
        name="Edge Split Angle",
        description="Edge Split Angle",
        min=0.0, max=180.0,
        default=prefs.export_ES_Angle,
        )
        
       
    except:
        exportMDL_path_Haku: StringProperty(
          name = "",
          description = "Path for Export MDL",
          subtype = 'FILE_PATH',
          default=""
        )
          
        exportMDL_NAME_Haku: StringProperty(
          name = "",
          description = "FILE_NAME",
          default="Object"
          )
        exportScale_Haku: FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=1000.0,
            default=1000.0,
        )
        use_setting_Haku: BoolProperty(
            name="Export Selection Only",
            description="Uncheck to export all objects",
            default=True,
        )

        export_skin2_Haku: BoolProperty(
            name="Export All Skins",
            description="Export additional skins",
            default=False,
        )
        export_center_Haku: BoolProperty(
            name="Center model (aligned to 32 units)",
            description="See above",
            default=True,
        )
        export_UseObjectName_Haku: BoolProperty(
            name="Use object name",
            description="Use object name",
            default=True,
        )
        export_individually_Haku: BoolProperty(
            name="Export individually",
            description="Export individually by its name.",
            default=True,
        )
        export_ForceOrigin: BoolProperty(
            name="Force origin as object location",
            description="",
            default=True,
        )
        
        export_ForceRotation: BoolProperty(
            name="Reset object rotation",
            description="",
            default=False,
        )
        
        export_ES_Angle: FloatProperty(
        name="Edge Split Angle",
        description="Edge Split Angle",
        min=0.0, max=180.0,
        default=30,
        )
        
    

class ExportMDLClassHelper(bpy.types.Panel):
    bl_idname = "Object_PT_MDL"
    bl_label = "ExportAsMDL by Haku"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category='POGO'
    name=bpy.props.StringProperty(name="Enter your name:")
    
        
    def draw(self, context):
        if bpy.context.mode== "OBJECT" or bpy.context.active_object.mode== "EDIT":
            layout=self.layout
            row=layout.row()
            box=layout.box()
            row.label(text="Name:")
            box.prop(context.scene.Hakuinputs, "export_UseObjectName_Haku")
            if not(bool(context.scene.Hakuinputs.export_UseObjectName_Haku)):
                box.prop(context.scene.Hakuinputs, "exportMDL_NAME_Haku")
            else:
                box.label()
            layout.label(text="Export Path:")
            box1=layout.box()
            box1.prop(context.scene.Hakuinputs, "exportMDL_path_Haku")
            layout.prop(context.scene.Hakuinputs, "exportScale_Haku")
            layout.prop(context.scene.Hakuinputs, "use_setting_Haku")
            layout.prop(context.scene.Hakuinputs, "export_skin2_Haku")
            layout.prop(context.scene.Hakuinputs, "export_center_Haku")
            
            layout=self.layout
            if bool(context.scene.Hakuinputs.export_UseObjectName_Haku)and bool(context.scene.Hakuinputs.use_setting_Haku):
                layout.prop(context.scene.Hakuinputs, "export_individually_Haku")
                if context.scene.Hakuinputs.export_individually_Haku:
                    layout.prop(context.scene.Hakuinputs, "export_ForceOrigin")
                    if context.scene.Hakuinputs.export_ForceOrigin:
                        layout.prop(context.scene.Hakuinputs, "export_ForceRotation")
                    else:
                        layout.label()
                else:
                    layout.label()
                    layout.label()
            else:
                layout.label()
                layout.label()
                layout.label()
            row1=layout.row()
            row1.scale_y=2
            row1.operator("exportmdl.hakuaddon",text="Export as MDL",icon="EXPORT")
            
            box2=layout.box()
            box2.prop(context.scene.Hakuinputs, "export_ES_Angle")
            box2.operator("edgesplit.hakuaddon",text="Edge Split modifier ",icon="MODIFIER")
        else:
            layout=self.layout
            layout.label(text="You are not in object or edit mode.")
def menu_func_exportMDL(self, context):
    self.layout.operator(ExportMDLClass.bl_idname, text="Export as MDL",icon = "EXPORT")

classes = [
  HakuProps,
  HakuMDLExecuteButton,
  ExportMDLClassHelper,
  HakuEdgeSplitExecuteButton
]

addon_keymaps = []

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.Hakuinputs = bpy.props.PointerProperty(type=HakuProps)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(HakuMDLExecuteButton.bl_idname, type="W", value='PRESS',shift=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.Hakuinputs
    
    # Remove the hotkey
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()