# filename: $exporterShortName.py
# "raw" export module, version 1.0 

import string
import os
import os.path
import sys
import log

class parseBuild():        
    global exportFile 
    exportFile = ""
    
    global commands
    commands = {}
    
    global resources
    resources = {}
 
    global VERBOSE
    VERBOSE = True
    
    global TIMERESOURCES
    TIMERESOURCES = True   
    
    def __init__(self, exportFile, commands, resources, VERBOSE, TIMERESOURCES):
        self.exportFile = exportFile
        self.commands = commands
        self.resources = resources        
        self.VERBOSE = VERBOSE
        self.TIMERESOURCES = TIMERESOURCES
                
        log.setLog("infoLog")        

        self.doExport(exportFile, commands, resources, VERBOSE, TIMERESOURCES)


    def doExport(self, exportFile, commands, resources, VERBOSE, TIMERESOURCES):
        
        if os.access(exportFile, os.W_OK):
            if os.path.exists(exportFile):
                if os.path.isfile(exportFile):
                    os.remove(exportFile)
                
        # open file for writing
        fileDescriptor = open(exportFile, 'w')
        
        for key in resources.keys():
            writeMe = key + ": " + str(resources[key])
            fileDescriptor.write(writeMe + "\n")

        # write the commands
        for command in commands:
            fileDescriptor.write("run: " + command + "\n")
        
        # close file
        fileDescriptor.close()
                