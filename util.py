
import hou
import sgtk
import re
import os
import glob
import yaml


cachePath = '$CACHE/$SHOT$CUT/$ELEM/$OS/$VER$TAKE/'

def startup ():
    hou.setPreference('misc.useexternalhelp.val', '1')
    hou.setPreference('misc.externalhelpurl.val', 'https://www.sidefx.com/ja/docs/houdini17.0/')

def setEnvValue ():
    engine = sgtk.platform.current_engine()
    print engine.context.entity_locations
    workPath = engine.context.entity_locations
    if len(workPath) == 0:
        return
    else:
        workPath = workPath[0]
    workPath = workPath.replace('\\', '/')
    print workPath
    match = re.match('P:/Project/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', workPath)
    if match is None:
        return
    proj     = match.group(1)
    roll     = match.group(3)
    sequence = match.group(4)
    cut      = match.group(5)
    hou.hscript('setenv -g PROJ = %s'% proj)
    hou.hscript('setenv -g SHOT = %s'% sequence)
    hou.hscript('setenv -g CUT = %s'% cut)

    user = os.environ['USERNAME']
    hou.hscript('setenv -g USER = %s'% user)
    cachePath = os.path.join('P:/CACHE', proj, user).replace('\\', '/')
    hou.hscript('setenv -g CACHE = %s'% cachePath)

    currentHip = hou.hipFile.basename()
    print currentHip
    if 'untitled' in currentHip:
        ver = 'v001'
        elem = 'efx'
    else:
        match = re.match('([a-zA-Z0-9]+)_([a-zA-Z0-9]+)_(v[0-9]+)', currentHip)
        print match
        if match is None:
            ver = 'v001'
            elem = 'efx'
        else:
            ver = match.group(3)
            elem = match.group(2)

    hou.hscript('setenv -g VER = %s'% ver)
    hou.hscript('setenv -g ELEM = %s'% elem)
    take = hou.getenv('TAKE', 't01')
    hou.hscript('setenv -g TAKE = %s'% take)

def incVer ():
    ver = hou.getenv('VER', 'v001')
    verNum = int(ver[1:])
    verNum += 1
    ver = 'v' + str(verNum).zfill(3)
    hou.hscript('setenv -g VER = %s'% ver)
    hou.hscript('setenv -g TAKE = %s'% 't01')

def incTake ():
    take = hou.getenv('TAKE', 't01')
    print take

    snapshotPath = os.path.join(os.path.split(hou.hipFile.path())[0], 'snapshots').replace('\\', '/')
    configFiles = glob.glob(snapshotPath+'/*.yml')
    writeSnapshotComment(configFiles[0], take)

    takeNum = int(take[1:])
    takeNum += 1
    take = 't' + str(takeNum).zfill(2)
    hou.hscript('setenv -g TAKE = %s'% take)

def writeSnapshotComment (configFile, comment):
    with open(configFile, 'r+') as f:
        data = yaml.load(f)
        key = data.keys()
        key.sort()
        data[key[-1]]['comment'] = comment
        f.write(yaml.dump(data))
