#!/usr/bin/env python3.10
import os, requests, dotenv
from datetime import datetime, timedelta


dotenv.load_dotenv()
api_key = os.getenv('KEY')
current_date = datetime.now()


# Feel free to add the tags you want this script to be applied to
tags_to_check = ['✍\uD83C\uDFFEtests', '\uD83D\uDCC6events']
# You can also change this if you'd like to change the tolarence of the time-checking
time_buffer = timedelta(minutes=2)


def callApi(path: str, method: str) -> list[dict] | None:
  headers = {
    'Authorization': f'Bearer {api_key}'
  }

  if method == 'GET':
    r = requests.get(f'https://api.ticktick.com/{path}', headers=headers)
    return r.json()
  elif method == 'POST':
    r = requests.post(f'https://api.ticktick.com/{path}', headers=headers)


task_projects = callApi('open/v1/project', 'GET')


# Loop through all of the projects and call the api to get all of the tasks
all_tasks = []

for project in task_projects:
  if project['kind'] != 'TASK': continue

  project_data = callApi(f'open/v1/project/{project["id"]}/data', 'GET')
  # For the sake of simplicity, I decided to add a 'projectName' key-value pair to the tasks data
  for i in range(len(project_data['tasks'])):
    project_data['tasks'][i]['projectName'] = project['name']

  all_tasks += project_data['tasks']


e_green = '\u001b[32m'
e_red = '\u001b[31m'
e_bold = '\u001b[1m'
e_reset = '\u001b[0m'

# Check to see if the tags on the task has the tags we want to mark completed
# and it is past the due date. If so, mark it as completed
for task in all_tasks:
  task_due_date_str = str(task['dueDate'])[:-5]
  task_due_date = datetime.fromisoformat(task_due_date_str)

  if task['isAllDay']: task_due_date.replace(hour=11, minute=59, second=59)

  if (any(e in task['tags'] for e in tags_to_check)):
    if (task_due_date < current_date + time_buffer):
      callApi(f'open/v1/project/{task["projectId"]}/task/{task["id"]}/complete', 'POST')
      print(f'Successfully completed item {e_green}"{task["title"]}"{e_reset} in list {e_red+e_bold}{task["projectName"]}{e_reset}')
      
time_to_complete = datetime.now() - current_date
print()
print(f"Done! Completed in {round(time_to_complete.total_seconds(), 2)} seconds" )
exit()
