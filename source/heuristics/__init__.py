import os, re, commands, time 

global heuristicsPyFiles

def __init__():
    global heuristicsPyFiles

    heuristicsFolderListing = os.listdir('heuristics')        
    patternPy = re.compile("(\.py$)", re.IGNORECASE)      
    heuristicsPyFiles = [file for file in heuristicsFolderListing if patternPy.search(file) and file != '__init__.py']

# acts as a filter to all heuristics
def process(pkgSrcPath, pkgDestDir, options, commands, VERBOSE, TIMERESOURCES):
    global heuristicsPyFiles

    if VERBOSE:
        print " 4:   heuristic build "
        if TIMERESOURCES:
            print "       task started on   "+ str(time.clock())

    heuristicsModuleName = lambda file: os.path.splitext(file)[0]
    
    for heuristicPyFile in heuristicsPyFiles:
        thisHeuristic = heuristicsModuleName(heuristicPyFile)
        thisHeuristicFull = "heuristics." + heuristicsModuleName(heuristicPyFile)
        
        if VERBOSE:
            print "      found heuristic module \"" + thisHeuristic + "\""

        heuristic = loadHeuristic(thisHeuristicFull, thisHeuristic)
        return heuristic.__init__(pkgSrcPath, pkgDestDir, options, commands, VERBOSE, TIMERESOURCES)
        
        if (heuristic.getApproval() == True):
            break
        
# the magic function that took over a week to figure out.. LOL make that over 2.. damn you __import__
def loadHeuristic(heuristicLocation, heuristicModule):
    try:
        module = __import__(heuristicLocation, "", "", heuristicModule, -1)
    except ImportError:
        return None
        
    return module


__init__()



