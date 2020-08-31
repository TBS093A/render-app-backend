import importlib
import sys
import os

from celery import Celery
from celery.signals import worker_init
from work.settings import (
    BPY_DEFAULT_RENDER_FILE,
    BPY_RENDER_DIR,
    BPY_DEVICE,
)

@worker_init.connect
def init_blender(worker, **kwargs):
    import_bpy()

def import_bpy(file_path=BPY_DEFAULT_RENDER_FILE, new_instance=False):
    if 'bpy' not in sys.modules:
        bpy = importlib.import_module('bpy')
        bpy.ops.wm.open_mainfile(file_path)

        preferences = bpy.context.user_preferences.addons['cycles'].preferences
        preferences.compute_device_type = 'CUDA'
        
        bpy.context.scene.cycles.device = BPY_DEVICE
        
        return sys.modules['bpy']

app = Celery('rendering')

