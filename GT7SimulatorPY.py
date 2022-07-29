#!/usr/bin/env python

"""GT7Simulator.py: An application for capturing and manipulating the data output by Gran Turismo 7 on PS5/PS4"""

__author__ = "The Brink of Tomorrow"
__copyright__ = "Copyright 2022, The Brink of Tomorrow"
__credits__ = ["Nenkai", "lmirel", "Bornhall"]
__license__ = "MIT"
__version__ = "0.1.04"
__maintainer__ = "The Brink of Tomorrow"
__email__ = "thebrinkoftomorrow@gmail.com"
__status__ = "Development"

import socket
import sys
import threading
import time
import struct
import datetime
import os

# pip install salsa20
from salsa20 import Salsa20_xor

import GT7SimulatorInterfaceData as GT7If
import GT7DisplayFileIO 
import GT7PlotData

DEBUG_ENABLED = False

serverAddress = ''

GT7_APP_NAME = 'GT7SimulatorPY.py'
GT7_INTRO_MESSAGE = GT7_APP_NAME + ' v.' + __version__
GT7_MAINMENU_TEXT = 'Usage: Enter "s" to start date capture, "h" to halt logging, "q" to quit, "help" for more options.\n'

# Datapacket expected size in bytes
GT7_DATAPACKET_EXPECTEDSIZE    = 0x128

# send heartbeat
def send_hb(t_s, t_ip, t_port):
	send_data = 'A'
	t_s.sendto(send_data.encode('utf-8'), (t_ip, t_port))

def printHelpMessage():
    print('Usage:  Type the following (plus <Return>):')
    print(  's\t(Re)Starts data packet capture\n' +
            'h\tHalts data packet capture\n' +
            'q\tQuits the application\n' +
            'r\tResets existing data already captured\n' +
            'o\tSaves the data captured to a binary file (name=./test-data.gt7)\n' +
            'z\tLoads the data (previously captured and saved) from a binary file (name=./test-data.gt7)\n' +
            'g\tGraphs the the data loaded from binary file (throttle, brake, speed, RPM\n' +
            'csv\tSaves the captured data to a .csv file (name=gt7-datalog-<date>-<time>.csv)\n' +
            'csvpos\tSaves the captured POSITION data to a .csv file (name=gt7-datalog-<date>-<time>.csv)\n'
            '\n')

def isWorthCapturing(dataPacket):
    mask1 = 0x9    # on track
    mask2 = 0x2    # paused
    binData = bin(struct.unpack('B', dataPacket[0x8E:0x8E+1])[0])[2:] 
    onTrack = mask1 & int(binData) 
    paused = mask2 & int(binData) 
#    print(mask, binData, result )
    if onTrack and not paused:
        return True
    return False

class GT7SimulatorLogging(threading.Thread):
    sendPort    = 33739
    recvPort    = 33740
    bufferSize  = 4096
    # State Variables
    counter = 0
    dataPacketArray = []
    loadedDataArray = []

    logging_should_run = False
    shutdown_app = False
    logging_in_progress = False
    output_to_stdout = True
    save_data_enabled = True
    
    def __init__(self, theIPAddress):
        super(GT7SimulatorLogging, self).__init__()
        self.serverIPAddress = theIPAddress

    def setUpConnection(self):
        # create dgram udp socket
        try:
            self.socketOut = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error:
            print('Failed to create sockets')
            sys.exit()

        if DEBUG_ENABLED: print("- Attempting to bind port: ", self.recvPort)
        # Binding port
        self.socketOut.bind(('', self.recvPort))
        self.socketOut.settimeout(10)
        send_hb(self.socketOut, self.serverIPAddress, self.sendPort)

    def resetLoop(self):
        print('\nDeleting logged data packets...\n')
        self.counter = 0
        del self.dataPacketArray[:]

    def printAppStatus(self):
        print('Status: Display On = ', self.output_to_stdout, ' : Logging to Memory = ', self.save_data_enabled)
    
    def printDataPacketArray(self, toprtDataPacketArray):
        if DEBUG_ENABLED: print('\nPrinting logged data packets...\n')
        temp_counter = 0
        for member in toprtDataPacketArray:
            print('\nPacket number: ', temp_counter)
            if len(member) == GT7_DATAPACKET_EXPECTEDSIZE:
                temp_data = GT7If.readData(member)
                GT7If.printStatus(temp_data, False)
            temp_counter += 1

    # not sure if I still need this - covert to .csv version,,,,???
    def outputtDataPacketArrayToTextFile(self):
        # datetime object containing current date and time
        now = datetime.now() #+ '-' + datetime.now().time
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        if DEBUG_ENABLED: print("date and time =", dt_string)

        print('Outputting logged data packets to file...\n')
        temp_counter = 0
        log_filename = './gt7-datalog-' + dt_string + '.txt'
        if DEBUG_ENABLED: print(log_filename)
        with open(log_filename,'w') as log_output_file:
            for member in self.dataPacketArray:
                print('\nPacket number: ', temp_counter, file=log_output_file)
   #            if isinstance(member, GT7If.SimulatorPacketGT7):
    #                GT7If.printStatus(member, False)
                temp_counter += 1



    def run(self,*args,**kwargs):
        while self.shutdown_app == False:
            if self.logging_should_run:
                if self.logging_in_progress == False:
                    self.run_logging_loop()

            time.sleep(0.5)


    def run_logging_loop(self):
        if self.counter == 0:
            del self.dataPacketArray[:]

        # setup the display output
        GT7DisplayFileIO.setUpDisplay(GT7_APP_NAME)

        # Sending hearbeat packet
        send_hb(self.socketOut, self.serverIPAddress, self.sendPort)

        pknt = 0
        while self.logging_should_run:
            self.logging_in_progress = True



            # receive message from server
            msgFromServer, ipAddressFromServer = self.socketOut.recvfrom(self.bufferSize)

            if len(msgFromServer) == GT7_DATAPACKET_EXPECTEDSIZE:
                if DEBUG_ENABLED: print("Received data size is correct")
        #        msg = "Message from Server {}".format(msgFromServer)
        #        print(msgFromServer)
            else:
                print("Received data size is incorrect")

            decryptedDataPacket = DecryptGT7DataPacket(msgFromServer)

            # Display capture packet to stdout
            if self.output_to_stdout:
                GT7DisplayFileIO.printDataPacket(decryptedDataPacket)
            # save every fifth data packet during "On Track" activity
            if (self.counter % 5) == 0 and isWorthCapturing(decryptedDataPacket) and self.save_data_enabled:
                self.dataPacketArray.append(decryptedDataPacket)

            pknt += 1 
            self.counter += 1
            if pknt > 100:
                # Sending hearbeat packet
                send_hb(self.socketOut, self.serverIPAddress, self.sendPort)
                pknt = 0
            #time.sleep(0.25)
    
        self.logging_in_progress = False



def DecryptGT7DataPacket(byteData : bytes):
    
    # Input should be 0x94 (or 0x128 in certain cases?)
    # BD : not sure what to do with this next ine
    # _salsa.Set(0);

    GT7_KEY = b'Simulator Interface Packet GT7 ver 0.0'
    oiv = byteData[0x40:0x44]
    iv1 = int.from_bytes(oiv, byteorder='little') # Seed IV is always located there
    iv2 = iv1 ^ 0xDEADBEAF #// Notice DEADBEAF, not DEADBEEF

    IV = bytearray()
    IV.extend(iv2.to_bytes(4, 'little'))
    IV.extend(iv1.to_bytes(4, 'little'))

    gt7DecrypedData = Salsa20_xor(byteData, bytes(IV), GT7_KEY[0:32])
    # Check magic number
    magic = int.from_bytes(gt7DecrypedData[0:4], byteorder='little')
    if magic != 0x47375330:
        return bytearray(b'')
    if DEBUG_ENABLED: print('Packet decryption successful')
    return gt7DecrypedData


def testPlotter(toPlotDataPacketArray):
    if DEBUG_ENABLED: print('\nPrinting logged data packets...\n')
    temp_counter = 0
    x_vec = []
    throttle_vec = []
    brake_vec = []
    speed_vec = []
    rpm_vec = []

    for member in toPlotDataPacketArray:
        #arbitray x-axis counter
        x_vec.append(temp_counter)
        # get values of interest and pack into vectors
        throttle_vec.append(struct.unpack('B', member[0x91:0x91+1])[0] / 2.55)
        brake_vec.append(struct.unpack('B', member[0x92:0x92+1])[0] / 2.55)
        speed_vec.append(3.6 * struct.unpack('f', member[0x4C:0x4C+4])[0]) 
        rpm_vec.append(struct.unpack('f', member[0x3C:0x3C+4])[0])

        temp_counter += 1
    y_list = [ throttle_vec, brake_vec, speed_vec, rpm_vec ]
    name_list = [ 'Throttle', 'Brake', 'Speed (KPH)', 'RPM' ]
#    print('Data:  ', x_vec, throttle_vec, speed_vec, rpm_vec)
    GT7PlotData.GT7StaticMultiPlotter(x_vec,y_list, name_list, 'GT7 Data Plot')



print(GT7_INTRO_MESSAGE)

# get ip address from command line
if len(sys.argv) == 2:
    serverAddress = sys.argv[1]
    print(serverAddress)
else:
    print('Run like : python3 ' + GT7_APP_NAME + ' <playstation-ip>')
    exit(1)

GT7_object = GT7SimulatorLogging(serverAddress)
GT7_object.setUpConnection()
GT7_object.start()

not_quit = True
while not_quit:
#    GT7_object.printAppStatus()

    keyboard_input = input(GT7_MAINMENU_TEXT)
    if DEBUG_ENABLED: print('Input received was: ', keyboard_input)
    if keyboard_input == 'h':
        if DEBUG_ENABLED: print('entered h')
        GT7_object.logging_should_run = False
    elif keyboard_input == 's':
        if DEBUG_ENABLED: print('entered s')
        GT7_object.logging_should_run = True
    elif keyboard_input == 'q':
        if DEBUG_ENABLED: print('entered q')
        GT7_object.logging_should_run = False
        GT7_object.shutdown_app = True
        not_quit = False
        os.system('cls||clear')
    elif keyboard_input == 'r':
        GT7_object.resetLoop()
    elif keyboard_input == 'p':
        GT7_object.printDataPacketArray(GT7_object.dataPacketArray)
    elif keyboard_input == 'o':
        GT7DisplayFileIO.outputDataPacketArrayToBinaryFile(GT7_object.dataPacketArray, True)
    elif keyboard_input == 'l':
        GT7_object.save_data_enabled = not GT7_object.save_data_enabled
    elif keyboard_input == 'd':
        GT7_object.output_to_stdout = not GT7_object.output_to_stdout
    elif keyboard_input == 'z':
        # load (previously saved) raw data packets
        GT7_object.loadedDataArray = GT7DisplayFileIO.loadDataPacketArrayFromBinaryFile('')
    elif keyboard_input == 'y':
        # print loaded (from previously saved) raw data packets
        if len(GT7_object.loadedDataArray) > 0:
            GT7_object.printDataPacketArray(GT7_object.loadedDataArray)
    elif keyboard_input == 'csv':
        # save loaded from previously saved) raw data packets as CSV file
        if len(GT7_object.loadedDataArray) > 0:
#            GT7_object.printDataPacketArray(GT7_object.loadedDataArray)
            GT7DisplayFileIO.outputDataPacketArrayToCSV(GT7_object.loadedDataArray)
    elif keyboard_input == 'csvpos':
        # save loaded from previously saved) raw data packets as CSV file
        if len(GT7_object.loadedDataArray) > 0:
#            GT7_object.printDataPacketArray(GT7_object.loadedDataArray)
            GT7DisplayFileIO.outputDataPacketArrayToCSVPosOnly(GT7_object.loadedDataArray)
    elif keyboard_input == 'g': 
        testPlotter(GT7_object.loadedDataArray)
    elif keyboard_input == 'help':
        os.system('cls||clear')
        printHelpMessage()
    elif keyboard_input == 'isontrack':
        isWorthCapturing(GT7_object.loadedDataArray[50])


