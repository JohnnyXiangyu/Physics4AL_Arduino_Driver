from SerialComm import Arduino
import time
from Msvcrt_Input import usrInput

if __name__ == "__main__":
    fileName = input("Specify filename: ")
    outFile = open(fileName, 'w')
    control = usrInput()
    board = Arduino() # initiate the port
    while True:
        data = board.communicate()
        outFile.write(data.rstrip('\n'))
        print(data, end='')
        if control.getInput() == 2:
            break
    outFile.close()
