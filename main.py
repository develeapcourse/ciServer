#!/usr/bin/python3

import json
import requests
import subprocess
import shutil
import os.path
import send_emails

from pathlib import Path
from config_build_run import Config
from logger import  ci_logger

headers = {'Content-Type': 'application/json'}

def main():

    ci_logger.start_cycle()

    app_config = get_configuration()

    last_run_date, last_run_commit  = init_run(app_config)
    print ('This run will check commits after = ' + str(last_run_date) + " - " + str(last_run_commit))

    current_run_date, current_run_commit = get_commit_info(app_config, last_run_date)
    print('Latest commit in origin = ' + str(current_run_date) + ' - ' + str(current_run_commit))

    if current_run_commit is None:

        print('[!] No commit in repo')
        exit()

    if current_run_commit != last_run_commit:
        execute_build(app_config, current_run_commit)
        save_current_run(app_config, current_run_date, current_run_commit)


def execute_build(app_config, current_run_commit):
    try:
        if not os.path.exists(app_config['build_dir']):
            os.makedirs(app_config['build_dir'])

        status = perform_clone_and_build(app_config, current_run_commit)

        if status != 0:
            print("Error in build")

            dist_list = str(app_config['dist_list']).split()
            send_emails.send(dist_list, app_config['msg_build_server_mail_subject'],
                             app_config['msg_build_failed'])

    except Exception as e:
        print(e)


def get_configuration():

    app_config_file = Path('.app_config')

    # doesn't exist
    if not app_config_file.is_file():
        print("Error! - configuration file not found")
        exit

    config = Config(app_config_file)

    # populate config parameters into dictionary
    app_config = {}
    app_config['api_url_base'] = config.get('Git', 'api_url_base')
    app_config['project_dir'] = config.get('Paths', 'project_dir')
    app_config['git_repo'] = config.get('Git', 'git_repo')
    app_config['last_run_file'] = config.get('Project', 'last_run_file')
    app_config['init_run_date'] = config.get('Project', 'init_run_date')
    app_config['build_dir'] = config.get('Paths', 'build_dir')
    app_config['devops_build_script'] = config.get('Paths', 'devops_build_script')
    app_config['dist_list'] = config.get('Mail', 'dist_list')
    app_config['msg_build_failed'] = config.get('Messages', 'msg_build_failed')
    app_config['msg_missing_config_file'] = config.get('Messages', 'msg_missing_config_file')
    app_config['msg_build_server_mail_subject'] = config.get('Messages', 'msg_build_server_mail_subject')

    return app_config

def perform_clone_and_build(app_config, current_run_commit):

    if current_run_commit is None or str(current_run_commit).strip() == '':
        print("Error! - commit cannot be empy")
        return 11

    # start from clean
    shutil.rmtree(app_config['build_dir'])
    git("clone", app_config['git_repo'], app_config['build_dir'])
    status = subprocess.call([app_config['devops_build_script'], current_run_commit, app_config['build_dir']])
    print("Return status from build script is: " + str(status))

    return status

def init_run(app_config):

    try:
        last_run_file = app_config['project_dir'] + "/" + app_config['last_run_file']
        last_run = open(last_run_file, "rt")
        last_run_date = last_run.readline().strip('\n')
        last_run_commit = last_run.readline().strip('\n')

        last_run.close()

    except Exception as e:
        # first run values
        last_run_date = app_config['init_run_date']
        last_run_commit = ''

    return last_run_date, last_run_commit

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def save_current_run(app_config, current_run_date, current_run_commit):
    print("Saving current commit")
    try:
        if current_run_date is None or str(current_run_date).strip() == '':
            print("Error! - commit date cannot be empy")
            exit()

        print("test current run date - " + str(current_run_date))
        print("test current run commit - " + str(current_run_commit))

        current_run_file = app_config['project_dir'] + "/" + app_config['last_run_file']
        current_run = open(current_run_file, "wt")
        current_run.truncate(0)  # clean the file
        current_run.write(current_run_date + '\n')
        current_run.write(current_run_commit + '\n')

        current_run.close()

    except Exception as e:

        print(e)

def get_commit_info(app_config, last_run_date):
    api_url = "%s?since=%s" % (app_config['api_url_base'],last_run_date)
    print ('Url for accessing origin repo = ' + str(api_url))
    response = requests.get(api_url)

    if response.status_code != 200:
        print("Error getting current commit from github")
        return None

    json_content = json.loads(response.content.decode('utf-8'))
    current_run_date = json_content[0]['commit']['committer']['date'] #only intrested in the latest commit
    current_run_commit = json_content[0]['sha']

    return current_run_date, current_run_commit

# Application entry point -> call main()
if __name__ == '__main__':
    main()