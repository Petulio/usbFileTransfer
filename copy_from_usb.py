import os
import pysftp
from shutil import copy

class FileUploader(object):

    def __init__(self, source, destination, host, port, username, private_key):
        self.source = source
        self.destination = destination
        self.host = host
        self.port = port
        self.username = username
        self.private_key = private_key
        
        self.cnopts = pysftp.CnOpts()
        # This is done to avoid an error during development, but is not recommended since it makes you vulnareble
        # to man in the middle attacks!
        self.cnopts.hostkeys = None  

    def copy_file(self):
        scr_files = os.listdir(source)
        for file_name in scr_files:
            full_file_name = os.path.join(self.source, file_name)
            if "" in full_file_name: #Fill in a character (or number) that the script should look for in the file name
                copy(full_file_name, self.destination)

    def transfer_status(self, x, y):
        promille_done = round(x/y*10000)
        times_to_print = 1000
        if promille_done % times_to_print == 0:
            print("{} '%' complete".format(round(x/y*100)))

    def upload(self):
        with pysftp.Connection(
                host=self.host, port=self.port, username=self.username, cnopts=self.cnopts, private_key=self.private_key
            ) as sftp:
            dest_files = os.listdir(destination)
            for file_name in dest_files:
                full_file_name = os.path.join(self.destination, file_name)
                if "" in full_file_name: #Fill in a character (or number) that the script should look for in the file name
                    print('Sending file:', full_file_name)
                    sftp.put(full_file_name, preserve_mtime=True, callback=lambda x,y: self.transfer_status(x,y))
                    print('Sent file:', full_file_name)
                    print('-----------------------------------------------------------------------------------------')


source = '' # Folder where to search and collect the file/files from the USB
destination = '' # Destination folder for the collected files
host = '' # Address (URL, IP) of server/cloud etc.
port = # The port number that should be used on the Host
username = '' # Your username on the host 
private_key = '' # Location/folder of the private key on the local device/computer

file_uploader = FileUploader(source, destination, host, port, username, private_key)
file_uploader.copy_file()
file_uploader.upload()