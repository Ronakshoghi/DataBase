# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import random
import os
import math
from array import array
from numpy import genfromtxt
import numpy as np

mdb.close()
Model = mdb.models['Model-1']

def macro_function():

    major_av = 0.095
    minor_av = 0.095
    print(major_av)
    print(minor_av)

    # depval
    depvar_val=200

    # x discritization
    nx = 3
    # y discritization
    ny = 3
    # z discritization
    nz = 3

    #lnx = av_grain_minor
    lnx = minor_av
    #wny = av_grain_major
    wny = major_av
    #dnz = 2*av_grain_minor
    dnz = lnx
    print(dnz,lnx,wny)

    # Dimension of the model
    # length
    ln = nx*lnx # x-direction
    # width
    wd = ny*wny # y-direction
    # depth
    dp = nz*dnz # z-direction

    # elements per grain - x dir
    egx = 3
    # elements per grain - y dir
    egy = 3
    # elements per grain - z dir
    egz = 3

    # random-fitted MDF switch - 1 for random and -0 for fitted
    mdf = 0

    volume = ln*wd*dp

    # number of state depenadant variables NOTE Jan: irrelevant in our case, because we delete materials created here
    n_st_var = 200
    # alloy number
    ialloy = 4

    low = 0
    up = 360

    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0),point2=(ln, wd))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type= DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=dp, sketch= mdb.models['Model-1'].sketches['__profile__'])


    # section defination
    for i in range (1,nx*ny*nz+1):
      mdb.models['Model-1'].HomogeneousSolidSection(material='Material-'+str(i),
      name='Section-'+str(i), thickness=None)


    # partition plane
    for i in range (1,nz):
      mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=i*dnz,
      principalPlane=XYPLANE)

    for i in range (1,ny):
      mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=i*wny,
      principalPlane=XZPLANE)

    for i in range (1,nx):
      mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=i*lnx,
      principalPlane=YZPLANE)

    # partitioning
    j = 2
    print(ln,wd,dp)
    for i in range (0,nz-1):
      mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
      mdb.models['Model-1'].parts['Part-1'].cells.getByBoundingBox(0,0,0.98*i*dnz,2*ln,2*wd,2*dp),
      datumPlane=mdb.models['Model-1'].parts['Part-1'].datums[j])
      j = j+1

    for i in range (0,ny-1):
      mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
      mdb.models['Model-1'].parts['Part-1'].cells.getByBoundingBox(0,0.98*i*wny,0,2*ln,2*wd,2*dp),
      datumPlane=mdb.models['Model-1'].parts['Part-1'].datums[j])
      j = j+1

    for i in range (0,nx-1):
      mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
      mdb.models['Model-1'].parts['Part-1'].cells.getByBoundingBox(0.98*i*lnx,0,0,2*ln,2*wd,2*dp),
      datumPlane=mdb.models['Model-1'].parts['Part-1'].datums[j])
      j = j+1

    # angle read

    nmi = nx*ny*nz

    #angles = genfromtxt('ang_set.csv', delimiter=',')
    #index_list = genfromtxt('index_list.csv', delimiter=' ')


    j = 1
    for i in range (0,nx):
      for k in range (0,ny):
        for m in range (0,nz):
          mdb.models['Model-1'].Material(name='Material-'+str(j))
          angles = np.random.normal(size=3)
          mdb.models['Model-1'].materials['Material-'+str(j)].UserMaterial(mechanicalConstants=(ialloy, 0, 1, 2))
          print(angles[0], angles[1], angles[2])
          mdb.models['Model-1'].materials['Material-'+str(j)].Depvar(n=depvar_val)
          mdb.models['Model-1'].HomogeneousSolidSection(material='Material-'+str(j), name='Section-'+str(j), thickness=None)
          mdb.models['Model-1'].parts['Part-1'].Set(cells=
          mdb.models['Model-1'].parts['Part-1'].cells.getByBoundingBox(0.99*i*lnx,0.99*k*wny,0.99*m*dnz,1.01*(i+1)*lnx,1.01*(k+1)*wny,1.01*(m+1)*dnz), name='Set-'+str(j))
          mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0,offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Part-1'].sets['Set-'+str(j)],			sectionName='Section-'+str(j), thicknessAssignment=FROM_SECTION)
          j=j+1
          print(j)


    # mesh geneartion
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1',
    part=mdb.models['Model-1'].parts['Part-1'])
    for i in range(nx+1):
    	for j in range(ny+1):
    		mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER,
            edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getByBoundingBox(
            i*lnx-0.5*lnx,j*wny-0.5*wny,-0.1,i*lnx+0.5*lnx,j*wny+0.5*wny,1.1*dp), number=egz)

    for i in range(nz+1):
    	for j in range(ny+1):
    		mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER,
            edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getByBoundingBox(
            -0.1,j*wny-0.5*wny,i*dnz-0.5*dnz,1.1*ln,j*wny+0.5*wny,i*dnz+0.5*dnz), number=egx)


    for i in range(nx+1):
    	for j in range(nz+1):
    		mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER,
            edges=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.getByBoundingBox(
            i*lnx-0.5*lnx,-0.1,j*dnz-0.5*dnz,i*lnx+0.5*lnx,1.1*wd,j*dnz+0.5*dnz), number=egy)


    mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF,
        distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD),
        ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].cells.getByBoundingBox(-0.1,-0.1,-0.1,2*ln,2*wd,2*dp), ))

    mdb.models['Model-1'].rootAssembly.generateMesh(regions=(mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))


    #save input file
    mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF,
    description='', echoPrint=OFF, explicitPrecision=SINGLE,
	getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=
	PERCENTAGE, model='Model-1', modelPrint=OFF, multiprocessingMode=DEFAULT,
	name='inputfile_model', nodalOutputPrecision=SINGLE, numCpus=1, numDomains=1,
	parallelizationMethodExplicit=DOMAIN, queue=None, scratch='', type=ANALYSIS,
    userSubroutine='', waitHours=0, waitMinutes=0)


    mdb.jobs['inputfile_model'].writeInput()
    del mdb.models['Model-1'].sketches['__profile__']




macro_function()
