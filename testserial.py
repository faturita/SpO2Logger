import time
import serial

ser = serial.Serial('COM16',19200, serial.EIGHTBITS, serial.PARITY_ODD, serial.STOPBITS_ONE)

strength = 1
dumpfile = open('sp02.dat', 'w+')

statebyte = -1

while True:
	#stringdata = ser.read(10)

	#bytedata = ord ( stringdata[1] )

	bytestoread = bytearray(5)

	ser.readinto(bytestoread)

	#print(bytestoread)

        if (strength == 0):
                break
	

	for bytedata in bytestoread:
		
		bit7 = (bytedata  & 128) >> 7
		bit6 = (bytedata  &  64) >> 6
		bit5 = (bytedata  &  32) >> 5
		bit4 = (bytedata  &  16) >> 4
		bit3 = (bytedata  &   8) >> 3
		bit2 = (bytedata  &   4) >> 2
		bit1 = (bytedata  &   2) >> 1
		bit0 = (bytedata  &   1) >> 0

		print(bit7,bit6,bit5,bit4,bit3,bit2,bit1,bit0,bytedata)


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
					break
				statebyte=statebyte+1

				if (statebyte==2):
					pulse = bit6*64+bit5*32+bit4*16+bit3*8+bit2*4+bit1*2+bit0;

				if (statebyte==3):
					pulse = pulse + bit7*128
					print('Pulse %d' % pulse)
					dumpfile.write('%s\n' %  str(pulse))
					dumpfile.flush()

				if (statebyte==5):
					statebyte =0
	

ser.close()

