# import du module cmds maya
from maya import cmds

# extraction des position des différents objets dans la l'espace
# extraction _L_shoulder_JNT
_L_shoulder_JNT_point = cmds.xform('_L_shoulder_JNT', q=True, ws=True, t=True)
# extraction _L_elbow_JNT
_L_elbow_JNT_point = cmds.xform('_L_elbow_JNT', q=True, ws=True, t=True)
# extraction _L_wrist_JNT
_L_wrist_JNT_point = cmds.xform('_L_wrist_JNT', q=True, ws=True, t=True)


### VECTOR
# import du module OpenMaya
from maya.api import OpenMaya
 
# convertion des listes de point en objet de type MVector
_L_shoulder_JNT_mVector = OpenMaya.MVector(_L_shoulder_JNT_point)
_L_elbow_JNT_mVector = OpenMaya.MVector(_L_elbow_JNT_point)
_L_wrist_JNT_mVector = OpenMaya.MVector(_L_wrist_JNT_point)
 
# calcul du vecteur qui part du coude vers l'épaule.
_L_upperArm_vect = _L_shoulder_JNT_mVector - _L_elbow_JNT_mVector
_L_upperArm_vect = _L_upperArm_vect.normal()

# calcul du vecteur qui part du coude vers le poignée
_L_lowerArm_vect = _L_wrist_JNT_mVector - _L_elbow_JNT_mVector
_L_lowerArm_vect = _L_lowerArm_vect.normal()

# calcul du vecteur qui part de l'épaule vers le coude.
_L_shoulder_vect = _L_elbow_JNT_mVector - _L_shoulder_JNT_mVector
_L_shoulder_vect = _L_shoulder_vect.normal()
        
# calcul de la longueur du vecteur _L_upperArm_vect
_L_upperArm_len = _L_upperArm_vect.length()
# calcul de la longueur du vecteur _L_lowerArm_vect
_L_lowerArm_len = _L_lowerArm_vect.length()


### DOT PRODUCT
angle_radian = _L_upperArm_vect.angle(_L_lowerArm_vect)


### CROSS PRODUCT
# Application au niveau upperArm
# calcul du vecteur normal, _L_aimUp_vect
_L_aimUp_vect =  _L_lowerArm_vect ^ _L_upperArm_vect
 
# utilisation du vecteur calculé _L_aimUp_vec pour calcuer zUpVec
zUpVec = _L_shoulder_vect ^_L_aimUp_vect

# Application au niveau lowerArm
# le _L_aimUp_vect est commun a toutes les position
# Calcul zLowerVec
zLowerVec = _L_aimUp_vect ^_L_lowerArm_vect
zLowerVec = zLowerVec.normal()


# MATRICES
# création de la list matrice upperArm
_L_shoulder_matrixList = [
    _L_shoulder_vect.x, _L_shoulder_vect.y, _L_shoulder_vect.z, 0.0,
    _L_aimUp_vect.x, _L_aimUp_vect.y, _L_aimUp_vect.z, 0.0,
    zUpVec.x, zUpVec.y, zUpVec.z, 0.0,
    _L_shoulder_JNT_mVector.x, _L_shoulder_JNT_mVector.y, _L_shoulder_JNT_mVector.z, 1.0
]

# Appliquer la matrice sur notre object _L_shoulder_JNT
cmds.xform('_L_shoulder_JNT', ws=True, m=_L_shoulder_matrixList)

# création de la list matrice lowerArm
_L_elbow_matrixList = [
    _L_lowerArm_vect.x, _L_lowerArm_vect.y, _L_lowerArm_vect.z, 0.0,
    _L_aimUp_vect.x, _L_aimUp_vect.y, _L_aimUp_vect.z, 0.0,
    zLowerVec.x, zLowerVec.y, zLowerVec.z, 0.0,
    _L_elbow_JNT_mVector.x, _L_elbow_JNT_mVector.y, _L_elbow_JNT_mVector.z, 1.0
]

# Appliquer la matrice sur notre object _L_shoulder_JNT
cmds.xform('_L_elbow_JNT', ws=True, m=_L_elbow_matrixList)

# création de la list matrice wristArm
_L_wrist_matrixList = [
    _L_lowerArm_vect.x, _L_lowerArm_vect.y, _L_lowerArm_vect.z, 0.0,
    _L_aimUp_vect.x, _L_aimUp_vect.y, _L_aimUp_vect.z, 0.0,
    zLowerVec.x, zLowerVec.y, zLowerVec.z, 0.0,
    _L_wrist_JNT_mVector.x, _L_wrist_JNT_mVector.y, _L_wrist_JNT_mVector.z, 1.0
]

# Appliquer la matrice sur notre object _L_shoulder_JNT
cmds.xform('_L_wrist_JNT', ws=True, m=_L_wrist_matrixList)
