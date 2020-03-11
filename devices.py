from DataAnalysis_GP.Serial_Communication import SerialPort


class SerialTextDevice:
    """
    Serial port device that return output in text format.  
    Supported operations: connect, start, stop, read, write  
    """

    def __init__(self):
        self.name = ""
        self.port = None

        self.child_process = None  # container for the child process which updates active buffer
        self.pipe_buffer = [] # buffer that's written by child process
        self.active_buffer = []  # buffer to be flushed
        self.old_buffer = []  # buffer that's already flushed

        self.active = False  # start = true, end = false
        self.timer = 0  # timer that records the starting time

    def connectDevice(self, details={"name": "", "deviceName": "", "baudRate": 9600}, flush_delay=0.1):
        """
        Create a port instance and put into self.port.  
        Details (name of instance, name of device and baud rate for serial device) will be passed by a dictionary.  
        Current flushing strategy: delay a certain number of seconds and flush.  
        """
        pass

    def disconnectDevice(self):
        """
        Close self.port  
        """
        pass

    def startReading(self):
        """
        Flush the port, record current time in timer.  
        Then pipe and create child process that writes into active buffer.  
        Without a endReading() call, the program should keep pushing data into the buffer.  
        """
        pass

    def endReading(self):
        """
        Interrupt reading.  
        This function call is designed to be end of a trial:  
            both local buffers are cleared
            pipe will be closed and destructed  
            child process terminated by sending a eof signal  
        """
        pass

    def flushToFile(self):
        """
        Copy the current active buffer over to old buffer, output the contents to file.  
        Then pop all written contents in active buffer.  
        """
        pass 

    def outputData(self):
        """
        Copy current pipe buffer over, append them to active buffer,  
        Then return this array-of-strings.  
        """
        pass

