from DataAnalysis_GP.Serial_Communication import SerialPort
import time
from DataAnalysis_GP.User_Input import usrInput

class Arduino(SerialPort):
    '''
    Receiver for Arduino device that is used in Physics 4AL
    BR is set to 9600 as most labs use this rate.
        *note: prototype class will override derived class function definitions
    '''

    def __init__(self, br = 9600):
        SerialPort.__init__(self, 'Arduino Uno', br)

    def sendData(self, purpose):
        '''
        send confirmation byte
        '''
        pass

    def readData(self):
        '''read the next four bytes from buffer'''
        if self.m_port.isOpen():
            result = self.m_port.readline()
            return result
        else:
            return False
    
    def communicate(self, purpose=0xFF):
        '''specify purpose argument for a special confirmation code'''
        receive = super().communicate(purpose)
        str_receive = ""
        for char in receive:
            str_receive += str(chr(char))
        return str_receive


if __name__ == "__main__":
    fileName = input("Specify filename: ")
    outFile = open(fileName, 'w')
    control = usrInput()
    board = Arduino(115200) # initiate the port
    while True:
        data = board.communicate()
        outFile.write(data.rstrip('\n'))
        print(data, end='')
        if 'q' in control.getInput():
            break
    outFile.close()
    board = None
    print('End of Trial')
