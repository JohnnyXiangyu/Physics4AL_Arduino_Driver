"""serial communication library (win64), inclusing base class Port \n
    API: \n
        __init__(name, baudrate) \n
        sendData(arg) customizable interface \n
        readData(arg) customizable interface \n
        communicate(arg) \n"""

import serial
import serial.tools.list_ports
import csv
import os

print('Loading serial communication module ...')


class VirtualPort:
    '''
    Virtual machine, designed for common usage. Defines the following working procedure:
        __init__: open designated file (by prompting user input)
        communicate: return a line of data from the open csv file
    '''

    def __init__(self):
        fileName = input(
            '| Enter filename to open (should be under directory ./Data_Analysis_win64/virtual_data/): ')
        fileName = './Data_Analysis_win64/virtual_data/' + fileName
        self.m_port = []

        try:
            csv_file = open(fileName, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 1:
                    # the first line is used for formating or other info, not defined yet
                    tempList = []
                    for item in row:
                        tempList.append(item)
                    self.m_port.append(tempList)
                line_count += 1

        except FileNotFoundError:
            os.system('cls')
            print('File not found. ')
            self.m_port = False

    def sendData(self):
        pass

    def readData(self):
        if len(self.m_port) <= 0:
            return []
        returnList = self.m_port[0]
        self.m_port.pop(0)
        return returnList

    def communicate(self):
        """return a designated response from serial port"""
        # communicate
        result = self.readData()

        return result


class SerialPort:
    '''
    Data source prototype class, defines the following working procedure:
        __init__: open port
        communicate: sendData, readData
    '''

    def __init__(self, name, br):
        port_list = list(serial.tools.list_ports.comports())
        self.m_name = ''
        self.m_br = br
        self.m_port = False
        # get input
        if len(port_list) <= 0:
            os.system('cls')
            print('| There is no serial device connected.')
        else:
            for i in port_list:
                if name in i.description:
                    self.m_name = i.device  # find the first designated device
            if self.m_name == '':
                os.system('cls')
                print('| The designated device is not connected. ')
            # port open
            else:
                self.m_port = serial.Serial(self.m_name, self.m_br)

    def __del__(self):
        # port close
        if self.m_port != False and self.m_port.isOpen() == True:
            self.m_port.close()

    def sendData(self, purpose):
        pass

    def readData(self):
        return ''

    def communicate(self, purpose='latest_sensing'):
        """return a designated response from serial port"""
        # communicate & error reporting
        if self.sendData(purpose) == False:
            return -1
        result = self.readData()
        if result == False:
            return -1

        # pack data
        list1 = []
        for char in result:
            list1.append(int(char))

        return list1


class Arduino(SerialPort):
    '''
    Receiver for Arduino device that is used in Physics 4AL
    BR is set to 9600 as most labs use this rate.
    '''

    def __init__(self):
        br = 9600
        SerialPort.__init__(self, 'Arduino Uno', br)

    def sendData(self, purpose=''):
        '''send confirmation byte'''
        if self.m_port.isOpen():
            self.m_port.write(chr(0xFF))
            return True
        else:
            return False

    def readData(self):
        '''read the next four bytes from buffer'''
        if self.m_port.isOpen():
            result = self.m_port.readline()
            self.m_port.reset_input_buffer()
            return result
        else:
            return False
