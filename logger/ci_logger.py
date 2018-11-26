import logging
from datetime import date
# import sys
import os, sys

try:
	DIR_NAME = sys.argv[1]
except Exception as e:
	print(e)

LOG_FORMAT = "%(levelname)s_-_%(asctime)s_-_%(message)s"

if not os.path.exists(DIR_NAME):
	try:
		os.makedirs(DIR_NAME)
	except Exception as e:
		print(e)


# create and config logger
logging.basicConfig(filename = DIR_NAME +"/ci_log-" + str(date.today()) + ".txt", 
					level = logging.DEBUG,
					format = LOG_FORMAT)

logger = logging.getLogger("ci_logger")


def ci_cycle():
	logger.debug("starts a CI cycle")
	

def last_commit(commit_name, commit_date):	
	logger.debug("last commit: %s date: %s", [str(commit_name), str(commit_date)])


def current_commit(commit_name, commit_date):
	logger.debug("current commit: %s date: %s", [str(commit_name), str(commit_date)])


def clone_from_remote(remote_url):
	logger.debug('cloning fromm %s', str(remote_url))

def end_cycle():
	logger.debug("end of CI cycle")
	