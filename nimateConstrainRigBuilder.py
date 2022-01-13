import maya.cmds as cmds

nimateRootLoc = cmds.ls('nimate_root')

locList = cmds.listRelatives(nimateRootLoc)

skeleton = cmds.group(em=1, n='nimate_RIG')

def buildSkeleton():
    cmds.parent(cmds.ls('Foot_R_JNT'), cmds.ls('Knee_R_JNT'))    
    cmds.parent(cmds.ls('Foot_L_JNT'), cmds.ls('Knee_L_JNT'))
    cmds.parent(cmds.ls('Knee_R_JNT'), cmds.ls('Hip_R_JNT'))
    cmds.parent(cmds.ls('Knee_L_JNT'), cmds.ls('Hip_L_JNT'))    
    cmds.parent(cmds.ls('Hip_*_JNT'), cmds.ls('Torso_JNT'))
    
    cmds.parent(cmds.ls('Elbow_R_JNT'), cmds.ls('Shoulder_R_JNT'))
    cmds.parent(cmds.ls('Elbow_L_JNT'), cmds.ls('Shoulder_L_JNT'))
    cmds.parent(cmds.ls('Hand_R_JNT'), cmds.ls('Elbow_R_JNT'))
    cmds.parent(cmds.ls('Hand_L_JNT'), cmds.ls('Elbow_L_JNT')) 
    
    cmds.parent(cmds.ls('Shoulder_*_JNT'), cmds.ls('Neck_JNT'))    
    cmds.parent(cmds.ls('Head_JNT'), cmds.ls('Neck_JNT'))
    cmds.parent(cmds.ls('Neck_JNT'), cmds.ls('Torso_JNT')) 

def constrainToLocators():
    for loc in locList:  
        if cmds.objectType(loc) == 'transform' and loc != nimateRootLoc:
            jnt = cmds.ls(str(loc) + '_JNT')
            if jnt != []:
                cmds.parentConstraint(loc, jnt, skipRotate=['x', 'y', 'z'])
          
def addPrefix(prefix='nimate'):
    for obj in cmds.listRelatives(skeleton, ad=1):
        cmds.rename(str(obj), prefix + '_' + str(obj)) 
            
for loc in locList:
    if(cmds.objectType(loc) == 'transform' and 'Left' not in str(loc) and 'Right' not in str(loc)):
        #pos = cmds.xform(loc, query=True, worldSpace=True, rotatePivot=True)
        jnt = cmds.joint(None, n=(str(loc) + '_JNT'))
        
        cmds.connectAttr(str(loc) + '.worldMatrix', jnt + '.offsetParentMatrix')
        cmds.parent(jnt, skeleton)

torsoPos = cmds.xform(cmds.ls('Torso_JNT'), query=True, worldSpace=True, rotatePivot=True)
#torsoJnt = cmds.ls('Torso_JNT')[0]
spineJnt = cmds.joint(p=torsoPos, n='Spine_JNT')
#cmds.parent(spineJnt, cmds.ls('Torso_JNT'))

buildSkeleton()
constrainToLocators()
addPrefix()