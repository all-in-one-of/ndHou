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
def createRopFromNull(oNull, isTimeDependent):
 
    sNullName = getRopNameFromOUT(oNull)
    print sNullName
    
    #create geometry(ROP)
    oGeoROP = hou.node('/out').createNode('geometry')
    oGeoROP.setName(sNullName)
    oGeoROP.parm("soppath").set(oNull.path())
    oGeoROP.parm("trange").set(1)
	
    fNodePath = oNull.parent().path() + "/" + sNullName
    #$print aa
    #parmNode = hou.node(fNodePath)
    # oGeoROP.parm("ver").set('`chs("'+ fNodePath +'/ver")`')

    if isTimeDependent==0:
        oGeoROP.parm("trange").set("off")
        sFilePath = util.cachePath + "$OS.bgeo.sc"
        oGeoROP.parm("sopoutput").set(sFilePath)
    else :
        oGeoROP.parm("trange").set("normal") 
        sFilePath = util.cachePath + "$OS.$F4.bgeo.sc"    
        oGeoROP.parm("sopoutput").set(sFilePath)
    
    
    #Set Parm "Initialize Simulation OP = 1"
    oGeoROP.parm("initsim").set(1)  
    
    #other
    #oGeoROP.setColor(hou.Color([1, 0.8 ,0]))
    oGeoROP.moveToGoodPosition()   
    
    return oGeoROP

#--------------------------------------------------------------------
#Create a filecache(SOP) from the selected Null
def createFilecacheSOP(oNull, oRop, isTimeDependent):
    sNullName = getRopNameFromOUT(oNull)
    oFileSOP = oNull.parent().createNode('filecache')
    oFileSOP.setName(sNullName)

    """
    #Create Custom Parameter
    group  = oFileSOP.parmTemplateGroup() 
    folder = hou.FolderParmTemplate("folder", "settings") 
    folder.addParmTemplate(hou.StringParmTemplate("ver", "ver", 1)) 
    group.append(folder) 
    oFileSOP.setParmTemplateGroup(group)
    #Set Custom Parameter Value
    oFileSOP.parm("ver").set("$VER")  
    """

    #Set File Path
    if isTimeDependent==0:
        oFileSOP.parm("trange").set("off")
        sFilePath = util.cachePath + "$OS.bgeo.sc"
    else :
        oFileSOP.parm("trange").set("normal") 
        sFilePath = util.cachePath + "$OS.$F4.bgeo.sc"
        
    oFileSOP.parm("file").set(sFilePath)
    
    
    #set file path from rop
    #oRopPath = oRop.parm("sopoutput")
    #oFileSOP.parm("file").set(oRopPath)
    #oFileSOP.parm("file").set(oRopPath.path())    
    #oFileSOP.parm("file").expression() 

    #set load Flag
    oFileSOP.parm("loadfromdisk").set(1)

    #set Loadtype
    oFileSOP.parm("loadtype").set(4)
    oFileSOP.parm("viewportlod").set(0)

    
    oFileSOP.setInput(0, oNull)
    oFileSOP.moveToGoodPosition()

    return oFileSOP

def CreateFetchFromFileCache(oNode):
	oChildren = oNode.children()
	oRend = [x for x in oChildren if x.type().name()=="rop_geometry"]

	oFetch = hou.node("/out").createNode('fetch')
	oFetch.setName("fetch_" + oNode.name())
	oFetch.parm("source").set(oRend[0].path())	