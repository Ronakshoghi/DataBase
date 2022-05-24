# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-2 replay file
# Internal Version: 2014_08_22-15.53.04 134497
# Run by shoghrm7 on Wed Mar 16 00:43:53 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=595.458984375, 
    height=192.616653442383)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
o1 = session.openOdb(
    name='/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared Files/Ronak_geometry_Periodic.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: /home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared Files/Ronak_geometry_Periodic.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       32
#: Number of Node Sets:          281
#: Number of Steps:              1
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Loading')
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Loading', frame=0)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Loading', frame=0)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Loading', frame=3)
execfile(
    '/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py', 
    __main__.__dict__)
#: Starting Script
#* OdbError: Cannot open file 
#* /home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared 
#* Files/geometry_Periodic.odb. *** ERROR: No such file: 
#* /home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared 
#* Files/geometry_Periodic.odb.
#* File 
#* "/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py", 
#* line 540, in <module>
#*     node=Result1.F_ODB('geometry_Periodic.odb', dimension, beginStep, 
#* endStep)
#* File 
#* "/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py", 
#* line 109, in F_ODB
#*     odb=openOdb(odbName,readOnly=True)
execfile(
    '/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py', 
    __main__.__dict__)
#: Starting Script
#* OdbError: Cannot open file 
#* /home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared 
#* Files/geometry_Periodic.odb. *** ERROR: No such file: 
#* /home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/Prepared 
#* Files/geometry_Periodic.odb.
#* File 
#* "/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py", 
#* line 540, in <module>
#*     node=Result1.F_ODB('geometry_Periodic.odb', dimension, beginStep, 
#* endStep)
#* File 
#* "/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py", 
#* line 109, in F_ODB
#*     odb=openOdb(odbName,readOnly=True)
execfile(
    '/home/users/shoghrm7/For_Ronak/Crystal_Plasticity_UMAT/Examples/Test/AbaqusOdbPostprocessor_2020.py', 
    __main__.__dict__)
#: Starting Script
#: [[  7.39117432e+01  -3.06403685e-08  -2.00442128e-06]
#:  [ -1.09361217e-07   0.00000000e+00   5.82890344e-13]
#:  [ -1.64953945e-12  -1.70705032e-08  -0.00000000e+00]]
session.animationController.setValues(animationType=SCALE_FACTOR, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=TIME_HISTORY)
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.animationController.setValues(animationType=SCALE_FACTOR, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.animationController.setValues(animationType=HARMONIC, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.760831, 
    farPlane=1.33462, width=1.04053, height=0.35703, cameraPosition=(1.06803, 
    0.366011, 0.579952), cameraUpVector=(-0.58218, 0.813016, -0.00847247), 
    cameraTarget=(0.148478, 0.130543, 0.14848))
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=ON)
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=OFF)
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=ON)
session.viewports['Viewport: 1'].odbDisplay.setValues(viewCut=OFF)
session.animationController.setValues(animationType=NONE)
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='RF', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='LE', outputPosition=INTEGRATION_POINT, refinement=(
    INVARIANT, 'Max. Principal'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='COORD', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='CF', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
session.animationController.setValues(animationType=TIME_HISTORY, viewports=(
    'Viewport: 1', ))
session.animationController.play(duration=UNLIMITED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.801067, 
    farPlane=1.29823, width=1.09556, height=0.375913, cameraPosition=(0.276027, 
    0.295972, 1.17234), cameraUpVector=(-0.335688, 0.836536, -0.433037), 
    cameraTarget=(0.144663, 0.130206, 0.151333))
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='CF', outputPosition=NODAL, refinement=(INVARIANT, 
    'Magnitude'), )
