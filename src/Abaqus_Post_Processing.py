# -*- coding: utf-8 -*-
"""
Author: Ronak Shoghi
Date: 23.05.22
Time: 14:44

"""
# !/usr/env/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
#
# Martin Boeff
#
#
# -------------------------------------------------------------------
import os
import sys
import numpy as np
import numpy.linalg as npl
import pickle

from odbAccess import *
# Access to Symbolic Constants defined in Abaqus
from abaqusConstants import *


# -------------------------------------------------------------------
##import matplotlib as MPL
# import matplotlib.pyplot as PyPlot
# from matplotlib.font_manager import FontProperties
# ------------------------------------------------------------------
# ==============================================================================
# ==============================================================================


class Class_NodeObject(object):

    def __init__(self):
        # Node number
        self.nodeNumer = []
        # Times
        self.steptime = []
        self.totaltime = []
        # Displacements
        self.u1 = []
        self.u2 = []
        self.u3 = []
        # Positions
        self.x = []
        self.y = []
        self.z = []
        # Reaktionforces
        self.rf1 = []
        self.rf2 = []
        self.rf3 = []
        # ConcentratedForces
        self.cf1 = []
        self.cf2 = []
        self.cf3 = []

        # Region definition abaqus
        self.abqRegion = []


class OdbData(object):

    def __init__(self):
        self.name = []

        # Times
        self.steptime = []
        self.totaltime = []

        # homogenized stress
        self.sigmaH = []
        self.sigmaHE = []

        # homogenized strain
        self.defH = []
        self.strainH = []
        self.strainHE = []

        # Plot
        self.strain11Plot = []
        self.strain22Plot = []
        self.strain33Plot = []
        self.strain12Plot = []
        self.strain13Plot = []
        self.strain23Plot = []

        self.defgrad11 = []
        self.defgrad22 = []
        self.defgrad33 = []
        self.defgrad12 = []
        self.defgrad13 = []
        self.defgrad23 = []
        self.defgrad21 = []
        self.defgrad31 = []
        self.defgrad32 = []

        self.sigmaPlot = []
        self.sigmaVPlot = []
        self.strainEPlot = []
        self.sigma11Plot = []
        self.sigma22Plot = []
        self.sigma33Plot = []
        self.sigma13Plot = []
        self.sigma23Plot = []
        self.sigma12Plot = []

        self.SDV156 = []
        self.SDV157 = []
        self.SDV158 = []
        self.SDV159 = []
        self.SDV160 = []
        self.SDV161 = []

    def F_ODB(self, odbName, dimension, firstStep, lastStep):

        # Open the ODB
        odb = openOdb(odbName, readOnly=True)

        # Show all setp stored in odb
        allSteps = odb.steps.keys()

        nodeObjectDict = dict()

        if dimension == '2d':
            # Dictionary definition
            nodeObjectDict['V1'] = Class_NodeObject()
            nodeObjectDict['V2'] = Class_NodeObject()
            nodeObjectDict['V4'] = Class_NodeObject()

            # Access to nodes
            nodeObjectDict['V1'].abqRegion = odb.rootAssembly.nodeSets['V1']
            nodeObjectDict['V2'].abqRegion = odb.rootAssembly.nodeSets['V2']
            nodeObjectDict['V4'].abqRegion = odb.rootAssembly.nodeSets['V4']

        if dimension == '3d':
            # Dictionary definition
            nodeObjectDict['V1'] = Class_NodeObject()
            nodeObjectDict['V2'] = Class_NodeObject()
            nodeObjectDict['V4'] = Class_NodeObject()
            nodeObjectDict['H1'] = Class_NodeObject()

            # Access to nodes
            nodeObjectDict['V1'].abqRegion = odb.rootAssembly.nodeSets['V1']
            nodeObjectDict['V2'].abqRegion = odb.rootAssembly.nodeSets['V2']
            nodeObjectDict['V4'].abqRegion = odb.rootAssembly.nodeSets['V4']
            nodeObjectDict['H1'].abqRegion = odb.rootAssembly.nodeSets['H1']

        # Loop over all steps
        for stepKey in range(firstStep, lastStep + 1):

            # Get current step name
            currentStepName = odb.steps.keys()[stepKey - 1]
            # print 'Step: ', currentStepName

            # Get number of frames in current step
            numberFrames = len(odb.steps[currentStepName].frames)
            # print 'Number of Frames: ', numberFrames

            # Loop over all frames in current step
            for cframe in range(numberFrames):

                # cframe=-1
                # Outputs saved in current frame
                currentFrame = odb.steps[currentStepName].frames[cframe]
                # print currentFrame

                # Time in step for the current frame
                stepTime = currentFrame.frameValue
                self.steptime.append(stepTime)

                # self.SDV156.append(currentFrame.fieldOutputs['SDV156'].getSubset(CENTROID).values[0].data)
                # self.SDV157.append(currentFrame.fieldOutputs['SDV157'].getSubset(CENTROID).values[0].data)
                # self.SDV158.append(currentFrame.fieldOutputs['SDV158'].getSubset(CENTROID).values[0].data)
                # self.SDV159.append(currentFrame.fieldOutputs['SDV159'].getSubset(CENTROID).values[0].data)
                # self.SDV160.append(currentFrame.fieldOutputs['SDV160'].getSubset(CENTROID).values[0].data)
                # self.SDV161.append(currentFrame.fieldOutputs['SDV161'].getSubset(CENTROID).values[0].data)
                Temp_SDV156 = []
                Temp_SDV157 = []
                Temp_SDV158 = []
                Temp_SDV159 = []
                Temp_SDV160 = []
                Temp_SDV161 = []
                for elementlabel in range(len(currentFrame.fieldOutputs['SDV156'].getSubset(CENTROID).values)):
                    Temp_SDV156.append(currentFrame.fieldOutputs['SDV156'].getSubset(CENTROID).values[elementlabel].data)
                    Temp_SDV157.append(currentFrame.fieldOutputs['SDV157'].getSubset(CENTROID).values[elementlabel].data)
                    Temp_SDV158.append(currentFrame.fieldOutputs['SDV158'].getSubset(CENTROID).values[elementlabel].data)
                    Temp_SDV159.append(currentFrame.fieldOutputs['SDV159'].getSubset(CENTROID).values[elementlabel].data)
                    Temp_SDV160.append(currentFrame.fieldOutputs['SDV160'].getSubset(CENTROID).values[elementlabel].data)
                    Temp_SDV161.append(currentFrame.fieldOutputs['SDV161'].getSubset(CENTROID).values[elementlabel].data)

                self.SDV156.append(np.mean(Temp_SDV156))
                self.SDV157.append(np.mean(Temp_SDV157))
                self.SDV158.append(np.mean(Temp_SDV158))
                self.SDV159.append(np.mean(Temp_SDV159))
                self.SDV160.append(np.mean(Temp_SDV160))
                self.SDV161.append(np.mean(Temp_SDV161))
                #########################################################
                # Nodal Results
                #########################################################
                displacementList = currentFrame.fieldOutputs['U']
                reaktionForceList = currentFrame.fieldOutputs['RF']
                concentratedForceList = currentFrame.fieldOutputs['CF']
                coordList = currentFrame.fieldOutputs['COORD']
                for node in nodeObjectDict:
                    ######
                    # Displacements
                    displacement = displacementList.getSubset(region=nodeObjectDict[node].abqRegion).values
                    u1 = displacement[0].data[0]
                    u2 = displacement[0].data[1]
                    if dimension == '3d':
                        u3 = displacement[0].data[2]
                    else:
                        u3 = 0.0
                    # Assign to Dictionary
                    nodeObjectDict[node].u1.append(u1)
                    nodeObjectDict[node].u2.append(u2)
                    nodeObjectDict[node].u3.append(u3)
                    ######
                    # Reaktion Force
                    reaktionForce = reaktionForceList.getSubset(region=nodeObjectDict[node].abqRegion).values
                    rf1 = reaktionForce[0].data[0]
                    rf2 = reaktionForce[0].data[1]
                    if dimension == '3d':
                        rf3 = reaktionForce[0].data[2]
                    else:
                        rf3 = 0.0
                    ######
                    # Concentrated Force
                    concentratedForce = concentratedForceList.getSubset(region=nodeObjectDict[node].abqRegion).values
                    cf1 = concentratedForce[0].data[0]
                    cf2 = concentratedForce[0].data[1]
                    if dimension == '3d':
                        cf3 = concentratedForce[0].data[2]
                    else:
                        cf3 = 0.0
                    # Assign to Dictionary
                    nodeObjectDict[node].rf1.append(rf1 + cf1)
                    nodeObjectDict[node].rf2.append(rf2 + cf2)
                    nodeObjectDict[node].rf3.append(rf3 + cf3)
                    ######
                    # Coordinate
                    coordinate = coordList.getSubset(region=nodeObjectDict[node].abqRegion).values
                    x = coordinate[0].data[0]
                    y = coordinate[0].data[1]
                    if dimension == '3d':
                        z = coordinate[0].data[2]
                    else:
                        z = 0.0
                    # Assign to Dictionary
                    nodeObjectDict[node].x.append(x)
                    nodeObjectDict[node].y.append(y)
                    nodeObjectDict[node].z.append(z)
        return nodeObjectDict

    def F_CalcSigmaH(self, nodeObjectDict, dimension):

        # Origin
        origin = [nodeObjectDict['V1'].x[0], nodeObjectDict['V1'].y[0], nodeObjectDict['V1'].z[0]]
        # Initial Vectors
        y12_0 = np.asmatrix([[nodeObjectDict['V2'].x[0] - origin[0], nodeObjectDict['V2'].y[0] - origin[1],
                              nodeObjectDict['V2'].z[0] - origin[2]]])
        y14_0 = np.asmatrix([[nodeObjectDict['V4'].x[0] - origin[0], nodeObjectDict['V4'].y[0] - origin[1],
                              nodeObjectDict['V4'].z[0] - origin[2]]])
        if dimension == '3d':
            y11_0 = np.asmatrix([[nodeObjectDict['H1'].x[0] - origin[0], nodeObjectDict['H1'].y[0] - origin[1],
                                  nodeObjectDict['H1'].z[0] - origin[2]]])
        else:
            y11_0 = np.asmatrix([nodeObjectDict['V1'].x[0], nodeObjectDict['V1'].y[0], nodeObjectDict['V1'].z[0] - 1.0])

        volume_0 = np.sqrt((np.inner(np.cross(y12_0, y14_0), y11_0).flat[0]) ** 2)

        for f in range(len(self.steptime)):

            y12 = np.asmatrix([[nodeObjectDict['V2'].x[f] - origin[0], nodeObjectDict['V2'].y[f] - origin[1],
                                nodeObjectDict['V2'].z[f] - origin[2]]])
            y14 = np.asmatrix([[nodeObjectDict['V4'].x[f] - origin[0], nodeObjectDict['V4'].y[f] - origin[1],
                                nodeObjectDict['V4'].z[f] - origin[2]]])
            if dimension == '3d':
                y11 = np.asmatrix([[nodeObjectDict['H1'].x[f] - origin[0], nodeObjectDict['H1'].y[f] - origin[1],
                                    nodeObjectDict['H1'].z[f] - origin[2]]])
            else:
                y11 = np.asmatrix(
                    [nodeObjectDict['V1'].x[0], nodeObjectDict['V1'].y[0], nodeObjectDict['V1'].z[0] - 1.0])
            # Volume of a spart
            volume = np.sqrt((np.inner(np.cross(y12, y14), y11).flat[0]) ** 2)

            # ReaktionForces
            # rf_V1 = np.asmatrix([[nodeObjectDict['V1'].rf1[f],nodeObjectDict['V1'].rf2[f],nodeObjectDict['V1'].rf3[f]]])
            rf_V2 = np.asmatrix(
                [[nodeObjectDict['V2'].rf1[f], nodeObjectDict['V2'].rf2[f], nodeObjectDict['V2'].rf3[f]]])
            rf_V4 = np.asmatrix(
                [[nodeObjectDict['V4'].rf1[f], nodeObjectDict['V4'].rf2[f], nodeObjectDict['V4'].rf3[f]]])
            if dimension == '3d':
                rf_H1 = np.asmatrix(
                    [[nodeObjectDict['H1'].rf1[f], nodeObjectDict['H1'].rf2[f], nodeObjectDict['H1'].rf3[f]]])
            else:
                rf_H1 = np.asmatrix([0, 0, 0])
            # print rf_H1
            # Homogenized stress
            self.sigmaH = 1. / volume_0 * (np.outer(rf_V2, y12) + np.outer(rf_V4, y14) + np.outer(rf_H1, y11))
            # print 'homgenized stress:'
            # print self.sigmaH

            # Mises Stress
            self.sigmaHE = F_CalcMises(self.sigmaH)
            # print self.sigmaHE

            # print F_CalcF3(y12,y14,y12_0,y14_0)
            uV2 = np.asmatrix([[nodeObjectDict['V2'].u1[f], nodeObjectDict['V2'].u2[f], nodeObjectDict['V2'].u3[f]]])
            uV4 = np.asmatrix([[nodeObjectDict['V4'].u1[f], nodeObjectDict['V4'].u2[f], nodeObjectDict['V4'].u3[f]]])
            if dimension == '3d':
                uH1 = np.asmatrix(
                    [[nodeObjectDict['H1'].u1[f], nodeObjectDict['H1'].u2[f], nodeObjectDict['H1'].u3[f]]])
            else:
                uH1 = np.asmatrix([0., 0., 0.])
            # self.strainH = F_CalcEps(uV2,uV4,uH1,y12_0,y14_0,y11_0)
            self.defGrad = CalcDefgrad(uV2, uV4, uH1, y12_0, y14_0, y11_0)
            self.strainH = F_CalcEps1(self.defGrad)

            # print 'homgenized strain:'
            # print self.strainH

            # Equivalent strain
            self.strainHE = F_CalcEqStrain(self.strainH)
            # print self.strainHE

            # F_CalcStiffness(self.sigmaH,self.strainH)

            # Stiffness=F_CalcStiffness(self.sigmaH,self.strainH)

            # print 'Stiffness: '
            # print Stiffness
            self.strain11Plot.append(self.strainH[0, 0])
            self.strain22Plot.append(self.strainH[1, 1])
            self.strain33Plot.append(self.strainH[2, 2])
            self.strain12Plot.append(self.strainH[0, 1])
            self.strain13Plot.append(self.strainH[0, 2])
            self.strain23Plot.append(self.strainH[1, 2])

            self.defgrad11.append(self.defGrad[0, 0])
            self.defgrad22.append(self.defGrad[1, 1])
            self.defgrad33.append(self.defGrad[2, 2])
            self.defgrad12.append(self.defGrad[0, 1])
            self.defgrad13.append(self.defGrad[0, 2])
            self.defgrad23.append(self.defGrad[1, 2])
            self.defgrad21.append(self.defGrad[1, 0])
            self.defgrad31.append(self.defGrad[2, 0])
            self.defgrad32.append(self.defGrad[2, 1])

            self.sigma11Plot.append(self.sigmaH[0, 0])
            self.sigma22Plot.append(self.sigmaH[1, 1])
            self.sigma33Plot.append(self.sigmaH[2, 2])
            self.sigma12Plot.append(self.sigmaH[0, 1])
            self.sigma13Plot.append(self.sigmaH[0, 2])
            self.sigma23Plot.append(self.sigmaH[1, 2])
            self.sigmaVPlot.append(self.sigmaHE)
            self.strainEPlot.append(self.strainHE)

        return


def F_VoigtNotationStress(stress):
    stressV = np.zeros(6)
    # Stress in Voigt notation
    stressV[0] = stress[0, 0]
    stressV[1] = stress[1, 1]
    stressV[2] = stress[2, 2]
    stressV[3] = stress[1, 2]
    stressV[4] = stress[0, 2]
    stressV[5] = stress[0, 1]
    return stressV


def F_VoigtNotationStrain(strain):
    strainV = np.zeros(6)
    # Strain in Voigt notation
    strainV[0] = strain[0, 0]
    strainV[1] = strain[1, 1]
    strainV[2] = strain[2, 2]
    strainV[3] = 2. * strain[1, 2]
    strainV[4] = 2. * strain[0, 2]
    strainV[5] = 2. * strain[0, 1]
    return strainV


# Delets errors in stress tensor that are smaller than 0.1%
def F_FilterVoigtVector(vector):
    Toleranz = 0.001
    maxVector = max(abs(vector))
    vectorNorm = abs(vector / maxVector)

    for i in range(len(vectorNorm)):
        if vectorNorm[i] < Toleranz:
            vector[i] = 0.0
    return vector


def F_CalcStiffness(sigmaH, strainH):
    # Convert stresses and strains to Voigt notation
    stress = F_VoigtNotationStress(sigmaH)
    strain = F_VoigtNotationStrain(strainH)

    # Throw out very small stress components which occur due to numerical errors
    stress = F_FilterVoigtVector(stress)
    strain = F_FilterVoigtVector(strain)

    # Take the only strain component (in Voigt notation) which is not zero
    maxStrain = max(strain)
    minStrain = min(strain)
    if abs(minStrain) > abs(maxStrain):
        maxStrain = minStrain  # To also consider negative strain entries

    # Calculate stiffness (only one entry in strain vector is allowed to be nonzero)
    C = np.zeros(6)
    C[0] = stress[0] / maxStrain
    C[1] = stress[1] / maxStrain
    C[2] = stress[2] / maxStrain
    C[3] = stress[3] / maxStrain
    C[4] = stress[4] / maxStrain
    C[5] = stress[5] / maxStrain

    return C


# Mises Stress
def F_CalcMises(sigmaM):
    # Pressure
    p = 0.
    I2 = 0.
    for i in range(3):
        p = p + 1. / 3. * sigmaM[i, i]

    for i in range(3):
        for j in range(3):
            # Invariant
            if i == j:
                I2 = I2 + (sigmaM[i, j] - p) * (sigmaM[i, j] - p)
            else:
                I2 = I2 + sigmaM[i, j] * sigmaM[i, j]

    sigmaE = np.sqrt(3. / 2. * I2)
    return sigmaE


# Equivalent strain
def F_CalcEqStrain(strainM):
    # hydro strain
    eh = 0.
    I2 = 0.
    for i in range(3):
        eh = eh + 1. / 3. * strainM[i, i]

    for i in range(3):
        for j in range(3):
            # Invariant
            if i == j:
                I2 = I2 + (strainM[i, j] - eh) * (strainM[i, j] - eh)
            else:
                I2 = I2 + strainM[i, j] * strainM[i, j]

    sigmaE = np.sqrt(2. / 3. * I2)
    return sigmaE


# Calculate Deformation gradient (as in Paper of Smit) not used for 3D
def F_CalcF2(y12, y14, y11, y12_0, y14_0, y11_0, volume_0):
    # Areas
    AreaH1V4 = npl.norm(np.cross(y11_0, y14_0))
    AreaH1V2 = npl.norm(np.cross(y12_0, y11_0))
    AreaV2V4 = npl.norm(np.cross(y12_0, y14_0))

    # Normals
    nH1V4 = np.cross(y11_0, y14_0) / AreaH1V4
    nH1V2 = np.cross(y12_0, y11_0) / AreaH1V2
    nV2V4 = np.cross(y12_0, y14_0) / AreaV2V4

    # Initial Volume
    # volume0 = npl.norm(np.dot(np.cross(y11_0,y14_0),y12_0))

    # Deformation gradient
    defgrad = np.zeros((3, 3))

    # defgrad = 1./volume_0 * (np.outer((y11+y14),nH1V4) *AreaH1V4 + np.outer((y12+y14),nV2V4) * AreaV2V4 + np.outer((y11+y12),nH1V2) * AreaH1V2)
    defgrad = 1. / volume_0 * (
                np.outer((y11 + y14), nH1V4) * AreaH1V4 + np.outer((y12 + y14), nV2V4) * AreaV2V4 + np.outer(
            (y11 + y12), nH1V2) * AreaH1V2)

    C = np.dot(np.transpose(defgrad), defgrad)

    E = 0.5 * (C - np.eye(3))

    return defgrad


def CalcDefgrad(uV2, uV4, uH1, y12_0, y14_0, y11_0):
    defgrad = np.zeros((3, 3))
    dx1 = npl.norm(y12_0)
    dx2 = npl.norm(y14_0)
    dx3 = npl.norm(y11_0)

    defgrad[0, 0] = 1 + uV2[0, 0] / dx1
    defgrad[1, 1] = 1 + uV4[0, 1] / dx2
    defgrad[2, 2] = 1 + (-uH1[0, 2]) / dx3
    defgrad[0, 1] = uV4[0, 0] / dx2
    defgrad[0, 2] = -uH1[0, 0] / dx3
    defgrad[1, 0] = uV2[0, 1] / dx1
    defgrad[1, 2] = -uH1[0, 1] / dx3
    defgrad[2, 0] = uV2[0, 2] / dx1
    defgrad[2, 1] = uV4[0, 2] / dx2

    return defgrad


# Strain Tensor (Geometrical)
def F_CalcEps(uV2, uV4, uH1, y12_0, y14_0, y11_0):
    eps = np.zeros((3, 3))
    dx1 = npl.norm(y12_0)
    dx2 = npl.norm(y14_0)
    dx3 = npl.norm(y11_0)
    # V2

    # eps[0,0] = uV2[0,0]/dx1
    # eps[1,0] = 0.5*(uV4[0,0]/dx2 + uV2[0,1]/dx1)
    # eps[2,0] = 0.5*(-uH1[0,0]/dx3 + uV2[0,2]/dx1)
    # V4
    # eps[0,1] = eps[1,0]
    # eps[1,1] = uV4[0,1]/dx2
    # eps[2,1] = 0.5*(-uH1[0,1]/dx3 + uV4[0,2]/dx2)
    # H1
    # eps[0,2] = eps[2,0]
    # eps[1,2] = eps[2,1]
    # eps[2,2] = -uH1[0,2]/dx3

    eps[0, 0] = uV2[0, 0] / dx1 + 0.5 * ((((uV2[0, 1]) ** 2) + ((uV2[0, 2]) ** 2) + ((uV2[0, 0]) ** 2)) / (dx1 ** 2))
    #       eps[1,0] = 0.5*(uV4[0,0]/dx2 + uV2[0,1]/dx1)
    eps[1, 0] = 0.5 * (
                uV4[0, 0] / dx2 + uV2[0, 1] / dx1 + (uV4[0, 0] * uV2[0, 0]) / (dx1 * dx2) + (uV4[0, 1] * uV2[0, 1]) / (
                    dx1 * dx2) + (uV4[0, 2] * uV2[0, 2]) / (dx1 * dx2))
    #       eps[2,0] = 0.5*(-uH1[0,0]/dx3 + uV2[0,2]/dx1)
    eps[2, 0] = 0.5 * (-uH1[0, 0] / dx3 + uV2[0, 2] / dx1 + (-uH1[0, 0] * uV2[0, 0]) / (dx1 * dx3) + (
                -uH1[0, 1] * uV2[0, 1]) / (dx1 * dx3) + (-uH1[0, 2] * uV2[0, 2]) / (dx1 * dx3))
    # V4
    eps[0, 1] = eps[1, 0]
    #       eps[1,1] = uV4[0,1]/dx2
    eps[1, 1] = uV4[0, 1] / dx2 + 0.5 * ((((uV4[0, 1]) ** 2) + ((uV4[0, 2]) ** 2) + ((uV4[0, 0]) ** 2)) / (dx2 ** 2))
    #       eps[2,1] = 0.5*(-uH1[0,1]/dx3 + uV4[0,2]/dx2)
    eps[2, 1] = 0.5 * (-uH1[0, 1] / dx3 + uV4[0, 2] / dx2 + (-uH1[0, 0] * uV4[0, 0]) / (dx1 * dx3) + (
                -uH1[0, 1] * uV4[0, 1]) / (dx1 * dx3) + (-uH1[0, 2] * uV4[0, 2]) / (dx2 * dx3))
    # H1
    eps[0, 2] = eps[2, 0]
    eps[1, 2] = eps[2, 1]
    #       eps[2,2] = -uH1[0,2]/dx3
    eps[2, 2] = -uH1[0, 2] / dx3 + 0.5 * ((((uV2[0, 0]) ** 2) + ((uV4[0, 1]) ** 2) + ((-uH1[0, 2]) ** 2)) / (dx3 ** 2))

    return eps


def F_CalcEps1(F):
    eps = np.zeros((3, 3))
    Ft = np.transpose(F)

    for i in range(3):
        for j in range(3):
            eps[i, j] = np.dot(Ft[i, :], F[:, j])

    eps = eps - np.identity(3)
    eps = eps * 0.5

    return eps


# ==============================================================================
# ==============================================================================

# Number of steps
beginStep = 1
endStep = 1
dimension = '3d'
for root, dir, files in os.walk(os.getcwd()):
    for filename in files:
        if ".odb" in filename:
            Key_File_Name = filename

Splitted_Name = Key_File_Name.split('_Abaqus')
Key = Splitted_Name[0]
odbName = '{}_Abaqus_Input_File.odb'.format(Key)
# Definition of Result Files

# Result1
Result1 = OdbData()
node = Result1.F_ODB(odbName, dimension, beginStep, endStep)
Result1.F_CalcSigmaH(node, dimension)
os.chdir('..')
Key_Results_Path = "{}/results".format(os.getcwd())
os.chdir(Key_Results_Path)
np.savetxt('{}/S11.out'.format(Key_Results_Path), Result1.sigma11Plot)
np.savetxt('{}/S22.out'.format(Key_Results_Path), Result1.sigma22Plot)
np.savetxt('{}/S33.out'.format(Key_Results_Path), Result1.sigma33Plot)
np.savetxt('{}/S12.out'.format(Key_Results_Path), Result1.sigma12Plot)
np.savetxt('{}/S23.out'.format(Key_Results_Path), Result1.sigma23Plot)
np.savetxt('{}/S13.out'.format(Key_Results_Path), Result1.sigma13Plot)
np.savetxt('{}/E11.out'.format(Key_Results_Path), Result1.strain11Plot)
np.savetxt('{}/E22.out'.format(Key_Results_Path), Result1.strain22Plot)
np.savetxt('{}/E33.out'.format(Key_Results_Path), Result1.strain33Plot)
np.savetxt('{}/E12.out'.format(Key_Results_Path), Result1.strain12Plot)
np.savetxt('{}/E13.out'.format(Key_Results_Path), Result1.strain13Plot)
np.savetxt('{}/E23.out'.format(Key_Results_Path), Result1.strain23Plot)
np.savetxt('{}/E.out'.format(Key_Results_Path), Result1.strainEPlot)
np.savetxt('{}/S.out'.format(Key_Results_Path), Result1.sigmaVPlot)
np.savetxt('{}/Ep11.out'.format(Key_Results_Path), Result1.SDV156)
np.savetxt('{}/Ep22.out'.format(Key_Results_Path), Result1.SDV157)
np.savetxt('{}/Ep33.out'.format(Key_Results_Path), Result1.SDV158)
np.savetxt('{}/Ep12.out'.format(Key_Results_Path), Result1.SDV159)
np.savetxt('{}/Ep13.out'.format(Key_Results_Path), Result1.SDV160)
np.savetxt('{}/Ep23.out'.format(Key_Results_Path), Result1.SDV161)
