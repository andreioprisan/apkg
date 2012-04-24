import ftplib
import md5
import time
import string
import os
import sys 
import log

class progress(object):
    def __init__(self, totalsize, fp):
        self.totalsize = totalsize
        self.fp = fp
        self.received = 0
    
    def __call__(self, data):
        global counter
        self.fp.write(data)
        self.received += len(data)
        if self.received/(self.totalsize/20) > counter:
            if counter % 2 == 0:
                sys.stdout.write(str(counter * 5))
            else:
                sys.stdout.write("  ")
            counter += 1

class downloadResources():
    global counter
    counter = 0
        
    global VERBOSE
    VERBOSE = True
    
    global TIMERESOURCES
    TIMERESOURCES = True

    global ftp
    
    global size
    
    global files
    files = {}
    
    global server 
    server = []
    
    global root
    root = []
    
    global location
    location = []
    
    global tags
    tags = []
            
    global tmpLocationFull
    
    
    def __init__(self, server, root, location, files, tmpLocationFull, VERBOSE, TIMERESOURCES):
        self.server = server
        self.root = root
        self.location = location
        self.files = files
        self.tmpLocationFull = tmpLocationFull        
        self.VERBOSE = VERBOSE
        self.TIMERESOURCES = TIMERESOURCES
                
        log.setLog("infoLog")        

        self.connectFtp(server)
        self.downloadFiles(root, location, files, tmpLocationFull)
        self.closeFtp()


    def getMD5(self, file):
        BLOCKSIZE = 1024*1024
        f = open(file, "rb")
        sum = md5.new()
        while 1:
            block = f.read(BLOCKSIZE)
            if not block:
                break
            sum.update(block)
        f.close()
        return sum.hexdigest()
        
    def connectFtp(self, server):
        self.ftp = ftplib.FTP(server)
        self.ftp.connect()
        self.ftp.login()

    def downloadFiles(self, root, location, files, tmpLocationFull):
        global counter
        
        endCounter = 0
        while endCounter != len(files['file']):

            fileName = files['file'][endCounter]

            correctMD5 = files['md5'][endCounter]            

            type = files['type'][endCounter]
            
            #fileName = os.path.basename(location)
            fileDestination = str(tmpLocationFull)+"/"+str(os.path.basename(fileName))
            
            # enter the correct folder on the ftp folder
            
            if type == "patch":
                self.ftp.cwd(str("/" + root + "/" + location + "/"))
            elif type == "archive":
                self.ftp.cwd(str("/" + root + "/"))
                        
            # get remote file size           
            remoteSize = self.ftp.size(fileName)
    
            sys.stdout.write("        file: "+fileName+" \n         size: "+str(remoteSize/1024)+"Kb ("+str(remoteSize)+" bytes)\n"); 
            sys.stdout.write("         process: ["); 
            
            # open an empty file to destination
            file = open(str(fileDestination), 'wb')
                
            # download the file
            w = progress(remoteSize, file)
            self.ftp.set_pasv(0)        
            self.ftp.retrbinary('RETR %s' % fileName, w, 32768)
    
            # get the total local file byte size 
            localSize = file.tell()  
            # close the downloaded file
            file.close()
            
            # reset file download counter
            counter = 0
            
            # download completed
            sys.stdout.write("100]\n")
            
            # check if written file is of the same size as the initial file size from the ftp server
            # also check md5 hashes
            if localSize==remoteSize:
                sys.stdout.write("         MD5: "); 
                currentMD5 = self.getMD5(fileDestination)
                if cmp(currentMD5, correctMD5) == 0:
                    sys.stdout.write("verified\n")
                else:
                    sys.stderr.write("\n\n")
                    sys.stderr.write("> fatal error: The downloaded file "+str(fileName)+" does not have matching MD5 digests.\n")
                    sys.stderr.write("               Expected: "+str(correctMD5)+"\n")
                    sys.stderr.write("               Received: "+str(currentMD5)+"\n")
                    sys.stderr.write("\n\n")
            else:
                sys.stderr.write("\n\n")
                sys.stderr.write("> fatal error: The downloaded file size is different than the one reported by the ftp server.\n")
                sys.stderr.write("\n\n")
                
            endCounter += 1
         

    def closeFtp(self):
        self.ftp.close()
       
    def getFiles(self):
        return files
     