import sys
import math
import array
import smbus
import i2chelp
import time

print "\n\nInitializing the I2C controller..."

bus = smbus.SMBus(1)

#Write a string of values to a register
def send_command(address,register,command):
	commandlength = len(command)
	#register = hex(register)
	listcommand = [int("".join([command[i],command[i+1]]),16) for i in xrange(0,commandlength-1,2)]
	
	#print[commandlength,address,type(address),register,type(register),command,type(command), listcommand,type(listcommand)]
	bus.write_i2c_block_data(address,register,listcommand)

#read command
def read_command(address,register,length):
	return bus.read_i2c_block_data(address,register,length)

# Ask user for the address (not gonna for now)

#address = int(raw_input("Enter the slave address of the controller as an hex number: "),16)
add_1=0x6a
add_2=0x6b
add_3=0x6c
add_4=0x6d
address=[add_1,add_2,add_3,add_4]

# Initialize the controller: send string 0A100900F0

initcode = [0x10,0x09,0x00,0xf0]
for i in xrange(0,4):
	bus.write_i2c_block_data(address[i],0x0A,initcode)
print "Done!\n"

channelnames = ['1','2','3','4','a','A']
singlechannel = ['1','2','3','4']

while True:
	print "-------------------------------------------------\nPlease choose one of the following menu options: \n-------------------------------------------------"
	print "V  :  Set a bias voltage"
	print "T  :  Set temperature"
	print "C  :  Set comparator threshold"
	print "1  :  Read TEC current"
	print "2  :  Read TEC voltage"
	print "3  :  Read high voltage"
	print "4  :  Read temperature"
	print "I  :  Initialize the detectors to standard operating settings"
	print "S  :  Shut down the detectors"
	print "Q  :  Quit the menu :("
	user_choice = raw_input("Choice: ")


####Setting the bias voltage
	if (user_choice == 'V') or (user_choice == 'v'):
		vchannel = raw_input("Please select a channel number (or a to set all at once): ")
		while vchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			vchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if vchannel in singlechannel:
			vaddress=[address[int(vchannel)-1]]
		else:
			vaddress = address
			vchannel = singlechannel

		input_voltage = float(raw_input("Please enter a voltage (in V): "))
		
		for i in xrange(0,len(vaddress)):
			vcode = i2chelp.volt2hex(input_voltage,vchannel[i])
			send_command(vaddress[i],0x02,vcode)
			print 'Voltage on channel '+str(vchannel[i])+' set to '+str(input_voltage)+'V'		
		print '\n'

####Setting the temperature
	elif (user_choice == 'T') or (user_choice == 't'):
		tchannel = raw_input("Please select a channel number (or a to set all at once): ")
		while tchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			tchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if tchannel in singlechannel:
			taddress=[address[int(tchannel)-1]]
		else:
			taddress = address
			tchannel = singlechannel

		temperature = float(raw_input("Please enter a temperature (in deg C): "))

		tcode = i2chelp.temp2hex(temperature)
		print '\n'
		for i in xrange(0,len(taddress)):
			send_command(taddress[i],0x01,tcode)	
			print 'Temperature on channel '+str(tchannel[i])+' set to '+str(temperature)+'C'
		print '\n'


######set comparitor threshold level
	elif (user_choice == 'C') or (user_choice == 'c'):
		cchannel = raw_input("Please select a channel number (or a to set all at once): ")
		while cchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			cchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if cchannel in singlechannel:
			caddress=[address[int(cchannel)-1]]
		else:
			caddress = address
			cchannel = singlechannel

		comp_threshold = float(raw_input("Please enter a value for the comparator threshold (in mV): "))
		ccode = i2chelp.comp2hex(comp_threshold)
		print '\n'
		for i in xrange(0,len(caddress)):
			send_command(caddress[i],0x03,ccode)	
			print 'Threshold on channel '+str(cchannel[i])+' set to '+str(comp_threshold)+'mV'
		print '\n'


#####Read the TEC current
	elif user_choice == '1':
		ichannel = raw_input("Please select a channel number (or a to read all at once): ")
		while ichannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			ichannel = raw_input("Please select a channel number (or A to set all at once): ")
		if ichannel in singlechannel:
			iaddress=[address[int(ichannel)-1]]
		else:
			iaddress = address
			ichannel = singlechannel
		print "Reading TEC current..."
		readicommand = '01'
		iread=range(len(iaddress))
		for i in xrange(0,len(iaddress)):		
			send_command(iaddress[i],0x00,readicommand)
			idata=read_command(iaddress[i],0x01,2)
			idata=i2chelp.hex2TECI(i2chelp.list2string(idata))
			iread[i] = ['Channel '+ str(ichannel[i])+': ',idata]	

		print "\nResult: " 
		for i in xrange(0,len(iread)):
			print iread[i][0]+str(iread[i][1])+' A'
		print "\n"



	
	elif user_choice == '2':
		vchannel = raw_input("Please select a channel number (or a to read all at once): ")
		while vchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			vchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if vchannel in singlechannel:
			vaddress=[address[int(vchannel)-1]]
		else:
			vaddress = address
			vchannel = singlechannel
		print "Reading TEC voltage..."
		readvcommand = '02'
		vread=range(len(vaddress))
		for i in xrange(0,len(vaddress)):		
			send_command(vaddress[i],0x00,readvcommand)
			vdata=read_command(vaddress[i],0x01,2)
			vdata=i2chelp.hex2TECV(i2chelp.list2string(vdata))
			vread[i] = ['Channel '+ str(vchannel[i])+': ',vdata]	

		print "\nResult: " 
		for i in xrange(0,len(vread)):
			print vread[i][0]+str(vread[i][1])+' V'
		print "\n"
		


	elif user_choice == '3':
		hvchannel = raw_input("Please select a channel number (or a to read all at once): ")
		while hvchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			hvchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if hvchannel in singlechannel:
			hvaddress=[address[int(hvchannel)-1]]
		else:
			hvaddress = address
			hvchannel = singlechannel
		print "Reading high voltage..."
		readHVcommand = '04'
		HVread=range(len(hvaddress))
		for i in xrange(0,len(hvaddress)):		
			send_command(hvaddress[i],0x00,readHVcommand)
			HVdata=read_command(hvaddress[i],0x01,2)
			HVdata=i2chelp.hex2volt(i2chelp.list2string(HVdata),hvchannel[i])
			HVread[i] = ['Channel '+ str(hvchannel[i])+': ',HVdata]	

		print "\nResult: " 
		for i in xrange(0,len(HVread)):
			print HVread[i][0]+str(HVread[i][1])+' V'
		print "\n"

#Reading out what the temperature is 
	elif user_choice == '4':
		Tchannel = raw_input("Please select a channel number (or a to read all at once): ")
		while Tchannel not in channelnames:
			print "User error, bad channel number choice. Choose from [1,2,3,4,a]"
			Tchannel = raw_input("Please select a channel number (or A to set all at once): ")
		if Tchannel in singlechannel:
			Taddress=[address[int(Tchannel)-1]]
		else:
			Taddress = address
			Tchannel = singlechannel
		print "Reading temperature..."
		readTcommand = '08'
		Tread=range(len(Taddress))
		
		for i in xrange(0,len(Taddress)):		
			send_command(Taddress[i],0x00,readTcommand)
			Tdata=read_command(Taddress[i],0x01,2)
			Tdata=i2chelp.hex2temp(i2chelp.list2string(Tdata))
			Tread[i] = ['Channel '+ str(Tchannel[i])+': ',Tdata]	

		print "\nResult: " 
		for i in xrange(0,len(Tread)):
			print Tread[i][0]+str(Tread[i][1])+'C'
		print "\n"


#Shutdown the channels
	elif (user_choice == 'S') or (user_choice == 's'):
		print "Commencing shutdown procedures..."
		#set temps to 0:
		for i in xrange(0,len(address)):
			send_command(address[i],0x01,'0000')	
			print 'Temperature on channel '+str(singlechannel[i])+' set to room temp (25 C)'
		#set HV to 0:
		for i in xrange(0,len(address)):
			send_command(address[i],0x02,'0000')	
			print 'Bias voltage on channel '+str(singlechannel[i])+' set to 0 V'
		#set comparitor to 0:
		for i in xrange(0,len(address)):
			send_command(address[i],0x03,'0000')	
			print 'Threshold on channel '+str(singlechannel[i])+' set to 0 mV'
		print "Done!"

#Initialize the channels
	elif (user_choice == 'I') or (user_choice == 'i'):
		print "Commencing startup procedures..."
		#set temps to 0:
		for i in xrange(0,len(address)):
			send_command(address[i],0x01,'09C5')
			time.sleep(8)
			print 'Temperature on channel '+str(singlechannel[i])+' set to -20C'
		#set HV to 0:
		workingvbias=[338,345,360,358]
		for i in xrange(0,len(address)):
			send_command(address[i],0x02,i2chelp.volt2hex(workingvbias[i],singlechannel[i]))	
			print 'Bias voltage on channel '+str(singlechannel[i])+' set to '+str(workingvbias[i])
		#set comparitor to 150mV:
		for i in xrange(0,len(address)):
			send_command(address[i],0x03,'048B')	
			print 'Threshold on channel '+str(singlechannel[i])+' set to 50 mV'
		print "Done!"


	elif user_choice == 'Q' or 'q':
		print "Goodbye!"
		sys.exit()

	else:
		print "Invalid option, try again."