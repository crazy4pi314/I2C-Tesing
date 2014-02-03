'''
Helper functions for I2C interfacing
Sarah Kaiser
Created: Mon Feb 3
Last updated: Mon Feb 3

'''
import sys
import math
import array



# Function definition is here
def changeme( mylist ):
   "This changes a passed list into this function"
   mylist.append([1,2,3,4]);
   print "Values inside the function: ", mylist
   return

# Now you can call changeme function
mylist = [10,20,30];
changeme( mylist );
print "Values outside the function: ", mylist























'''






print ""
print "Initializing the Aardvark I2C/SPI controller..."
print ""

# Find a port with an Aardvark device
(num, ports, unique_ids) = aa_find_devices_ext(16, 16)

port = int(ports[0])

if num > 0:
	print "Device found on port " + str(ports[0])
	#print "Unique device ID: " + str(unique_ids[0])

print ""
print "Attempting to initialize..."

# Try to open the port for the device
handle = aa_open(int(ports[0]))
if (handle <= 0):
	print "Error, could not initialize the device."
	print handle
	sys.exit()
else:
	print "Initialization successful, device handle = %d" % handle
	print ""

# Configure the SPI subsystem to use GPIO and I2C
aa_configure(handle, AA_CONFIG_GPIO_I2C)

# Ask user for the address
address = int(raw_input("Enter the slave address of the controller as an integer: "))

# Initialize the controller: send string A0100900F0
print "Turning various things on..."

init_command = array('B', "A0100900F0") 

bytes_written = aa_i2c_write(handle, address, AA_I2C_NO_FLAGS, init_command)

if bytes_written < 0:
	print "Error: %s" % aa_status_string(bytes_written)
elif bytes_written == 0:
	print "No bytes written."
elif bytes_written != len(init_command):
	print "Only %d of %d possible bytes written" % (bytes_written, len(init_command))

while True:
	print "Menu, written just for you by Olivia. Please choose one of the following menu options: "
	print "V  :  Set a high voltage"
	print "T  :  Set temperature"
	print "C  :  Set comparator threshold"
	print "1  :  Read TEC current"
	print "2  :  Read TEC voltage"
	print "3  :  Read high voltage"
	print "4  :  Read temperature"
	print "Q  :  Quit the menu :("

	user_choice = raw_input("Choice: ")

	if (user_choice == 'V') or (user_choice == 'v'):
		input_voltage = raw_input("Please enter a voltage (in V): ")

		# Check for invalid voltages
		while (input_voltage > 500) or (input_voltage < 0):
			print "User error, stupid voltage choice. Does not compute. Please try again."	
			input_voltage = raw_input("Please try entering a voltage again (in V): ")

		# Turn into an int 
		rounded_voltage = math.floor(4096*float(input_voltage)/500)
		# Get the hex string value
		vhexval_raw = hex(rounded_voltage)

		# Remove the initial '0x'
		vhexval = vhexval_raw[2:]
		# Pad with 0s at the beginning to get a 4 bit string
		while len(vhexval) < 4:
			vhexval = "0" + vhexval

		# Command to send to controller
		command = array('B', "03" + vhexval)
		
		# Send command
		bytes_written = aa_i2c_write(handle, address, AA_I2C_NO_FLAGS, command)
		
		if bytes_written < 0:
			print "Error: %s" % aa_status_string(bytes_written)
			break
		elif bytes_written == 0:
			print "No bytes written."
			break
		elif bytes_written != len(command):
			print "Only %d of %d possible bytes written" % (bytes_written, len(command)) 


	elif (user_choice == 'T') or (user_choice == 't'):
		temperature = raw_input("Please enter a temperature (in deg C): ")

		# Check for invalid temperatures
		while (temperature > 40) or (temperature < -40):
			if temperature > 40:
				print "Ouch! Too hot!"
				temperature = raw_input("Please enter a temperature (in deg C): ")
			else:
				print "Oh no, too cold." 
				temperature = raw_input("Please enter a temperature (in deg C): ")

		# Convert user input (assumed integer) to hex
		thexval_raw = hex(temperature) 
		
		# Format the hex string by removing '0x' and pad beginning with 0
		thexval = thexval_raw[2:]
		while len(thexval) < 4:
			thexval = "0" + thexval

		# Command to send to controller
		command = array('B', "01" + thexval)

		# Send command
		bytes_written = aa_i2c_write(handle, address, AA_I2C_NO_FLAGS, command)
		
		if bytes_written < 0:
			print "Error: %s" % aa_status_string(bytes_written)
			break
		elif bytes_written == 0:
			print "No bytes written."
			break
		elif bytes_written != len(command):
			print "Only %d of %d possible bytes written" % (bytes_written, len(command)) 


	elif (user_choice == 'C') or (user_choice == 'c'):
		comp_threshold = raw_input("Please enter a value for the comparator threshold (in mV): ")

		# Check for invalid comparator threshold voltage
		while (comp_threshold > 500) or (comp_threshold < 0):
			print "User error, stupid comparator threshold choice. Try again, if you dare..."	
			input_voltage = raw_input("Please try entering a threshold again (in mV): ")

		# Turn into an int
		rounded_comp_threshold = math.floor(comp_threshold)
		# Convert to hex
		chexval_raw = hex(rounded_comp_threshold)

		# Format the hex string by removing '0x' and pad beginning with 0
		chexval = chexval_raw[2:]
		while len(chexval) < 4:
			chexval = "0" + chexval 
		
		# Command to send to controller
		command = array('B', "02" + chexval)

		# Send command
		bytes_written = aa_i2c_write(handle, address, AA_I2C_NO_FLAGS, command)
		
		if bytes_written < 0:
			print "Error: %s" % aa_status_string(bytes_written)
			break
		elif bytes_written == 0:
			print "No bytes written."
			break
		elif bytes_written != len(command):
			print "Only %d of %d possible bytes written" % (bytes_written, len(command)) 


	elif user_choice == '1':
		print "Reading TEC current..."
		
		# Send a command to write-only box asking for a value to be sent to readout register
		command = "000101"

		# Read from the box
		(bytes_read, data_in) = aa_i2c_read(handle, address, AA_I2C_NO_FLAGS, 2)

		if bytes_read < 0:
			print "Error: %s" % aa_status_string(bytes_read)
			break
		elif bytes_read == 0:
			print "Error: no bytes read."
			break
		elif bytes_read != 2:
			print "Error: 2 bytes expected, only %d received" % bytes_read
			break
		else:
			print "Result: " + str(data_in)

	
	elif user_choice == '2':
		print "Reading TEC voltage..."

		command = "000201"

		# Read from the box
		(bytes_read, data_in) = aa_i2c_read(handle, address, AA_I2C_NO_FLAGS, 2)

		if bytes_read < 0:
			print "Error: %s" % aa_status_string(bytes_read)
			break
		elif bytes_read == 0:
			print "Error: no bytes read."
			break
		elif bytes_read != 2:
			print "Error: 2 bytes expected, only %d received" % bytes_read
			break
		else:
			print "Result: " + str(data_in)


	elif user_choice == '3':
		print "Reading high voltage..."

		command = "000401"

		# Read from the box
		(bytes_read, data_in) = aa_i2c_read(handle, address, AA_I2C_NO_FLAGS, 2)

		if bytes_read < 0:
			print "Error: %s" % aa_status_string(bytes_read)
			break
		elif bytes_read == 0:
			print "Error: no bytes read."
			break
		elif bytes_read != 2:
			print "Error: 2 bytes expected, only %d received" % bytes_read
			break
		else:
			print "Result: " + str(data_in)


	elif user_choice == '4':
		print "Reading temperature..."

		command = "000801"

		# Read from the box
		(bytes_read, data_in) = aa_i2c_read(handle, address, AA_I2C_NO_FLAGS, 2)

		if bytes_read < 0:
			print "Error: %s" % aa_status_string(bytes_read)
			break
		elif bytes_read == 0:
			print "Error: no bytes read."
			break
		elif bytes_read != 2:
			print "Error: 2 bytes expected, only %d received" % bytes_read
			break
		else:
			print "Result: " + str(data_in)


	elif user_choice == 'Q' or 'q':
		print "Goodbye!"
		sys.exit()

	else:
		print "Invalid option, try again."



print "Exiting, closing Aardvark device."
aa_close(handle)
'''