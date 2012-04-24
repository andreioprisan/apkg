import sys, string, time, log
from xml.dom import minidom, Node 

class parser:
    global files
    files = {}

    global root
    root = []

    global protocol
    protocol = []
    
    global server
    server = []
    
    global location
    location = []

    global tags
    tags = []
    
    global environment 
    environment = []
    
    global pkgName 
    pkgName = ""
    
    global pkgVersion
    pkgVersion = ""
    
    global pkgRevision
    pkgRevision = ""
    
    global pkgArchitecture
    pkgArchitecture = ""

    global paramStack
    paramStack = []

    global buildCommands
    buildCommands = []

    global gnuConfig
    gnuConfig = []
    
    global makeBuild
    makeBuild = []
    
    global makeInstall
    makeInstall = []
    
    global resources
    resources = {}

    global XMLManifest
    XMLManifest = ""
    
    global stage
    stage = ""
    
    global VERBOSE
    VERBOSE = True
    
    global inEnvironment
    inEnvironment = False

    global inExecute
    inExecute = False
    
    global inFormal
    inFormal = False

    global inBuild
    inBuild = False
    
    global inDescriptor
    inDescriptor = False
    
    global inGnuconfig
    inGnuconfig = False
    
    global inMake
    inMake = False

    global inMkDir
    inMkDir = False
    
    global inRm
    inRm = False
            
    def __init__(self, XMLManifest, VERBOSE):
        self.XMLManifest = XMLManifest
        self.VERBOSE = VERBOSE
        self.parseXMLManifest(XMLManifest)
        self.prepareFileList(resources, files)
        log.setLog("infoLog")        
        
    def prepareFileList(self, resources, files):     
        for key,val in resources.items():
            if cmp(val[1],"archive") == 0: 
                files[key] = val[0]
            elif cmp(val[1],"patch") == 0: 
                files[key] = location[0]+"/"+val[0]
 
    def expandTree(self, TreeNode):
        global pkgName, pkgVersion, pkgRevision, pkgArchitecture, stage, paramStack
        global inEnvironment, inExecute, inFormal, inBuild, inDescriptor, inGnuconfig, inMake, inMkDir, inRm
        resourceMD5 = ""
        base = ""
        last = ""
        
        #print "BEGIN" 
        for TreeNode in TreeNode.childNodes:
            #print "TAG:" + TreeNode.nodeName + " TYPE: " + str(TreeNode.nodeType)
            print "X:" + last
            
            if TreeNode.nodeType == Node.ELEMENT_NODE:
                if  cmp(TreeNode.nodeName, "resource") == 0 or \
                    cmp(TreeNode.nodeName, "archive") == 0 or \
                    cmp(TreeNode.nodeName, "patch") == 0 or \
                    cmp(TreeNode.nodeName, "file") == 0 or \
                    cmp(TreeNode.nodeName, "environment") == 0 or \
                    cmp(TreeNode.nodeName, "execute") == 0 or \
                    cmp(TreeNode.nodeName, "gnuconfig") == 0 or \
                    cmp(TreeNode.nodeName, "make") == 0 or \
                    cmp(TreeNode.nodeName, "rm") == 0 or \
                    cmp(TreeNode.nodeName, "mkdir") == 0 or \
                    cmp(TreeNode.nodeName, "ln") == 0 or \
                    cmp(TreeNode.nodeName, "ls") == 0 or \
                    cmp(TreeNode.nodeName, "param") == 0 or \
                    cmp(TreeNode.nodeName, "prefix") == 0 or \
                    cmp(TreeNode.nodeName, "loc") == 0 or \
                    cmp(TreeNode.nodeName, "locale") == 0:
                    tags.append(TreeNode.nodeName)
                
                
                NodeAttributes = TreeNode.attributes
                for attributeName in NodeAttributes.keys():
                    attributeValue = NodeAttributes.get(attributeName).nodeValue
                    if cmp(attributeName, "protocol") == 0:
                        protocol.append(str(attributeValue))
                    elif cmp(attributeName, "server") == 0:
                        server.append(str(attributeValue))
                    elif cmp(attributeName, "root") == 0:
                        root.append(str(attributeValue))
                    elif cmp(attributeName, "location") == 0:
                        location.append(str(attributeValue))  
                    elif cmp(attributeName, "md5") == 0:
                        resourceMD5 = str(attributeValue)
                    elif cmp(attributeName, "stage") == 0:
                        stage = str(attributeValue)
                    elif cmp(attributeName, "base") == 0:
                        base = str(attributeValue)
                        
                    if cmp(TreeNode.nodeName, "environment") == 0 and cmp(attributeName, "inherit") == 0: 
                        log.debug("env inherited")
                        
                content = []
                for child in TreeNode.childNodes:
                    if child.nodeType == Node.TEXT_NODE:
                        content.append(child.nodeValue)
                        
                if content:
                    contentField = string.join(content)
                    if cmp(string.strip(contentField),"") != 0: 
                        
                        if cmp(string.strip(resourceMD5),"") != 0:
                            tags.pop()        
                            type = tags.pop()
                            resources[resourceMD5] = string.strip(contentField), type
                            tags.append(type)
                                        

                print "COMMANDS:" + str(buildCommands)    
                            
                # check open tags            
                if  cmp(string.strip(TreeNode.nodeName), "formal") == 0 and \
                    cmp(string.strip(contentField), "") == 0 :
                    inFormal = True

                if  cmp(string.strip(TreeNode.nodeName), "descriptor") == 0 and \
                    cmp(string.strip(contentField), "") == 0 :
                    inDescriptor = True
                
                if  cmp(string.strip(TreeNode.nodeName), "build") == 0 and \
                    cmp(string.strip(contentField), "") == 0 :
                    inBuild = True

                if  cmp(string.strip(TreeNode.nodeName), "environment") == 0 and \
                    cmp(string.strip(contentField), "") == 0 :
                    inEnvironment = True

                if  cmp(string.strip(TreeNode.nodeName), "execute") == 0 and \
                    cmp(string.strip(contentField), "") == 0 :
                    inExecute = True
                
                
                # check end tags   
                #  on tag close, build commands to pas to commands stack
                                
                print "LAST: " + last
 
                if  cmp(last, "environment") == 0:
                    inEnvironment = False                

                if  cmp(last, "descriptor") == 0:
                    inDescriptor = False

                if  cmp(last, "formal") == 0:
                    inFormal = False
                    
                if  cmp(last, "build") == 0:
                    inBuild = False

                if  cmp(last, "execute") == 0:
                    inExecute = False
                
                if  cmp(last, "gnuconfig") == 0:
                    inGnuconfig = False
                    
                    # create configure command
                    gnuconfigCommand = "./configure "
                    # append all options
                    for param in set(paramStack):
                        gnuconfigCommand = gnuconfigCommand + " " + param
                    # add command to command stack
                    buildCommands.append(gnuconfigCommand)
                    
                    paramStack = []

                if  cmp(last, "make") == 0:
                    inMake = False    

                    print "adding MAKE"
                    # create make command
                    makeCommand = "make "
                    # append all options
                    for param in set(paramStack):
                        makeCommand = makeCommand + " " + param
                    
                    # add command to command stack
                    buildCommands.append(makeCommand)
                    
                    paramStack = []

                    if cmp(stage, "") != 0:
                        stage = ""    

                if  cmp(last, "mkdir") == 0:
                    inMkDir = False
                    
                    # create mkdir command
                    mkdirCommand = "mkdir -p "
                    # append all options
                    for param in set(paramStack):
                        mkdirCommand = mkdirCommand + base + "/" + param + " "
                    
                    # add command to command stack
                    buildCommands.append(mkdirCommand)
                    
                    paramStack = []
                    
                    # clear base
                    if cmp(base, "") != 0:
                        base = ""  

                if  cmp(last, "rm") == 0:
                    inRm = False
                    
                    # create mkdir command
                    rmCommand = "rm -fr "
                    # append all options
                    print paramStack
                    for param in set(paramStack):
                        rmCommand = rmCommand + "DESTDIR/" + param + " "
                    
                    # add command to command stack
                    buildCommands.append(rmCommand)

                    paramStack = []
                    
                                    
                
                #tags: locale chost cflags cppflags cxxflags ldflags
                if inEnvironment:
                    if  cmp(string.strip(TreeNode.nodeName), "locale") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "chost") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "cflags") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "cppflags") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "cxxflags") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "ldflags") == 0 or \
                        cmp(string.strip(TreeNode.nodeName), "makeflags") == 0:

                        apendThis = string.strip(TreeNode.nodeName).upper() + "=\"" + string.strip(contentField) + "\" " 
                        environment.append(apendThis)
                                    
                if inDescriptor:
                    if inFormal:
                        if  cmp(string.strip(TreeNode.nodeName), "name") == 0:
                             pkgName = string.strip(contentField)
                        elif  cmp(string.strip(TreeNode.nodeName), "version") == 0:
                             pkgVersion = string.strip(contentField)
                        elif  cmp(string.strip(TreeNode.nodeName), "revision") == 0:
                             pkgRevision = string.strip(contentField)
                        elif  cmp(string.strip(TreeNode.nodeName), "architecture") == 0:
                             pkgArchitecture = string.strip(contentField)
                       
                if inBuild:
                    if inExecute:
                        print "EXEC" + string.strip(TreeNode.nodeName)
                        # open tag status in execute
                        if  cmp(string.strip(TreeNode.nodeName), "gnuconfig") == 0 and \
                            cmp(string.strip(contentField), "") == 0 :
                            inGnuconfig = True
                        elif  cmp(string.strip(TreeNode.nodeName), "make") == 0 and \
                            cmp(string.strip(contentField), "") == 0 :
                            inMake = True
                        elif  cmp(string.strip(TreeNode.nodeName), "mkdir") == 0 and \
                            cmp(string.strip(contentField), "") == 0 :
                            inMkDir = True
                        elif  cmp(string.strip(TreeNode.nodeName), "rm") == 0 and \
                            cmp(string.strip(contentField), "") == 0 :
                            inRm = True

                        if inGnuconfig:
                            if  (cmp(string.strip(TreeNode.nodeName), "prefix") == 0):
                                 apendThis = "--prefix=" + string.strip(contentField)
                                 paramStack.append(apendThis)  
                            elif (cmp(string.strip(TreeNode.nodeName), "param") == 0):
                                 apendThis = string.strip(contentField)
                                 paramStack.append(apendThis)
                        elif inMake:
                            if (stage != "install"):
                                if  (cmp(string.strip(TreeNode.nodeName), "prefix") == 0):
                                     apendThis = "PREFIX=" + string.strip(contentField)
                                     paramStack.append(apendThis)
                                elif (cmp(string.strip(TreeNode.nodeName), "param") == 0):
                                    apendThis = string.strip(contentField)
                                    paramStack.append(apendThis)

                            elif (stage == "install"):
                                for attributeName in NodeAttributes.keys():
                                    attributeValue = NodeAttributes.get(attributeName).nodeValue
                                    if cmp(attributeName, "base") == 0:
                                        base = str(attributeValue)

                                if  (cmp(string.strip(TreeNode.nodeName), "prefix") == 0):
                                    if (cmp(base, "") != 0):
                                        apendThis = "PREFIX=" + base + "/" + string.strip(contentField)
                                    else:
                                        apendThis = "PREFIX=" + string.strip(contentField)
                                    paramStack.append(apendThis)
                                elif (cmp(string.strip(TreeNode.nodeName), "param") == 0):
                                    apendThis = string.strip(contentField)
                                    paramStack.append(apendThis)  
                                    
                                print "INSTALL"+ str(paramStack) + "/" +  string.strip(TreeNode.nodeName)
                        elif inMkDir: 
                            if  (cmp(string.strip(TreeNode.nodeName), "dir") == 0):
                                apendThis = string.strip(contentField)
                                paramStack.append(apendThis)  
                                
                        elif inRm: 
                            if  (cmp(string.strip(TreeNode.nodeName), "loc") == 0):
                                apendThis = string.strip(contentField)
                                paramStack.append(apendThis)  
                                                        
                log.info("<tag> " + str(TreeNode.nodeName) + " : " + string.strip(contentField))
                log.info("BEFORE:" + last)
                
                last = str(TreeNode.nodeName)                                 
                log.info("NBEFORE:" + last)
                
                self.expandTree(TreeNode+1)
                
        
    def parseXMLManifest(self, XMLManifest):
        global VERBOSE
        
        if VERBOSE:
            log.info("(1): parsing XML manifest file")
            log.info(" 1:   reading XML file")
            log.info("       task started on "+ str(time.clock()))
    
        parsedXMLManifest = minidom.parse(XMLManifest)
        TreeNode = parsedXMLManifest.documentElement
        
        if VERBOSE:
            log.info("       task ended on   "+ str(time.clock()))
        
        if VERBOSE:
            log.info(" 2:   parsing XML file")
            log.info("       task started on "+ str(time.clock()))    
        
        self.expandTree(TreeNode)
    
        if VERBOSE:
            log.info("       task ended on   "+ str(time.clock()))
       
        
    def getProtocol(self):
        return protocol
        
    def getServer(self):
        return server
    
    def getRoot(self):
        return root
    
    def getLocation(self):
        return location
    
    def getTags(self):
        return tags
    
    def getResources(self):
        return resources
    
    def getFiles(self):
        return files
    
    def getEnvironment(self):
        return environment
    
    def getLang(self):
        return language

    def getPkgName(self):
        return pkgName

    def getPkgVersion(self):
        return pkgVersion

    def getPkgRevision(self):
        return pkgRevision

    def getPkgArchitecture(self):
        return pkgArchitecture

    def getPkgInfo(self):
        return {
                    'name'       :   pkgName,
                    'version'    :   pkgVersion,
                    'revision'   :   pkgRevision,
                    'arch'       :   pkgArchitecture
               }
    
    def getConfigOpts(self):
        configList = ""
        for configOpt in gnuConfig:
            configList = configList + " " + configOpt 
        return configList

    def getMakeBuildOpts(self):
        paramList = ""
        for param in makeBuild:
            paramList = paramList + " " + param 
        return paramList

    def getMakeInstallOpts(self):
        paramList = ""
        for param in makeInstall:
            paramList = paramList + " " + param 
        return paramList

    def getBuildCommands(self):
        buildCommandsDict = {}
        
        if (self.getConfigOpts() != ""):
            buildCommandsDict["configure"] = self.getConfigOpts()
            
        if (self.getMakeBuildOpts() != ""):
            buildCommandsDict["make"] = self.getMakeBuildOpts()

        if (self.getMakeInstallOpts() != ""):
            buildCommandsDict["make install"] = self.getMakeInstallOpts()
        
        return buildCommandsDict
    
    def getBuildEnv(self):
        buildEnvDict = {}
        #buildEnvDict = { "language" : self.getLang() }
        
        return buildEnvDict
     