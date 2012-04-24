# filename: $heuristicShortName.py
# automake heuristic, version 1.0 

import os, commands, time, subprocess, log, re, sys

heuristicShortName = "automake"
heuristicName = "GNU Automake"
heuristicVersion = "1.0"
heuristicDesc = "This heuristic provides a means to build packages using the GNU Automake method"

heuristicApproved = True

global configOptions
configOptions = []

global options
options = {}

global commands
commands = {}

global commandsSet
commandsSet = []

global configBased
configBased = False

global VERBOSE
VERBOSE = False

global TIMERESOURCES
TIMERESOURCES = False

buildContinue = True

class grep:
    # grep-like class wrapper

    def __init__(self,pat,flags=0):
        self.fun = re.compile(pat,flags).match
    def __ror__(self,input):
        return ifilter(self.fun,input)
                        
def __init__(pkgPath, pkgDestDir, optionsDict, commandsDict, verbosity_level, timeresources_show):
	global VERBOSE
	VERBOSE = verbosity_level
	
	global TIMERESOURCES
	TIMERESOURCES = timeresources_show
	
	global commands
	commands = commandsDict
	
	global options
	options = optionsDict
	
	global commandsSet
    
	log.setLog("infoLog")        

	if (cmp(pkgPath, "") != 0):
		checkAppropriate(pkgPath)
        runConfigBased(pkgPath)

	if (heuristicApproved == True):
		if VERBOSE:
			log.info("       commencing package build with heuristic \"" + heuristicShortName + "\"")
			if TIMERESOURCES:
				log.info("        task started on   "+ str(time.clock()))
		buildPkg(pkgPath, pkgDestDir)
		
	return commandsSet

def getheuristicShortName():
	return heuristicShortName
	
def getheuristicName():
	return heuristicName

def heuristicVersion():
	return heuristicVersion

def getApproval():
	return heuristicApproved

def describeMe():
	return heuristicDesc
	
def checkAppropriate(pkgPath):
	global heuristicApproved
	
	if VERBOSE:
		log.info("       self-check: checking if heuristic is appropriate for this package")
		log.info("        checking: "+ pkgPath)
	
	if (os.path.exists(pkgPath + r'/configure')):
		log.info("        found ./configure")
	elif (os.path.exists(pkgPath + r'/Makefile')):
		log.info("        found Makefile")
	else:
		heuristicApproved = False
	
def checkProgress():
	global buildContinue
	
	if not buildContinue:
		sys.exit(1)
	
def buildPkg(pkgPath, pkgDestDir):
	global buildContinue
	global commands
	global configOptions
	global configBased
	
	log.info("  building in " + pkgPath)
	
	pwd = os.getcwd()
	os.chdir(pkgPath) 
    
	if configBased:
		if commands.has_key('configure') or len(configOptions) != 0:
			runConfigScript(pkgPath, configOptions)
		else:
			runConfigParser(pkgPath)
			runConfigScript(pkgPath, configOptions)
		checkProgress()
			
	if buildContinue:
		runMake(pkgPath)
		
	checkProgress()
	 
	if buildContinue:
		runMakeInstallDestDir(pkgPath, pkgDestDir)
	
	checkProgress()
		
	os.chdir(pwd)

def runConfigParser(pkgPath):
	global buildContinue
	global configOptions
	global commandsSet	
	
	if (os.path.exists(pkgPath + r'/configure')):
		log.info("  (R): parsing ./configure ")
		
	commandOutput = subprocess.Popen(["./configure", "--help"], stdout=subprocess.PIPE).communicate()[0]
	
	# PARSE ./configure --help FOR ALL USEFUL PARAMETERS THAT THE USER CAN ANSWER TO
	
	log.info("        heuristic [automake]: automatic parse of ./configure options")

	# fine tuning directory installation parameters (bindir, mandir)
	log.info("        heuristic [automake]: fine tuning installation directories")

	configInstallDirs = []

	# --prefix=
	question = "        heuristic [automake]: [default=/usr]: --prefix="
	prefixPath = raw_input(question)
	if prefixPath == "":
		configInstallDirs.append("--prefix=/usr")
	else:
		configInstallDirs.append("--prefix=" + prefixPath)

	# --bindir=
	enableOptionParsing = re.findall('(.*)  --bindir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/bin]: --bindir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --bindir="

		runCommandConfirmation = raw_input(question)

		if runCommandConfirmation == "":
			configInstallDirs.append("--bindir=/usr/bin")
		else:
			configInstallDirs.append("--bindir=" + runCommandConfirmation)
		
	# --sbindir=
	enableOptionParsing = re.findall('(.*)  --sbindir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/sbin]: --sbindir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --sbindir="

		runCommandConfirmation = raw_input(question)
				
		if runCommandConfirmation == "":
			configInstallDirs.append("--sbindir=/usr/sbin")
		else:
			configInstallDirs.append("--sbindir=" + runCommandConfirmation)

	# --libexecdir=
	enableOptionParsing = re.findall('(.*)  --libexecdir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/libexec]: --libexecdir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --libexecdir="

		runCommandConfirmation = raw_input(question)

		if runCommandConfirmation == "":
			configInstallDirs.append("--libexecdir=/usr/libexec")
		else:
			configInstallDirs.append("--libexecdir=" + runCommandConfirmation)
			
	# --datadir=
	enableOptionParsing = re.findall('(.*)  --datadir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/share]: --datadir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --datadir="

		runCommandConfirmation = raw_input(question)
		if runCommandConfirmation == "":
			configInstallDirs.append("--datadir=/usr/share")
		else:
			configInstallDirs.append("--datadir=" + runCommandConfirmation)
		
	# --sysconfdir=
	enableOptionParsing = re.findall('(.*)  --sysconfdir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/etc]: --sysconfdir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --sysconfdir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--sysconfdir=/usr/etc")
		else:
			configInstallDirs.append("--sysconfdir=" + runCommandConfirmation)
		
	# --sharedstatedir=
	enableOptionParsing = re.findall('(.*)  --sharedstatedir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/com]: --sharedstatedir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --sharedstatedir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--sharedstatedir=/usr/com")
		else:
			configInstallDirs.append("--sharedstatedir=" + runCommandConfirmation)		

	# --localstatedir=
	enableOptionParsing = re.findall('(.*)  --localstatedir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/var]: --localstatedir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --localstatedir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--localstatedir=/usr/var")
		else:
			configInstallDirs.append("--localstatedir=" + runCommandConfirmation)		

	# --libdir=
	enableOptionParsing = re.findall('(.*)  --libdir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/lib]: --libdir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --libdir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--libdir=/usr/lib")
		else:
			configInstallDirs.append("--libdir=" + runCommandConfirmation)		

	# --includedir=
	enableOptionParsing = re.findall('(.*)  --includedir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/include]: --includedir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --includedir="

		runCommandConfirmation = raw_input(question)

		if runCommandConfirmation == "":
			configInstallDirs.append("--includedir=/usr/include")
		else:
			configInstallDirs.append("--includedir=" + runCommandConfirmation)		
		
	# --oldincludedir=
	enableOptionParsing = re.findall('(.*)  --oldincludedir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/include]: --oldincludedir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --oldincludedir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--oldincludedir=/usr/include")
		else:
			configInstallDirs.append("--oldincludedir=" + runCommandConfirmation)		
		
	# --infodir=
	enableOptionParsing = re.findall('(.*)  --infodir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/info]: --infodir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --infodir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--infodir=/usr/info")
		else:
			configInstallDirs.append("--infodir=" + runCommandConfirmation)		

	# --mandir=
	enableOptionParsing = re.findall('(.*)  --mandir=(.*)', commandOutput)
	if len(enableOptionParsing) != 0:
		parseLine = enableOptionParsing[0][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				thisDetails += character	

		thisOption = re.sub('=DIR','', thisOption)
		
		if thisDetails == "" :
			question = "        heuristic [automake]: [default=/usr/mandir]: --mandir="
		else:
			question = "        heuristic [automake]: " + thisDetails.strip() + ": --mandir="

		runCommandConfirmation = raw_input(question)
		
		if runCommandConfirmation == "":
			configInstallDirs.append("--mandir=/usr/man")
		else:
			configInstallDirs.append("--mandir=" + runCommandConfirmation)		
			
	log.info("        heuristic [automake]: parsing --enable flags")

	#parse for --enable feature flags
	enableOptionParsing = re.findall('(.*)  --enable-(.*)', commandOutput)
	
	configEnableFlags = {}
	
	#user selected flags go here
	configEnableFlagsSelected = []
	
	endCounter = 0
	while endCounter != len(enableOptionParsing):
		# parse each line in the help that matches enable
		parseLine = enableOptionParsing[endCounter][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			# add options
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				# add verbose option details for each enable flag
				thisDetails += character	
		
		# override flags (can hide scanned flags)
		if thisOption.strip() != "FEATURE[=ARG]":
			# make a list of all available enable features and their details
			configEnableFlags[thisOption.strip()] = thisDetails.strip()
	
		endCounter += 1
	
	for option, details in configEnableFlags.items():
		# prompt the user for which flags to enable
		runCommandConfirmation = None
		if details == "" :
			question = "        heuristic [automake]: enable feature' " + option +"'? (y/n): "
		else :
			question = "        heuristic [automake]: enable feature '" + option +"' ("+ details +")? (y/n): "
	
		while runCommandConfirmation not in ('y','ye','yes','n','no'):
			runCommandConfirmation = raw_input(question).lower()
			
			if runCommandConfirmation not in ('y','ye','yes','n','no'):
				log.info("        heuristic [automake]:  Please enter Y or N")
			else:				
				if  runCommandConfirmation.lower() == "y" or \
	                runCommandConfirmation.lower() == "yes" or \
	                runCommandConfirmation.lower() == "ye":
					# make a ./configure parsable list of enabled features
					configEnableFlagsSelected.append("--enable-" + option + "=yes")
					log.info("        heuristic [automake]: enabled feature '"+ option + "'")

				elif runCommandConfirmation.lower() == "n" or \
	                 runCommandConfirmation.lower() == "no":
					configEnableFlagsSelected.append("--disable-" + option)
					log.info("        heuristic [automake]: disabled feature '"+ option + "'")

	log.info("        heuristic [automake]: parsing --disable flags")

	#parse for --disable feature flags
	disableOptionParsing = re.findall('(.*)  --disable-(.*)', commandOutput)
	
	configDisableFlags = {}
		
	endCounter = 0
	while endCounter != len(disableOptionParsing):
		# parse each line in the help that matches enable
		parseLine = disableOptionParsing[endCounter][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			# add options
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				# add verbose option details for each enable flag
				thisDetails += character	
		
		# override flags (can hide scanned flags)
		if thisOption.strip() != "FEATURE":
			# make a list of all available enable features and their details
			configDisableFlags[thisOption.strip()] = thisDetails.strip()
	
		endCounter += 1
	
	for option, details in configDisableFlags.items():
		# prompt the user for which flags to disable
		runCommandConfirmation = None
		if details == "" :
			question = "        heuristic [automake]: disable feature '" + option +"'? (y/n): "
		else :
			question = "        heuristic [automake]: disable feature '" + option +"' ("+ details +")? (y/n): "
	
		while runCommandConfirmation not in ('y','ye','yes','n','no'):
			runCommandConfirmation = raw_input(question).lower()
			
			if runCommandConfirmation not in ('y','ye','yes','n','no'):
				log.info("        heuristic [automake]:  Please enter Y or N")
			else:				
				if  runCommandConfirmation.lower() == "y" or \
	                runCommandConfirmation.lower() == "yes" or \
	                runCommandConfirmation.lower() == "ye":
					# make a ./configure parsable list of enabled features
					configEnableFlagsSelected.append("--disable-" + option)
					log.info("        heuristic [automake]: disabled feature '"+ option + "'")

				elif runCommandConfirmation.lower() == "n" or \
	                 runCommandConfirmation.lower() == "no":
					log.info("        heuristic [automake]: did not disabled feature '"+ option + "'")


	#print configEnableFlagsSelected

	log.info("        heuristic [automake]: parsing --with flags")
		
	#parse for --with packages flags
	withOptionParsing = re.findall('(.*)  --with-(.*)', commandOutput)
	
	configWithPackagesFlags = {}
	configWithPackagesFlagsSelected = []	
		
	endCounter = 0
	while endCounter != len(withOptionParsing):
		# parse each line in the help that matches enable
		parseLine = withOptionParsing[endCounter][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			# add options
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				# add verbose option details for each enable flag
				thisDetails += character	
		
		# override flags (can hide scanned flags)
		if thisOption.strip() != "PACKAGE[=ARG]":
			# make a list of all available enable features and their details
			configWithPackagesFlags[thisOption.strip()] = thisDetails.strip()
	
		endCounter += 1
	
	for option, details in configWithPackagesFlags.items():
		# prompt the user for which flags to disable
		runCommandConfirmation = None
		
		# check for =DIR parameters in enabling other packages
		# i.e. library prefix search path for libiconv-prefix or libintl-prefix, among the most common
		isDIR = re.findall('(.*)=DIR(.*)',option)
		
		if len(isDIR) != 0:
			option = re.sub('\[=DIR\]','', option)
			question = "        heuristic [automake]: with package path '" + option +"'="
			runCommandConfirmation = raw_input(question)
			configWithPackagesFlagsSelected.append("--with-" + option + "=" + runCommandConfirmation)

		else:
			if details == "" :
				question = "        heuristic [automake]: with package '" + option +"'? (y/n): "
			else :
				question = "        heuristic [automake]: with package '" + option +"' ("+ details +")? (y/n): "
		
			while runCommandConfirmation not in ('y','ye','yes','n','no'):
				runCommandConfirmation = raw_input(question).lower()
				
				if runCommandConfirmation not in ('y','ye','yes','n','no'):
					log.info("        heuristic [automake]:  Please enter Y or N")
				else:				
					if  runCommandConfirmation.lower() == "y" or \
		                runCommandConfirmation.lower() == "yes" or \
		                runCommandConfirmation.lower() == "ye":
						# make a ./configure parsable list of enabled features
						configWithPackagesFlagsSelected.append("--with-" + option + "=yes")
						log.info("        heuristic [automake]: with package '"+ option + "'")
	
					elif runCommandConfirmation.lower() == "n" or \
		                 runCommandConfirmation.lower() == "no":
						configWithPackagesFlagsSelected.append("--without-" + option)
						log.info("        heuristic [automake]: without package '"+ option + "'")
						
						
	log.info("        heuristic [automake]: parsing --without flags")
						
	#parse for --without packages flags
	withoutOptionParsing = re.findall('(.*)  --without-(.*)', commandOutput)
	
	configWithoutPackagesFlags = {}
		
	endCounter = 0
	while endCounter != len(withoutOptionParsing):
		# parse each line in the help that matches enable
		parseLine = withoutOptionParsing[endCounter][1].strip()

		thisOption = " "
		thisDetails = " "
		okPassthrough = False
		
		for character in parseLine:	
			# add options
			if not okPassthrough:				
				if character != ' ':
					thisOption += character
				else:	
					okPassthrough = True
			else:
				# add verbose option details for each enable flag
				thisDetails += character	
		
		# override flags (can hide scanned flags)
		if thisOption.strip() != "PACKAGE":
			# make a list of all available enable features and their details
			configWithoutPackagesFlags[thisOption.strip()] = thisDetails.strip()
	
		endCounter += 1
	
	for option, details in configWithoutPackagesFlags.items():
		# prompt the user for which flags to disable
		runCommandConfirmation = None
		
		# check for =DIR parameters in enabling/disabling other packages
		# i.e. library prefix search path for libiconv-prefix or libintl-prefix, among the most common
		isDIR = re.findall('(.*)=DIR(.*)',option)
		
		if len(isDIR) != 0:
			option = re.sub('\[=DIR\]','', option)
			question = "        heuristic [automake]: with package path '" + option +"'="
			runCommandConfirmation = raw_input(question)
			configWithPackagesFlagsSelected.append("--without-" + option + "=" + runCommandConfirmation)

		else:
			if details == "" :
				question = "        heuristic [automake]: without package '" + option +"'? (y/n): "
			else :
				question = "        heuristic [automake]: without package '" + option +"' ("+ details +")? (y/n): "
		
			while runCommandConfirmation not in ('y','ye','yes','n','no'):
				runCommandConfirmation = raw_input(question).lower()
				
				if runCommandConfirmation not in ('y','ye','yes','n','no'):
					log.info("        heuristic [automake]:  Please enter Y or N")
				else:				
					if  runCommandConfirmation.lower() == "y" or \
		                runCommandConfirmation.lower() == "yes" or \
		                runCommandConfirmation.lower() == "ye":
						# make a ./configure parsable list of enabled features
						configWithPackagesFlagsSelected.append("--without-" + option)
						log.info("        heuristic [automake]: without package '"+ option + "'")
	
					elif runCommandConfirmation.lower() == "n" or \
		                 runCommandConfirmation.lower() == "no":
						log.info("        heuristic [automake]: no action on package '"+ option + "'")						

    # convert all flags into one
	for option in configInstallDirs:
		configOptions.append(option)
	
	for option in configEnableFlagsSelected:
		configOptions.append(option)
	
	for option in configWithPackagesFlagsSelected:
		configOptions.append(option)
	
	configParamsStr = ""
	
	for param in configOptions:
		configParamsStr += param + " "
	
	fullConfigCommand = "./configure " + configParamsStr 
	commandsSet.append(fullConfigCommand)    
		
def runConfigBased(pkgPath):
    global configBased
    if (os.path.exists(pkgPath + r'/configure')):
        configBased = True
    else:
        configBased = False
    
def runConfigScript(pkgPath, configParams):
	global buildContinue
	
	configParamsStr = ""
	for param in configParams:
		configParamsStr += param + " "

	if (os.path.exists(pkgPath + r'/configure')):
		log.info("  (R): ./configure " + configParamsStr)
				
		#1. runs command and outputs as it runs
		# errCode = subprocess.call(["./configure", ""])
		#OR
		#2. commandOutput = subprocess.Popen(["./configure", ""], stdout=subprocess.PIPE).communicate()[0]
		#   commandErrCode = subprocess.Popen(["./configure", ""], stdout=subprocess.PIPE).communicate()[1]
		# for now we choose path 1 (we should probably ask the user in the future)
		
		# run ./configure
						
		runCommandConfirmation = None
        question = "        heuristic [automake]: Run suggested command? (Y/N): "
            
        while runCommandConfirmation not in ('y','ye','yes','n','no'):
            runCommandConfirmation = raw_input(question).lower()
            if runCommandConfirmation not in ('y','ye','yes','n','no'):
                log.info("        heuristic:  Please enter Y or N")
            
            if  runCommandConfirmation.lower() == "y" or \
                runCommandConfirmation.lower() == "yes" or \
                runCommandConfirmation.lower() == "ye":
                
                
                print 40*"-"
                
                runCommand = "./configure " + str(configParamsStr)
                commandErrCode = subprocess.call(runCommand, shell=True)
                
                print 40*"-"
            else:
                log.info("      (R): command not run")

		# check ./configure error code
		# TODO: make sure that all known configure error codes are documented and
		#       a plan of action is set for each
		if (commandErrCode == 256):
			log.info("   error code 256 returned")
			log.info("  (S): make distclean")
			buildContinue = False
			commandErrCode = subprocess.call(["make distclean", ""])
			if (cmp(commandErrCode, 0) == 0):
				log.info("  (S): success")
			else:
				log.info("  (S): command failed (error code " + str(commandErrCode) + ")")
				buildContinue = False
		elif (commandErrCode != 0):
			log.info("  (S): command failed (unknown error code " + str(commandErrCode) + ")")
			buildContinue = False
		else:
			log.info("  (R): success")
				
def runMake(pkgPath):
	global buildContinue
	global commandsSet    
	
	if (os.path.exists(pkgPath + r'/Makefile')):
		log.info("  (R): make")
		
		runCommandConfirmation = None
        question = "        heuristic [automake]: Run suggested command? (Y/N): "
            
        while runCommandConfirmation not in ('y','ye','yes','n','no'):
            runCommandConfirmation = raw_input(question).lower()
            if runCommandConfirmation not in ('y','ye','yes','n','no'):
                log.info("        heuristic:  Please enter Y or N")
            
            if  runCommandConfirmation.lower() == "y" or \
                runCommandConfirmation.lower() == "yes" or \
                runCommandConfirmation.lower() == "ye":
                
                print 40*"-"
                commandErrCode = subprocess.call("make", shell=True)
                print 40*"-"
                
                if (commandErrCode != 0):
					log.info("  (S): command failed (error code " + str(commandErrCode) + ")")
					buildContinue = False
                
                if (commandErrCode == 0):
					log.info("  (R): success")
					commandsSet.append("make")

            else:
                log.info("      (R): command not run")

		
def runMakeInstallDestDir(pkgPath, pkgDestDir):
	global buildContinue

	if (os.path.exists(pkgPath + r'/Makefile')):
		log.info("  (R): make DESTDIR=" + pkgDestDir +" install")
		
        runCommandConfirmation = None
        question = "        heuristic [automake]: Run suggested command? (Y/N): "
            
        while runCommandConfirmation not in ('y','ye','yes','n','no'):
            runCommandConfirmation = raw_input(question).lower()
            if runCommandConfirmation not in ('y','ye','yes','n','no'):
                log.info("        heuristic:  Please enter Y or N")
            
            if  runCommandConfirmation.lower() == "y" or \
                runCommandConfirmation.lower() == "yes" or \
                runCommandConfirmation.lower() == "ye":
                
                print 40*"-"
                # run "make DESTDIR=$DIR install"    
                commandErrCode = subprocess.call("make DESTDIR=" + pkgDestDir + " install", shell=True)    
                print 40*"-"
                
                if (commandErrCode != 0):
                    log.info("  (S): command failed (error code " + str(commandErrCode) + ")")
                    buildContinue = False
                
                if (commandErrCode == 0):
                    log.info("  (R): success")
                    commandsSet.append("make DESTDIR=$TMP install")
        
            else:
                log.info("      (R): command not run")

					