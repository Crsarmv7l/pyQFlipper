#!/usr/bin/python3

import sys
import os
import time
import serial
import serial.tools.list_ports

mainlst = ["Upload to Flipper", "Download from Flipper", "Rename on Flipper", "Delete from Flipper", "Exit"]
lst = ["subghz", "nfc", "lfrfid", "infrared", "ibutton", "badusb"]
file_extensions =[".sub", ".nfc", ".rfid", ".ir", "ibtn",".txt"]

def list(menulist, ret):
    os.system('clear')
    splash()
    output = ""
    i = 1
    for item in menulist:
        output = ""
        if ret == 1:
            output = "Upload to "
        elif ret == 2:
            output = "Download from "
        elif ret == 3: 
            output = "Rename in "
        elif ret == 4:
            output = "Delete from "
        print(str(i) + ". " + output + item)
        i+=1
    return i-1
          
def menu(ret):
    if ret == 0:
        i = list(mainlst, ret)
    else:
        i = list(lst, ret)
    selection = input("\nEnter Selection Number: ")
    if not selection.isnumeric() or i < int(selection) < 0:
        selection = 0
        print("Invalid Selection, returning to Main Menu")
        time.sleep(1)
    return (int(selection))

def find_device():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in ports:
        if desc.find("Flipper") != -1:
            return(port)
    #if we pass the for loop its not there
    print("Flipper not found")
    sys.exit()
        
def flipper_check(filename, filelist):
    onflipperflg = False
    for item in filelist:
        if item.find(".") != -1 and item.find(filename) != -1:
            onflipperflg = True
            filename = item
            break
    return onflipperflg, filename

def host_check(path, filename):
    onhostflg = False
    for x in os.listdir(path):
        if x[x.find("."):] in file_extensions:
            if x.find(filename) != -1:
                onhostflg = True
                filename = x
                break
    return onhostflg, filename
    

def show_files(file):
    for item in file:
        if item[item.find("."):] in file_extensions:
            print(item)
            
def splash():  
    print(r"""    
                  ______ _ _                       
                  │  ___│ (_)                      
 _ __  _   _  __ _│ │_  │ │_ _ __  _ __   ___ _ __ 
│ '_ ╲│ │ │ │╱ _` │  _│ │ │ │ '_ ╲│ '_ ╲ ╱ _ ╲ '__│
│ │_) │ │_│ │ (_│ │ │   │ │ │ │_) │ │_) │  __╱ │   
│ .__╱ ╲__, │╲__, ╲_│   │_│_│ .__╱│ .__╱ ╲___│_│   
│ │     __╱ │   │ │         │ │   │ │              
│_│    │___╱    │_│         │_│   │_│ 

By: L0rdDaikon
The Pirates Plunder, find us on Discord
""")

def main():
    flipper = Serial()
    while True:
        flipper.open()
        ret = menu(0)
        if ret >= len(mainlst):
            break
        elif ret != 0:
            selection = menu(ret)
            if selection != 0 and selection < len(lst):
                selection = selection -1
                flipperpath = "/ext/"
                localpath = os.getcwd() + "/"
                if ret == 1:
                    os.system('clear')
                    print("Files available to upload:\n")
                    for x in os.listdir(localpath):
                        if x[x.find("."):] in file_extensions:
                            print(x)
                    filename = input("\nEnter Filename to Upload (or exit): ")
                    if filename.upper() == "EXIT":
                        pass
                    else:
                        check1, filename = host_check(localpath, filename)
                        if check1:
                            files = flipper.get_files("storage list " + flipperpath + lst[selection])
                            check2, null = flipper_check(filename, files)
                            if not check2:
                                flipper.upload(localpath + filename, flipperpath + lst[selection] + "/" + filename)
                                flipper.close()
                                time.sleep(1)
                            else:
                                print("The File already exists on the Flipper")
                                time.sleep(1)
                        else:
                            print("File does not exist locally")
                            time.sleep(1)         
                elif ret == 2:
                    os.system('clear')
                    print("Files Available for Download in " + lst[selection] + ":\n" )
                    files = flipper.get_files("storage list " + flipperpath + lst[selection])
                    show_files(files)
                    filename = input("\nEnter Filename to Download (or exit): ")
                    if filename.upper() == "EXIT":
                        pass
                    else:
                        check1, filename = flipper_check(filename, files)
                        if check1:
                            check2, null = host_check(localpath, filename)
                            if not check2:
                                flipper.download(localpath + filename, flipperpath + lst[selection] + "/" + filename)
                                flipper.close()
                                time.sleep(1)
                            else:
                                print("The File already exists locally")
                                time.sleep(1)
                        else:
                            print("The File does not exist on the Flipper")
                            time.sleep(1)
                elif ret == 3:
                    os.system('clear')
                    print("Files Available for Rename in " + lst[selection] + ":\n" )
                    files = flipper.get_files("storage list " + flipperpath + lst[selection])
                    show_files(files)
                    ogfilename = input("\nEnter Filename to Rename (or exit): ")
                    if ogfilename.upper() == "EXIT":
                        pass
                    else:
                        check1, filename = flipper_check(ogfilename, files)
                        if check1:
                            newfilename = input("\nEnter New Filename: ")
                            check2, null = flipper_check(newfilename, files)
                            if check2:
                                print("The new Filename already exists on the Flipper")
                                time.sleep(1)
                            else:
                                if newfilename.find(".") == -1:
                                    newfilename = newfilename + filename[filename.find("."):]
                                cmd = "storage rename " + flipperpath + lst[selection] + "/" + filename + " " + flipperpath + lst[selection] + "/" + newfilename + "\r"
                                flipper.write(cmd.encode())
                                print("Renamed " + lst[selection] + " file " + ogfilename + " to " + newfilename)
                                time.sleep(1)
                        else:
                            print("The File does not exist on the Flipper")
                            time.sleep(1)
                elif ret == 4:
                    os.system('clear')
                    print("Files Available for Delete in " + lst[selection] + ":\n" )
                    files = flipper.get_files("storage list " + flipperpath + lst[selection])
                    show_files(files)
                    filename = input("\nEnter Filename to Delete (or exit): ")
                    if filename.upper() == "EXIT":
                        pass
                    else:
                        check1, filename = flipper_check(filename, files)
                        if check1:
                            cmd = "storage remove " + flipperpath + lst[selection] + "/" + filename + "\r"
                            flipper.write(cmd.encode())
                            print("Removed " + filename + " from " + lst[selection])
                            time.sleep(1)
                        else:
                            print("The File does not exist on the Flipper")
                            time.sleep(1)
                    
    time.sleep(1)
    flipper.close()
    os.system('clear')
    sys.exit()    
    
class Serial():
    def __init__(self, port=find_device(), baudrate=230400):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.open()
        self.ser.write("\n\n\r".encode())
        self.ser.read_until(b'>:') 

    def open(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            time.sleep(0.5)
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=None)
        except serial.SerialException as e:
            print("Error opening serial port:", e)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'\x03')
            self.ser.close()
                    
    def flush(self):
        while self.ser.inWaiting() > 0:
            a = self.ser.read(1)
            
    def upload(self, localpath, flipperpath):
        if self.ser and self.ser.is_open:
            with open(localpath, "r") as file:
                data = file.read()
                file.close()
            data = data.split("\n")
            cmd = "storage write " + flipperpath + "\r"
            self.ser.write(cmd.encode())
            for part in data:
                part = part + "\n"
                self.ser.write(part.encode())
                self.flush()
            print("Wrote to " + flipperpath)
            
    def download(self, localpath, flipperpath):
        if self.ser and self.ser.is_open:
            cmd = "storage read " + flipperpath + "\r"
            self.ser.write(cmd.encode())
            for i in range(2):
                self.ser.readline()
            time.sleep(0.4)
            file = ""
            while self.ser.inWaiting() > 0:
                a = self.ser.read(1).decode()
                file += a
            if file[-3:] == ">: ":
                file = file[:-6]
            f = open(localpath, "w")
            f.write(file)
            f.close()
            print("Wrote to " + localpath)
        
    def get_files(self, payload):
        if self.ser and self.ser.is_open:
            payload = payload + "\r"
            length= len(payload) + 4
            self.ser.write(payload.encode())
            time.sleep(0.5)
            files = ""
            while self.ser.inWaiting() > 0:
                a = self.ser.read(1).decode()
                files += a
            files = files[length:-3]
            files = files.split(" ")
            return files
            
    def write (self, data):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(data)
            except serial.SerialException as e:
                print("Error sending data:", e)    

if __name__ == '__main__':
    main()
