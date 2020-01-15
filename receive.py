import SerialComm as ser
import time

if __name__ == "__main__":
    board = ser.Arduino()
    while True:
        print(board.communicate())
        time.sleep(1)
    pass
