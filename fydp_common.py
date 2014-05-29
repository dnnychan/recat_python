import serial
from math import cos,sin,pi
from time import sleep

def matrixmult (A, B):
	# Create the result matrix
	# Dimensions would be rows_A x cols_B
	C = [[0 for row in range(len(B[0]))] for col in range(len(A))]

	for i in range(len(A)):
			for j in range(len(B[0])):
					for k in range(len(A[0])):
							C[i][j] += A[i][k]*B[k][j]
	return C

def makeRotMatrix(M1,M2,M3,M4):
	return matrixmult(M1,matrixmult(M2,matrixmult(M3,M4)))
	
class Arduino(object):
	def __init__(self):
		
		self.ser = serial.Serial('/dev/tty.usbserial-AH00PEC5') 	#adjust this to your port
		self.ser.readline() 		# get startup message
		print self.ser.name
		self.ser.write('clear\n')
		self.ser.readline()		# stupid arduino echos what you send
		
	def sendPoint (self, x, y, z):
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
		self.ser.write('gPos\n')
		self.ser.readline()
		response = self.ser.readline()
		pos=response.split()

		print response
	
		return pos
		
	def bldcSpeed(self,speed):
		self.ser.write('bldc {0:0>4.0f}\n'.format(speed))
		self.ser.readline()
	
	def stepSpeed(self,speed):
		self.ser.write('step {0:0>2.0f}\n'.format(speed))
		self.ser.readline()
		
	def turnOn(self):
		self.ser.write('on\n')
		self.ser.readline()
		
	def turnOff(self):
		self.ser.write('off\n')
		self.ser.readline()
	
	def stop(self):
		self.ser.write('stop\n')
		self.ser.readline()
		
	def cont(self):
		self.ser.write('cont\n')
		self.ser.readline()		
		
	def waitForQueue(self):
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
