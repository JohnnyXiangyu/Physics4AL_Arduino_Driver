import devices 
import time 
from DataAnalysis_GP.User_Input import usrInput

if __name__ == '__main__':
    fileName = input("Specify filename: ")

    board = devices.SerialTextDevice('my device') # initiate the device
    board.startTrial(details={"name": "Arduino", "br": 9600})

    outFile = open(fileName, 'w')
    control = usrInput()
    while True:
        data = board.outputData()
        if data != None:
            for line in data:
                # outFile.write(line)
                print(line)
        if 'q' in control.getInput():
            break
    outFile.close()
    board = None
    print('End of Trial')
