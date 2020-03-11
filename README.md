# Arduino General-Purpose Template  

To avoid the trouble that inlcude path has to be configured everytime a new assignment is created, I made this template that reflects only my computer's file structure, especially location of Arduino app.  
This template contains mainly just appropriate configuration files that might help during the course Physics 4AL, UCLA W2020, in the way that they enable intellisense within VSCode. Install Arduino first before any of the json files can work!  

## Note

These files are created in Windows 10, so they use CRLF endings.  

## TODO

### Create a react app that enable most of the operations for this app

### Design backend API for the following operations

Connect device (generate custom class, might need to modify device classes)  
Read data (timing will be controlled by frontend app, it'll send request for data in each cycle)  
Start/end trial, mark event (user input taken by frontend, and an API takes that to backend)  

### Backend maintains 2 buffers

One volatile, used for API reads, the other is a larger and idle data structure that store all data so far.  
On finish, both will be destroyed.  

### Abstraction for device that implement the following

* manual connecting

* manual disconnecting

* start data collection (which should keep running)

* end data collection (stop receiving data)

* buffer for raw data

* API that translate each data line to a common interface

### Figure out how to start the app with a webpage
