import log, os, commands, time

global archiveExtensions
archiveExtensions = [".tar", ".gz", ".bz2"] 
#todo: add native support for other archive formats (i.e. .z, .zip)

def __init__():
    log.setLog("infoLog")
    
def unarchive(fileList, tmpLocationFull, tmpSrcLocation, VERBOSE, TIMERESOURCES):
    VERBOSE = VERBOSE
    TIMERESOURCES = TIMERESOURCES
    global archiveExtensions
    
    archiveType = ''
    
    for location in fileList:
        if os.path.splitext(location)[1] in archiveExtensions:
            if os.path.splitext(location)[1] == ".tar":
                archiveType = "tar"
            elif os.path.splitext(location)[1] == ".tgz":
                archiveType = "tgz"
            elif os.path.splitext(location)[1] == ".tbz2":
                archiveType = "tbz2"
            elif os.path.splitext(location)[1] == ".gz":
                # reparsing necessary
                if os.path.splitext(os.path.splitext(location)[0])[1] == ".tar":
                    archiveType = "tgz"
                else:
                    archiveType = "gz"
            elif os.path.splitext(location)[1] == ".bz2":
                # reparsing necessary
                if os.path.splitext(os.path.splitext(location)[0])[1] == ".tar":
                    archiveType = "tbz2"
                else:
                    archiveType = "bz2"
            else:
                log.error("> fatal error (code 10): unsupported archive file: " + location + "\n ")
            
        if archiveType != "":
            if archiveType == "tar":
                flags = "-xf"
            elif archiveType == "gz":
                flags = "-zf"
            elif archiveType == "tgz":
                flags = "-xzf"
            elif archiveType == "bz2":
                flags = "-jf"
            elif archiveType == "tbz2":
                flags = "-xjf"
                
            if VERBOSE:
                log.info("      extracting " + location)
                
            fullArchivePathName = str(tmpLocationFull) + r"/" + str(location)
            unarchiveCommand = "tar "+ str(flags) + " " + str(fullArchivePathName) + " --directory=" + str(tmpSrcLocation)
            
            if VERBOSE:
                log.info("      (R): " + unarchiveCommand)
                if TIMERESOURCES:
                        log.info("       task started on   "+ str(time.clock()))
                
            runCommandConfirmation = None
            question = "        heuristic: Run suggested command? (Y/N): "
            
            while runCommandConfirmation not in ('y','ye','yes','n','no'):
                runCommandConfirmation = raw_input(question).lower()
                if runCommandConfirmation not in ('y','ye','yes','n','no'):
                    log.info("        heuristic:  Please enter Y or N")
            
            if  runCommandConfirmation.lower() == "y" or \
                runCommandConfirmation.lower() == "yes" or \
                runCommandConfirmation.lower() == "ye":
                
                commandRunError = commands.getstatusoutput(unarchiveCommand)
            else:
                log.info("      (R): command not run")

            
            if (cmp(commandRunError[0], 0) == 0):
                if VERBOSE:
                    if TIMERESOURCES:
                        log.info("       task ended on   "+ str(time.clock()))
                    log.info("      (R): success")
            else: 
                log.info("      (R): command failed (error code " + str(commandRunError[0]) + ")")
                
        archiveType = ''
 
    if VERBOSE:    
        if TIMERESOURCES:
            log.info("       task started on   "+ str(time.clock()))
        log.info(" 3:   completed")            

def archive(tmpDestDir, pkgInfo):
    VERBOSE = True
    TIMERESOURCES = True
    
    pwd = os.getcwd()
    os.chdir(tmpDestDir)
    
    if VERBOSE:
        log.info("      building package archive")
                
    pkgArchiveName = pkgInfo['pkgName'] + "-" + pkgInfo['pkgVersion'] + "-" + pkgInfo['pkgRevision'] + "." + "x86" + ".tar.bz2"      
    archiveCommand = "tar cjf " + pwd + r"/" + pkgArchiveName + " *"
            
    if VERBOSE:
        log.info("      (R): " + archiveCommand)
        if TIMERESOURCES:
            log.info("       task started on   "+ str(time.clock()))
                        
    commandRunError = commands.getstatusoutput(archiveCommand)
            
    if (cmp(commandRunError[0], 0) == 0):
        if VERBOSE:
            if TIMERESOURCES:
                log.info("       task ended on   "+ str(time.clock()))
            log.info("      (R): success")
    else: 
        log.info("      (R): command failed (error code " + str(commandRunError[0]) + ")")     
    
    os.chdir(pwd)

    