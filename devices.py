from DataAnalysis_GP.Serial_Communication import SerialPort, PortError
import multiprocessing
import time
import os


class Error(Exception):
    pass


class DeviceError(Error):
    def __init__(self, message):
        self.message = message


class SerialTextDevice:
    """
    Serial port device that return output in text format.  
    Supported operations: connect, start, stop, read, write  
    This class uses multiprocessing to implement because readings from serial port is discrete.  
    (There's no guarantee that driver code (the server) and a text serial device is synchronized.)
    """

    def __init__(self, name):
        self.name = name
        # self.port = None

        # container for the child process which updates active buffer
        self.child_process = None

        self.child_pipe = None      # buffer that's written by child process
        self.parent_pipe = None

        self.active_buffer = []     # buffer to be flushed

        self.is_active = False         # start = true, end = false
        # timer that records the starting time (in seconds)
        self.timer = 0.0

        # some formatting related issues
        self.extra_timestamp = False
        self.delimiter = ","

    # def connectDevice(self, details={"name": "", "br": 9600}, extra_timestamp=False, delimiter=","):
    #     """
    #     Create a port instance and put into self.port.  
    #     Details (name of instance, name of device and baud rate for serial device) will be passed by a dictionary.  
    #     Current flushing strategy: let child process delay and flush.  
    #     extra_timestamp option gives user flexibility over whether to add a driver code timestamp or not  
    #     """
    #     self.port = SerialPort(details['name'], details['br'])
    #     if self.port.m_port == None:
    #         err_text = self.port.m_error  # report error from port
    #         # deallocate the port (let port definition do the freeing work)
    #         self.port = None
    #         raise(PortError(err_text))
    #     else:
    #         self.extra_timestamp = extra_timestamp
    #         self.delimiter = delimiter
    #         self.port.m_port.close()
    #         return 'connect-success'  # return a success message

    def __del__(self):
        self.reset()

    def reset(self):
        """
        Free the following resources:  
            child process (if there is one)
            serial port instance (if there is one)
        It's supposed to put device instance into its initial state
        """
        self.endTrial()
        self.port = None

    def readPort(self, details={"name": "", "br": 9600}, extra_timestamp=False, delimiter=","):
        """
        Read data from port.  
        For serial text device, it reads a line and put it into the buffer.  
        All read data will be converted to string for a serial text device.  
        """
        self.parent_pipe.close()
        port = SerialPort(details['name'], details['br'])
        if port.m_port == None:
            err_text = port.m_error  # report error from port
            # deallocate the port (let port definition do the freeing work)
            port = None
            raise(PortError(err_text))
        else:
            self.extra_timestamp = extra_timestamp
            self.delimiter = delimiter

        time.sleep(0.1)
        port.flushInput()
        self.child_pipe.send('child-started')
        while True:
            new_data = port.readline()
            new_line = ""
            for byte in new_data:
                new_line = new_line + str(chr(byte))
            try:
                self.child_pipe.send((time.time() - self.timer, new_line))
            except BrokenPipeError:
                # when the other end is closed
                print('parent pipe closed: exiting')
                self.child_pipe.close()
                port.m_port.close()
                break
        return

    def startTrial(self, details={"name": "", "br": 9600}, extra_timestamp=False, delimiter=","):
        """
        Record current time in timer.  
        Then pipe and create child process that writes into active buffer.
        Child process will write a message into pipe before it starts looping.    
        """
        self.timer = time.time()
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        self.child_process = multiprocessing.Process(target=self.readPort, args=(details, extra_timestamp, delimiter))
        self.child_process.start()
        
        # block-wait for the child process to start properly
        try:
            start_message = self.parent_pipe.recv()
        except EOFError:
            raise(DeviceError('child process failed to start'))
        if start_message != 'child-started':
            raise(DeviceError('child process failed to start'))
        else:
            self.is_active = True
            self.child_pipe.close()

    def endTrial(self):
        """
        Interrupt reading.  
        This function call is designed to be end of a trial:  
            reset active buffer to empty, and return its previous contents  
            close parent pipe, join child process, then set pipes and child process to None  
        Finally it will return the latest version of active buffer  
        """
        if self.is_active:
            self.parent_pipe.close()
            print('wait...')
            self.child_process.join()
            print('joined...')
            temp_buffer = self.active_buffer.copy()
            self.active_buffer = []
            self.child_process = None
            self.is_active = False
            return temp_buffer

    def outputData(self):
        """
        Copy current pipe buffer over to a local copy, append them to active buffer,  
        Then return this array-of-strings.  
        """
        # TODO: trying to receive all tuples from the pipe
        new_lines = []
        while self.parent_pipe.poll():
            new_lines.append(self.parent_pipe.recv())

        # format a list of output strings (including stripping all newlines)
        if new_lines != []:
            new_outputs = []
            for line in new_lines:
                # disassemble the tuple first
                new_timestamp, new_string = line
                if self.extra_timestamp:
                    new_string = str(new_timestamp) + self.delimiter + new_string
                new_string = new_string.strip('\r\n')
                new_outputs.append(new_string)
            self.active_buffer.append(new_outputs)
            return new_outputs
        else:
            return None
