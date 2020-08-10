"""
Ceci est un exercice pour presenter l'utilisation de \
    l'alebre lineaire dans un plug-ins python \
        vous pouvez a partir de ce plug-in creer une chaine de 3 joints \
            ces joints seront positionner en fonction de la position de \
                3 locators en input du node
"""

import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math


class DvAlgebraPlug(OpenMayaMPx.MPxNode):

    # Define node properties.
    kname = "dvAlgebraPlug"
    kplugin_id = OpenMaya.MTypeId(0x90000005)

    # Define node attributes.
    shoulder_pos = OpenMaya.MObject()
    elbow_pos = OpenMaya.MObject()
    wrist_pos = OpenMaya.MObject()
    parentInverseMatrix = OpenMaya.MObject()

    # OUTPUTS
    output_shoulder = OpenMaya.MObject()

    output_shoulder_translate = OpenMaya.MObject()
    output_shoulder_translateX = OpenMaya.MObject()
    output_shoulder_translateY = OpenMaya.MObject()
    output_shoulder_translateZ = OpenMaya.MObject()

    output_shoulder_rotate = OpenMaya.MObject()
    output_shoulder_rotateX = OpenMaya.MObject()
    output_shoulder_rotateY = OpenMaya.MObject()
    output_shoulder_rotateZ = OpenMaya.MObject()

    output_shoulder_scale = OpenMaya.MObject()
    output_shoulder_scaleX = OpenMaya.MObject()
    output_shoulder_scaleY = OpenMaya.MObject()
    output_shoulder_scaleZ = OpenMaya.MObject()

    output_elbow = OpenMaya.MObject()

    output_elbow_translate = OpenMaya.MObject()
    output_elbow_translateX = OpenMaya.MObject()
    output_elbow_translateY = OpenMaya.MObject()
    output_elbow_translateZ = OpenMaya.MObject()

    output_elbow_rotate = OpenMaya.MObject()
    output_elbow_rotateX = OpenMaya.MObject()
    output_elbow_rotateY = OpenMaya.MObject()
    output_elbow_rotateZ = OpenMaya.MObject()

    output_elbow_scale = OpenMaya.MObject()
    output_elbow_scaleX = OpenMaya.MObject()
    output_elbow_scaleY = OpenMaya.MObject()
    output_elbow_scaleZ = OpenMaya.MObject()

    output_wrist = OpenMaya.MObject()

    output_wrist_translate = OpenMaya.MObject()
    output_wrist_translateX = OpenMaya.MObject()
    output_wrist_translateY = OpenMaya.MObject()
    output_wrist_translateZ = OpenMaya.MObject()

    output_wrist_rotate = OpenMaya.MObject()
    output_wrist_rotateX = OpenMaya.MObject()
    output_wrist_rotateY = OpenMaya.MObject()
    output_wrist_rotateZ = OpenMaya.MObject()

    output_wrist_scale = OpenMaya.MObject()
    output_wrist_scaleX = OpenMaya.MObject()
    output_wrist_scaleY = OpenMaya.MObject()
    output_wrist_scaleZ = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compose_matrix(self, x_list, y_list, z_list, pos_list):

        current_matrixList = [
            x_list.x, x_list.y, x_list.z, 0.0,
            y_list.x, y_list.y, y_list.z, 0.0,
            z_list.x, z_list.y, z_list.z, 0.0,
            pos_list.x, pos_list.y, pos_list.z, 1.0
        ]

        # Declaration script util
        util = OpenMaya.MScriptUtil()

        # Convertir notre liste _shoulder_matrixList en MMatrix
        current_mMatrix = OpenMaya.MMatrix()
        util.createMatrixFromList(current_matrixList, current_mMatrix)

        return current_mMatrix

    def decompose_matrix(self, mMatrix):
        # Convertir MMatrix en MTransformMatrix
        mTrsfmMtx = OpenMaya.MTransformationMatrix(mMatrix)

        # Valeurs translation
        trans = mTrsfmMtx.translation(OpenMaya.MSpace.kWorld)

        # Valeur rotation Euler en radian
        quat = mTrsfmMtx.rotation()
        angles = quat.asEulerRotation()

        # Extraire scale.
        scale = [1.0, 1.0, 1.0]

        return [trans.x, trans.y, trans.z], [angles.x, angles.y, angles.z], scale

    def compute(self, plug, data):

        # Read plugs.
        shoulder_point = data.inputValue(
                DvAlgebraPlug.shoulder_pos
            ).asDouble3()

        elbow_point = data.inputValue(
                DvAlgebraPlug.elbow_pos
            ).asDouble3()

        wrist_point = data.inputValue(
                DvAlgebraPlug.wrist_pos
            ).asDouble3()

        parentInverseMatrix_mMatrix = data.inputValue(
                DvAlgebraPlug.parentInverseMatrix
            ).asMatrix()

        # convertion des listes de point en objet de type MVector
        shoulder_JNT_mVector = OpenMaya.MVector(
                shoulder_point[0],
                shoulder_point[1],
                shoulder_point[2]
            )
        elbow_JNT_mVector = OpenMaya.MVector(
                elbow_point[0],
                elbow_point[1],
                elbow_point[2]
            )
        wrist_JNT_mVector = OpenMaya.MVector(
                wrist_point[0],
                wrist_point[1],
                wrist_point[2]
            )

        # calcul du vecteur qui part du coude vers l'epaule.
        upperArm_vect = shoulder_JNT_mVector - elbow_JNT_mVector
        upperArm_vect = upperArm_vect.normal()

        # calcul du vecteur qui part du coude vers le poignee
        lowerArm_vect = wrist_JNT_mVector - elbow_JNT_mVector
        lowerArm_vect = lowerArm_vect.normal()

        shoulder_vect = elbow_JNT_mVector - shoulder_JNT_mVector
        shoulder_vect = shoulder_vect.normal()

        # calcul du vecteur normal, _aimUp_vect
        aimUp_vect = lowerArm_vect ^ upperArm_vect

        # utilisation du vecteur calcule _aimUp_vec pour calcuer zUpVec
        zUpVec = shoulder_vect ^ aimUp_vect
        zUpVec = zUpVec.normal()

        # yUpVec = zUpVec ^ shoulder_vect
        # Application au niveau lowerArm
        # le _aimUp_vect est commun a toutes les position
        # Calcul zLowerVec
        zLowerVec = aimUp_vect ^ lowerArm_vect
        zLowerVec = zLowerVec.normal()

        # creation de la list matrice upperArm
        shoulder_mMatrix = self.compose_matrix(
                shoulder_vect,
                aimUp_vect,
                zUpVec,
                shoulder_JNT_mVector
            )

        # creation de la list matrice lowerArm
        elbow_mMatrix = self.compose_matrix(
                lowerArm_vect,
                aimUp_vect,
                zLowerVec,
                elbow_JNT_mVector
            )

        # creation de la list matrice wristArm
        wrist_mMatrix = self.compose_matrix(
                lowerArm_vect,
                aimUp_vect,
                zLowerVec,
                wrist_JNT_mVector
            )

        # Projection de _shoulder_mMatrix dans parentInverseMatrix_mMatrix
        final_shoulder_mMatrix = shoulder_mMatrix * parentInverseMatrix_mMatrix

        # Projection de _elbow_mMatrix dans final_shoulder_mMatrix
        final_elbow_mMatrix = elbow_mMatrix * shoulder_mMatrix.inverse()

        # Projection de _wrist_mMatrix dans final_elbow_mMatrix
        final_wrist_mMatrix = wrist_mMatrix * elbow_mMatrix.inverse()

        shoulder_transform = self.decompose_matrix(final_shoulder_mMatrix)
        elbow_transform = self.decompose_matrix(final_elbow_mMatrix)
        wrist_transform = self.decompose_matrix(final_wrist_mMatrix)

        # OUTPUTS
        output_shoulder_handle = data.outputValue(self.output_shoulder)
        output_elbow_handle = data.outputValue(self.output_elbow)
        output_wrist_handle = data.outputValue(self.output_wrist)

        # Set output shoulder
        out_shoulder_tr = output_shoulder_handle.child(
                DvAlgebraPlug.output_shoulder_translate
            )
        out_shoulder_tr.set3Double(
                shoulder_transform[0][0],
                shoulder_transform[0][1],
                shoulder_transform[0][2]
            )

        out_shoulder_rot = output_shoulder_handle.child(
                DvAlgebraPlug.output_shoulder_rotate
            )
        out_shoulder_rot.set3Double(
                shoulder_transform[1][0],
                shoulder_transform[1][1],
                shoulder_transform[1][2]
            )

        out_shoulder_scl = output_shoulder_handle.child(
                DvAlgebraPlug.output_shoulder_scale
            )
        out_shoulder_scl.set3Double(
                shoulder_transform[2][0],
                shoulder_transform[2][1],
                shoulder_transform[2][2]
            )

        output_shoulder_handle.setClean()

        # Set output elbow
        out_elbow_tr = output_elbow_handle.child(
                DvAlgebraPlug.output_elbow_translate
            )
        out_elbow_tr.set3Double(
                elbow_transform[0][0],
                elbow_transform[0][1],
                elbow_transform[0][2]
            )

        out_elbow_rot = output_elbow_handle.child(
                DvAlgebraPlug.output_elbow_rotate
            )
        out_elbow_rot.set3Double(
                elbow_transform[1][0],
                elbow_transform[1][1],
                elbow_transform[1][2]
            )

        out_elbow_scl = output_elbow_handle.child(
                DvAlgebraPlug.output_elbow_scale
            )
        out_elbow_scl.set3Double(
                elbow_transform[2][0],
                elbow_transform[2][1],
                elbow_transform[2][2]
            )

        output_elbow_handle.setClean()

        # Set output wrist
        out_wrist_tr = output_wrist_handle.child(
                DvAlgebraPlug.output_wrist_translate
            )
        out_wrist_tr.set3Double(
                wrist_transform[0][0],
                wrist_transform[0][1],
                wrist_transform[0][2]
            )

        out_wrist_rot = output_wrist_handle.child(
                DvAlgebraPlug.output_wrist_rotate
            )
        out_wrist_rot.set3Double(
                wrist_transform[1][0],
                wrist_transform[1][1],
                wrist_transform[1][2]
            )

        out_wrist_scl = output_wrist_handle.child(
                DvAlgebraPlug.output_wrist_scale
            )
        out_wrist_scl.set3Double(
                wrist_transform[2][0],
                wrist_transform[2][1],
                wrist_transform[2][2]
            )

        output_wrist_handle.setClean()

        data.setClean(plug)

        return True


def creator():
    return OpenMayaMPx.asMPxPtr(DvAlgebraPlug())


def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()

    # INPUTS
    DvAlgebraPlug.shoulder_pos = nAttr.create(
            "shoulder_pos",
            "shoulder_pos",
            OpenMaya.MFnNumericData.k3Double
        )
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.shoulder_pos)

    DvAlgebraPlug.elbow_pos = nAttr.create(
            "elbow_pos",
            "elbow_pos",
            OpenMaya.MFnNumericData.k3Double
        )
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.elbow_pos)

    DvAlgebraPlug.wrist_pos = nAttr.create(
            "wrist_pos",
            "wrist_pos",
            OpenMaya.MFnNumericData.k3Double
        )
    nAttr.setWritable(True)
    nAttr.setStorable(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.wrist_pos)

    DvAlgebraPlug.parentInverseMatrix = mAttr.create(
            "parentInverseMatrix",
            "pim"
        )
    mAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.parentInverseMatrix)

    # OUTPUTS
    # SHOULDER
    # Translate
    DvAlgebraPlug.output_shoulder_translateX = nAttr.create(
        "output_shoulder_translateX",
        "ostx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_translateY = nAttr.create(
        "output_shoulder_translateY",
        "osty",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_translateZ = nAttr.create(
        "output_shoulder_translateZ",
        "ostz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_translate = nAttr.create(
        "output_shoulder_translate",   "ost",
        DvAlgebraPlug.output_shoulder_translateX,
        DvAlgebraPlug.output_shoulder_translateY,
        DvAlgebraPlug.output_shoulder_translateZ
    )
    nAttr.setStorable(False)

    # Rotate
    DvAlgebraPlug.output_shoulder_rotateX = uAttr.create(
        "output_shoulder_rotateX",
        "osrx",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_shoulder_rotateY = uAttr.create(
        "output_shoulder_rotateY",
        "osry",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_shoulder_rotateZ = uAttr.create(
        "output_shoulder_rotateZ",
        "osrz",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_shoulder_rotate = nAttr.create(
        "output_shoulder_rotate",   "osr",
        DvAlgebraPlug.output_shoulder_rotateX,
        DvAlgebraPlug.output_shoulder_rotateY,
        DvAlgebraPlug.output_shoulder_rotateZ
    )
    nAttr.setStorable(False)

    # Scale
    DvAlgebraPlug.output_shoulder_scaleX = nAttr.create(
        "output_shoulder_scaleX",
        "ossx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_scaleY = nAttr.create(
        "output_shoulder_scaleY",
        "ossy",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_scaleZ = nAttr.create(
        "output_shoulder_scaleZ",
        "ossz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_shoulder_scale = nAttr.create(
        "output_shoulder_scale",   "oss",
        DvAlgebraPlug.output_shoulder_scaleX,
        DvAlgebraPlug.output_shoulder_scaleY,
        DvAlgebraPlug.output_shoulder_scaleZ
    )
    nAttr.setStorable(False)

    DvAlgebraPlug.output_shoulder = cAttr.create("shoulder_xform", "sxf")
    cAttr.addChild(DvAlgebraPlug.output_shoulder_translate)
    cAttr.addChild(DvAlgebraPlug.output_shoulder_rotate)
    cAttr.addChild(DvAlgebraPlug.output_shoulder_scale)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_shoulder)

    # ELBOW
    # Translate
    DvAlgebraPlug.output_elbow_translateX = nAttr.create(
        "output_elbow_translateX",
        "oetx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_translateY = nAttr.create(
        "output_elbow_translateY",
        "oety",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_translateZ = nAttr.create(
        "output_elbow_translateZ",
        "oetz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_translate = nAttr.create(
        "output_elbow_translate",   "oet",
        DvAlgebraPlug.output_elbow_translateX,
        DvAlgebraPlug.output_elbow_translateY,
        DvAlgebraPlug.output_elbow_translateZ
    )
    nAttr.setStorable(False)

    # Rotate
    DvAlgebraPlug.output_elbow_rotateX = uAttr.create(
        "output_elbow_rotateX",
        "oerx",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_elbow_rotateY = uAttr.create(
        "output_elbow_rotateY",
        "oery",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_elbow_rotateZ = uAttr.create(
        "output_elbow_rotateZ",
        "oerz",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_elbow_rotate = nAttr.create(
        "output_elbow_rotate",   "oer",
        DvAlgebraPlug.output_elbow_rotateX,
        DvAlgebraPlug.output_elbow_rotateY,
        DvAlgebraPlug.output_elbow_rotateZ
    )
    nAttr.setStorable(False)

    # Scale
    DvAlgebraPlug.output_elbow_scaleX = nAttr.create(
        "output_elbow_scaleX",
        "oesx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_scaleY = nAttr.create(
        "output_elbow_scaleY",
        "oesy",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_scaleZ = nAttr.create(
        "output_elbow_scaleZ",
        "oesz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_elbow_scale = nAttr.create(
        "output_elbow_scale",   "oes",
        DvAlgebraPlug.output_elbow_scaleX,
        DvAlgebraPlug.output_elbow_scaleY,
        DvAlgebraPlug.output_elbow_scaleZ
    )
    nAttr.setStorable(False)

    DvAlgebraPlug.output_elbow = cAttr.create("elbow_xform", "exf")
    cAttr.addChild(DvAlgebraPlug.output_elbow_translate)
    cAttr.addChild(DvAlgebraPlug.output_elbow_rotate)
    cAttr.addChild(DvAlgebraPlug.output_elbow_scale)
    cAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_elbow)

    # WRIST
    # Translate
    DvAlgebraPlug.output_wrist_translateX = nAttr.create(
        "output_wrist_translateX",
        "owtx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_translateY = nAttr.create(
        "output_wrist_translateY",
        "owty",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_translateZ = nAttr.create(
        "output_wrist_translateZ",
        "owtz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_translate = nAttr.create(
        "output_wrist_translate",   "owt",
        DvAlgebraPlug.output_wrist_translateX,
        DvAlgebraPlug.output_wrist_translateY,
        DvAlgebraPlug.output_wrist_translateZ
    )
    nAttr.setStorable(False)

    # Rotate
    DvAlgebraPlug.output_wrist_rotateX = uAttr.create(
        "output_wrist_rotateX",
        "owrx",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_wrist_rotateY = uAttr.create(
        "output_wrist_rotateY",
        "owry",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_wrist_rotateZ = uAttr.create(
        "output_wrist_rotateZ",
        "owrz",
        OpenMaya.MFnUnitAttribute.kAngle,
        0.0
    )
    DvAlgebraPlug.output_wrist_rotate = nAttr.create(
        "output_wrist_rotate",   "owr",
        DvAlgebraPlug.output_wrist_rotateX,
        DvAlgebraPlug.output_wrist_rotateY,
        DvAlgebraPlug.output_wrist_rotateZ
    )
    nAttr.setStorable(False)

    # Scale
    DvAlgebraPlug.output_wrist_scaleX = nAttr.create(
        "output_wrist_scaleX",
        "owsx",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_scaleY = nAttr.create(
        "output_wrist_scaleY",
        "owsy",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_scaleZ = nAttr.create(
        "output_wrist_scaleZ",
        "owsz",
        OpenMaya.MFnNumericData.kDouble,
        0.0
    )
    DvAlgebraPlug.output_wrist_scale = nAttr.create(
        "output_wrist_scale",   "ows",
        DvAlgebraPlug.output_wrist_scaleX,
        DvAlgebraPlug.output_wrist_scaleY,
        DvAlgebraPlug.output_wrist_scaleZ
    )
    nAttr.setStorable(False)

    DvAlgebraPlug.output_wrist = cAttr.create("wrist_xform", "wxf")
    cAttr.addChild(DvAlgebraPlug.output_wrist_translate)
    cAttr.addChild(DvAlgebraPlug.output_wrist_rotate)
    cAttr.addChild(DvAlgebraPlug.output_wrist_scale)
    cAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_wrist)

    # Include both outputs.
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.shoulder_pos,
            DvAlgebraPlug.output_shoulder
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.elbow_pos,
            DvAlgebraPlug.output_shoulder
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.wrist_pos,
            DvAlgebraPlug.output_shoulder
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.parentInverseMatrix,
            DvAlgebraPlug.output_shoulder
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.shoulder_pos,
            DvAlgebraPlug.output_elbow
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.elbow_pos,
            DvAlgebraPlug.output_elbow
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.wrist_pos,
            DvAlgebraPlug.output_elbow
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.parentInverseMatrix,
            DvAlgebraPlug.output_elbow
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.shoulder_pos,
            DvAlgebraPlug.output_wrist
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.elbow_pos,
            DvAlgebraPlug.output_wrist
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.wrist_pos,
            DvAlgebraPlug.output_wrist
        )
    DvAlgebraPlug.attributeAffects(
            DvAlgebraPlug.parentInverseMatrix,
            DvAlgebraPlug.output_wrist
        )


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "damsOLabo", "1.0", "Any")
    try:
        plugin.registerNode(
                DvAlgebraPlug.kname,
                DvAlgebraPlug.kplugin_id,
                creator,
                initialize
            )
    except:
        raise RuntimeError, "Failed to register node: '{}'".format(DvAlgebraPlug.kname)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(DvAlgebraPlug.kplugin_id)
    except:
        raise RuntimeError, "Failed to register node: '{}'".format(DvAlgebraPlug.kname)
