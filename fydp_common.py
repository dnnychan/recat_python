# common files for use with RECAT
import serial
from math import cos,sin,pi
from time import sleep

def matrixmult (A, B):	# matrix multiplication
	# Create the result matrix
	# Dimensions would be rows_A x cols_B
	C = [[0 for row in range(len(B[0]))] for col in range(len(A))]

	for i in range(len(A)):
			for j in range(len(B[0])):
					for k in range(len(A[0])):
							C[i][j] += A[i][k]*B[k][j]
	return C

def makeRotMatrix(M1,M2,M3,M4):	# generate a transformation matrix given 4 matrices
	return matrixmult(M1,matrixmult(M2,matrixmult(M3,M4)))
	
class Arduino(object):
# arduino class (the recat object)
	def __init__(self):
		
		self.ser = serial.Serial('/dev/tty.usbserial-AH00PEC5') 	#adjust this to your port
		self.ser.readline() 		# get startup message
		print self.ser.name
		self.ser.write('clear\n')
		self.ser.readline()		# stupid arduino echos what you send
		
	def sendPoint (self, x, y, z):
	# send a point to add to the queue on the recat
		if (x < 0):
			x = 0
		if (y < 0):
			y = 0
		if (z < 0):
			z = 0
		self.ser.write('goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(x,y,z))
		#print 'goto {0:0>5.2f} {1:0>5.2f} {2:0>6.2f}\n'.format(x,y,z)
		self.ser.readline()
		
	def getAngles (self):
	# read the angles of the magnetic encoders
		self.ser.write('gAng\n')
		self.ser.readline()
		response = self.ser.readline()
		thetas=response.split()

		print response

		theta_1 = float(thetas[0])*pi/180
		theta_2 = float(thetas[1])*pi/180
		theta_3 = -float(thetas[2])*pi/180
		theta_4 = float(thetas[3])*pi/180
	
		return (theta_1,theta_2,theta_3,theta_4)
	
	def getPosition(self):
	# read the current position of the drill on the gantry
		self.ser.write('gPos\n')
		self.ser.readline()
		response = self.ser.readline()
		pos=response.split()

		print response
	
		return pos
		
	def bldcSpeed(self,speed):	# change the speed of the drill
		self.ser.write('bldc {0:0>4.0f}\n'.format(speed))
		self.ser.readline()
	
	def stepSpeed(self,speed):	# change of fast to step
		self.ser.write('step {0:0>2.0f}\n'.format(speed))
		self.ser.readline()
		
	def turnOn(self):						# turn on the motors
		self.ser.write('on\n')
		self.ser.readline()
			
	def turnOff(self):					# turn off the motors
		self.ser.write('off\n')
		self.ser.readline()
	
	def stop(self):							# stronger stop
		self.ser.write('stop\n')
		self.ser.readline()
		
	def cont(self):							# continue from where you left off
		self.ser.write('cont\n')
		self.ser.readline()		
		
	def waitForQueue(self):			# wait for the destination points queue is empty. this is to prevent dumping too much data into the queue which crashes the arduino
	 	self.ser.write('qEmp\n')
		self.ser.readline()
		is_ready = self.ser.readline()
		print "waiting for queue"
		#print repr(is_ready)
		while (is_ready.startswith('0')):	#wait for previous set of points to be processed before sending next batch
			self.ser.write('qEmp\n')
			self.ser.readline()
			is_ready = self.ser.readline()
			#self.getPosition()
			#print is_ready
			sleep(1)
		
	def __del__(self):
		self.ser.flush()
		self.ser.close()
		
arduino = Arduino()
