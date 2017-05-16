#coding: latin-1

# http://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

import matplotlib.pyplot as plt

class Plotter:

    def __init__(self,rangeval,minval,maxval):
        # You probably won't need this if you're embedding things in a tkinter plot...
        import matplotlib.pyplot as plt
        plt.ion()

        self.x = []
        self.y = []
        self.z = []

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.line1, = self.ax.plot(self.x,'r', label='X') # Returns a tuple of line objects, thus the comma
        self.line2, = self.ax.plot(self.y,'g', label='Y')
        self.line3, = self.ax.plot(self.z,'b', label='Z')

        self.rangeval = rangeval
        self.ax.axis([0, rangeval, minval, maxval])
        self.plcounter = 0
        self.plotx = []

    def plotdata(self,new_values):
        # is  a valid message struct
        #print new_values

        self.x.append( float(new_values[0]))
        self.y.append( float(new_values[1]))
        self.z.append( float(new_values[2]))

        self.plotx.append( self.plcounter )

        self.line1.set_ydata(self.x)
        self.line2.set_ydata(self.y)
        self.line3.set_ydata(self.z)

        self.line1.set_xdata(self.plotx)
        self.line2.set_xdata(self.plotx)
        self.line3.set_xdata(self.plotx)

        self.fig.canvas.draw()
        plt.pause(0.000001)

        self.plcounter = self.plcounter+1

        if self.plcounter > self.rangeval:
          self.plcounter = 0
          self.plotx[:] = []
          self.x[:] = []
          self.y[:] = []
          self.z[:] = []


plotter = Plotter(500,-500,500)


import time
import serial

serialname = 'COM16'
serialname = '/dev/tty.SLAB_USBtoUART'

ser = serial.Serial(serialname,19200, serial.EIGHTBITS, serial.PARITY_ODD, serial.STOPBITS_ONE)

strength = 1
dumpfile = open('data/sp02.dat', 'w+')

statebyte = -1

while True:
	#stringdata = ser.read(10)

	#bytedata = ord ( stringdata[1] )

	bytestoread = bytearray(5)

	ser.readinto(bytestoread)

	#print(bytestoread)

	if (strength == 0):
		pass
		#break


	for bytedata in bytestoread:

		bit7 = (bytedata  & 128) >> 7
		bit6 = (bytedata  &  64) >> 6
		bit5 = (bytedata  &  32) >> 5
		bit4 = (bytedata  &  16) >> 4
		bit3 = (bytedata  &   8) >> 3
		bit2 = (bytedata  &   4) >> 2
		bit1 = (bytedata  &   2) >> 1
		bit0 = (bytedata  &   1) >> 0

		#print(bit7,bit6,bit5,bit4,bit3,bit2,bit1,bit0,bytedata)


		if (bit7==1 and statebyte<=0):
			# Byte 1
			statebyte=1

			if (bit4!=0  or bit5 !=0 ):
				print('Searching too long dropping Sp02')


			strength = bit3*8+bit2*4+bit1*2+bit0;
			print('Signal Strength:%d' % strength)

		else:
			if (statebyte>0):
				if (bit7!=0):
					print('Protocol error')
					strength = 0
					#break

				statebyte=statebyte+1

				if (statebyte==2):
					pulse = bit6*64+bit5*32+bit4*16+bit3*8+bit2*4+bit1*2+bit0;

				if (statebyte==3):
					pulse = pulse + bit7*128
					print('Pulse %d' % pulse)

					plotter.plotdata( [pulse, 0, 0])

					dumpfile.write('%s\n' %  str(pulse))
					dumpfile.flush()

				if (statebyte==5):
					statebyte =0


ser.close()
