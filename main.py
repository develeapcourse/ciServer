import json
import requests
import subprocess
import shutil
import tarfile
import os

from config_build_run import Config
from logger import  ci_logger

headers = {'Content-Type': 'application/json'}

def main():

    ci_logger.start_cycle()

    api_url_base, build_dir, devops_build_script, git_repo, last_run_file, project_dir = get_configuration()
    last_run_date, last_run_commit  = init_run(project_dir, last_run_file)
    print ('test last run = ' + str(last_run_date) + " - " + str(last_run_commit))

    current_run_date, current_run_commit = get_commit_info(api_url_base, last_run_date)
    print('test current run = ' + str(current_run_date) + ' - ' + str(current_run_commit))

    if current_run_commit is None:

        print('[!] No commit in repo')
        exit()

    if current_run_commit != last_run_commit:

        try:

            if not os.path.exists(build_dir):
                os.makedirs(build_dir)

            perform_clone_and_build(build_dir, current_run_commit, devops_build_script, git_repo, project_dir)
            save_current_run(current_run_date, current_run_commit, project_dir, last_run_file)

        except Exception as e:
            print(e)

def get_configuration():
    config = Config('.app_config')

    api_url_base = config.get('Git', 'api_url_base')
    project_dir = config.get('Paths', 'project_dir')
    git_repo = config.get('Git', 'git_repo')
    last_run_file = config.get('Project', 'last_run_file')
    build_dir = config.get('Paths', 'build_dir')
    devops_build_script = config.get('Paths', 'devops_build_script')

    print("test url base = " + str(api_url_base))
    print("test project_dir = " + str(project_dir))
    print("test git_repo = " + str(git_repo))
    print("test last_run_file = " + str(last_run_file))

    return api_url_base, build_dir, devops_build_script, git_repo, last_run_file, project_dir

def perform_clone_and_build(build_dir, current_run_commit, devops_build_script, git_repo, project_dir):
    # start from clean
    if current_run_commit is None or str(current_run_commit).strip() == '':
        print("Error! - commit cannot be empy")
        exit()

    shutil.rmtree(build_dir)
    git("clone", git_repo, build_dir)
    subprocess.call([devops_build_script, current_run_commit, build_dir])

def init_run(project_dir, last_run_file):

    try:
        last_run_file = project_dir + "/" + last_run_file
        last_run = open(last_run_file, "rt")
        last_run_date = last_run.readline().strip('\n')
        print("test last run date - " + str(last_run_date))
        last_run_commit = last_run.readline().strip('\n')
        print("test last run commit - " + str(last_run_commit))

        last_run.close()

    except Exception as e:
        # first run values
        last_run_date = '2018-11-24T00:00:00Z'
        last_run_commit = ''

    return last_run_date, last_run_commit

#TODO - delete
def archive_artifacts(current_run_date, project_dir, project_name):
    archives_dir = project_dir + "/archives/"
    tar_name = archives_dir + project_name + "-" + current_run_date
    tar = tarfile.open(tar_name, "w")

    for name in ["artifact1", "artifact2", "artifact2"]:
        tar.add(name)
        tar.close()

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def save_current_run(current_run_date, current_run_commit, project_dir, last_run_file):

    try:
        if current_run_date is None or str(current_run_date).strip() == '':
            print("Error! - commit date cannot be empy")
            exit()

        print("test current run date - " + str(current_run_date))
        print("test current run commit - " + str(current_run_commit))

        current_run_file = project_dir + "/" + last_run_file
        current_run = open(current_run_file, "wt")
        current_run.truncate(0)  # clean the file
        current_run.write(current_run_date + '\n')
        current_run.write(current_run_commit + '\n')

        current_run.close()

    except Exception as e:

        print(e)

def get_commit_info(api_url_base, last_run_date):
    api_url = "%s?since=%s" % (api_url_base,last_run_date)
    print ('api url = ' + str(api_url))
    response = requests.get(api_url)

    if response.status_code != 200:
        return None

    json_content = json.loads(response.content.decode('utf-8'))
    current_run_date = json_content[0]['commit']['committer']['date'] #only intrested in the latest commit
    current_run_commit = json_content[0]['sha']

    return current_run_date, current_run_commit

# Application entry point -> call main()
if __name__ == '__main__':
    main()
