# sends a bunch of commands to UART port
import serial
from math import cos,sin,pi
from time import sleep,time

ser = serial.Serial('/dev/tty.usbserial-AH00PEC5')
ser.readline() 		# get startup message
print ser.name
ser.write('clear\n')
ser.readline()		# stupid arduino echos what you send

# Draw a circle
#ser.write('goto 10.00 10.00 020.00\n')
#for theta in range(0,628,5):
#	ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(10.00+5*cos(theta/100.0),10.00+5*sin(theta/100.0),20))

# Queue capacity test
# ser.write('goto 00.00 10.00 020.00\n')
# for i in range(0,200,1):		# 250 crashes my computer, I assume it's because the Arduino is full.
# 	ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(i*2.0/100,10,20))
# 	sleep(.01)


# multiple circles test
# r = 1;
# is_ready = 0
# ser.write('goto 05.00 05.00 010.00\n')
# ser.readline()
# sleep(5)
# ser.write('on\n')
# ser.readline()
# for z in range(1,10,1):
# 	print z
# 	for theta in range(0,628,5):
# 		ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(05.00+r*cos(theta/100.0),05.00+r*sin(theta/100.0),10+z))
# 		ser.readline()
# 		sleep(0.01) # sanity
# 	ser.write('qEmp\n')
# 	ser.readline()
# 	is_ready = ser.readline()
# 	#print is_ready
# 	while (is_ready == '0\n'):	#wait for previous set of points to be processed before sending next batch
# 		ser.write('qEmp\n')
# 		ser.readline()
# 		is_ready = ser.readline()
# 		#print is_ready
# 		sleep(1)
# 		
# ser.write('off\n')

# point tracking test
def matrixmult (A, B):
	# Create the result matrix
	# Dimensions would be rows_A x cols_B
	C = [[0 for row in range(len(B[0]))] for col in range(len(A))]

	for i in range(len(A)):
			for j in range(len(B[0])):
					for k in range(len(A[0])):
							C[i][j] += A[i][k]*B[k][j]
	return C

def getAngles ():
	ser.write('gAng\n')
	ser.readline()
	response = ser.readline()
	thetas=response.split()

	print response

	theta_1 = float(thetas[0])*pi/180
	theta_2 = float(thetas[1])*pi/180
	theta_3 = -float(thetas[2])*pi/180
	theta_4 = float(thetas[3])*pi/180
	
	return (theta_1,theta_2,theta_3,theta_4)
	
def sendPoint (x, y, z):
	ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(x,y,z))
	ser.readline()

r1=-32.5
r2=-62.5
r3=-15
r4x=-12.98
r4y=-(75.22+33)
r4z=-65.5

theta_1, theta_2, theta_3, theta_4 = getAngles()
"""
#convert gantry [[0],[0],[0]] to absolute
gToAP = [[r4x],[-r4y],[-r4z],[1]] # tip of drill to translate to first joint
gToA1 = [[1,0,0,0],[0,cos(-theta_4),-sin(-theta_4),-r3],[0,sin(-theta_4),cos(-theta_4),0],[0,0,0,1]]
gToA2 = [[cos(-theta_3),0,sin(-theta_3),0],[0,1,0,-r2],[-sin(-theta_3),0,cos(-theta_3),0],[0,0,0,1]]
gToA3 = [[1,0,0,0],[0,cos(-theta_2),-sin(-theta_2),-r1],[0,sin(-theta_2),cos(-theta_2),0],[0,0,0,1]]
gToA4 = [[cos(-theta_1),-sin(-theta_1),0,0],[sin(-theta_1),cos(-theta_1),0,0],[0,0,1,0],[0,0,0,1]]

gToAF = matrixmult(gToA4,matrixmult(gToA3,matrixmult(gToA2,gToA1)))
absolute_point = matrixmult(gToAF,gToAP)
print absolute_point
"""

# raw_input("adjust the arm")
# 
# theta_1, theta_2, theta_3, theta_4 = getAngles()

#CT_to_abs_trans = [-67.8094, 213.6525, 136.5743]
#CT_to_abs_TF = [[0.9900,-0.1287,0.0579,CT_to_abs_trans[0]],[-0.1308,-0.9908,-0.0345,CT_to_abs_trans[1]],[0.0529,-0.0417,-0.9977,CT_to_abs_trans[2]],[0,0,0,1]]
CT_to_abs_TF = [[0.9930,0.0423,0.1099,-107.3036],[0.0396,-0.9989,-0.0267,214.3965],[0.1109,-0.0222,-0.9936,119.5928],[0,0,0,1]]
 
#CT_point = [[90,110.9375,135.625],[42.5,67.5,53.75],[124.6875,115.3125,102.8125],[1]]
CT_point = [[90,91.25,135.625],[42.5,15,53.75],[124.6875,115.3125,102.8125],[1]]

for i in range(2):
	destination_point = [[CT_point[0][i]],[CT_point[1][i]],[CT_point[2][i]],[1]]
	absolute_point = matrixmult(CT_to_abs_TF,destination_point)
	print absolute_point

	# convert stuff from absolute coordinates to gantry coordinates
	aToG1 = [[cos(theta_1),-sin(theta_1),0,0],[sin(theta_1),cos(theta_1),0,r1],[0,0,1,0],[0,0,0,1]]
	aToG2 = [[1,0,0,0],[0,cos(theta_2),-sin(theta_2),r2],[0,sin(theta_2),cos(theta_2),0],[0,0,0,1]]
	aToG3 = [[cos(theta_3),0,sin(theta_3),0],[0,1,0,r3],[-sin(theta_3),0,cos(theta_3),0],[0,0,0,1]]
	aToG4 = [[1,0,0,-r4x],[0,cos(theta_4),-sin(theta_4),r4y],[0,sin(theta_4),cos(theta_4),r4z],[0,0,0,1]]

	aToG=matrixmult(aToG4,matrixmult(aToG3,matrixmult(aToG2,aToG1)))
	gantry_point=matrixmult(aToG,absolute_point)
	print gantry_point
	sendPoint(gantry_point[0][0],gantry_point[1][0],gantry_point[2][0])
	sendPoint(gantry_point[0][0],gantry_point[1][0],1)
	print '\n'

# for theta in range(0,628,5):
# 	P=[[10.00+5*cos(theta/100.0)],[240.00+5*sin(theta/100.0)],[25],[1]]
# 	#ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(10.00+5*cos(theta/100.0),10.00+5*sin(theta/100.0),20))
# 	target=matrixmult(TF,P)
# 	#print target
# 	#print matrixmult(T2,matrixmult(T1,P))
# 
# 	ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(target[0][0],target[1][0],target[2][0]))
# 	ser.readline()

ser.write('on\n')
ser.readline()
ser.write('bldc 20\n')
ser.readline()

# P=[[10],[240],[0],[1]]
# target=matrixmult(TF,P)
# ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(target[0][0],target[1][0],target[2][0]))
# ser.readline()
# ser.write('goto 00.00 00.00 000.00\n')
# ser.readline()

raw_input("shut down motor")
ser.write('off\n')
ser.readline()