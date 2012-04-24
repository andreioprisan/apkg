import os, re, commands, time
import log 

def __init__():
    log.setLog("infoLog")
    
# acts as a filter to resource handlers
def download(resourceType, server, root, location, files, tmpLocationFull, VERBOSE, TIMERESOURCES):

    if (resourceType == "ftp"):
        pyFile = "ftp.py"
    elif (resourceType == "http"):
        pyFile = "http.py"
        
    moduleName = lambda file: os.path.splitext(file)[0]
        
    thisResource = moduleName(pyFile)
    thisResourceFull = "resources." + moduleName(pyFile)
        
    resource = loadModule(thisResourceFull, thisResource)
    
    if VERBOSE:
        log.info(" 2:   download resources")
        log.info("       task started on "+ str(time.clock()))    

    resource.downloadResources(server, root, location, files, tmpLocationFull, VERBOSE, TIMERESOURCES)
    
    if VERBOSE:
        log.info("       task ended on   "+ str(time.clock()))
        log.info(" 2:   completed")

        
# the magic function that took over a week to figure out.. LOL make that over 2.. damn you __import__
def loadModule(location, module):
    try:
        module = __import__(location, "", "", module, -1)
    except ImportError:
        return None
        
    return module





