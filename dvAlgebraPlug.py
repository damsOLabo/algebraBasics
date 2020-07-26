"""
Ceci est un exercice pour presenter l'utilisation de \
    l'alèbre linéaire dans un plug-ins python

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
        # Shoulder
    output_shouler = OpenMaya.MObject()

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

    def decompose_matrix(self, mMatrix):
        # Convertir MMatrix en MTransformMatrix
        mTrsfmMtx = OpenMaya.MTransformationMatrix(mMatrix)

        # Valeurs translation
        trans = mTrsfmMtx.translation(OpenMaya.MSpace.kWorld)

        # Valeur rotation Euler en radians
        eulerRot = mTrsfmMtx.rotation()

        # Convertion radian en degrees
        angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

        # Extraire scale.
        scale = mTrsfmMtx.scale(OpenMaya.MSpace.kWorld)

        return trans, angles, scale

    def compute(self, plug, data):
        # Include all outputs here.
        if plug != self.shoulder_ouptut and plug != self.elbow_ouptut and plug != self.wrist_ouptut:
            return OpenMaya.kUnknownParameter

        # Get plugs.
        shoulder_point = data.inputValue(DvAlgebraPlug.shoulder_pos).asDouble3()
        elbow_point = data.inputValue(DvAlgebraPlug.elbow_pos).asDouble3()
        wrist_point = data.inputValue(DvAlgebraPlug.wrist_pos).asDouble3()
        parentInverseMatrix_mMatrix = data.inputValue(DvAlgebraPlug.parentInverseMatrix).asMatrix()

        # convertion des listes de point en objet de type MVector
        shoulder_JNT_mVector = OpenMaya.MVector(shoulder_point)
        elbow_JNT_mVector = OpenMaya.MVector(elbow_point)
        wrist_JNT_mVector = OpenMaya.MVector(wrist_point)

        # calcul du vecteur qui part du coude vers l'épaule.
        upperArm_vect = shoulder_JNT_mVector - elbow_JNT_mVector
        # calcul du vecteur qui part du coude vers le poignée
        lowerArm_vect = wrist_JNT_mVector - elbow_JNT_mVector

        # normaliser les vecteurs
        upperArm_vect = upperArm_vect.normal()
        lowerArm_vect = lowerArm_vect.normal()

        # Application au niveau upperArm
        # inversion du sens du vecteur _upperArm_vect
        upperArm_vect = (-1) * upperArm_vect

        # calcul du vecteur normal, _aimUp_vect
        aimUp_vect = upperArm_vect ^ lowerArm_vect

        # utilisation du vecteur calculé _aimUp_vec pour calcuer zUpVec
        zUpVec = aimUp_vect ^ upperArm_vect

        # Application au niveau lowerArm
        # le _aimUp_vect est commun a toutes les position
        # Calcul zLowerVec
        zLowerVec = aimUp_vect ^ lowerArm_vect

        # création de la list matrice upperArm
        shoulder_matrixList = [
            upperArm_vect.x, upperArm_vect.y, upperArm_vect.z, 0.0,
            aimUp_vect.x, aimUp_vect.y, aimUp_vect.z, 0.0,
            zUpVec.x, zUpVec.y, zUpVec.z, 0.0,
            shoulder_JNT_mVector.x, shoulder_JNT_mVector.y, shoulder_JNT_mVector.z, 1.0
        ]

        # création de la list matrice lowerArm
        elbow_matrixList = [
            lowerArm_vect.x, lowerArm_vect.y, lowerArm_vect.z, 0.0,
            aimUp_vect.x, aimUp_vect.y, aimUp_vect.z, 0.0,
            zLowerVec.x, zLowerVec.y, zLowerVec.z, 0.0,
            elbow_JNT_mVector.x, elbow_JNT_mVector.y, elbow_JNT_mVector.z, 1.0
        ]

        # création de la list matrice wristArm
        wrist_matrixList = [
            lowerArm_vect.x, lowerArm_vect.y, lowerArm_vect.z, 0.0,
            aimUp_vect.x, aimUp_vect.y, aimUp_vect.z, 0.0,
            zLowerVec.x, zLowerVec.y, zLowerVec.z, 0.0,
            wrist_JNT_mVector.x, wrist_JNT_mVector.y, wrist_JNT_mVector.z, 1.0
        ]

        # Déclaration script util
        util = OpenMaya.MScriptUtil()

        # Convertir notre liste _shoulder_matrixList en MMatrix
        shoulder_mMatrix = OpenMaya.MMatrix()
        util.createMatrixFromList(shoulder_matrixList, shoulder_mMatrix)

        # Convertir notre liste _elbow_matrixList en MMatrix
        elbow_mMatrix = OpenMaya.MMatrix()
        util.createMatrixFromList(elbow_matrixList, elbow_mMatrix)

        # Convertir notre liste _wrist_matrixList en MMatrix
        wrist_mMatrix = OpenMaya.MMatrix()
        util.createMatrixFromList(wrist_matrixList, wrist_mMatrix)

        # Projection de _shoulder_mMatrix dans parentInverseMatrix_mMatrix
        final_shoulder_mMatrix = shoulder_mMatrix * parentInverseMatrix_mMatrix
        # Projection de _elbow_mMatrix dans final_shoulder_mMatrix
        final_elbow_mMatrix = elbow_mMatrix * final_shoulder_mMatrix.inverse()
        # Projection de _wrist_mMatrix dans final_elbow_mMatrix
        final_wrist_mMatrix = wrist_mMatrix * final_elbow_mMatrix.inverse()

        shoulder_transform = self.decompose_matrix(final_shoulder_mMatrix)
        elbow_transform = self.decompose_matrix(final_elbow_mMatrix)
        wrist_transform = self.decompose_matrix(final_wrist_mMatrix)

        # OUTPUTS
        output_shouler = data.outputValue(self.output_shouler)
        output_elbow = data.outputValue(self.output_elbow)
        output_wrist = data.outputValue(self.output_wrist)


        # Set output 1.
        if plug == self.shoulder_ouptut:
            out_shoulder_tr = output_shoulder.child(DvAlgebraPlug.output_shoulder_translate)
            out_shoulder_tr.set3Double(shoulder_transform[0][0], shoulder_transform[0][1], shoulder_transform[0][2])

            out_shoulder_rot = output_shouler.child(DvAlgebraPlug.output_shoulder_rotate)
            out_shoulder_rot.set3Double(shoulder_transform[1][0], shoulder_transform[1][1], shoulder_transform[1][2])

            out_shoulder_scl = output_shouler.child(DvAlgebraPlug.output_shoulder_rotate)
            out_shoulder_scl.set3Double(shoulder_transform[2][0], shoulder_transform[2][1], shoulder_transform[2][2])

            output_shouler.setClean()

        # Set output 2.
        if plug == self.elbow_ouptut:
            out_elbow_tr = output_elbow.child(DvAlgebraPlug.output_elbow_translate)
            out_elbow_tr.set3Double(elbow_transform[0][0], elbow_transform[0][1], elbow_transform[0][2])

            out_elbow_rot = output_shouler.child(DvAlgebraPlug.output_elbow_rotate)
            out_elbow_rot.set3Double(elbow_transform[1][0], elbow_transform[1][1], elbow_transform[1][2])

            out_elbow_scl = output_shouler.child(DvAlgebraPlug.output_elbow_rotate)
            out_elbow_scl.set3Double(elbow_transform[2][0], elbow_transform[2][1], elbow_transform[2][2])

            output_elbow.setClean()

        # Set output 2.
        if plug == self.wrist_ouptut:
            out_wrist_tr = output_wrist.child(DvAlgebraPlug.output_wrist_translate)
            out_wrist_tr.set3Double(wrist_transform[0][0], wrist_transform[0][1], wrist_transform[0][2])

            out_wrist_rot = output_shouler.child(DvAlgebraPlug.output_wrist_rotate)
            out_wrist_rot.set3Double(wrist_transform[1][0], wrist_transform[1][1], wrist_transform[1][2])

            out_wrist_scl = output_shouler.child(DvAlgebraPlug.output_wrist_rotate)
            out_wrist_scl.set3Double(wrist_transform[2][0], wrist_transform[2][1], wrist_transform[2][2])

            output_wrist.setClean()

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
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.shoulder_pos)

    DvAlgebraPlug.elbow_pos = nAttr.create(
            "elbow_pos",
            "elbow_pos",
            OpenMaya.MFnNumericData.k3Double
        )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.elbow_pos)

    DvAlgebraPlug.wrist_pos = nAttr.create(
            "wrist_pos",
            "wrist_pos",
            OpenMaya.MFnNumericData.k3Double
        )
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.wrist_pos)

    DvAlgebraPlug.parentInverseMatrix = mAttr.create(
            "parentInverseMatrix",
            "pim"
        )
    mAttr.setStorable(False)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.parentInverseMatrix)

    # OUTPUTS
    ## SHOULDER
    ### Translate
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

    ### Rotate
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
    DvAlgebraPlug.output_shoulder_rotate = uAttr.create(
        "output_shoulder_rotate",   "osr",
        DvAlgebraPlug.output_shoulder_rotateX,
        DvAlgebraPlug.output_shoulder_rotateY,
        DvAlgebraPlug.output_shoulder_rotateZ
    )
    nAttr.setStorable(False)

    ### Scale
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

    DvAlgebraPlug.output_shouler = cAttr.create("shoulder_xform", "sxf")
    cAttr.addChild(DvAlgebraPlug.output_shoulder_translate)
    cAttr.addChild(DvAlgebraPlug.output_shoulder_rotate)
    cAttr.addChild(DvAlgebraPlug.output_shoulder_scale)
    cAttr.setStorable(False)
    cAttr.setArray(True)
    cAttr.setUsesArrayDataBuilder(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_shouler)

    ## ELBOW
    ### Translate
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

    ### Rotate
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
    DvAlgebraPlug.output_elbow_rotate = uAttr.create(
        "output_elbow_rotate",   "oer",
        DvAlgebraPlug.output_elbow_rotateX,
        DvAlgebraPlug.output_elbow_rotateY,
        DvAlgebraPlug.output_elbow_rotateZ
    )
    nAttr.setStorable(False)

    ### Scale
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

    DvAlgebraPlug.output_shouler = cAttr.create("elbow_xform", "sxf")
    cAttr.addChild(DvAlgebraPlug.output_elbow_translate)
    cAttr.addChild(DvAlgebraPlug.output_elbow_rotate)
    cAttr.addChild(DvAlgebraPlug.output_elbow_scale)
    cAttr.setStorable(False)
    cAttr.setArray(True)
    cAttr.setUsesArrayDataBuilder(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_elbow)

    ## WRIST
    ### Translate
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

    ### Rotate
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
    DvAlgebraPlug.output_wrist_rotate = uAttr.create(
        "output_wrist_rotate",   "owr",
        DvAlgebraPlug.output_wrist_rotateX,
        DvAlgebraPlug.output_wrist_rotateY,
        DvAlgebraPlug.output_wrist_rotateZ
    )
    nAttr.setStorable(False)

    ### Scale
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

    DvAlgebraPlug.output_shouler = cAttr.create("wrist_xform", "sxf")
    cAttr.addChild(DvAlgebraPlug.output_wrist_translate)
    cAttr.addChild(DvAlgebraPlug.output_wrist_rotate)
    cAttr.addChild(DvAlgebraPlug.output_wrist_scale)
    cAttr.setStorable(False)
    cAttr.setArray(True)
    cAttr.setUsesArrayDataBuilder(True)
    DvAlgebraPlug.addAttribute(DvAlgebraPlug.output_wrist)


    # Include both outputs.
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.shoulder_pos, DvAlgebraPlug.output_shouler)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.elbow_pos, DvAlgebraPlug.output_shouler)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.wrist_pos, DvAlgebraPlug.output_shouler)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.parentInverseMatrix, DvAlgebraPlug.output_shouler)

    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.shoulder_pos, DvAlgebraPlug.output_elbow)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.elbow_pos, DvAlgebraPlug.output_elbow)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.wrist_pos, DvAlgebraPlug.output_elbow)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.parentInverseMatrix, DvAlgebraPlug.output_elbow)

    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.shoulder_pos, DvAlgebraPlug.output_wrist)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.elbow_pos, DvAlgebraPlug.output_wrist)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.wrist_pos, DvAlgebraPlug.output_wrist)
    DvAlgebraPlug.attributeAffects(DvAlgebraPlug.parentInverseMatrix, DvAlgebraPlug.output_wrist)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "damsOLabo", "1.0", "Any")
    try:
        plugin.registerNode(DvAlgebraPlug.kname, DvAlgebraPlug.kplugin_id, creator, initialize)
    except:
        raise RuntimeError, "Failed to register node: '{}'".format(DvAlgebraPlug.kname)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(DvAlgebraPlug.kplugin_id)
    except:
        raise RuntimeError, "Failed to register node: '{}'".format(DvAlgebraPlug.kname)
