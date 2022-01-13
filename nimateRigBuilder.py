import maya.cmds as cmds
import maya.mel as mel

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
    
def orientJoints():
    for jnt in cmds.listRelatives(skeleton, ad=1):
        mel.eval("cometJointOrient")
   
def connectMatrices():
    for jnt in cmds.listRelatives(skeleton, ad=1): #allDescedants    
        #print(jnt)    
        if(str(jnt) != 'Torso_JNT'):  # for all joints except root
            par = cmds.listRelatives(jnt, parent=True)
            parName = str(par[0])
            
            if(parName != 'nimate_RIG'): # and cmds.listRelatives(jnt, children=True)):
                multMatrix = cmds.createNode('multMatrix') # create multMatrix node
                cmds.connectAttr(parName + '.parentInverseMatrix[0]', multMatrix + '.matrixIn[1]') # connect parent joint's parent inverse matrix
                cmds.connectAttr(str(jnt).replace('_JNT', '') + '.worldMatrix[0]', multMatrix + '.matrixIn[0]') # connect current joint locator's world matrix
                if(cmds.isConnected(parName.replace('_JNT', '') + '.worldMatrix', jnt + '.offsetParentMatrix')): # if other connections are found in the offsetparentmatrix, disconnect them
                    cmds.disconnectAttr(parName.replace('_JNT', '') + '.worldMatrix', jnt + '.offsetParentMatrix')
                if(cmds.isConnected(str(jnt).replace('_JNT', '') + '.worldMatrix', jnt + '.offsetParentMatrix')):
                    cmds.disconnectAttr(str(jnt).replace('_JNT', '') + '.worldMatrix', jnt + '.offsetParentMatrix')
                cmds.connectAttr(multMatrix + '.matrixSum', str(jnt) + '.offsetParentMatrix') # connect multmatrix output to joint's offset parent matrix
                
                cmds.setAttr(jnt + '.translateX', 0) # zero all transforms on joint
                cmds.setAttr(jnt + '.translateY', 0)
                cmds.setAttr(jnt + '.translateZ', 0)
        else:
            cmds.connectAttr(str(jnt).replace('_JNT', '') + '.worldMatrix', jnt + '.offsetParentMatrix')
 
for loc in locList:
    if(cmds.objectType(loc) == 'transform' and 'Left' not in str(loc) and 'Right' not in str(loc)):
        #pos = cmds.xform(loc, query=True, worldSpace=True, rotatePivot=True)
        jnt = cmds.joint(None, n=(str(loc) + '_JNT'))
        
        cmds.connectAttr(str(loc) + '.worldMatrix', jnt + '.offsetParentMatrix')
        cmds.parent(jnt, skeleton)
        cmds.disconnectAttr(str(loc) + '.worldMatrix', jnt + '.offsetParentMatrix')

buildSkeleton()
#orientJoints()
connectMatrices()

