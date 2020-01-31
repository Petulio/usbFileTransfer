# **Automated usb file transfer**
A project where a Raspberri Pi 3 is used to automate a process of downloading specific files from a external USB-device and uploading them to the cloud.
### The idea behind the chain:
* Make the raspberry pi execute a script when a USB-device is inserted
* Get the script to search for specific files and download them to a folder inside the raspberry pi
* Upload the files to a server via sftp
### The actual steps:
1. **Udev rule** -> triggered by USB insert, executes service file in systemd
2. **Service file** -> executes shell script 1
3. **Shell script 1** -> executes shell script 2 as Pi 
4. **Shell script 2** -> executes python script 
5. **Python script** -> does the task of copying files and uploading them
# Getting started
### Set up the Raspberry Pi 
* [Easy-to-follow installation guide](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) - A complete guide for setting up the RP
* [Setup list](https://www.raspberrypi.org/documentation/setup/) - A list with what you will need
* [Software download](https://www.raspberrypi.org/downloads/) - The download page for the software
# Create a udev-rule
* Udev is the device manager for the Linux kernel
* It allows you to identify devices based on their properties and it allows for rules that specify what name is given to a device. By creating your own rules you can set udev to run/execute a script or .service files when a usb-device is connected and mounted.
* Read through ***[THIS](https://linuxconfig.org/tutorial-on-how-to-write-basic-udev-rules-in-linux)*** tutorial about udev rules before proceeding.

**_Remember to run terminal as root in all the coming steps, as explained in the link above!_**
### Directory:
Use preferred text editor and create a new file in directory below
```
nano /etc/udev/rules.d/<file_name>.rules
```
### Inside the rule:
Set the rule to react everytime any usb-unit is added and mounted:
```
ACTION=="add", ATTRS{idVendor}=="****", ATTRS{idProduct}=="****", ENV{SYSTEMD_WANTS}="<file_name>.service" 
```
 If you wish for the rule to react to specific devices then you have to change:
```
****
``` 

It is important to set the udev rule to trigger a [systemd](https://www.linux.com/tutorials/understanding-and-using-systemd/) unit file since the [RUN](https://linux.die.net/man/7/udev) command only can be used for short runnings tasks. That is why
```
ENV{SYSTEMD_WANTS}="<file_name>.service"
```
is used in the udev rule. 
<br/><br/>***Remember that the service file is not yet created, in the next step we will look at how to create one.***
# Create a systemd unit file
Use preferred text editor and create a new file in below directory
```
nano /etc/systemd/system/<file_name>.service
```
***It is important that the name matches the one written in the udev rule***
### Inside the service file:
Set the file to execute a desired script. In this case the **first** of the two shell scripts 
```
[Unit]
Description=<file_description>

[Service]
Type=simple
ExecStart=/home/pi/<trigger_script1>.sh %I
```
**In the next step we will look at how to create the scripts**
# Create two shell scripts
In this example the scripts will be created in the users home directory
```
nano /home/pi/<trigger_scriptX>.sh
```
### Inside the **first** shell script:
Set the script to execute another shell script, **but as a regular user (Pi)**. This is done to avoid future problems with permissions
```
#! /bin/bash
/bin/su -c "/home/pi/trigger_script2.sh" - pi
```
### Inside the **second** shell script:
Set the script to execute the python script
```
#! /bin/bash 
/usr/bin/python3 /home/pi/<python_script>.py 
```
***Remember to always match all the script names or else they won't be executed***
# The Python script
The python script can be developed in several different IDE's and OS's. My script was developed in VScode, running on macOS High Sierra, and it can be found in the link below.<br/>
### Some important notes:
* This is where most of the work will be done: searching, copying, downloading and uploading
* Raspbian comes with both python 2 & 3 pre-installed by default (Lite version only comes with python 2).
* Python 3 is used in this project
* SFTP is used for the upload
### Directory:
```
/Home/Pi/<python_script>.py
```
* [Link to my script](https://github.com/Petulio/usbFileTransfer/blob/master/copy_from_usb.py)

# SFTP
### SHH
* To be able to use sftp you have to have your own set of SSH-keys in the RP
* [A brief tutorial on how to manage SSH on RP](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)

To check if a SSH directory already exists type the following
```
ls ~/.ssh
```
To create a new pair of keys 
```
ssh-keygen -t rsa -b 4096 -C "<your_email_address>" -m PEM
```
***It is important to use above format since the python library [Paramiko](https://github.com/paramiko/paramiko) doesn't support openSSH formatted private keys, which in recent Unix-based operating systems is the default format. Since pysftp is based on this library it inherits this issue.***

* Read more about the issue [here](https://github.com/paramiko/paramiko/issues/1313) and [here](https://github.com/paramiko/paramiko/pull/1343)

### Pysftp
The python library [pysftp](https://pypi.org/project/pysftp/) was used for handling the upload of the files via SFTP. To install it enter the command below in the terminal
```
pip3 install pysftp
```
* [More info about the library and how to use it](https://pysftp.readthedocs.io/en/release_0.2.9/)


# Testing
First of all it is important to reload both the udev rules and the systemd files
```
udevadm control --reload-rules
```
```
systemctl daemon-reload
```
After this you should be ready to go. Just insert any USB-device to a port and wait to see if the files have been copied and uploaded. 
<br/><br/>***If something isn't working then double check that all the script names matches the ones to be executed. Alternatively make your scripts flag all the steps to see where the process dies.***