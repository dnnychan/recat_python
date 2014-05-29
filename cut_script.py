# use cut path and send to arduino
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

cut_path_file = open("CutPathJONN.txt",'r')
matrix_file = open("tf_matrix.txt",'r')
gantry_file = open("gantry_coordinates.txt", 'w')

# read transformation matrix
CT_to_abs_matrix= [[],[],[],[]]
for idx, lines in enumerate(matrix_file):
	this_line = lines.split()
	CT_to_abs_matrix[idx]=[float(this_line[0]),float(this_line[1]),float(this_line[2]),float(this_line[3])]

matrix_file.close()

fydp_common.arduino.stepSpeed(5)
fydp_common.arduino.sendPoint(0,0,0)
#fydp_common.arduino.stepSpeed(50)
raw_input("move the thing")

theta_1, theta_2, theta_3, theta_4 = fydp_common.arduino.getAngles()
#theta_3=0
raw_input("angles")
started_to_cut = 0

# convert stuff from absolute coordinates to gantry coordinates
aToG1 = [[cos(theta_1),-sin(theta_1),0,0],[sin(theta_1),cos(theta_1),0,r1],[0,0,1,0],[0,0,0,1]]
aToG2 = [[1,0,0,0],[0,cos(theta_2),-sin(theta_2),r2],[0,sin(theta_2),cos(theta_2),0],[0,0,0,1]]
aToG3 = [[cos(theta_3),0,sin(theta_3),0],[0,1,0,r3],[-sin(theta_3),0,cos(theta_3),0],[0,0,0,1]]
aToG4 = [[1,0,0,-r4x],[0,cos(theta_4),-sin(theta_4),r4y],[0,sin(theta_4),cos(theta_4),r4z],[0,0,0,1]]

aToGF = fydp_common.makeRotMatrix(aToG4,aToG3,aToG2,aToG1)

#fydp_common.arduino.bldcSpeed(1300)

points_sent = 0
for line in cut_path_file:
	points = line.split(' to ')
	p0=points[0].split()
	p1=points[1].split()
	abs_p0 = fydp_common.matrixmult(CT_to_abs_matrix,[[float(p0[0])],[float(p0[1])],[float(p0[2])],[1]])
	abs_p1 = fydp_common.matrixmult(CT_to_abs_matrix,[[float(p1[0])],[float(p1[1])],[float(p1[2])],[1]])

	gantry_p0 = fydp_common.matrixmult(aToGF,abs_p0)
	gantry_p1 = fydp_common.matrixmult(aToGF,abs_p1)
	#print abs_p0
	print gantry_p0
	print gantry_p1
	gantry_file.write(str(gantry_p0[0][0])+' '+str(gantry_p0[1][0])+' '+str(gantry_p0[2][0])+' to ')
	gantry_file.write(str(gantry_p1[0][0])+' '+str(gantry_p1[1][0])+' '+str(gantry_p1[2][0])+'\n')

	
	fydp_common.arduino.sendPoint(gantry_p0[0][0],gantry_p0[1][0],gantry_p0[2][0])
	fydp_common.arduino.sendPoint(gantry_p1[0][0],gantry_p1[1][0],gantry_p1[2][0])
	
	points_sent = points_sent + 2
	if points_sent > 100:
		if (started_to_cut == 0):
			raw_input("start the drill")
			fydp_common.arduino.bldcSpeed(1200)
			fydp_common.arduino.stepSpeed(15)
			started_to_cut = 1
		print '\nlast CT point ' + points[0] + ' to ' + points[1]
		fydp_common.arduino.waitForQueue()
		points_sent = 0

cut_path_file.close()
gantry_file.close()

fydp_common.arduino.waitForQueue()
print "it's done??"
fydp_common.arduino.turnOff()