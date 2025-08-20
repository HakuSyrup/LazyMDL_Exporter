bl_info = {
    "name": "Lazy MDL Exporter v2",
    "author": "HakuShiro",
    "version": (2, 0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Toolshelf(T)",
    "description": "Lazy MDL Exporter",
    "warning": "Please uninstall any previous versions before installing",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}

import bpy

from . import preferences
from . import operators
from . import ui
from . import utils

# Global variable for export counting
export_sum = 0

classes = [
    preferences.LazyMDLExporter_Preferences,
    utils.LazyMDLExporter_Props,
    operators.LazyMDLExporter_Export,
    operators.LazyMDLExporter_EdgeSplit,
    ui.LazyMDLExporter_Panel,
]

addon_keymaps = []

def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register scene properties
    bpy.types.Scene.Hakuinputs = bpy.props.PointerProperty(type=utils.LazyMDLExporter_Props)
    
    # Register keymap
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            operators.LazyMDLExporter_Export.bl_idname,
            type="W",
            value='PRESS',
            shift=True
        )
        addon_keymaps.append((km, kmi))
    
    # Initialize properties with preferences if available
    try:
        if hasattr(bpy.context, 'scene') and bpy.context.scene:
            utils.sync_props_with_prefs(bpy.context.scene.Hakuinputs)
    except:
        pass  # Ignore errors during registration


def unregister():
    # Remove keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    # Unregister scene properties
    if hasattr(bpy.types.Scene, 'Hakuinputs'):
        del bpy.types.Scene.Hakuinputs
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()