import hou
import re
import util

reload(util)

#--------------------------------------------------------------------
#It returns the name except for "OUT_" from node name "OUT_aaa_aaa"
def getRopNameFromOUT(oNode):
    # sName = oSelNode.name()
    p = re.match('(OUT_)([A-Za-z][A-Za-z0-9]*)(_[A-Za-z][A-Za-z0-9]*)?\Z', oNode.name())

    if(p.group(3)):
        return p.group(2)+p.group(3)
    
    else:
        return p.group(2)

#--------------------------------------------------------------------
# Create a geometry(ROP) from the selected Null
def createAlembicFromNull(oNull, isTimeDependent):
    sNullName = getRopNameFromOUT(oNull)
    oNull.setColor(hou.Color([1,0,0]))
    
    #create geometry(ROP)
    oGeoROP = hou.node('/out').createNode('alembic')
    oGeoROP.setName(sNullName)
    oGeoROP.parm("use_sop_path").set(1)
    oGeoROP.parm("sop_path").set(oNull.path())
    oGeoROP.parm("filename").set(util.cachePath + '$OS.abc')

    #Set File Path
    if isTimeDependent==0:
        oGeoROP.parm("trange").set("off")
    else :
        oGeoROP.parm("trange").set("normal") 

    
    #other
    #oGeoROP.setColor(hou.Color([1, 0.8 ,0]))
    oGeoROP.moveToGoodPosition()   
    
    return oGeoROP
