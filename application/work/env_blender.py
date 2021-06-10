import os

def makeDirIfNotExist(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# model and render dirs for blender func

RENDER_DIR = os.path.join(BASE_DIR, 'static/render')
MODEL_DIR = os.path.join(BASE_DIR, 'static/models')

makeDirIfNotExist(RENDER_DIR)
makeDirIfNotExist(MODEL_DIR)

# blender envs

BPY_DEFAULT_RENDER_FILE = os.path.join(MODEL_DIR, 'uklady_dloni_ver_16_18.01.2014_2.blend')
BPY_RENDER_DIR = RENDER_DIR
BPY_DEVICE = 'CPU'