import sys
import os
import datetime
import struct

DEBUG_ENABLED = False

# Datapacket and binary file info
GT7_DATAPACKET_EXPECTEDSIZE    = 0x128
GT7_BINARY_FILE_HEADER = b'GT7B'
GT7_BINARY_FILE_HEADER_SIZE = 4
GT7_BINARY_FILE_VERSION = b'0x01'
GT7_BINARY_FILE_VERSION_SIZE = 4

# start of code copied from : https://github.com/Bornhall/gt7telemetry/blob/main/gt7racedata.py

# ansi prefix
pref = "\033["

# generic print function
def printData(row,label,value,column=1):
	print('{}{};{}H{:<10}:{:>10}'.format(pref,row,column,label,value))

def printAt(str, row=1, column=1, bold=0, underline=0, reverse=0):
	sys.stdout.write('{}{};{}H'.format(pref, row, column))
	if reverse:
		sys.stdout.write('{}7m'.format(pref))
	if bold:
		sys.stdout.write('{}1m'.format(pref))
	if underline:
		sys.stdout.write('{}4m'.format(pref))
	if not bold and not underline and not reverse:
		sys.stdout.write('{}0m'.format(pref))
	sys.stdout.write(str)
	#print('{}{};{}H;{}m{}'.format(pref, row, column, bold, str), end='')

def secondsToLaptime(seconds):
	remaining = seconds
	minutes = seconds // 60
	remaining = seconds % 60
	return '{:01.0f}:{:06.3f}'.format(minutes, remaining)


def setUpDisplay(t_app_name):
    # clear terminal
    os.system('cls||clear')

    printAt(t_app_name + ':  Enter h to halt)', 1, 1, bold=1)
    printAt('Packet ID:', 1, 73)

    printAt('{:<92}'.format('Current Track Data'), 3, 1, reverse=1, bold=1)
    printAt('Time on track:', 3, 41, reverse=1)
    printAt('Laps:    /', 5, 1)
    printAt('Position:   /', 5, 21)
    printAt('Best Lap Time:', 7, 1)
    printAt('Last Lap Time:', 8, 1)

    printAt('{:<92}'.format('Current Car Data'), 10, 1, reverse=1, bold=1)
    printAt('Car ID:', 10, 41, reverse=1)
    printAt('Throttle:    %', 12, 1)
    printAt('RPM:        rpm', 12, 21)
    printAt('Speed:        kph', 12, 41)
    printAt('Brake:       %', 13, 1)
    printAt('Gear:   ( )', 13, 21)
    printAt('Boost:        kPa', 13, 41)

    printAt('Clutch:       /', 15, 1)
    printAt('RPM After Clutch:        rpm', 15, 31)

    printAt('Oil Temperature:       ??C', 17, 1)
    printAt('Water Temperature:       ??C', 17, 31)
    printAt('Oil Pressure:          bar', 18, 1)
    printAt('Body/Ride Height:        mm', 18, 31)

    printAt('Tyre Data', 20, 1, underline=1)
    printAt('FL:        ??C', 21, 1)
    printAt('FR:        ??C', 21, 21)
    printAt('??:      /       cm', 21, 41)
    printAt('           kph', 22, 1)
    printAt('           kph', 22, 21)
    printAt('RL:        ??C', 25, 1)
    printAt('RR:        ??C', 25, 21)
    printAt('??:      /       cm', 25, 41)
    printAt('           kph', 26, 1)
    printAt('           kph', 26, 21)

    printAt('Gearing', 29, 1, underline=1)
    printAt('1st:', 30, 1)
    printAt('2nd:', 31, 1)
    printAt('3rd:', 32, 1)
    printAt('4th:', 33, 1)
    printAt('5th:', 34, 1)
    printAt('6th:', 35, 1)
    printAt('7th:', 36, 1)
    printAt('8th:', 37, 1)
    printAt('???:', 39, 1)

    printAt('Positioning (m)', 29, 21, underline=1)
    printAt('X:', 30, 21)
    printAt('Y:', 31, 21)
    printAt('Z:', 32, 21)

    printAt('Velocity (m/s)', 29, 41, underline=1)
    printAt('X:', 30, 41)
    printAt('Y:', 31, 41)
    printAt('Z:', 32, 41)

    printAt('Rotation', 34, 21, underline=1)
    printAt('P:', 35, 21)
    printAt('Y:', 36, 21)
    printAt('R:', 37, 21)

    printAt('Angular (r/s)', 34, 41, underline=1)
    printAt('X:', 35, 41)
    printAt('Y:', 36, 41)
    printAt('Z:', 37, 41)

    printAt('N/S:', 39, 21)

    sys.stdout.flush()



def printDataPacket(ddata):
    cgear = struct.unpack('B', ddata[0x90:0x90+1])[0] & 0b00001111
    sgear = struct.unpack('B', ddata[0x90:0x90+1])[0] >> 4
    if cgear < 1:
        cgear = 'R'
    if sgear > 14:
        sgear = '???'

    printAt('{:>8}'.format(str(datetime.timedelta(seconds=round(struct.unpack('i', ddata[0x80:0x80+4])[0] / 1000)))), 3, 56, reverse=1)	# time of day on track

    printAt('{:3.0f}'.format(struct.unpack('h', ddata[0x74:0x74+2])[0]), 5, 7)						# current lap
    printAt('{:3.0f}'.format(struct.unpack('h', ddata[0x76:0x76+2])[0]), 5, 11)						# total laps

    printAt('{:2.0f}'.format(struct.unpack('h', ddata[0x84:0x84+2])[0]), 5, 31)						# current position
    printAt('{:2.0f}'.format(struct.unpack('h', ddata[0x86:0x86+2])[0]), 5, 34)						# total positions

    printAt('{:>9}'.format(secondsToLaptime(struct.unpack('i', ddata[0x78:0x78+4])[0] / 1000)), 7, 16)		# best lap time
    printAt('{:>9}'.format(secondsToLaptime(struct.unpack('i', ddata[0x7C:0x7C+4])[0] / 1000)), 8, 16)		# last lap time

    printAt('{:5.0f}'.format(struct.unpack('i', ddata[0x124:0x124+4])[0]), 10, 48, reverse=1)		# car id

    printAt('{:3.0f}'.format(struct.unpack('B', ddata[0x91:0x91+1])[0] / 2.55), 12, 11)				# throttle
    printAt('{:7.0f}'.format(struct.unpack('f', ddata[0x3C:0x3C+4])[0]), 12, 25)					# rpm
    printAt('{:7.1f}'.format(3.6 * struct.unpack('f', ddata[0x4C:0x4C+4])[0]), 12, 47)				# speed kph

    printAt('{:3.0f}'.format(struct.unpack('B', ddata[0x92:0x92+1])[0] / 2.55), 13, 11)				# brake
    printAt('{}'.format(cgear), 13, 27)																# actual gear
    printAt('{}'.format(sgear), 13, 30)																# suggested gear
    printAt('{:7.2f}'.format(struct.unpack('f', ddata[0x50:0x50+4])[0] - 1), 13, 47)				# boost

    printAt('{:5.3f}'.format(struct.unpack('f', ddata[0xF4:0xF4+4])[0]), 15, 9)						# clutch
    printAt('{:5.3f}'.format(struct.unpack('f', ddata[0xF8:0xF8+4])[0]), 15, 17)					# clutch engaged
    printAt('{:7.0f}'.format(struct.unpack('f', ddata[0xFC:0xFC+4])[0]), 15, 48)					# rpm after clutch

    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x5C:0x5C+4])[0]), 17, 17)					# oil temp
    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x58:0x58+4])[0]), 17, 49)					# water temp

    printAt('{:6.2f}'.format(struct.unpack('f', ddata[0x54:0x54+4])[0]), 18, 17)					# oil pressure
    printAt('{:6.0f}'.format(1000 * struct.unpack('f', ddata[0x38:0x38+4])[0]), 18, 49)				# ride height

    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x60:0x60+4])[0]), 21, 5)						# tyre temp FL
    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x64:0x64+4])[0]), 21, 25)					# tyre temp FR
    printAt('{:6.1f}'.format(200 * struct.unpack('f', ddata[0xB4:0xB4+4])[0]), 21, 43)				# tyre diameter FR
    printAt('{:6.1f}'.format(200 * struct.unpack('f', ddata[0xB8:0xB8+4])[0]), 21, 50)				# tyre diameter FL

    printAt('{:6.1f}'.format(3.6 * struct.unpack('f', ddata[0xB4:0xB4+4])[0] * struct.unpack('f', ddata[0xA4:0xA4+4])[0]), 22, 5)						# tyre speed FL
    printAt('{:6.1f}'.format(3.6 * struct.unpack('f', ddata[0xB8:0xB8+4])[0] * struct.unpack('f', ddata[0xA8:0xA8+4])[0]), 22, 25)						# tyre speed FR

    printAt('{:6.3f}'.format(struct.unpack('f', ddata[0xC4:0xC4+4])[0]), 23, 5)						# suspension FL
    printAt('{:6.3f}'.format(struct.unpack('f', ddata[0xC8:0xC8+4])[0]), 23, 25)					# suspension FR

    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x68:0x68+4])[0]), 25, 5)						# tyre temp RL
    printAt('{:6.1f}'.format(struct.unpack('f', ddata[0x6C:0x6C+4])[0]), 25, 25)					# tyre temp RR
    printAt('{:6.1f}'.format(200 * struct.unpack('f', ddata[0xBC:0xBC+4])[0]), 25, 43)				# tyre diameter RR
    printAt('{:6.1f}'.format(200 * struct.unpack('f', ddata[0xC0:0xC0+4])[0]), 25, 50)				# tyre diameter RL

    printAt('{:6.1f}'.format(3.6 * struct.unpack('f', ddata[0xBC:0xBC+4])[0] * struct.unpack('f', ddata[0xAC:0xAC+4])[0]), 26, 5)						# tyre speed RL
    printAt('{:6.1f}'.format(3.6 * struct.unpack('f', ddata[0xC0:0xC0+4])[0] * struct.unpack('f', ddata[0xB0:0xB0+4])[0]), 26, 25)						# tyre speed RR

    printAt('{:6.3f}'.format(struct.unpack('f', ddata[0xCC:0xCC+4])[0]), 27, 5)						# suspension RL
    printAt('{:6.3f}'.format(struct.unpack('f', ddata[0xD0:0xD0+4])[0]), 27, 25)					# suspension RR

    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x104:0x104+4])[0]), 30, 5)					# 1st gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x108:0x108+4])[0]), 31, 5)					# 2nd gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x10C:0x10C+4])[0]), 32, 5)					# 3rd gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x110:0x110+4])[0]), 33, 5)					# 4th gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x114:0x114+4])[0]), 34, 5)					# 5th gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x118:0x118+4])[0]), 35, 5)					# 6th gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x11C:0x11C+4])[0]), 36, 5)					# 7th gear
    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x120:0x120+4])[0]), 37, 5)					# 8th gear

    printAt('{:7.3f}'.format(struct.unpack('f', ddata[0x100:0x100+4])[0]), 39, 5)					# ??? gear

    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x04:0x04+4])[0]), 30, 23)					# pos X
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x08:0x08+4])[0]), 31, 23)					# pos Y
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x0C:0x0C+4])[0]), 32, 23)					# pos Z

    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x10:0x10+4])[0]), 30, 43)					# velocity X
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x14:0x14+4])[0]), 31, 43)					# velocity Y
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x18:0x18+4])[0]), 32, 43)					# velocity Z

    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x1C:0x1C+4])[0]), 35, 23)					# rot Pitch
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x20:0x20+4])[0]), 36, 23)					# rot Yaw
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x24:0x24+4])[0]), 37, 23)					# rot Roll

    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x2C:0x2C+4])[0]), 35, 43)					# angular velocity X
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x30:0x30+4])[0]), 36, 43)					# angular velocity Y
    printAt('{:9.4f}'.format(struct.unpack('f', ddata[0x34:0x34+4])[0]), 37, 43)					# angular velocity Z

    printAt('{:7.4f}'.format(struct.unpack('f', ddata[0x28:0x28+4])[0]), 39, 25)					# rot ???

    printAt('Rev Limiter {:5.0f} rpm'.format(struct.unpack('h', ddata[0x88:0x88+2])[0]), 12, 71)		# rpm rev limiter
    printAt('Unknown RPM {:5.0f} rpm'.format(struct.unpack('h', ddata[0x8A:0x8A+2])[0]), 13, 71)		# rpm for what?
    printAt('Est. Speed  {:5.0f} kph'.format(struct.unpack('h', ddata[0x8C:0x8C+2])[0]), 14, 71)		# estimated speed

    printAt('0x48 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0x48:0x48+4])[0]), 21, 71)			# 0x48 = ???
    printAt('0x8E BITS  =  {:0>8}'.format(bin(struct.unpack('B', ddata[0x8E:0x8E+1])[0])[2:]), 23, 71)	# various flags (see https://github.com/Nenkai/PDTools/blob/master/PDTools.SimulatorInterface/SimulatorPacketG7S0.cs)
    printAt('0x8F BITS  =  {:0>8}'.format(bin(struct.unpack('B', ddata[0x8F:0x8F+1])[0])[2:]), 24, 71)	# various flags (see https://github.com/Nenkai/PDTools/blob/master/PDTools.SimulatorInterface/SimulatorPacketG7S0.cs)
    printAt('0x93 BITS  =  {:0>8}'.format(bin(struct.unpack('B', ddata[0x93:0x93+1])[0])[2:]), 25, 71)	# 0x93 = ???

    printAt('0x94 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0x94:0x94+4])[0]), 27, 71)			# 0x94 = ???
    printAt('0x98 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0x98:0x98+4])[0]), 28, 71)			# 0x98 = ???
    printAt('0x9C FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0x9C:0x9C+4])[0]), 29, 71)			# 0x9C = ???
    printAt('0xA0 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xA0:0xA0+4])[0]), 30, 71)			# 0xA0 = ???

    printAt('0xD4 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xD4:0xD4+4])[0]), 32, 71)			# 0xD4 = ???
    printAt('0xD8 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xD8:0xD8+4])[0]), 33, 71)			# 0xD8 = ???
    printAt('0xDC FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xDC:0xDC+4])[0]), 34, 71)			# 0xDC = ???
    printAt('0xE0 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xE0:0xE0+4])[0]), 35, 71)			# 0xE0 = ???

    printAt('0xE4 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xE4:0xE4+4])[0]), 36, 71)			# 0xE4 = ???
    printAt('0xE8 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xE8:0xE8+4])[0]), 37, 71)			# 0xE8 = ???
    printAt('0xEC FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xEC:0xEC+4])[0]), 38, 71)			# 0xEC = ???
    printAt('0xF0 FLOAT {:11.5f}'.format(struct.unpack('f', ddata[0xF0:0xF0+4])[0]), 39, 71)			# 0xF0 = ???

    printAt('{:>10}'.format(struct.unpack('i', ddata[0x70:0x70+4])[0]), 1, 83)						# packet id

# end of code from : https://github.com/Bornhall/gt7telemetry/blob/main/gt7racedata.py

def outputDataPacketArrayToBinaryFile(t_dataPacketArray, testing):
    # datetime object containing current date and time
    now = datetime.datetime.now() #+ '-' + datetime.now().time
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    if DEBUG_ENABLED: print("date and time =", dt_string)

    temp_counter = 0
    binary_filename = 'test-file.gt7'

    if testing == False:
        binary_filename = './gt7-datalog-' + dt_string + '.gt7'

    print('Outputting logged data packets to file...', binary_filename)

    with open(binary_filename,'wb') as binary_file:
        # write header info
        binary_file.write(GT7_BINARY_FILE_HEADER) 
        binary_file.write(GT7_BINARY_FILE_VERSION) 
        # iterate through all the data packets nd write to the file
        for member in t_dataPacketArray:
            if DEBUG_ENABLED: print('\nPacket number: ', temp_counter)
            # write data
            binary_file.write(member)
            temp_counter += 1
        # Close file
        binary_file.close()

def loadDataPacketArrayFromBinaryFile(fileName):
    temp_counter = 0
    if fileName == '':
        # for easy testing
        binary_filename = 'test-file.gt7'
    else:
        binary_filename = fileName
    #        binary_filename = './gt7-datalog-' + dt_string + '.gt7'

    print('Loading and printing previously saved data packets from file: ', binary_filename)

    with open(binary_filename,'rb') as binary_file:
        # read write data
        if binary_file.read(GT7_BINARY_FILE_HEADER_SIZE) !=GT7_BINARY_FILE_HEADER :
            print('Load aborted: File header not recognised')
            return b''
        print('File version: ', str(binary_file.read(GT7_BINARY_FILE_VERSION_SIZE)))

        data_in = binary_file.read(GT7_DATAPACKET_EXPECTEDSIZE)
        loadedDataArray = []
        while len(data_in) > 0:
            loadedDataArray.append(data_in)
            temp_counter += 1
            data_in = binary_file.read(GT7_DATAPACKET_EXPECTEDSIZE)
        # Close file
        if DEBUG_ENABLED: print('\nTotal Packets loaded: ', temp_counter)
        binary_file.close()

    return loadedDataArray

def outputDataPacketArrayToCSV(t_dataPacketArray):
    print('Not yet implemented - sorry :-(')

def outputDataPacketArrayToCSVPosOnly(t_dataPacketArray):
    # datetime object containing current date and time
    now = datetime.datetime.now() #+ '-' + datetime.now().time
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    if DEBUG_ENABLED: print("date and time =", dt_string)

    print('Outputting logged data packets to CSV file...\n')
    temp_counter = 0
    csv_filename = './gt7-datalog-' + dt_string + '.csv'
    if DEBUG_ENABLED: print(csv_filename)
    with open(csv_filename,'w') as csv_output_file:
        for member in t_dataPacketArray:
            print('{:9.4f}'.format(struct.unpack('f', member[0x04:0x04+4])[0])
                    + ',' +  
                    '{:9.4f}'.format(struct.unpack('f', member[0x08:0x08+4])[0])
                    + ',' +
                    '{:9.4f}'.format(struct.unpack('f', member[0x0C:0x0C+4])[0])
                    + ',', file=csv_output_file)
            temp_counter += 1