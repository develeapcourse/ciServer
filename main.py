import json
import requests
import datetime
import subprocess
import sys
import shutil

api_token = 'your_api_token'
api_url_base = "https://api.github.com/repos/develeapcourse/gan_shmuel/commits"

# headers = {'Content-Type': 'application/json',
#            'Authorization': 'Bearer {0}'.format(api_token)}

def main():

    working_dir = "/tmp/gan_shmuel"

    last_run_data = init_run()

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

                shutil.rmtree(working_dir)

                git("clone", "https://github.com/develeapcourse/gan_shmuel.git", working_dir)

                # subprocess.call("build", shell=True)

                # subprocess.call("move_artifacts", shell=True)

                save_current_data(current_run_date, current_run_commit)


            except Exception as e:

                print(e)


    else:

        print('[!] No Commit in repo')

def init_run():

    try:

        last_run = open("last.txt", "rt")

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

def save_current_data(current_run_date, current_run_commit):

    try:

        current_run = open("last.txt", "wt")

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
