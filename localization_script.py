# localization get some points
import fydp_common
from time import sleep,time
from math import cos,sin,pi

dimensions_file = open("arm_dimensions.txt",'r')
r=dimensions_file.read().split()
r1=float(r[0])
r2=float(r[1])
r3=float(r[2])
r4x=float(r[3])
r4y=float(r[4])
r4z=float(r[5])
dimensions_file.close()

ct_file = open("ct_coordinates (2).txt",'r')	# get the chosen CT coordinates from mark's software
num_points = int(ct_file.readline().split()[0])
print "Locate " + str(num_points) + " points"
abs_file = open("abs_coordinates.txt", 'w')		# store the absolute coordinates here

for i in range(num_points):
	raw_input("Locate " + ct_file.readline().split()[0])
	theta_1, theta_2, theta_3, theta_4 = fydp_common.arduino.getAngles()	# read angles from the arduino once the tip is fixed

	#convert gantry [[0],[0],[0]] to absolute
	gToAP = [[r4x],[-r4y],[-r4z],[1]] # tip of drill to translate to first joint; gantry to absolute
	gToA1 = [[1,0,0,0],[0,cos(-theta_4),-sin(-theta_4),-r3],[0,sin(-theta_4),cos(-theta_4),0],[0,0,0,1]]
	gToA2 = [[cos(-theta_3),0,sin(-theta_3),0],[0,1,0,-r2],[-sin(-theta_3),0,cos(-theta_3),0],[0,0,0,1]]
	gToA3 = [[1,0,0,0],[0,cos(-theta_2),-sin(-theta_2),-r1],[0,sin(-theta_2),cos(-theta_2),0],[0,0,0,1]]
	gToA4 = [[cos(-theta_1),-sin(-theta_1),0,0],[sin(-theta_1),cos(-theta_1),0,0],[0,0,1,0],[0,0,0,1]]
	
	#using the angles, generate a rotation matrix to find the absolute point

	gToAF = fydp_common.makeRotMatrix(gToA4,gToA3,gToA2,gToA1)
	absolute_point = fydp_common.matrixmult(gToAF,gToAP)

	print absolute_point

	abs_file.write(str(absolute_point[0][0])+' '+str(absolute_point[1][0])+' '+str(absolute_point[2][0])+'\n')
	# write absolute point to file
	
print "done!"
abs_file.close()
ct_file.close()