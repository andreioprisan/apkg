# filename: $exporterShortName.py
# "rpm" export module, version 1.0 

import string

import os
import os.path
import sys

import log
# pattern matching
import re

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
        
        
        fileDescriptor.write("Summary: " + str(resources['pkgDescriptorInformation']['summary']) + "\n")
        fileDescriptor.write("Name: " + str(resources['pkgDescriptorFormal']['pkgName']) + "\n")
        fileDescriptor.write("Version: " + str(resources['pkgDescriptorFormal']['pkgVersion']) + "\n")
        fileDescriptor.write("Revision: " + str(resources['pkgDescriptorFormal']['pkgRevision']) + "\n")
        fileDescriptor.write("Copyright: " + str(resources['pkgDescriptorInformation']['license']) + "\n")
        
        categoryDetails = str(resources['pkgDescriptorDistribution']['categoryMinor']) + "/" + str(resources['pkgDescriptorDistribution']['categoryMajor'])
        if categoryDetails.strip() != "/":
            fileDescriptor.write("Group: " + str(resources['pkgDescriptorDistribution']['categoryMajor']) + "\n")
        
        # make source and patch list
        resourcesCounter = 0
        resourcesCount = len(resources['pkgBuildResourceFiles']['file']) - 1
        fileType = resources['pkgBuildResourceFiles']['type'][0]
        if resourcesCount == 0:
            fileType = resources['pkgBuildResourceFiles']['type'][0]
            if fileType == "archive":
                fileRemoteLocation = str(resources['pkgBuildResourceInformation']['protocol']) + "://" + str(resources['pkgBuildResourceInformation']['server']) + "/" + str(resources['pkgBuildResourceInformation']['root']) + "/"  
                fileDescriptor.write("Source: " + str(fileRemoteLocation) + "" + str(resources['pkgBuildResourceFiles']['file'][resourcesCounter]) + "\n")
            elif fileType == "patch":
                fileRemoteLocation = str(resources['pkgBuildResourceInformation']['protocol']) + "://" + str(resources['pkgBuildResourceInformation']['server']) + "/" + str(resources['pkgBuildResourceInformation']['root']) + "/" + str(resources['pkgBuildResourceInformation']['location']) + "/"  
                fileDescriptor.write("Patch: " + str(fileRemoteLocation) + "" + str(resources['pkgBuildResourceFiles']['file'][resourcesCounter]) + "\n")
        else:
            for fileType in resources['pkgBuildResourceFiles']['type']:
                if fileType == "archive":
                    fileRemoteLocation = str(resources['pkgBuildResourceInformation']['protocol']) + "://" + str(resources['pkgBuildResourceInformation']['server']) + "/" + str(resources['pkgBuildResourceInformation']['root']) + "/"  
                    fileDescriptor.write("Source" + resourcesCounter + ": " + str(fileRemoteLocation) + "" + str(resources['pkgBuildResourceFiles']['file'][resourcesCounter]) + "\n")
                elif fileType == "patch":
                    fileRemoteLocation = str(resources['pkgBuildResourceInformation']['protocol']) + "://" + str(resources['pkgBuildResourceInformation']['server']) + "/" + str(resources['pkgBuildResourceInformation']['root']) + "/" + str(resources['pkgBuildResourceInformation']['location']) + "/"  
                    fileDescriptor.write("Patch" + resourcesCounter + ": " + str(fileRemoteLocation) + "" + str(resources['pkgBuildResourceFiles']['file'][resourcesCounter]) + "\n")
                resourcesCounter += 1
                
        fileDescriptor.write("BuildRoot: /var/tmp/%{name}-%{version}-%{revision}-buildroot\n\n")

        # description
        fileDescriptor.write("%description\n\n")
        fileDescriptor.write(resources['pkgDescriptorInformation']['description'] + "\n\n")

        fileDescriptor.write("%prep\n")
        fileDescriptor.write("%setup -q\n\n")
        fileDescriptor.write("%build\n")

        # write the commands
        for command in commands:
            if len(re.findall('(.*)./configure(.*)', command)) != 0:
                fileDescriptor.write(command + "\n")
            if len(re.findall('(.*)make(.*)install(.*)', command)) == 0 and len(re.findall('(.*)make(.*)', command)) != 0:
                fileDescriptor.write(command + "\n")
            if len(re.findall('(.*)make(.*)install(.*)', command)) != 0:
                fileDescriptor.write("\n%makeinstall\n")
        
        fileDescriptor.write("\n%changelog\n- generated by apkg 0.7 - heuristic [automake] 1.0\n")
        
        # close file
        fileDescriptor.close()
                