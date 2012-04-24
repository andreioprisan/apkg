import os, re, commands, time 
import log

def __init__():
    log.setLog("infoLog")
    
# acts as a filter to resource handlers 
def parseResults(exportType, exportFile, commands, resources, VERBOSE, TIMERESOURCES):

    if (exportType == "raw"):
        pyFile = "raw.py"
    elif (exportType == "rpm"):
        pyFile = "rpm.py"        
    elif (exportType == "xml"):
        pyFile = "xml.py"
    elif (exportType == "sh"):
        pyFile = "sh.py"
        
        
    moduleName = lambda file: os.path.splitext(file)[0]
        
    thisResource = moduleName(pyFile)
    thisResourceFull = "export." + moduleName(pyFile)
        
    exportMethod = loadModule(thisResourceFull, thisResource)
    
    if VERBOSE:
        log.info(" 5:   export build resources")
        log.info("       task started on "+ str(time.clock()))    

    exportMethod.parseBuild(exportFile, commands, resources, VERBOSE, TIMERESOURCES)
    
    if VERBOSE:
        log.info("       task ended on   "+ str(time.clock()))
        log.info(" 5:   completed")

        
# the magic function that took over a week to figure out.. LOL make that over 2.. damn you __import__
def loadModule(location, module):
    try:
        module = __import__(location, "", "", module, -1)
    except ImportError:
        return None
        
    return module





