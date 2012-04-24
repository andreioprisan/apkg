import logging
import logging.config
import time
import string

global logger

def __init__():
    #configure logger
    logging.config.fileConfig("log.conf")

def setLog(format): 
    global logger
    #create logger for the specific module 
    logger = logging.getLogger(format)
    return logger
    
def debug(message):
    global logger
    logger.debug(message)

def info(message):
    global logger
    logger.info(message)

def warn(message):
    global logger
    logger.warn(message)

def error(message):
    global logger
    logger.error("error: " + str(message))
    exit()

def critical(message):
    global logger
    logger.critical("fatal error: " + str(message))
    exit()

def information(preSpaces, postSpaces, step, datails):
    global logger
    logger.info(" "*preSpaces + step + " "*postSpaces + datails + " " + str(time.clock()))

def startTaskTime(preSpaces, postSpaces, spacer):
    global logger
    logger.info(" "*preSpaces + spacer + " "*postSpaces + "task started on "+ str(time.clock()))

def endTaskTime(preSpaces, postSpaces, spacer):
    global logger
    logger.info(" "*preSpaces + spacer + " "*postSpaces + "task ended on "+ str(time.clock()))
    

__init__()