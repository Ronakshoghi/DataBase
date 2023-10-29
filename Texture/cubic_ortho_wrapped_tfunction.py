"""
This file contains python methods which wrap the Cubic Orthorhombic GSH functions provided in
cubic_ortho_tfunction_python.txt. To efficiently use the functions, import the "governor" method.
When called, this method will return a list of the GSH functions and a corresponding list of the indexes.

Created by: Andreas E. Robertson
Contact: arobertson38@gatech.edu
"""
import numpy as np


# Single methods

def wrapped0(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 0 1 1

	"""
	return phi*0.0 + 1.0

def wrapped1(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 4 1 1

	"""
	return 1/np.sqrt(2)*(5/48*((np.cos(phi)**4-2*np.cos(phi)**2+1)*np.cos(4*phi2)+7*np.cos(phi)**4-6*np.cos(phi)**2+3/5)*7**(1/2)*3**(1/2)+(-1)**4*5/48*((np.cos(phi)**4-2*np.cos(phi)**2+1)*np.cos(4*phi2)+7*np.cos(phi)**4-6*np.cos(phi)**2+3/5)*7**(1/2)*3**(1/2))


def wrapped2(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 4 2 1

	"""
	return 1/np.sqrt(2)*(1/96*((np.cos(phi)-1)**2*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))+(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))+(14*np.cos(phi)**2-2)*np.exp(2*np.sqrt(-1+0j)*phi1))*5**(1/2)*2**(1/2)*(np.cos(phi)-1)*21**(1/2)*(1+np.cos(phi))+(-1)**4*1/96*((np.cos(phi)-1)**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))+(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))+(14*np.cos(phi)**2-2)*np.exp(-2*np.sqrt(-1+0j)*phi1))*5**(1/2)*2**(1/2)*(np.cos(phi)-1)*21**(1/2)*(1+np.cos(phi)))


def wrapped3(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 4 3 1

	"""
	return 1/np.sqrt(2)*(1/192*3**(1/2)*((np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+((1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))+14*np.exp(4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*5**(1/2)+(-1)**4*1/192*3**(1/2)*((np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+((1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))+14*np.exp(-4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*5**(1/2))


def wrapped4(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 6 1 1

	"""
	return 1/np.sqrt(2)*(1/64*(-231*np.cos(phi)**6+483*np.cos(phi)**4-273*np.cos(phi)**2+21)*2**(1/2)*np.cos(4*phi2)+1/64*2**(1/2)*(231*np.cos(phi)**6-315*np.cos(phi)**4+105*np.cos(phi)**2-5)+(-1)**6*1/64*(-231*np.cos(phi)**6+483*np.cos(phi)**4-273*np.cos(phi)**2+21)*2**(1/2)*np.cos(4*phi2)+1/64*2**(1/2)*(231*np.cos(phi)**6-315*np.cos(phi)**4+105*np.cos(phi)**2-5))


def wrapped5(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 6 2 1

	"""
	return 1/np.sqrt(2)*(-33/256*7**(1/2)*2**(1/2)*((np.cos(phi)**2+2/3*np.cos(phi)+1/33)*(np.cos(phi)-1)**2*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**2-2/3*np.cos(phi)+1/33)*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))-2*(np.cos(phi)**4-6/11*np.cos(phi)**2+1/33)*np.exp(2*np.sqrt(-1+0j)*phi1))*(np.cos(phi)-1)*15**(1/2)*(1+np.cos(phi))+(-1)**6*-33/256*7**(1/2)*2**(1/2)*((np.cos(phi)**2+2/3*np.cos(phi)+1/33)*(np.cos(phi)-1)**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**2-2/3*np.cos(phi)+1/33)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))-2*(np.cos(phi)**4-6/11*np.cos(phi)**2+1/33)*np.exp(-2*np.sqrt(-1+0j)*phi1))*(np.cos(phi)-1)*15**(1/2)*(1+np.cos(phi)))


def wrapped6(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 6 3 1

	"""
	return 1/np.sqrt(2)*(33/64*(-1/2*(np.cos(phi)-1)**4*(np.cos(phi)**2+4/3*np.cos(phi)+13/33)*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(-1/2*(1+np.cos(phi))**2*(np.cos(phi)**2-4/3*np.cos(phi)+13/33)*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))+(np.cos(phi)-1)**2*(np.cos(phi)**2-1/11)*np.exp(4*np.sqrt(-1+0j)*phi1)))*7**(1/2)+(-1)**6*33/64*(-1/2*(np.cos(phi)-1)**4*(np.cos(phi)**2+4/3*np.cos(phi)+13/33)*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(-1/2*(1+np.cos(phi))**2*(np.cos(phi)**2-4/3*np.cos(phi)+13/33)*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))+(np.cos(phi)-1)**2*(np.cos(phi)**2-1/11)*np.exp(-4*np.sqrt(-1+0j)*phi1)))*7**(1/2))


def wrapped7(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 6 4 1

	"""
	return 1/np.sqrt(2)*(-1/256*7**(1/2)*((np.cos(phi)-1)**4*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-2*np.exp(6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*33**(1/2)*(1+np.cos(phi))+(-1)**6*-1/256*7**(1/2)*((np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-2*np.exp(-6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*33**(1/2)*(1+np.cos(phi)))


def wrapped8(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 8 1 1

	"""
	return 1/np.sqrt(2)*(455/256*11**(1/2)*3**(1/2)*((np.cos(phi)-1)**2*(1+np.cos(phi))**2*(np.cos(phi)**4-2/5*np.cos(phi)**2+1/65)*np.cos(4*phi2)+1/28*(np.cos(phi)-1)**4*(1+np.cos(phi))**4*np.cos(8*phi2)+99/28*np.cos(phi)**8-33/5*np.cos(phi)**6+99/26*np.cos(phi)**4-9/13*np.cos(phi)**2+1/52)+(-1)**8*455/256*11**(1/2)*3**(1/2)*((np.cos(phi)-1)**2*(1+np.cos(phi))**2*(np.cos(phi)**4-2/5*np.cos(phi)**2+1/65)*np.cos(4*phi2)+1/28*(np.cos(phi)-1)**4*(1+np.cos(phi))**4*np.cos(8*phi2)+99/28*np.cos(phi)**8-33/5*np.cos(phi)**6+99/26*np.cos(phi)**4-9/13*np.cos(phi)**2+1/52))


def wrapped9(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 8 2 1

	"""
	return 1/np.sqrt(2)*(13/3072*5**(1/2)*11**(1/2)*((1+np.cos(phi))**2*(np.cos(phi)-1)**4*np.exp(2*np.sqrt(-1+0j)*(phi1-4*phi2))+28*(np.cos(phi)**4+np.cos(phi)**3-1/7*np.cos(phi)-1/91)*(np.cos(phi)-1)**2*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))+28*(np.cos(phi)**4-np.cos(phi)**3+1/7*np.cos(phi)-1/91)*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))+(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(phi1+4*phi2))+198*(np.cos(phi)**6-np.cos(phi)**4+3/13*np.cos(phi)**2-1/143)*np.exp(2*np.sqrt(-1+0j)*phi1))*3**(1/2)*(np.cos(phi)-1)*7**(1/2)*(1+np.cos(phi))+(-1)**8*13/3072*5**(1/2)*11**(1/2)*((1+np.cos(phi))**2*(np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(phi1-4*phi2))+28*(np.cos(phi)**4+np.cos(phi)**3-1/7*np.cos(phi)-1/91)*(np.cos(phi)-1)**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))+28*(np.cos(phi)**4-np.cos(phi)**3+1/7*np.cos(phi)-1/91)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))+(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(phi1+4*phi2))+198*(np.cos(phi)**6-np.cos(phi)**4+3/13*np.cos(phi)**2-1/143)*np.exp(-2*np.sqrt(-1+0j)*phi1))*3**(1/2)*(np.cos(phi)-1)*7**(1/2)*(1+np.cos(phi)))


def wrapped10(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 8 3 1

	"""
	return 1/np.sqrt(2)*(455/1536*3**(1/2)*2**(1/2)*7**(1/2)*(1/28*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(4*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**4+2*np.cos(phi)**3+6/5*np.cos(phi)**2+6/35*np.cos(phi)-9/455)*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+(1/28*(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(4*np.sqrt(-1+0j)*(phi1+2*phi2))+(1+np.cos(phi))**2*(np.cos(phi)**4-2*np.cos(phi)**3+6/5*np.cos(phi)**2-6/35*np.cos(phi)-9/455)*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))+99/14*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/5*np.cos(phi)**2+1/65)*np.exp(4*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2)+(-1)**8*455/1536*3**(1/2)*2**(1/2)*7**(1/2)*(1/28*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(-4*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**4+2*np.cos(phi)**3+6/5*np.cos(phi)**2+6/35*np.cos(phi)-9/455)*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+(1/28*(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(-4*np.sqrt(-1+0j)*(phi1+2*phi2))+(1+np.cos(phi))**2*(np.cos(phi)**4-2*np.cos(phi)**3+6/5*np.cos(phi)**2-6/35*np.cos(phi)-9/455)*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))+99/14*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/5*np.cos(phi)**2+1/65)*np.exp(-4*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2))


def wrapped11(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 8 4 1

	"""
	return 1/np.sqrt(2)*(5/1024*(np.cos(phi)-1)*(1+np.cos(phi))*13**(1/2)*((np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+28*(np.cos(phi)-1)**4*(np.cos(phi)**2+np.cos(phi)+1/5)*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(28*(np.cos(phi)**2-np.cos(phi)+1/5)*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(3*phi1+4*phi2))+198*(np.cos(phi)**2-1/15)*(np.cos(phi)-1)**2*np.exp(6*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2)+(-1)**8*5/1024*(np.cos(phi)-1)*(1+np.cos(phi))*13**(1/2)*((np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+28*(np.cos(phi)-1)**4*(np.cos(phi)**2+np.cos(phi)+1/5)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(28*(np.cos(phi)**2-np.cos(phi)+1/5)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+4*phi2))+198*(np.cos(phi)**2-1/15)*(np.cos(phi)-1)**2*np.exp(-6*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2))


def wrapped12(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 8 5 1

	"""
	return 1/np.sqrt(2)*(7/3072*3**(1/2)*13**(1/2)*2**(1/2)*5**(1/2)*((1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1-phi2))+(np.cos(phi)-1)**2*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1+phi2))+1/28*(np.cos(phi)-1)**8*np.exp(8*np.sqrt(-1+0j)*(phi1-phi2))+1/28*((1+np.cos(phi))**4*np.exp(8*np.sqrt(-1+0j)*(phi1+phi2))+198*np.exp(8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**4)*(1+np.cos(phi))**4)+(-1)**8*1/12288*(28*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-phi2))+(np.cos(phi)-1)**8*np.exp(-8*np.sqrt(-1+0j)*(phi1-phi2))+((28*np.cos(phi)**4-56*np.cos(phi)**2+28)*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+phi2))+(1+np.cos(phi))**4*np.exp(-8*np.sqrt(-1+0j)*(phi1+phi2))+198*np.exp(-8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**4)*(1+np.cos(phi))**4)*3**(1/2)*13**(1/2)*2**(1/2)*5**(1/2))


def wrapped13(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 9 1 1

	"""
	return 1/np.sqrt(2)*(-1/512*np.sqrt(-1+0j)*17**(1/2)*3**(1/2)*7**(1/2)*1430**(1/2)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.cos(phi)*(np.cos(phi)**4*np.sin(8*phi2)-34*np.cos(phi)**4*np.sin(4*phi2)-2*np.cos(phi)**2*np.sin(8*phi2)+20*np.cos(phi)**2*np.sin(4*phi2)+np.sin(8*phi2)-2*np.sin(4*phi2))+(-1)**9*-1/512*np.sqrt(-1+0j)*17**(1/2)*3**(1/2)*7**(1/2)*1430**(1/2)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.cos(phi)*(np.cos(phi)**4*np.sin(8*phi2)-34*np.cos(phi)**4*np.sin(4*phi2)-2*np.cos(phi)**2*np.sin(8*phi2)+20*np.cos(phi)**2*np.sin(4*phi2)+np.sin(8*phi2)-2*np.sin(4*phi2)))


def wrapped14(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 9 2 1

	"""
	return 1/np.sqrt(2)*(-51/256*7**(1/2)*26**(1/2)*3**(1/2)*(np.cos(phi)-1)*17**(1/2)*(-1/34*(2/9+np.cos(phi))*(np.cos(phi)-1)**4*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(phi1-4*phi2))+(np.cos(phi)**5+10/9*np.cos(phi)**4-10/153*np.cos(phi)**3-5/17*np.cos(phi)**2-5/153*np.cos(phi)+1/153)*(np.cos(phi)-1)**2*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))-((np.cos(phi)**5-10/9*np.cos(phi)**4-10/153*np.cos(phi)**3+5/17*np.cos(phi)**2-5/153*np.cos(phi)-1/153)*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))-1/34*np.exp(2*np.sqrt(-1+0j)*(phi1+4*phi2))*(np.cos(phi)-2/9)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2)*(1+np.cos(phi))**2)*(1+np.cos(phi))+(-1)**9*51/256*7**(1/2)*26**(1/2)*3**(1/2)*(np.cos(phi)-1)*17**(1/2)*(-1/34*(2/9+np.cos(phi))*(np.cos(phi)-1)**4*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-4*phi2))+(np.cos(phi)**5+10/9*np.cos(phi)**4-10/153*np.cos(phi)**3-5/17*np.cos(phi)**2-5/153*np.cos(phi)+1/153)*(np.cos(phi)-1)**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))-((np.cos(phi)**5-10/9*np.cos(phi)**4-10/153*np.cos(phi)**3+5/17*np.cos(phi)**2-5/153*np.cos(phi)-1/153)*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))-1/34*np.exp(-2*np.sqrt(-1+0j)*(phi1+4*phi2))*(np.cos(phi)-2/9)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2)*(1+np.cos(phi))**2)*(1+np.cos(phi)))


def wrapped15(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 9 3 1

	"""
	return 1/np.sqrt(2)*(-21/512*17**(1/2)*3**(1/2)*(-(4/9+np.cos(phi))*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(phi1-2*phi2))+34*(np.cos(phi)**5+20/9*np.cos(phi)**4+230/153*np.cos(phi)**3+10/51*np.cos(phi)**2-5/51*np.cos(phi)-2/119)*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+((-4/9+np.cos(phi))*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(phi1+2*phi2))-34*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))*(np.cos(phi)**5-20/9*np.cos(phi)**4+230/153*np.cos(phi)**3-10/51*np.cos(phi)**2-5/51*np.cos(phi)+2/119))*(1+np.cos(phi))**4)+(-1)**9*21/512*17**(1/2)*3**(1/2)*(-(4/9+np.cos(phi))*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(phi1-2*phi2))+34*(np.cos(phi)**5+20/9*np.cos(phi)**4+230/153*np.cos(phi)**3+10/51*np.cos(phi)**2-5/51*np.cos(phi)-2/119)*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+((-4/9+np.cos(phi))*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+2*phi2))-34*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))*(np.cos(phi)**5-20/9*np.cos(phi)**4+230/153*np.cos(phi)**3-10/51*np.cos(phi)**2-5/51*np.cos(phi)+2/119))*(1+np.cos(phi))**4))


def wrapped16(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 9 4 1

	"""
	return 1/np.sqrt(2)*(51/256*(1/34*(np.cos(phi)+2/3)*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(3*phi1-4*phi2))-(np.cos(phi)**3+4/3*np.cos(phi)**2+23/51*np.cos(phi)+1/51)*(np.cos(phi)-1)**4*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((np.cos(phi)**3-4/3*np.cos(phi)**2+23/51*np.cos(phi)-1/51)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-1/34*(np.cos(phi)-2/3)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+4*phi2))*(1+np.cos(phi))**2)*(1+np.cos(phi))**4)*7**(1/2)*2**(1/2)*(np.cos(phi)-1)*17**(1/2)*(1+np.cos(phi))+(-1)**9*-51/256*(1/34*(np.cos(phi)+2/3)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-4*phi2))-(np.cos(phi)**3+4/3*np.cos(phi)**2+23/51*np.cos(phi)+1/51)*(np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((np.cos(phi)**3-4/3*np.cos(phi)**2+23/51*np.cos(phi)-1/51)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-1/34*(np.cos(phi)-2/3)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+4*phi2))*(1+np.cos(phi))**2)*(1+np.cos(phi))**4)*7**(1/2)*2**(1/2)*(np.cos(phi)-1)*17**(1/2)*(1+np.cos(phi)))


def wrapped17(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 9 5 1

	"""
	return 1/np.sqrt(2)*(-3/1024*7**(1/2)*3**(1/2)*(34*(4/9+np.cos(phi))*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(2*phi1-phi2))-34*(-4/9+np.cos(phi))*(np.cos(phi)-1)**2*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1+phi2))-(np.cos(phi)-1)**8*(np.cos(phi)+8/9)*np.exp(8*np.sqrt(-1+0j)*(phi1-phi2))+(np.cos(phi)-8/9)*(1+np.cos(phi))**8*np.exp(8*np.sqrt(-1+0j)*(phi1+phi2)))+(-1)**9*-51/512*7**(1/2)*3**(1/2)*(-(4/9+np.cos(phi))*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-phi2))+1/34*(np.cos(phi)-1)**8*(np.cos(phi)+8/9)*np.exp(-8*np.sqrt(-1+0j)*(phi1-phi2))+((-4/9+np.cos(phi))*(np.cos(phi)-1)**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+phi2))-1/34*(np.cos(phi)-8/9)*np.exp(-8*np.sqrt(-1+0j)*(phi1+phi2))*(1+np.cos(phi))**2)*(1+np.cos(phi))**6))


def wrapped18(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 1 1

	"""
	return 1/np.sqrt(2)*(-3553/1024*5**(1/2)*((np.cos(phi)**6-15/19*np.cos(phi)**4+45/323*np.cos(phi)**2-1/323)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.cos(4*phi2)+1/12*(np.cos(phi)-1)**4*(np.cos(phi)**2-1/19)*(1+np.cos(phi))**4*np.cos(8*phi2)-13/12*np.cos(phi)**10+195/76*np.cos(phi)**8-1365/646*np.cos(phi)**6+455/646*np.cos(phi)**4-105/1292*np.cos(phi)**2+21/14212)*3**(1/2)*2**(1/2)*13**(1/2)+(-1)**10*-3553/1024*5**(1/2)*((np.cos(phi)**6-15/19*np.cos(phi)**4+45/323*np.cos(phi)**2-1/323)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.cos(4*phi2)+1/12*(np.cos(phi)-1)**4*(np.cos(phi)**2-1/19)*(1+np.cos(phi))**4*np.cos(8*phi2)-13/12*np.cos(phi)**10+195/76*np.cos(phi)**8-1365/646*np.cos(phi)**6+455/646*np.cos(phi)**4-105/1292*np.cos(phi)**2+21/14212)*3**(1/2)*2**(1/2)*13**(1/2))


def wrapped19(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 2 1

	"""
	return 1/np.sqrt(2)*(-4845/2048*13**(1/2)*(1/12*(np.cos(phi)**2+2/5*np.cos(phi)-1/95)*(np.cos(phi)-1)**4*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(phi1-4*phi2))+(np.cos(phi)-1)**2*(np.cos(phi)**6+6/5*np.cos(phi)**5-3/19*np.cos(phi)**4-28/57*np.cos(phi)**3-1/17*np.cos(phi)**2+10/323*np.cos(phi)+13/4845)*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))+(1+np.cos(phi))**2*(np.cos(phi)**6-6/5*np.cos(phi)**5-3/19*np.cos(phi)**4+28/57*np.cos(phi)**3-1/17*np.cos(phi)**2-10/323*np.cos(phi)+13/4845)*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))+1/12*(np.cos(phi)**2-2/5*np.cos(phi)-1/95)*(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(phi1+4*phi2))-13/6*np.exp(2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/19*np.cos(phi)**6+210/323*np.cos(phi)**4-28/323*np.cos(phi)**2+7/4199))*11**(1/2)*(np.cos(phi)-1)*(1+np.cos(phi))+(-1)**10*-4845/2048*13**(1/2)*(1/12*(np.cos(phi)**2+2/5*np.cos(phi)-1/95)*(np.cos(phi)-1)**4*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(phi1-4*phi2))+(np.cos(phi)-1)**2*(np.cos(phi)**6+6/5*np.cos(phi)**5-3/19*np.cos(phi)**4-28/57*np.cos(phi)**3-1/17*np.cos(phi)**2+10/323*np.cos(phi)+13/4845)*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))+(1+np.cos(phi))**2*(np.cos(phi)**6-6/5*np.cos(phi)**5-3/19*np.cos(phi)**4+28/57*np.cos(phi)**3-1/17*np.cos(phi)**2-10/323*np.cos(phi)+13/4845)*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))+1/12*(np.cos(phi)**2-2/5*np.cos(phi)-1/95)*(np.cos(phi)-1)**2*(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(phi1+4*phi2))-13/6*np.exp(-2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/19*np.cos(phi)**6+210/323*np.cos(phi)**4-28/323*np.cos(phi)**2+7/4199))*11**(1/2)*(np.cos(phi)-1)*(1+np.cos(phi)))


def wrapped20(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 3 1

	"""
	return 1/np.sqrt(2)*(-1615/4096*((np.cos(phi)-1)**6*(1+np.cos(phi))**2*(np.cos(phi)**2+4/5*np.cos(phi)+11/95)*np.exp(4*np.sqrt(-1+0j)*(phi1-2*phi2))+12*(np.cos(phi)**6+12/5*np.cos(phi)**5+33/19*np.cos(phi)**4+8/57*np.cos(phi)**3-83/323*np.cos(phi)**2-20/323*np.cos(phi)+1/4845)*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+((np.cos(phi)-1)**2*(1+np.cos(phi))**4*(np.cos(phi)**2-4/5*np.cos(phi)+11/95)*np.exp(4*np.sqrt(-1+0j)*(phi1+2*phi2))+12*(1+np.cos(phi))**2*(np.cos(phi)**6-12/5*np.cos(phi)**5+33/19*np.cos(phi)**4-8/57*np.cos(phi)**3-83/323*np.cos(phi)**2+20/323*np.cos(phi)+1/4845)*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))-26*(np.cos(phi)-1)**2*np.exp(4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**6-15/19*np.cos(phi)**4+45/323*np.cos(phi)**2-1/323))*(1+np.cos(phi))**2)*11**(1/2)+(-1)**10*-1615/4096*((np.cos(phi)-1)**6*(1+np.cos(phi))**2*(np.cos(phi)**2+4/5*np.cos(phi)+11/95)*np.exp(-4*np.sqrt(-1+0j)*(phi1-2*phi2))+12*(np.cos(phi)**6+12/5*np.cos(phi)**5+33/19*np.cos(phi)**4+8/57*np.cos(phi)**3-83/323*np.cos(phi)**2-20/323*np.cos(phi)+1/4845)*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+((np.cos(phi)-1)**2*(1+np.cos(phi))**4*(np.cos(phi)**2-4/5*np.cos(phi)+11/95)*np.exp(-4*np.sqrt(-1+0j)*(phi1+2*phi2))+12*(1+np.cos(phi))**2*(np.cos(phi)**6-12/5*np.cos(phi)**5+33/19*np.cos(phi)**4-8/57*np.cos(phi)**3-83/323*np.cos(phi)**2+20/323*np.cos(phi)+1/4845)*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))-26*(np.cos(phi)-1)**2*np.exp(-4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**6-15/19*np.cos(phi)**4+45/323*np.cos(phi)**2-1/323))*(1+np.cos(phi))**2)*11**(1/2))


def wrapped21(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 4 1

	"""
	return 1/np.sqrt(2)*(-4845/4096*11**(1/2)*(1/12*(np.cos(phi)**2+6/5*np.cos(phi)+31/95)*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+(np.cos(phi)**4+8/5*np.cos(phi)**3+66/95*np.cos(phi)**2+8/285*np.cos(phi)-83/4845)*(np.cos(phi)-1)**4*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((1+np.cos(phi))**2*(np.cos(phi)**4-8/5*np.cos(phi)**3+66/95*np.cos(phi)**2-8/285*np.cos(phi)-83/4845)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+1/12*(1+np.cos(phi))**4*(np.cos(phi)**2-6/5*np.cos(phi)+31/95)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+4*phi2))-13/6*(np.cos(phi)**4-6/19*np.cos(phi)**2+3/323)*np.exp(6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*(1+np.cos(phi))+(-1)**10*-4845/4096*11**(1/2)*(1/12*(np.cos(phi)**2+6/5*np.cos(phi)+31/95)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+(np.cos(phi)**4+8/5*np.cos(phi)**3+66/95*np.cos(phi)**2+8/285*np.cos(phi)-83/4845)*(np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((1+np.cos(phi))**2*(np.cos(phi)**4-8/5*np.cos(phi)**3+66/95*np.cos(phi)**2-8/285*np.cos(phi)-83/4845)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+1/12*(1+np.cos(phi))**4*(np.cos(phi)**2-6/5*np.cos(phi)+31/95)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+4*phi2))-13/6*(np.cos(phi)**4-6/19*np.cos(phi)**2+3/323)*np.exp(-6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*(1+np.cos(phi)))


def wrapped22(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 5 1

	"""
	return 1/np.sqrt(2)*(-95/2048*11**(1/2)*((np.cos(phi)-1)**6*(np.cos(phi)**2+4/5*np.cos(phi)+11/95)*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(2*phi1-phi2))+(np.cos(phi)**2-4/5*np.cos(phi)+11/95)*(np.cos(phi)-1)**2*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1+phi2))+1/12*(np.cos(phi)-1)**8*(np.cos(phi)**2+8/5*np.cos(phi)+59/95)*np.exp(8*np.sqrt(-1+0j)*(phi1-phi2))+1/12*((np.cos(phi)**2-8/5*np.cos(phi)+59/95)*(1+np.cos(phi))**4*np.exp(8*np.sqrt(-1+0j)*(phi1+phi2))-26*(np.cos(phi)-1)**4*(np.cos(phi)**2-1/19)*np.exp(8*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**4)*3**(1/2)*17**(1/2)+(-1)**10*-95/24576*(12*(np.cos(phi)-1)**6*(np.cos(phi)**2+4/5*np.cos(phi)+11/95)*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-phi2))+(np.cos(phi)-1)**8*(np.cos(phi)**2+8/5*np.cos(phi)+59/95)*np.exp(-8*np.sqrt(-1+0j)*(phi1-phi2))+(12*(np.cos(phi)**2-4/5*np.cos(phi)+11/95)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+phi2))+(np.cos(phi)**2-8/5*np.cos(phi)+59/95)*(1+np.cos(phi))**4*np.exp(-8*np.sqrt(-1+0j)*(phi1+phi2))-26*(np.cos(phi)-1)**4*(np.cos(phi)**2-1/19)*np.exp(-8*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**4)*11**(1/2)*3**(1/2)*17**(1/2))


def wrapped23(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 10 6 1

	"""
	return 1/np.sqrt(2)*(13/24576*(-1/26*(np.cos(phi)-1)**8*np.exp(2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+(-6/13*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+(1+np.cos(phi))**2*(-6/13*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(5*phi1+2*phi2))-1/26*(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+np.exp(10*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**4))*(1+np.cos(phi))**2)*3**(1/2)*11**(1/2)*(1+np.cos(phi))*19**(1/2)*2**(1/2)*5**(1/2)*(np.cos(phi)-1)*17**(1/2)+(-1)**10*13/24576*(-1/26*(np.cos(phi)-1)**8*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+(-6/13*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+(1+np.cos(phi))**2*(-6/13*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+2*phi2))-1/26*(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+np.exp(-10*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**4))*(1+np.cos(phi))**2)*3**(1/2)*11**(1/2)*(1+np.cos(phi))*19**(1/2)*2**(1/2)*5**(1/2)*(np.cos(phi)-1)*17**(1/2))


def wrapped24(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 1 1

	"""
	return 1/np.sqrt(2)*(-2028117/209920*41**(1/2)*11**(1/2)*((np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(1+np.cos(phi))**2*(np.cos(phi)-1)**2*np.cos(4*phi2)-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4*np.cos(8*phi2)-3/4*np.cos(phi)**12+99/46*np.cos(phi)**10-1485/644*np.cos(phi)**8+495/437*np.cos(phi)**6-7425/29716*np.cos(phi)**4+297/14858*np.cos(phi)**2-99/386308)+(-1)**12*-2028117/209920*41**(1/2)*11**(1/2)*((np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(1+np.cos(phi))**2*(np.cos(phi)-1)**2*np.cos(4*phi2)-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4*np.cos(8*phi2)-3/4*np.cos(phi)**12+99/46*np.cos(phi)**10-1485/644*np.cos(phi)**8+495/437*np.cos(phi)**6-7425/29716*np.cos(phi)**4+297/14858*np.cos(phi)**2-99/386308))


def wrapped25(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 1 2

	"""
	return 1/np.sqrt(2)*(245157/13434880*7**(1/2)*17**(1/2)*23**(1/2)*3**(1/2)*2**(1/2)*13**(1/2)*(1025/735471*(np.cos(phi)-1)**6*(1+np.cos(phi))**6*np.cos(12*phi2)+(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(1+np.cos(phi))**2*(np.cos(phi)-1)**2*np.cos(4*phi2)+14/969*(1+np.cos(phi))**4*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4*np.cos(8*phi2)+182/99*np.cos(phi)**12+14/22287+4550/7429*np.cos(phi)**4-3640/1311*np.cos(phi)**6+130/23*np.cos(phi)**8-364/69*np.cos(phi)**10-364/7429*np.cos(phi)**2)*19**(1/2)*41**(1/2)+(-1)**12*245157/13434880*7**(1/2)*17**(1/2)*23**(1/2)*3**(1/2)*2**(1/2)*13**(1/2)*(1025/735471*(np.cos(phi)-1)**6*(1+np.cos(phi))**6*np.cos(12*phi2)+(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(1+np.cos(phi))**2*(np.cos(phi)-1)**2*np.cos(4*phi2)+14/969*(1+np.cos(phi))**4*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4*np.cos(8*phi2)+182/99*np.cos(phi)**12+14/22287+4550/7429*np.cos(phi)**4-3640/1311*np.cos(phi)**6+130/23*np.cos(phi)**8-364/69*np.cos(phi)**10-364/7429*np.cos(phi)**2)*19**(1/2)*41**(1/2))


def wrapped26(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 2 1

	"""
	return 1/np.sqrt(2)*(735471/839680*3**(1/2)*13**(1/2)*(1+np.cos(phi))*(np.cos(phi)-1)*2**(1/2)*7**(1/2)*41**(1/2)*(1/6*(1+np.cos(phi))**2*(np.cos(phi)-1)**4*(np.cos(phi)**4+2/3*np.cos(phi)**3-2/23*np.cos(phi)**2-18/253*np.cos(phi)-1/759)*np.exp(2*np.sqrt(-1+0j)*(phi1-4*phi2))-2/3*(np.cos(phi)-1)**2*(np.cos(phi)**8+4/3*np.cos(phi)**7-28/69*np.cos(phi)**6-252/253*np.cos(phi)**5-70/759*np.cos(phi)**4+140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2-100/14421*np.cos(phi)-155/245157)*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))-2/3*(1+np.cos(phi))**2*(np.cos(phi)**8-4/3*np.cos(phi)**7-28/69*np.cos(phi)**6+252/253*np.cos(phi)**5-70/759*np.cos(phi)**4-140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2+100/14421*np.cos(phi)-155/245157)*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))+1/6*(1+np.cos(phi))**4*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/3*np.cos(phi)**3-2/23*np.cos(phi)**2+18/253*np.cos(phi)-1/759)*np.exp(2*np.sqrt(-1+0j)*(phi1+4*phi2))+np.exp(2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**10-45/23*np.cos(phi)**8+30/23*np.cos(phi)**6-150/437*np.cos(phi)**4+225/7429*np.cos(phi)**2-3/7429))+(-1)**12*735471/839680*3**(1/2)*13**(1/2)*(1+np.cos(phi))*(np.cos(phi)-1)*2**(1/2)*7**(1/2)*41**(1/2)*(1/6*(1+np.cos(phi))**2*(np.cos(phi)-1)**4*(np.cos(phi)**4+2/3*np.cos(phi)**3-2/23*np.cos(phi)**2-18/253*np.cos(phi)-1/759)*np.exp(-2*np.sqrt(-1+0j)*(phi1-4*phi2))-2/3*(np.cos(phi)-1)**2*(np.cos(phi)**8+4/3*np.cos(phi)**7-28/69*np.cos(phi)**6-252/253*np.cos(phi)**5-70/759*np.cos(phi)**4+140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2-100/14421*np.cos(phi)-155/245157)*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))-2/3*(1+np.cos(phi))**2*(np.cos(phi)**8-4/3*np.cos(phi)**7-28/69*np.cos(phi)**6+252/253*np.cos(phi)**5-70/759*np.cos(phi)**4-140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2+100/14421*np.cos(phi)-155/245157)*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))+1/6*(1+np.cos(phi))**4*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/3*np.cos(phi)**3-2/23*np.cos(phi)**2+18/253*np.cos(phi)-1/759)*np.exp(-2*np.sqrt(-1+0j)*(phi1+4*phi2))+np.exp(-2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**10-45/23*np.cos(phi)**8+30/23*np.cos(phi)**6-150/437*np.cos(phi)**4+225/7429*np.cos(phi)**2-3/7429)))


def wrapped27(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 2 2

	"""
	return 1/np.sqrt(2)*(676039/3358720*(1025/2704156*(1+np.cos(phi))**4*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(phi1-6*phi2))+33/8398*(1+np.cos(phi))**2*(np.cos(phi)-1)**4*(np.cos(phi)**4+2/3*np.cos(phi)**3-2/23*np.cos(phi)**2-18/253*np.cos(phi)-1/759)*np.exp(2*np.sqrt(-1+0j)*(phi1-4*phi2))+99/364*(np.cos(phi)-1)**2*(np.cos(phi)**8+4/3*np.cos(phi)**7-28/69*np.cos(phi)**6-252/253*np.cos(phi)**5-70/759*np.cos(phi)**4+140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2-100/14421*np.cos(phi)-155/245157)*np.exp(2*np.sqrt(-1+0j)*(phi1-2*phi2))+99/364*(1+np.cos(phi))**2*(np.cos(phi)**8-4/3*np.cos(phi)**7-28/69*np.cos(phi)**6+252/253*np.cos(phi)**5-70/759*np.cos(phi)**4-140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2+100/14421*np.cos(phi)-155/245157)*np.exp(2*np.sqrt(-1+0j)*(phi1+2*phi2))+33/8398*(1+np.cos(phi))**4*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/3*np.cos(phi)**3-2/23*np.cos(phi)**2+18/253*np.cos(phi)-1/759)*np.exp(2*np.sqrt(-1+0j)*(phi1+4*phi2))+1025/2704156*(np.cos(phi)-1)**4*(1+np.cos(phi))**6*np.exp(2*np.sqrt(-1+0j)*(phi1+6*phi2))+np.exp(2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**10-45/23*np.cos(phi)**8+30/23*np.cos(phi)**6-150/437*np.cos(phi)**4+225/7429*np.cos(phi)**2-3/7429))*17**(1/2)*23**(1/2)*(1+np.cos(phi))*(np.cos(phi)-1)*11**(1/2)*19**(1/2)*41**(1/2)+(-1)**12*676039/3358720*(1025/2704156*(1+np.cos(phi))**4*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(phi1-6*phi2))+33/8398*(1+np.cos(phi))**2*(np.cos(phi)-1)**4*(np.cos(phi)**4+2/3*np.cos(phi)**3-2/23*np.cos(phi)**2-18/253*np.cos(phi)-1/759)*np.exp(-2*np.sqrt(-1+0j)*(phi1-4*phi2))+99/364*(np.cos(phi)-1)**2*(np.cos(phi)**8+4/3*np.cos(phi)**7-28/69*np.cos(phi)**6-252/253*np.cos(phi)**5-70/759*np.cos(phi)**4+140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2-100/14421*np.cos(phi)-155/245157)*np.exp(-2*np.sqrt(-1+0j)*(phi1-2*phi2))+99/364*(1+np.cos(phi))**2*(np.cos(phi)**8-4/3*np.cos(phi)**7-28/69*np.cos(phi)**6+252/253*np.cos(phi)**5-70/759*np.cos(phi)**4-140/759*np.cos(phi)**3+140/4807*np.cos(phi)**2+100/14421*np.cos(phi)-155/245157)*np.exp(-2*np.sqrt(-1+0j)*(phi1+2*phi2))+33/8398*(1+np.cos(phi))**4*(np.cos(phi)-1)**2*(np.cos(phi)**4-2/3*np.cos(phi)**3-2/23*np.cos(phi)**2+18/253*np.cos(phi)-1/759)*np.exp(-2*np.sqrt(-1+0j)*(phi1+4*phi2))+1025/2704156*(np.cos(phi)-1)**4*(1+np.cos(phi))**6*np.exp(-2*np.sqrt(-1+0j)*(phi1+6*phi2))+np.exp(-2*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**10-45/23*np.cos(phi)**8+30/23*np.cos(phi)**6-150/437*np.cos(phi)**4+225/7429*np.cos(phi)**2-3/7429))*17**(1/2)*23**(1/2)*(1+np.cos(phi))*(np.cos(phi)-1)*11**(1/2)*19**(1/2)*41**(1/2))


def wrapped28(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 3 1

	"""
	return 1/np.sqrt(2)*(-735471/839680*13**(1/2)*7**(1/2)*41**(1/2)*(-1/4*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(4*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**8+8/3*np.cos(phi)**7+140/69*np.cos(phi)**6-56/253*np.cos(phi)**5-210/253*np.cos(phi)**4-56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2+680/43263*np.cos(phi)+239/735471)*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*np.exp(4*np.sqrt(-1+0j)*(phi1+2*phi2))+(np.cos(phi)**8-8/3*np.cos(phi)**7+140/69*np.cos(phi)**6+56/253*np.cos(phi)**5-210/253*np.cos(phi)**4+56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2-680/43263*np.cos(phi)+239/735471)*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))-3/2*np.exp(4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(np.cos(phi)-1)**2))+(-1)**12*-735471/839680*13**(1/2)*7**(1/2)*41**(1/2)*(-1/4*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(-4*np.sqrt(-1+0j)*(phi1-2*phi2))+(np.cos(phi)**8+8/3*np.cos(phi)**7+140/69*np.cos(phi)**6-56/253*np.cos(phi)**5-210/253*np.cos(phi)**4-56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2+680/43263*np.cos(phi)+239/735471)*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+2*phi2))+(np.cos(phi)**8-8/3*np.cos(phi)**7+140/69*np.cos(phi)**6+56/253*np.cos(phi)**5-210/253*np.cos(phi)**4+56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2-680/43263*np.cos(phi)+239/735471)*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))-3/2*np.exp(-4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(np.cos(phi)-1)**2)))


def wrapped29(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 3 2

	"""
	return 1/np.sqrt(2)*(676039/13434880*(1025/2704156*(1+np.cos(phi))**4*(np.cos(phi)-1)**8*np.exp(4*np.sqrt(-1+0j)*(phi1-3*phi2))+33/8398*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(4*np.sqrt(-1+0j)*(phi1-2*phi2))+99/364*(np.cos(phi)**8+8/3*np.cos(phi)**7+140/69*np.cos(phi)**6-56/253*np.cos(phi)**5-210/253*np.cos(phi)**4-56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2+680/43263*np.cos(phi)+239/735471)*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(33/8398*(1+np.cos(phi))**4*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*np.exp(4*np.sqrt(-1+0j)*(phi1+2*phi2))+1025/2704156*(np.cos(phi)-1)**4*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(phi1+3*phi2))+99/364*(np.cos(phi)**8-8/3*np.cos(phi)**7+140/69*np.cos(phi)**6+56/253*np.cos(phi)**5-210/253*np.cos(phi)**4+56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2-680/43263*np.cos(phi)+239/735471)*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(phi1+phi2))+np.exp(4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(np.cos(phi)-1)**2))*3**(1/2)*17**(1/2)*23**(1/2)*2**(1/2)*11**(1/2)*19**(1/2)*41**(1/2)+(-1)**12*676039/13434880*(1025/2704156*(1+np.cos(phi))**4*(np.cos(phi)-1)**8*np.exp(-4*np.sqrt(-1+0j)*(phi1-3*phi2))+33/8398*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*(np.cos(phi)-1)**6*np.exp(-4*np.sqrt(-1+0j)*(phi1-2*phi2))+99/364*(np.cos(phi)**8+8/3*np.cos(phi)**7+140/69*np.cos(phi)**6-56/253*np.cos(phi)**5-210/253*np.cos(phi)**4-56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2+680/43263*np.cos(phi)+239/735471)*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**2*(33/8398*(1+np.cos(phi))**4*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+2*phi2))+1025/2704156*(np.cos(phi)-1)**4*(1+np.cos(phi))**6*np.exp(-4*np.sqrt(-1+0j)*(phi1+3*phi2))+99/364*(np.cos(phi)**8-8/3*np.cos(phi)**7+140/69*np.cos(phi)**6+56/253*np.cos(phi)**5-210/253*np.cos(phi)**4+56/253*np.cos(phi)**3+196/4807*np.cos(phi)**2-680/43263*np.cos(phi)+239/735471)*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(phi1+phi2))+np.exp(-4*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**8-28/23*np.cos(phi)**6+10/23*np.cos(phi)**4-20/437*np.cos(phi)**2+5/7429)*(np.cos(phi)-1)**2))*3**(1/2)*17**(1/2)*23**(1/2)*2**(1/2)*11**(1/2)*19**(1/2)*41**(1/2))


def wrapped30(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 4 1

	"""
	return 1/np.sqrt(2)*(-100947/419840*17**(1/2)*(-1/4*(np.cos(phi)**4+2*np.cos(phi)**3+30/23*np.cos(phi)**2+74/253*np.cos(phi)+19/1771)*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+(np.cos(phi)-1)**4*(np.cos(phi)**6+2*np.cos(phi)**5+25/23*np.cos(phi)**4-20/253*np.cos(phi)**3-45/253*np.cos(phi)**2-6/253*np.cos(phi)+7/4807)*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**2*((np.cos(phi)**6-2*np.cos(phi)**5+25/23*np.cos(phi)**4+20/253*np.cos(phi)**3-45/253*np.cos(phi)**2+6/253*np.cos(phi)+7/4807)*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-2*np.cos(phi)**3+30/23*np.cos(phi)**2-74/253*np.cos(phi)+19/1771)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+4*phi2))-3/2*(np.cos(phi)-1)**2*np.exp(6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**6-15/23*np.cos(phi)**4+15/161*np.cos(phi)**2-5/3059)))*13**(1/2)*(np.cos(phi)-1)*41**(1/2)*(1+np.cos(phi))+(-1)**12*-100947/419840*(-1/4*(np.cos(phi)**4+2*np.cos(phi)**3+30/23*np.cos(phi)**2+74/253*np.cos(phi)+19/1771)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+(np.cos(phi)**6+2*np.cos(phi)**5+25/23*np.cos(phi)**4-20/253*np.cos(phi)**3-45/253*np.cos(phi)**2-6/253*np.cos(phi)+7/4807)*(np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+((np.cos(phi)**6-2*np.cos(phi)**5+25/23*np.cos(phi)**4+20/253*np.cos(phi)**3-45/253*np.cos(phi)**2+6/253*np.cos(phi)+7/4807)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))-1/4*(1+np.cos(phi))**4*(np.cos(phi)**4-2*np.cos(phi)**3+30/23*np.cos(phi)**2-74/253*np.cos(phi)+19/1771)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+4*phi2))-3/2*(np.cos(phi)**6-15/23*np.cos(phi)**4+15/161*np.cos(phi)**2-5/3059)*(np.cos(phi)-1)**2*np.exp(-6*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2)*17**(1/2)*13**(1/2)*(np.cos(phi)-1)*41**(1/2)*(1+np.cos(phi)))


def wrapped31(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 4 2

	"""
	return 1/np.sqrt(2)*(676039/20152320*3**(1/2)*11**(1/2)*(1+np.cos(phi))*23**(1/2)*(33/8398*(np.cos(phi)**4+2*np.cos(phi)**3+30/23*np.cos(phi)**2+74/253*np.cos(phi)+19/1771)*(np.cos(phi)-1)**6*np.exp(2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+99/364*(np.cos(phi)-1)**4*(np.cos(phi)**6+2*np.cos(phi)**5+25/23*np.cos(phi)**4-20/253*np.cos(phi)**3-45/253*np.cos(phi)**2-6/253*np.cos(phi)+7/4807)*np.exp(2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**2*(99/364*(np.cos(phi)**6-2*np.cos(phi)**5+25/23*np.cos(phi)**4+20/253*np.cos(phi)**3-45/253*np.cos(phi)**2+6/253*np.cos(phi)+7/4807)*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+33/8398*(1+np.cos(phi))**4*(np.cos(phi)**4-2*np.cos(phi)**3+30/23*np.cos(phi)**2-74/253*np.cos(phi)+19/1771)*np.exp(2*np.sqrt(-1+0j)*(3*phi1+4*phi2))+(np.cos(phi)-1)**2*(1025/2704156*(np.cos(phi)-1)**6*np.exp(6*np.sqrt(-1+0j)*(phi1-2*phi2))+1025/2704156*(1+np.cos(phi))**6*np.exp(6*np.sqrt(-1+0j)*(phi1+2*phi2))+np.exp(6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**6-15/23*np.cos(phi)**4+15/161*np.cos(phi)**2-5/3059))))*2**(1/2)*(np.cos(phi)-1)*7**(1/2)*19**(1/2)*41**(1/2)+(-1)**12*676039/20152320*3**(1/2)*11**(1/2)*(1+np.cos(phi))*23**(1/2)*2**(1/2)*(np.cos(phi)-1)*(33/8398*(np.cos(phi)**4+2*np.cos(phi)**3+30/23*np.cos(phi)**2+74/253*np.cos(phi)+19/1771)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-4*phi2))+99/364*(np.cos(phi)**6+2*np.cos(phi)**5+25/23*np.cos(phi)**4-20/253*np.cos(phi)**3-45/253*np.cos(phi)**2-6/253*np.cos(phi)+7/4807)*(np.cos(phi)-1)**4*np.exp(-2*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**2*(99/364*(np.cos(phi)**6-2*np.cos(phi)**5+25/23*np.cos(phi)**4+20/253*np.cos(phi)**3-45/253*np.cos(phi)**2+6/253*np.cos(phi)+7/4807)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+2*phi2))+33/8398*(1+np.cos(phi))**4*(np.cos(phi)**4-2*np.cos(phi)**3+30/23*np.cos(phi)**2-74/253*np.cos(phi)+19/1771)*np.exp(-2*np.sqrt(-1+0j)*(3*phi1+4*phi2))+(1025/2704156*(np.cos(phi)-1)**6*np.exp(-6*np.sqrt(-1+0j)*(phi1-2*phi2))+1025/2704156*(1+np.cos(phi))**6*np.exp(-6*np.sqrt(-1+0j)*(phi1+2*phi2))+np.exp(-6*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**6-15/23*np.cos(phi)**4+15/161*np.cos(phi)**2-5/3059))*(np.cos(phi)-1)**2))*7**(1/2)*19**(1/2)*41**(1/2))


def wrapped32(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 5 1

	"""
	return 1/np.sqrt(2)*(15939/1679360*(-2/3*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(2*phi1-phi2))-2/3*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1+phi2))+1/6*(np.cos(phi)**4+8/3*np.cos(phi)**3+58/23*np.cos(phi)**2+248/253*np.cos(phi)+673/5313)*(np.cos(phi)-1)**8*np.exp(8*np.sqrt(-1+0j)*(phi1-phi2))+(1+np.cos(phi))**4*(1/6*(np.cos(phi)**4-8/3*np.cos(phi)**3+58/23*np.cos(phi)**2-248/253*np.cos(phi)+673/5313)*(1+np.cos(phi))**4*np.exp(8*np.sqrt(-1+0j)*(phi1+phi2))+np.exp(8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4))*3**(1/2)*17**(1/2)*41**(1/2)*2**(1/2)*13**(1/2)*19**(1/2)+(-1)**12*15939/1679360*3**(1/2)*17**(1/2)*41**(1/2)*2**(1/2)*13**(1/2)*19**(1/2)*(-2/3*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-phi2))+1/6*(np.cos(phi)**4+8/3*np.cos(phi)**3+58/23*np.cos(phi)**2+248/253*np.cos(phi)+673/5313)*(np.cos(phi)-1)**8*np.exp(-8*np.sqrt(-1+0j)*(phi1-phi2))+(-2/3*(np.cos(phi)-1)**2*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+phi2))+1/6*(np.cos(phi)**4-8/3*np.cos(phi)**3+58/23*np.cos(phi)**2-248/253*np.cos(phi)+673/5313)*(1+np.cos(phi))**4*np.exp(-8*np.sqrt(-1+0j)*(phi1+phi2))+np.exp(-8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4)*(1+np.cos(phi))**4))


def wrapped33(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 5 2

	"""
	return 1/np.sqrt(2)*(5/131072*11**(1/2)*41**(1/2)*((1+np.cos(phi))**2*(np.cos(phi)-1)**10*np.exp(4*np.sqrt(-1+0j)*(2*phi1-3*phi2))+735471/1025*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(2*phi1-phi2))+(np.cos(phi)-1)**2*(1+np.cos(phi))**10*np.exp(4*np.sqrt(-1+0j)*(2*phi1+3*phi2))+735471/1025*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(np.cos(phi)-1)**2*(1+np.cos(phi))**6*np.exp(4*np.sqrt(-1+0j)*(2*phi1+phi2))+10626/1025*(np.cos(phi)**4+8/3*np.cos(phi)**3+58/23*np.cos(phi)**2+248/253*np.cos(phi)+673/5313)*(np.cos(phi)-1)**8*np.exp(8*np.sqrt(-1+0j)*(phi1-phi2))+10626/1025*((np.cos(phi)**4-8/3*np.cos(phi)**3+58/23*np.cos(phi)**2-248/253*np.cos(phi)+673/5313)*(1+np.cos(phi))**4*np.exp(8*np.sqrt(-1+0j)*(phi1+phi2))+8398/33*np.exp(8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4)*(1+np.cos(phi))**4)*7**(1/2)*23**(1/2)+(-1)**12*5313/13434880*(1025/10626*(1+np.cos(phi))**2*(np.cos(phi)-1)**10*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-3*phi2))+969/14*(np.cos(phi)-1)**6*(1+np.cos(phi))**2*(np.cos(phi)**4+4/3*np.cos(phi)**3+10/23*np.cos(phi)**2-4/253*np.cos(phi)-3/253)*np.exp(-4*np.sqrt(-1+0j)*(2*phi1-phi2))+1025/10626*(np.cos(phi)-1)**2*(1+np.cos(phi))**10*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+3*phi2))+(np.cos(phi)**4+8/3*np.cos(phi)**3+58/23*np.cos(phi)**2+248/253*np.cos(phi)+673/5313)*(np.cos(phi)-1)**8*np.exp(-8*np.sqrt(-1+0j)*(phi1-phi2))+(969/14*(np.cos(phi)-1)**2*(np.cos(phi)**4-4/3*np.cos(phi)**3+10/23*np.cos(phi)**2+4/253*np.cos(phi)-3/253)*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(2*phi1+phi2))+(np.cos(phi)**4-8/3*np.cos(phi)**3+58/23*np.cos(phi)**2-248/253*np.cos(phi)+673/5313)*(1+np.cos(phi))**4*np.exp(-8*np.sqrt(-1+0j)*(phi1+phi2))+8398/33*np.exp(-8*np.sqrt(-1+0j)*phi1)*(np.cos(phi)**4-6/23*np.cos(phi)**2+1/161)*(np.cos(phi)-1)**4)*(1+np.cos(phi))**4)*11**(1/2)*41**(1/2)*7**(1/2)*23**(1/2))


def wrapped34(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 6 1

	"""
	return 1/np.sqrt(2)*(207/839680*7**(1/2)*13**(1/2)*(1+np.cos(phi))*19**(1/2)*3**(1/2)*(np.cos(phi)-1)*11**(1/2)*(1/6*(np.cos(phi)**2+4/3*np.cos(phi)+29/69)*(np.cos(phi)-1)**8*np.exp(2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+(-2/3*(np.cos(phi)-1)**6*(np.cos(phi)**2+2/3*np.cos(phi)+5/69)*np.exp(2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+(1+np.cos(phi))**2*(-2/3*(np.cos(phi)**2-2/3*np.cos(phi)+5/69)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(5*phi1+2*phi2))+1/6*(np.cos(phi)**2-4/3*np.cos(phi)+29/69)*(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+(np.cos(phi)**2-1/23)*(np.cos(phi)-1)**4*np.exp(10*np.sqrt(-1+0j)*phi1)))*(1+np.cos(phi))**2)*17**(1/2)*41**(1/2)+(-1)**12*207/839680*7**(1/2)*(1/6*(np.cos(phi)**2+4/3*np.cos(phi)+29/69)*(np.cos(phi)-1)**8*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+(1+np.cos(phi))**2*(-2/3*(np.cos(phi)**2+2/3*np.cos(phi)+5/69)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+(-2/3*(np.cos(phi)-1)**2*(np.cos(phi)**2-2/3*np.cos(phi)+5/69)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+2*phi2))+1/6*(np.cos(phi)**2-4/3*np.cos(phi)+29/69)*(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+(np.cos(phi)-1)**4*(np.cos(phi)**2-1/23)*np.exp(-10*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2))*13**(1/2)*(1+np.cos(phi))*19**(1/2)*3**(1/2)*(np.cos(phi)-1)*11**(1/2)*17**(1/2)*41**(1/2))


def wrapped35(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 6 2

	"""
	return 1/np.sqrt(2)*(5313/13434880*23**(1/2)*(1025/10626*(np.cos(phi)-1)**10*np.exp(2*np.sqrt(-1+0j)*(5*phi1-6*phi2))+(np.cos(phi)**2+4/3*np.cos(phi)+29/69)*(np.cos(phi)-1)**8*np.exp(2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+969/14*((np.cos(phi)-1)**6*(np.cos(phi)**2+2/3*np.cos(phi)+5/69)*np.exp(2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+((np.cos(phi)**2-2/3*np.cos(phi)+5/69)*(np.cos(phi)-1)**2*(1+np.cos(phi))**2*np.exp(2*np.sqrt(-1+0j)*(5*phi1+2*phi2))+14/969*(np.cos(phi)**2-4/3*np.cos(phi)+29/69)*(1+np.cos(phi))**4*np.exp(2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+1025/735471*(1+np.cos(phi))**6*np.exp(2*np.sqrt(-1+0j)*(5*phi1+6*phi2))+364/99*(np.cos(phi)**2-1/23)*(np.cos(phi)-1)**4*np.exp(10*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*41**(1/2)*(1+np.cos(phi))+(-1)**12*5313/13434880*23**(1/2)*(1025/10626*(np.cos(phi)-1)**10*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-6*phi2))+(np.cos(phi)**2+4/3*np.cos(phi)+29/69)*(np.cos(phi)-1)**8*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-4*phi2))+969/14*((np.cos(phi)**2+2/3*np.cos(phi)+5/69)*(np.cos(phi)-1)**6*np.exp(-2*np.sqrt(-1+0j)*(5*phi1-2*phi2))+((np.cos(phi)-1)**2*(np.cos(phi)**2-2/3*np.cos(phi)+5/69)*(1+np.cos(phi))**2*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+2*phi2))+14/969*(np.cos(phi)**2-4/3*np.cos(phi)+29/69)*(1+np.cos(phi))**4*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+4*phi2))+1025/735471*(1+np.cos(phi))**6*np.exp(-2*np.sqrt(-1+0j)*(5*phi1+6*phi2))+364/99*(np.cos(phi)-1)**4*(np.cos(phi)**2-1/23)*np.exp(-10*np.sqrt(-1+0j)*phi1))*(1+np.cos(phi))**2)*(1+np.cos(phi))**2)*2**(1/2)*(np.cos(phi)-1)*41**(1/2)*(1+np.cos(phi)))


def wrapped36(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 7 1

	"""
	return 1/np.sqrt(2)*(9/1679360*(1/6*(np.cos(phi)-1)**8*np.exp(4*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**2*(-2/3*(np.cos(phi)-1)**6*np.exp(4*np.sqrt(-1+0j)*(3*phi1-phi2))+(1+np.cos(phi))**2*(1/6*(1+np.cos(phi))**4*np.exp(4*np.sqrt(-1+0j)*(3*phi1+2*phi2))+(np.cos(phi)-1)**2*(-2/3*(1+np.cos(phi))**2*np.exp(4*np.sqrt(-1+0j)*(3*phi1+phi2))+np.exp(12*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2))))*11**(1/2)*17**(1/2)*(1+np.cos(phi))**2*23**(1/2)*7**(1/2)*(np.cos(phi)-1)**2*13**(1/2)*19**(1/2)*41**(1/2)+(-1)**12*9/1679360*11**(1/2)*17**(1/2)*(1+np.cos(phi))**2*23**(1/2)*(1/6*(np.cos(phi)-1)**8*np.exp(-4*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(-2/3*(np.cos(phi)-1)**6*np.exp(-4*np.sqrt(-1+0j)*(3*phi1-phi2))+(1/6*(1+np.cos(phi))**4*np.exp(-4*np.sqrt(-1+0j)*(3*phi1+2*phi2))+(np.cos(phi)-1)**2*(-2/3*(1+np.cos(phi))**2*np.exp(-4*np.sqrt(-1+0j)*(3*phi1+phi2))+np.exp(-12*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**2))*(1+np.cos(phi))**2)*(1+np.cos(phi))**2)*7**(1/2)*(np.cos(phi)-1)**2*13**(1/2)*19**(1/2)*41**(1/2))


def wrapped37(phi1, phi, phi2):
	"""
	Method for the Cubic Orthorhombic GSH function corresponding to the index set: 12 7 2

	"""
	return 1/np.sqrt(2)*(245157/53739520*3**(1/2)*(14/969*(1+np.cos(phi))**2*(np.cos(phi)-1)**10*np.exp(4*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**4*(np.cos(phi)-1)**8*np.exp(4*np.sqrt(-1+0j)*(3*phi1-phi2))+14/969*(np.cos(phi)-1)**2*(1+np.cos(phi))**10*np.exp(4*np.sqrt(-1+0j)*(3*phi1+2*phi2))+1025/735471*(np.cos(phi)-1)**12*np.exp(12*np.sqrt(-1+0j)*(phi1-phi2))+((1+np.cos(phi))**2*(np.cos(phi)-1)**4*np.exp(4*np.sqrt(-1+0j)*(3*phi1+phi2))+1025/735471*(1+np.cos(phi))**6*np.exp(12*np.sqrt(-1+0j)*(phi1+phi2))+364/99*np.exp(12*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**6)*(1+np.cos(phi))**6)*2**(1/2)*41**(1/2)+(-1)**12*245157/53739520*3**(1/2)*(14/969*(1+np.cos(phi))**2*(np.cos(phi)-1)**10*np.exp(-4*np.sqrt(-1+0j)*(3*phi1-2*phi2))+(1+np.cos(phi))**4*(np.cos(phi)-1)**8*np.exp(-4*np.sqrt(-1+0j)*(3*phi1-phi2))+14/969*(np.cos(phi)-1)**2*(1+np.cos(phi))**10*np.exp(-4*np.sqrt(-1+0j)*(3*phi1+2*phi2))+1025/735471*(np.cos(phi)-1)**12*np.exp(-12*np.sqrt(-1+0j)*(phi1-phi2))+((1+np.cos(phi))**2*(np.cos(phi)-1)**4*np.exp(-4*np.sqrt(-1+0j)*(3*phi1+phi2))+1025/735471*(1+np.cos(phi))**6*np.exp(-12*np.sqrt(-1+0j)*(phi1+phi2))+364/99*np.exp(-12*np.sqrt(-1+0j)*phi1)*(np.cos(phi)-1)**6)*(1+np.cos(phi))**6)*2**(1/2)*41**(1/2))


def governor():
	"""
	Method that returns all other methods in this file as well as the indexes that they correspond to.
	"""
	funcs = [wrapped0, wrapped1, wrapped2, wrapped3, wrapped4, wrapped5, wrapped6, wrapped7, wrapped8, wrapped9, wrapped10, wrapped11, wrapped12, wrapped13, wrapped14, wrapped15, wrapped16, wrapped17, wrapped18, wrapped19, wrapped20, wrapped21, wrapped22, wrapped23, wrapped24, wrapped25, wrapped26, wrapped27, wrapped28, wrapped29, wrapped30, wrapped31, wrapped32, wrapped33, wrapped34, wrapped35, wrapped36, wrapped37]
	indx = [[0, 1, 1], [4, 1, 1], [4, 2, 1], [4, 3, 1], [6, 1, 1], [6, 2, 1], [6, 3, 1], [6, 4, 1], [8, 1, 1], [8, 2, 1], [8, 3, 1], [8, 4, 1], [8, 5, 1], [9, 1, 1], [9, 2, 1], [9, 3, 1], [9, 4, 1], [9, 5, 1], [10, 1, 1], [10, 2, 1], [10, 3, 1], [10, 4, 1], [10, 5, 1], [10, 6, 1], [12, 1, 1], [12, 1, 2], [12, 2, 1], [12, 2, 2], [12, 3, 1], [12, 3, 2], [12, 4, 1], [12, 4, 2], [12, 5, 1], [12, 5, 2], [12, 6, 1], [12, 6, 2], [12, 7, 1], [12, 7, 2]]
	return funcs, indx

