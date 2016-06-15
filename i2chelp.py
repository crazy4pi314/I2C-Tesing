'''
Helper functions for I2C interfacing
Sarah Kaiser
Created: Mon Feb 3 2015
Last updated: Fri Mar 28 2015

'''
import sys
import math
import array

'''
General Utilites
'''
lsb = 2*2.5/4096;

#Resistance of thermistor as a function of temperature
def Rthermistor10k(temp):
	return 10000*math.exp(3892*((298.15-(temp+273.15))/(298.15*(temp+273.15))))

#Temperature of thermistor as a function of resistance
def Tthermistor10k(R):
	return (326.3457990944156-273.15*math.log(0.0001*R))/(13.053831963776624+math.log(0.0001*R))

#This changes a passed int into the n character hex string representing that number
def int2phex(intval,n):
   		hexval=hex(intval)[2:].zfill(n).upper()   		
   		return hexval
#This changes a passed int into the 2 character hex string representing that number
def int2phex2(intval):
   		hexval=hex(intval)[2:].zfill(2).upper()   		
   		return hexval

#This changes a voltage into a codeword
def v2code(v):
   		code=int(round((v*4096)/(2.5-lsb)+lsb))   		
   		return code

#switch to 10 bit readout 
def hex10bitcode(hex16):
	return int(bin(int(hex16,16))[2:].zfill(16)[4:],2)

#convert 10 bit codeword to voltage
def code2volt(code10bit,adcrange):
	return ((adcrange-2*lsb)/(4096))*code10bit+lsb




#read data to a string
def list2string(list):
	return "".join(map(int2phex2,list))
	

'''
DAC converting functions
'''
# Convert User HV to hex code
def volt2hex(HVval,channel):
	# Check for invalid voltages
	if (HVval > 500) or (HVval < 0):
		print "User error, stupid voltage choice. Does not compute. Please try again."
		code='0000'	
		return '0000'
	else:
		
		if (channel=='1'):
			code=int2phex(max(int(round(7.41129*HVval-10.922907)),0),4)

   		elif (channel=='2'):
			code=int2phex(max(int(round(7.3529590*HVval-7.1530270)),0),4) 

		elif (channel=='3'):
			code=int2phex(max(int(round(7.3563918*HVval-9.2322928)),0),4) 

		elif (channel=='4'):
			code=int2phex(max(int(round(7.3705900*HVval-5.7497629)),0),4) 

		#original test diode code
		#code=int2phex(int(round((6.99655*HVval+4.125)),4) 		
   		return code

# Convert User temp to hex code
def temp2hex(temp):
	# Check for invalid temps
	temp=int(temp)
	if (temp > 50) or (temp < -50):
		print "User error, stupid temperature choice. Does not compute. Please try again."	
		return '0000'
	else:
   		r=Rthermistor10k(temp)
   		rdivide=2.5*(r/(r+65000))
   		code=int2phex(v2code(rdivide),4)
   		return code

# Convert User comparitor level to hex code
def comp2hex(comp):
	# Check for invalid voltages
	if (comp > 500) or (comp < 0):
		print "User error, stupid threshold choice. Does not compute. Please try again."	
		return '0000'
	else:  
   		code=int2phex(v2code(comp/211.5),4)
   		return code




'''
ADC converting functions
'''
# Convert User hex code to HV
def hex2volt(hexval,channel):
	intcode=2*hex10bitcode(hexval)
	if (channel=='1'):
		volt=0.14778832632815772*intcode-0.011304923293643755

   	elif (channel=='2'):
		volt=0.14913241674799574*intcode+0.26857746986763315

	elif (channel=='3'):
		volt=0.14835849676737672*intcode+0.6480556230452933 

	elif (channel=='4'):
		volt=0.14865430420790374*intcode-0.408404208038313
		
	#original detector equation
   	#volt=0.285855*intcode-0.5896118255011659	
   	return round(volt,3)

# Convert User hex code to temp
def hex2temp(hexval):
		intcode=hex10bitcode(hexval)
		volt=code2volt(intcode,5)
		voltdivider=(volt*65000)/(2.5-volt)
		temp=Tthermistor10k(voltdivider)
   		return round(temp,2)

# Convert User hex code to TEC voltage
def hex2TECV(hexval):
		intcode=hex10bitcode(hexval)
		volt=code2volt(intcode,5)
   		return round(volt,3)

# Convert User hex code to TEC current
def hex2TECI(hexval):
		intcode=hex10bitcode(hexval)
		volt=code2volt(intcode,5)
		current=volt/(0.05+0.27)
   		return round(current,3)

'''
DAC testing
'''
# #Testing the HV functions
# hv= int(raw_input('Set the High Voltage (V):\n'));

# hvout = volt2hex( hv );
# print "HV codeword: ", hvout


# #Testing the temp functions
# t= int(raw_input('Set the temperature (C):\n'));

# tout = temp2hex( t );
# print "Temperature codeword: ", tout

# #Testing the temp functions
# comp=int(raw_input('Set the comparitor threshold (mV):\n'));

# compout = comp2hex( comp );
# print "Comparitor threshold codeword: ", compout

'''
ADC testing
'''
# #Testing the HV readout
# hv= raw_input('Readout the High Voltage:\n');
# hvout = hex2volt( hv );
# print "HV (V): ", hvout

# #Testing the temperature readout
# t= raw_input('Readout the temperature:\n');
# tout = hex2temp( t );
# print "Temp (C): ", tout

# #Testing the TEC voltage readout
# v= raw_input('Readout the TEC voltage:\n');
# vout = hex2TECV( v );
# print "TEC Voltage (V): ", vout

# #Testing the TEC current readout
# v= raw_input('Readout the TEC current:\n');
# vout = hex2TECI( v );
# print "TEC current (A): ", vout













