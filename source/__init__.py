# apkg.py -- abstract package tree
# Copyright 2008 apkg.org
# Distributed under the terms of the GNU General Public License v2

# apkg release information
VERSION="0.7"
COPYRIGHT = "Copyright 2008 apkg.org"
COPYRIGHT2 = "Distributed under the terms of the GNU General Public License v2"
AUTHOR = "Andrei Oprisan"
AUTHOREMAIL = "andrei@apkg.org"
BUGTRACK = "http://apkg.org/bugtrack"

# debug verbosity
global VERBOSE 
VERBOSE = True
global TIMERESOURCES 
TIMERESOURCES = True

# global temps
global tmpLocation
global tmpLocationFull
global tmpSrcLocation
global tmpBuildRootLocation
# global valiables
global xmlConfigFile

global args

global specType

global exportFile
exportFile = ""

global exportFileType
exportFileType = ""

global heuristicsCommands
heuristicsCommands = []

# environment check: check OS for *nix like environment
def osCheck():
    if VERBOSE:
        print " 2:   checking environment"
        if TIMERESOURCES:
            print "       task started on "+ str(time.clock())

    osInfo = os.uname()
    architecture = osInfo[4]
    platform = osInfo[0]

    if platform not in ["Darwin", "FreeBSD", "IRIX64", "Linux", "SunOS"]: 
        sys.stdout.write("> warning    : Unsuported platform detected.\n")
        sys.stdout.write("               "+str(platform)+" is not yet supported by apkg\n")
        sys.stdout.write("               Delaying execution for 15 seconds\n")
        sleep(15)
    
    if VERBOSE:
        if TIMERESOURCES:
            print "       task ended on   "+ str(time.clock())
        print " 2:   completed"

def checkSystemArguments():
    import getopt

    global VERBOSE
    global TIMERESOURCES 

    global xmlConfigFile
    global specType
    
    global exportFile
    global exportFileType

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvVct", ["help", "verbose", "version", "copyright", "license", "bugs", "config=", "spec-type=", "export=", "export-type="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
        
    xmlConfigFile = ""
    
    exportFile = ""
    exportFileType = ""
    
    VERBOSE = False
    specType = "RPM"
    
    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-V", "--version"):
            version()
            sys.exit()
        elif opt in ("", "--copyright"):
            copyright()
            sys.exit()
        elif opt in ("", "--license"):
            lic()
            sys.exit()
        elif opt in ("", "--bugs"):
            bugs()
            sys.exit()        
        elif opt in ("-c", "--config"):
            xmlConfigFile = arg
        elif opt in ("", "--export"):
            exportFile = arg
        elif opt in ("", "--export-type"):
            exportFileType = arg
        elif opt in ("-t", "--spec-type"):
            specType = arg
        else:
            assert False, "unknown option"
    
    VERBOSE = True
    
    if xmlConfigFile == "":
        usage()
        sys.exit(2)
    else:    
    	print "using file: " + str(xmlConfigFile)
    
	# for now
	#xmlConfigFile = "config.xml"
    
def bugs():
    print "Please report bugs to %s" % BUGTRACK
        
def version():
    print 'apkg %s' % VERSION
    
def about():
    print 'Written by Andrei Oprisan <andrei@apkg.org>, 2008'

def copyright():
    print '%s' % COPYRIGHT
    
def lic():
    print '%s' % COPYRIGHT2

def usage():
    print "Usage: apkg [OPTIONS...] [FILE]... \n\
apkg is an abstract package creation and analysis platform \nthat can assist you in your package building activities. \n\
\n\
Examples:\n\
  --config=FILE              build using an XML configuration file\n\
\n\
 Options:\n\
  -v, --verbose              enable miscellaneous process debug information\n\
\n\
 Export:\n\
  --export=FILE              export processed build to file spec file\n\
  --export-type=             export format type\n\
    [raw|rpm|sh|xml]\n\
\n\
 Other options:\n\
  -h, --help                 Show this help list\n\
      --license              Show licensing information\n\
      --copyright            Show copyright information\n\
      --bugs                 Show bug submission details\n\
  -V, --version              Shot program version\n\
 "

def environmentSetup():
    if VERBOSE:
        log.info("(1): build")

    global tmpLocation
    global tmpLocationFull
    global tmpSrcLocation
    global tmpBuildRootLocation
    
    if VERBOSE:
        log.info(" 1:   creating environment")
        if TIMERESOURCES:
            log.info("       task started on "+ str(time.clock()))    

    tmpLocation = "apkg-" + str(os.getpid())
    tmpLocationFull = '/var/tmp/' + str(tmpLocation)

    if os.access('/var/tmp', os.W_OK):
        if os.path.exists(tmpLocationFull):
            if os.path.isfile(tmpLocationFull):
                os.remove(tmpLocationFull)
            if os.path.isdir(tmpLocationFull):
                os.removedirs(tmpLocationFull)
        else:
            tmpSrcLocation = tmpLocationFull + r"/src"
            tmpBuildRootLocation = tmpLocationFull + r"/bin"

            os.mkdir(tmpLocationFull, 0700)
            os.mkdir(tmpSrcLocation, 0700)
            os.mkdir(tmpBuildRootLocation, 0700)
            
            if not os.access(str(tmpLocationFull), os.W_OK) or not os.access(str(tmpSrcLocation), os.W_OK) or not os.access(str(tmpBuildRootLocation), os.W_OK):
                log.critical("could not create a temporary process working folder.")
            
    else:
        log.critical("could not create a temporary process working folder (/var/tmp not writeable)")

    if VERBOSE:
        if TIMERESOURCES:
            log.info("       task ended on   "+ str(time.clock()))
        log.info(" 1:   completed")

def environmentCleanup():
    envCleanup = "rm -fr " + tmpLocationFull
    
    if VERBOSE:
        log.info(" 6:   cleanup")
        log.info("      (R): " + envCleanup)
        
        if TIMERESOURCES:
            log.info("       task started on "+ str(time.clock()))    

    commandRunError = commands.getstatusoutput(envCleanup)
            
    if (cmp(commandRunError[0], 0) == 0):
        if VERBOSE:
            if TIMERESOURCES:
                log.info("       task ended on   "+ str(time.clock()))
            log.info("      (R): success")
    else: 
        log.info("      (R): command failed (error code " + str(commandRunError[0]) + ")")

        
def main():
    global exportFile
    global exportFileType
    global heuristicsCommands
    
    xmlControl = parser.reader(xmlConfigFile, VERBOSE, TIMERESOURCES)
    
#    xmlControl = xmlControlParser.parser(xmlConfigFile, VERBOSE)
#    print xmlControl.getBuildCommands()

    environmentSetup()
    
    #print xmlControl
    resources.download( xmlControl['pkgBuildResourceInformation']['protocol'], \
                        xmlControl['pkgBuildResourceInformation']['server'], \
                        xmlControl['pkgBuildResourceInformation']['root'], \
                        xmlControl['pkgBuildResourceInformation']['location'], \
                        xmlControl['pkgBuildResourceFiles'], \
                        tmpLocationFull, \
                        VERBOSE, TIMERESOURCES)
    
    # extract archives to tmp/src
    if VERBOSE:
        log.info(" 3:   extracting source tarballs")
        if TIMERESOURCES:
            log.info("       task started on   "+ str(time.clock()))

    archiver.unarchive(xmlControl['pkgBuildResourceFiles']['file'], tmpLocationFull, tmpSrcLocation, VERBOSE, TIMERESOURCES)
    
    #prepareResources
    #runBuildScript
    
    #env = str(xmlControl.getEnvironment())
    
    tmpSrcLocationDir = tmpSrcLocation + "/" + os.listdir(tmpSrcLocation)[0];
    
    # initiate heuristic process
    heuristicsCommands = heuristics.process( tmpSrcLocationDir, \
                                             tmpBuildRootLocation, \
                                             xmlControl['pkgBuildEnvironment'], \
                                             xmlControl['pkgBuildExecute'], \
                                             VERBOSE, TIMERESOURCES)
    
    # create archive from build
    archiver.archive(tmpBuildRootLocation, xmlControl['pkgDescriptorFormal'])
        
    commands = {}    
    # export resources
    if exportFile != "" and exportFileType != "":
        export.parseResults(exportFileType, exportFile, heuristicsCommands, xmlControl, VERBOSE, TIMERESOURCES)    
        
    # clean up environment
    environmentCleanup()
    
# start program execution

if __name__ == '__main__':
    try:
        import sys, time, log
       
        #creating the default log
        log.setLog("infoLog")        
    except ImportError, e:
        log.critical("failed initial module import.\n" + str(e))

    # check arguments
    # no need to continue with module loading if incorrect options are passed
    checkSystemArguments()
    args = xmlConfigFile    
    
    if VERBOSE:
        log.info("(0): apkg initialization")
        log.info(" 1:   loading modules")
        if TIMERESOURCES:
            log.info("       task started on "+ str(time.clock()))
                    
    try:
        # general operations
        import os, commands
        
        ### apkg modules ### 
        # logger
        import log
        
        # parse config file
        #import xmlControlParser
        
        import parser
        
        # download resources
        import resources
        
        # archiver
        import archiver
        
        # export results
        import export
        
        # analyze source code and choose build scheme
        # goes through all in heuristics/ and stops checking once a useful heuristic is found
        import heuristics
            
    except ImportError, e:
        log.critical("\n\n\> fatal error: failed module import.\n               here is some useful debug information:\n    "+str(e)+"\n\n")
    
    if VERBOSE:
        if TIMERESOURCES:
            log.info("       task ended on   "+ str(time.clock()))
        log.info(" 1:   completed")
   
   
    #initiate OS check
    osCheck() 
    
    #start apkg in earnest
    main()


