from maya import cmds

cmds.file(new=True, f=True)
cmds.loadPlugin("dvAlgebraPlug.py")
cmds.file(new=True, f=True)

root_grp = cmds.createNode("transform", n="root_GRP")
targets_grp = cmds.createNode("transform", n="targets_GRP")
deform_grp = cmds.createNode("transform", n="deform_GRP")

cmds.setAttr(targets_grp + ".inheritsTransform", 0)

cmds.parent(targets_grp, root_grp)
cmds.parent(deform_grp, root_grp)

algerbra_node = cmds.createNode("dvAlgebraPlug")

locators = {
        "shoulder_target": [0.0, 1.0, 0.0],
        "elbow_target": [1.0, 1.0, -1.0],
        "wrist_target" : [3.0, 1.0, -1.0]
    }

locator_nodes = []
for loc, pos in locators.items():
    current_loc = cmds.spaceLocator(n=loc)[0]
    cmds.xform(current_loc, ws=True, t=pos)
    locator_nodes.append(current_loc)

for locator_node in locator_nodes:
    base_name = locator_node.split("_")[0]
    cmds.connectAttr(locator_node + ".worldPosition[0]", algerbra_node + "." + base_name + "_pos")

cmds.parent(locator_nodes, targets_grp)

cmds.select(d=True)
jnts=["shoulder_JNT", "elbow_JNT", "wrist_JNT"]
jnt_nodes=[]
for jnt in jnts:
    base_name = jnt.split("_")[0]
    current_jnt = cmds.joint(n=jnt)
    for attr in ["translate", "jointOrient", "scale"]:
        
        if attr == "jointOrient":
            node_attr = "rotate"
        else:
            node_attr = attr
            
        for axis in ["X", "Y", "Z"]:
            cmds.connectAttr(algerbra_node + ".output_{}_{}{}".format(base_name, node_attr, axis), current_jnt + ".{}{}".format(attr, axis))

    jnt_nodes.append(current_jnt)
    
cmds.parent(jnt_nodes[0], deform_grp)

cmds.connectAttr(deform_grp + ".worldInverseMatrix[0]", algerbra_node + ".parentInverseMatrix", f=True)
