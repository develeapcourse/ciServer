import json
import requests
# import datetime
import subprocess
# import sys
import shutil
import tarfile
import os

api_token = 'your_api_token'
api_url_base = "https://api.github.com/repos/develeapcourse/gan_shmuel/commits"

# headers = {'Content-Type': 'application/json',
#            'Authorization': 'Bearer {0}'.format(api_token)}

def main():

    project_name = "gan_shmuel"
    project_dir = "/tmp/" + project_name
    git_repo = "https://github.com/develeapcourse/" + project_name + ".git"

    last_run_data = init_run(project_dir)

    last_run_date = last_run_data[0]
    last_run_commit = last_run_data[1]

    # print ('last run = ' + str(last_run_date) + "," + str(last_run_commit))

    current_commit_data = get_commit_info(last_run_date)

    # print ('current run =' + str(current_commit_data[0]) + ", " + str(current_commit_data[1]))

    if current_commit_data is not None:

        current_run_date = current_commit_data[0]
        current_run_commit = current_commit_data[1]

        if current_run_commit != last_run_commit:

            try:

                build_dir = project_dir + "/build"

                if not os.path.exists(build_dir):
                    os.makedirs(build_dir)

                shutil.rmtree(build_dir)

                git("clone", git_repo, build_dir)

                # subprocess.call("build", shell=True)

                # archive_artifacts(current_run_date, project_dir, project_name)

                save_current_data(current_run_date, current_run_commit, project_dir)



            except Exception as e:

                print(e)


    else:

        print('[!] No Commit in repo')

def archive_artifacts(current_run_date, project_dir, project_name):

    archives_dir = project_dir + "/archives/"
    tar_name = archives_dir + project_name + "-" + current_run_date

    tar = tarfile.open(tar_name, "w")

    for name in ["artifact1", "artifact2", "artifact2"]:
        tar.add(name)
        tar.close()

def init_run(project_dir):

    try:

        last_run_file = project_dir + "/.last.txt"
        last_run = open(last_run_file, "rt")

        last_run_date = last_run.readline()
        last_run_commit = last_run.readline()

        last_run.close()

    except Exception as e:
        # first run values
        last_run_date = '2018-11-24T00:00:00Z'
        last_run_commit = ''

    return last_run_date, last_run_commit


def git(*args):

    return subprocess.check_call(['git'] + list(args))

def save_current_data(current_run_date, current_run_commit, project_dir):

    try:

        current_run_file = project_dir + "/.last.txt"
        current_run = open(current_run_file, "wt")

        current_run.truncate(0)  # need '0' when using r+
        current_run.write(current_run_date + '\n')
        current_run.write(current_run_commit + '\n')

        current_run.close()

    except Exception as e:

        print(e)



def get_commit_info(last_run_date):

    api_url = "%s?since=%s" % (api_url_base,last_run_date)
    print ('api url = ' + str(api_url))

    # response = requests.get(api_url, headers=headers)
    response = requests.get(api_url)
    print ('test=' + str(response))

    if response.status_code == 200:
        # lastRunDate = datetime.datetime.now()
        json_content = json.loads(response.content.decode('utf-8'))

        current_run_date = json_content[0]['commit']['committer']['date']
        current_run_commit = json_content[0]['sha']

        return current_run_date, current_run_commit

    else:
        return None

# Application entry point -> call main()
main()
