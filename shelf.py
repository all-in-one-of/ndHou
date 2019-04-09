
import hou

import os
import subprocess

def openHip ():
    hipPath = os.path.split(hou.hipFile.path())[0].replace('/', '\\')
    cmd = ['explorer.exe', hipPath]
    subprocess.call(cmd)