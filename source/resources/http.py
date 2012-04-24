from urllib import urlopen
import md5 
import time
import string
import os
import sys
import log

class progress(object):
    def __init__(self, totalsize, fp, outfile):
        global counter
        
        self.totalsize = totalsize
        self.fp = fp
        self.received = 0
        
        for line in fp:
            outfile.write(line)
            self.received+=len(line)

            if (int(self.received)/(int(self.totalsize)/20) > counter):
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

    global url
    
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
        
        self.downloadFiles(server, root, files, tmpLocationFull)


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
        
    def createStream(self, url):
        url = urlopen(url, None, None)
        fileSize = url.info().getheader("Content-Length")
    
        if not fileSize:
            fileSize="?"

        return (url, fileSize)
    
    def download(self, inStream, outStream):
        outStream.write(inStream.read())
        outStream.close()
                
    def downloadFiles(self, server, root, files, tmpLocationFull):
        global counter

        endCounter = 0
        		
        while endCounter != len(files['file']):

            fileName = files['file'][endCounter]

            correctMD5 = files['md5'][endCounter]
            
            type = files['type'][endCounter]
            
            #fileName = os.path.basename(location)
            fileDestination = str(tmpLocationFull)+"/"+str(os.path.basename(fileName))

            outfile = open(fileDestination, "wb")

            fullLocation = "http://" + server + "/" + root + "/" + fileName

            # get remote file size                       
            url, remoteSize=self.createStream(fullLocation)
            
            sys.stdout.write("file: "+str(fileName)+" \n size: "+str(remoteSize)+"Kb ("+str(remoteSize)+" bytes)\n"); 
            sys.stdout.write(" process: ["); 
            
            # download the file
            progress(remoteSize, url, outfile)

            # get the total local file byte size 
            localSize = outfile.tell()  
                        
            # reset file download counter
            counter = 0
            
            # download completed
            sys.stdout.write("100]\n")
            
            # check if written file is of the same size as the initial file size from the ftp server
            # also check md5 hashes
            if (int(localSize) == int(remoteSize)):
                sys.stdout.write(" MD5: "); 
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
                sys.stderr.write("\n\n" + str(localSize) + " " + str(remoteSize))

            # close the downloaded file
            outfile.close()

            # close server connection
            url.close()
            
            endCounter += 1


    def getFiles(self):
        return files
     