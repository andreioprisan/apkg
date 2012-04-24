import log
import sys, string
import xml.dom.minidom
from xml.dom.minidom import Node

global VERBOSE
VERBOSE = False

global TIMERESOURCES 
TIMERESOURCES = False

global pkgName, pkgVersion, pkgRevision, pkgArchitecture, pkgCategoryMajor, pkgCategoryMinor
global files, root, protocol, server, location, tags, environment
global paramStack, buildCommands
global xmlConfigFile     
     
global inFormal, inInformation, inDependency, inArchitecture  
inDependency = False      
inInformation = False
inArchitecture = False
inFormal = False

global pkgDescriptor

pkgDescriptor = { 
                    'pkgDescriptorFormal'                       :   '',
                    'pkgDescriptorInformation'                  :   '',
                    'pkgDescriptorDistribution'                 :   '',
                    'pkgDescriptorDistributionDependencyRun'    :   '',
                    'pkgDescriptorDistributionDependencyBuild'  :   '',
                    'pkgBuildResourceInformation'               :   '',
                    'pkgBuildResourceFiles'                     :   ''                            
                }

global pkgDescriptorFormal

pkgDescriptorFormal =   { 
                            'pkgName'       :   '',
                            'pkgVersion'    :   '',
                            'pkgRevision'   :   ''
                        }

global  pkgDescriptorInformation
 
pkgDescriptorInformation =  { 
                                'homepage'      :   '',
                                'license'       :   '',
                                'summary'       :   '',
                                'description'   :   ''
                            }


global  pkgDescriptorDistribution

pkgDescriptorDistribution = {
                                'distributionName'      :   '',
                                'distributionVersion'   :   '',
                                'maintainerName'        :   '',
                                'maintainerEmail'       :   '',
                                'categoryMajor'         :   '',
                                'categoryMinor'         :   '',
                                'architecture'          :   ''
                             }

global  pkgDescriptorDistributionDependencyRun

pkgDescriptorDistributionDependencyRun =    {
                                                'pkgName'           :   [],
                                                'pkgVersionOperand' :   [],
                                                'pkgVersion'        :   [],
                                                'pkgRevision'       :   []
                                            }

global pkgDescriptorDistributionDependencyBuild

pkgDescriptorDistributionDependencyBuild =  {
                                                'pkgName'           :   [],
                                                'pkgVersionOperand' :   [],
                                                'pkgVersion'        :   [],
                                                'pkgRevision'       :   []
                                            }

global  pkgBuildResourceInformation
                
pkgBuildResourceInformation    =    {
                                         'protocol'     :   '',
                                         'server'       :   '', 
                                         'root'         :   '',
                                         'location'     :   '',
                                         'patchLevel'   :   ''
                                    }

global pkgBuildResourceFiles

pkgBuildResourceFiles   =   {
                                'type'  :   [],
                                'md5'   :   [],
                                'file' :   []
                            }

global pkgBuildExecute
pkgBuildExecute     = {}

global pkgBuildEnvironment
pkgBuildEnvironment     = {}

files = {}

tags = []
environment = []
paramStack = []
buildCommands = []
    
pkgArchitecture = ""
pkgCategoryMajor = ""
pkgCategoryMinor = ""

global  PKG_DESCRIPTOR_FORMAL,\
        PKG_DESCRIPTOR_INFORMATION, \
        PKG_DESCRIPTOR_DISTRIBUTION, \
        PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER, \
        PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY, \
        PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, \
        PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, \
        PKG_BUILD_RESOURCE_INFORMATION, \
        PKG_BUILD_RESOURCE_FILES, \
        PKG_BUILD_EXECUTE, \
        PARSE_TAG, \
        PARSE_PARAMETER
        
PARSE_TAG                                       =   1
PARSE_PARAMETER                                 =   2

PKG_DESCRIPTOR_FORMAL                           =   10

PKG_DESCRIPTOR_INFORMATION                      =   20

PKG_DESCRIPTOR_DISTRIBUTION                     =   30
PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER          =   31
PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY            =   32

PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN      =   40
PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD    =   41

PKG_BUILD_RESOURCE_INFORMATION                  =   50
PKG_BUILD_RESOURCE_FILES                        =   51

PKG_BUILD_EXECUTE                               =   60

def __init__(xmlConfigFile, verbose, timeResources):
    global VERBOSE, TIMERESOURCES
    VERBOSE = verbose
    TIMERESOURCES = timeResources
        
    log.setLog("infoLog")
    
    #xmlManifestVersion = "1.0"
    #
    #if (xmlManifestVersion == "1.0"):
    #    print "m"
    #elif  (xmlManifestVersion == "1.1"):
    #    print "m"        
    #else:
    #    log.critical("unknown XML manifest version: " + xmlManifestVersion)
    
    if VERBOSE:
        log.information(1, 3, "2:", "reading XML file")
    if TIMERESOURCES:
        log.startTaskTime(1, 4, "  ")
    
    read(xmlConfigFile)
    
    if TIMERESOURCES:
        log.endTaskTime(1, 4, "  ")
    if VERBOSE:
        log.information(1, 3, "2:", "read XML file")
        
    return parseVars()

def parseVars():
    global  pkgDescriptorFormal, \
            pkgDescriptorInformation, \
            pkgDescriptorDistribution, \
            pkgDescriptorDistributionDependencyRun, \
            pkgDescriptorDistributionDependencyBuild, \
            pkgBuildResourceInformation, \
            pkgBuildResourceFiles, \
            pkgBuildExecute, \
            pkgBuildEnvironment, \
            pkgDescriptor
            
    pkgDescriptor['pkgDescriptorFormal'] = pkgDescriptorFormal
    pkgDescriptor['pkgDescriptorInformation'] = pkgDescriptorInformation
    pkgDescriptor['pkgDescriptorDistribution'] = pkgDescriptorDistribution
    pkgDescriptor['pkgDescriptorDistributionDependencyRun'] = pkgDescriptorDistributionDependencyRun
    pkgDescriptor['pkgDescriptorDistributionDependencyBuild'] = pkgDescriptorDistributionDependencyBuild
    pkgDescriptor['pkgBuildResourceInformation'] = pkgBuildResourceInformation
    pkgDescriptor['pkgBuildResourceFiles'] = pkgBuildResourceFiles
    pkgDescriptor['pkgBuildExecute'] = pkgBuildExecute
    pkgDescriptor['pkgBuildEnvironment'] = pkgBuildEnvironment
    
    return pkgDescriptor


def parseTag(varName, varSet, tagValue, parentNode, parseType):
    global  PKG_DESCRIPTOR_FORMAL, \
            PKG_DESCRIPTOR_INFORMATION, \
            PKG_DESCRIPTOR_DISTRIBUTION, \
            PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER, \
            PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY, \
            PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, \
            PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, \
            PKG_BUILD_RESOURCE_INFORMATION, \
            PKG_BUILD_RESOURCE_FILES,  \
            PKG_BUILD_EXECUTE, \
            PARSE_TAG, \
            PARSE_PARAMETER

    if (varSet == PKG_DESCRIPTOR_FORMAL):
        global pkgDescriptorFormal
    elif (varSet == PKG_DESCRIPTOR_INFORMATION):
        global pkgDescriptorInformation
    elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION or \
          varSet == PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER or \
          varSet == PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY):
        global pkgDescriptorDistribution
    elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN):
        global pkgDescriptorDistributionDependencyRun 
    elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD):
        global pkgDescriptorDistributionDependencyBuild
    elif (varSet == PKG_BUILD_RESOURCE_INFORMATION):
        global pkgBuildResourceInformation
    elif (varSet == PKG_BUILD_RESOURCE_FILES):
        global pkgBuildResourceFiles
    elif (varSet == PKG_BUILD_EXECUTE):
        global pkgBuildExecute

    returnVar = ""        
    if (parseType == PARSE_TAG):        
        if (cmp(string.strip(parentNode.nodeName), str(tagValue)) == 0):
            for textNode in parentNode.childNodes:
                if (textNode.nodeType == Node.TEXT_NODE):
                    returnVar = string.strip(textNode.nodeValue)
    elif (parseType == PARSE_PARAMETER):
        returnVar = "" 
        returnVar = parentNode.strip()
        
    if (cmp(returnVar.strip(), "") != 0):
        if (varSet == PKG_DESCRIPTOR_FORMAL):
            pkgDescriptorFormal[varName]        = returnVar
        elif (varSet == PKG_DESCRIPTOR_INFORMATION):
            pkgDescriptorInformation[varName]    = returnVar
        elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION or \
              varSet == PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER or \
              varSet == PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY):
            pkgDescriptorDistribution[varName]   = returnVar  
        elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN):
            pkgDescriptorDistributionDependencyRun[varName].append(returnVar)
        elif (varSet == PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD):
            pkgDescriptorDistributionDependencyBuild[varName].append(returnVar)
        elif (varSet == PKG_BUILD_RESOURCE_INFORMATION):
            pkgBuildResourceInformation[varName] = returnVar
        elif (varSet == PKG_BUILD_RESOURCE_FILES):
            pkgBuildResourceFiles[varName].append(returnVar)
        elif (varSet == PKG_BUILD_EXECUTE):
            pkgDescriptorDistributionDependencyBuild[varName].append(returnVar)
            
    #print pkgDescriptorFormal

                                
def read(configFile):
    global pkgName, pkgVersion, pkgRevision, pkgArchitecture, pkgCategoryMajor, pkgCategoryMinor
    global pkgInformation

    global xmlConfigFile
    xmlConfigFile = configFile
    
    global inFormal
        
    doc = xml.dom.minidom.parse(xmlConfigFile)
    
    mapping = {}
    
    for node in doc.childNodes:
        for level1Node in node.childNodes:
            # in level 1 nodes
            #    level 1 nodes:    descriptor
            #                      build  
            if (string.strip(level1Node.nodeName) == "descriptor"):
                 # in level 1 node:    descriptor
                for descriptorSubNode in level1Node.childNodes:
                    # in descriptor child nodes
                    #    descriptor child nodes:     formal
                    if (string.strip(descriptorSubNode.nodeName) == "formal"):
                        for formalSubNode in descriptorSubNode.childNodes:
                            parseTag("pkgName", PKG_DESCRIPTOR_FORMAL, "name", formalSubNode, PARSE_TAG)
                            parseTag("pkgVersion", PKG_DESCRIPTOR_FORMAL, "version", formalSubNode, PARSE_TAG)                            
                            parseTag("pkgRevision", PKG_DESCRIPTOR_FORMAL, "revision", formalSubNode, PARSE_TAG)
                    #                                information
                    elif (string.strip(descriptorSubNode.nodeName) == "information"):
                        for informationSubNode in descriptorSubNode.childNodes:
                            parseTag("homepage", PKG_DESCRIPTOR_INFORMATION, "homepage", informationSubNode, PARSE_TAG)
                            parseTag("license", PKG_DESCRIPTOR_INFORMATION, "license", informationSubNode, PARSE_TAG)                            
                            parseTag("summary", PKG_DESCRIPTOR_INFORMATION, "summary", informationSubNode, PARSE_TAG)
                            parseTag("description", PKG_DESCRIPTOR_INFORMATION, "description", informationSubNode, PARSE_TAG)
                    #                                distribution
                    elif (string.strip(descriptorSubNode.nodeName) == "distribution"):
                        for distributionSubNode in descriptorSubNode.childNodes:
                            parseTag("distributionName", PKG_DESCRIPTOR_DISTRIBUTION, "name", distributionSubNode, PARSE_TAG)
                            parseTag("distributionVersion", PKG_DESCRIPTOR_DISTRIBUTION, "version", distributionSubNode, PARSE_TAG)
                            
                            if (string.strip(distributionSubNode.nodeName) == "maintainer"):
                                for maintainerSubNode in distributionSubNode.childNodes:
                                    parseTag("maintainerName", PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER, "name", maintainerSubNode, PARSE_TAG)
                                    parseTag("maintainerEmail", PKG_DESCRIPTOR_DISTRIBUTION_MAINTAINER, "email", maintainerSubNode, PARSE_TAG)
                            elif (string.strip(distributionSubNode.nodeName) == "category"):
                                for categorySubNode in distributionSubNode.childNodes:
                                    parseTag("categoryMajor", PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY, "major", categorySubNode, PARSE_TAG)
                                    parseTag("categoryMinor", PKG_DESCRIPTOR_DISTRIBUTION_CATEGORY, "minor", categorySubNode, PARSE_TAG)
                            
                            parseTag("architecture", PKG_DESCRIPTOR_DISTRIBUTION, "architecture", distributionSubNode, PARSE_TAG)
                            
                            if (string.strip(distributionSubNode.nodeName) == "dependency"):
                                for dependencySubNode in distributionSubNode.childNodes:
                                    if (string.strip(dependencySubNode.nodeName) == "run"):
                                        for dependencyPkgSubNode in dependencySubNode.childNodes:
                                            if (string.strip(dependencyPkgSubNode.nodeName) == "pkg"):
                                                for pkgSubNode in dependencyPkgSubNode.childNodes:
                                                    if (string.strip(pkgSubNode.nodeName) == "name"):
                                                        parseTag("pkgName", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, "name", pkgSubNode, PARSE_TAG)
                                                    elif (string.strip(pkgSubNode.nodeName) == "version"):
                                                        parseTag("pkgVersion", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, "version", pkgSubNode, PARSE_TAG)                                    
                                                    elif (string.strip(pkgSubNode.nodeName) == "operand"):
                                                        parseTag("pkgVersionOperand", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, "operand", pkgSubNode, PARSE_TAG)
                                                    elif (string.strip(pkgSubNode.nodeName) == "revision"):
                                                        parseTag("pkgRevision", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_RUN, "revision", pkgSubNode, PARSE_TAG)
                                    elif (string.strip(dependencySubNode.nodeName) == "build"):
                                        for dependencyPkgSubNode in dependencySubNode.childNodes:
                                            if (string.strip(dependencyPkgSubNode.nodeName) == "pkg"):
                                                for pkgSubNode in dependencyPkgSubNode.childNodes:
                                                    if (string.strip(pkgSubNode.nodeName) == "name"):
                                                        parseTag("pkgName", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, "name", pkgSubNode, PARSE_TAG)
                                                    elif (string.strip(pkgSubNode.nodeName) == "version"):
                                                        parseTag("pkgVersion", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, "version", pkgSubNode, PARSE_TAG)                                    
                                                    elif (string.strip(pkgSubNode.nodeName) == "operand"):
                                                        parseTag("pkgVersionOperand", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, "operand", pkgSubNode, PARSE_TAG)
                                                    elif (string.strip(pkgSubNode.nodeName) == "revision"):
                                                        parseTag("pkgRevision", PKG_DESCRIPTOR_DISTRIBUTION_DEPENDENCY_BUILD, "revision", pkgSubNode, PARSE_TAG)
                
            elif (cmp(level1Node.nodeName, "build") == 0):
                 # in level 1 node:    build
                for buildSubNode in level1Node.childNodes:
                    # in build child nodes
                    #    build child nodes:     resource
                    if (string.strip(buildSubNode.nodeName) == "resource"):
                        NodeAttributes = buildSubNode.attributes
                        for attributeName in NodeAttributes.keys():
                            attributeValue = NodeAttributes.get(attributeName).nodeValue
                            
                            if (string.strip(attributeName) == "protocol"):
                                parseTag("protocol", PKG_BUILD_RESOURCE_INFORMATION, attributeName, attributeValue, PARSE_PARAMETER)
                            elif (string.strip(attributeName) == "server"):
                                parseTag("server", PKG_BUILD_RESOURCE_INFORMATION, attributeName, attributeValue, PARSE_PARAMETER)                                    
                            elif (string.strip(attributeName) == "root"):
                                parseTag("root", PKG_BUILD_RESOURCE_INFORMATION, attributeName, attributeValue, PARSE_PARAMETER)                                    

                        for resourceSubNode in buildSubNode.childNodes:
                            # in resource child nodes
                            #    resource child nodes:     archive
                            if (string.strip(resourceSubNode.nodeName) == "archive"):
                                for archiveNode in resourceSubNode.childNodes:
                                    if (string.strip(archiveNode.nodeName) == "file"):
                                        parseTag("type", PKG_BUILD_RESOURCE_FILES, "type", "archive", PARSE_PARAMETER)
                                        parseTag("file", PKG_BUILD_RESOURCE_FILES, "file", archiveNode, PARSE_TAG)

                                        NodeAttributes = archiveNode.attributes
                                        for attributeName in NodeAttributes.keys():
                                            attributeValue = NodeAttributes.get(attributeName).nodeValue
                                            
                                            if (string.strip(attributeName) == "md5"):
                                                parseTag("md5", PKG_BUILD_RESOURCE_FILES, "md5", attributeValue, PARSE_PARAMETER)

                            elif (string.strip(resourceSubNode.nodeName) == "patch"):
                                NodeAttributes = resourceSubNode.attributes
                                for attributeName in NodeAttributes.keys():
                                    attributeValue = NodeAttributes.get(attributeName).nodeValue
                                    
                                    if (string.strip(attributeName) == "level"):
                                        parseTag("patchLevel", PKG_BUILD_RESOURCE_INFORMATION, "level", attributeValue, PARSE_PARAMETER)
                                    elif (string.strip(attributeName) == "location"):
                                        parseTag("location", PKG_BUILD_RESOURCE_INFORMATION, attributeName, attributeValue, PARSE_PARAMETER)                                    

                                
                                for archiveNode in resourceSubNode.childNodes:
                                    if (string.strip(archiveNode.nodeName) == "file"):
                                        parseTag("type", PKG_BUILD_RESOURCE_FILES, "type", "patch", PARSE_PARAMETER)
                                        parseTag("file", PKG_BUILD_RESOURCE_FILES, "file", archiveNode, PARSE_TAG)

                                        NodeAttributes = archiveNode.attributes
                                        for attributeName in NodeAttributes.keys():
                                            attributeValue = NodeAttributes.get(attributeName).nodeValue
                                            
                                            if (string.strip(attributeName) == "md5"):
                                                parseTag("md5", PKG_BUILD_RESOURCE_FILES, "md5", attributeValue, PARSE_PARAMETER)

    
def getProtocol():
    print pkgBuildResourceInformation['protocol']
    return pkgName

    
def getPkgName():
    return pkgName

def getPkgVersion():
    return pkgVersion

def getPkgRevision():
    return pkgRevision

def getPkgArchitecture():
    return pkgArchitecture

def getPkgDescriptorFormal():
    return pkgDescriptorFormal


