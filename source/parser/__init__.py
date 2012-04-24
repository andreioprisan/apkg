import os, sys, re, commands, time 
import log

def a():
    return "a"

def __init__():
    # initialize logging profile
    log.setLog("infoLog")

# load module function        
def loadModule(location, module):
    try:
        module = __import__(location, "", "", module, -1)
    except ImportError:
        log.critical(ImportError)
        return None
        
    return module

    
def reader(xmlConfigFile, VERBOSE, TIMERESOURCES):
    # load XML parser        
    resource = loadModule("parser.reader", "reader")

    #print str(xmlConfigFile) + " " + str(VERBOSE) + " " + str(TIMERESOURCES)
    return resource.__init__(xmlConfigFile, VERBOSE, TIMERESOURCES)
    #resource.readMe(xmlConfigFile)
    
    
def writer(xmlConfigFileIn, xmlConfigFileOut, VERBOSE, TIMERESOURCES):
    resource = loadModule("parser.writer", "writer")
    resource.__init__(xmlConfigFileIn, xmlConfigFileOut, VERBOSE, TIMERESOURCES)
    




