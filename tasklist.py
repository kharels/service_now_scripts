import pysnow
import getpass
from datetime import datetime, timedelta
from prettytable import PrettyTable
from typing import Any, Union

x = PrettyTable()
x.field_names = ["Change Number", "State", "Change Task Number", "Start Date", "End Date", "Assigned to"]
# x.field_names = ["Change Number","State","Change Task Number","Short Description","Start Date","End Date",
# "Assigned to"]
today = datetime.today()
fourteen_days_ago = today - timedelta(days=30)
group_name = 'Version Control (Harvest)'
group_id = '21eba9456fbd0500886324dfae3ee42f'


def pick_instance():
    ans = input("""Select serviceNOW instance:
    1. hmsprod
    2. hmstest
    3. hmsdev

    Your Choice[1]: """)
    if ans == '':
        instance = 'hmsprod'
    else:
        ans_choices = {'1': 'hmsprod', '2': 'hmstest', '3': 'hmsdev'}
        instance = ans_choices[ans]
        print(instance)

    return instance


myinstance = pick_instance()
myusername = input("username: ")
mypassword = getpass.getpass()
c = pysnow.Client(instance=myinstance, user=myusername, password=mypassword)
c_request = c.resource(api_path='/table/change_request')
c_task_request = c.resource(api_path='/table/change_task')
user = c.resource(api_path='/table/sys_user')


def get_ctasks():
    qb1 = (
        pysnow.QueryBuilder()
            .field('assignment_group').equals(group_id)
            .AND()
            .field('sys_created_on').between(fourteen_days_ago, today)
    )

    response = c_task_request.get(query=qb1, stream=True)
    return response


response = get_ctasks()

for record in response.all():
    short_desc = record['short_description']
    ctask_number: Union[str, Any] = record['number']
    if record['assigned_to'] == '':
        task_assigned_to = "No one"
    else:
        task_assigned_to = user.get(query={'sys_id': record['assigned_to']['value']}).one()['name']

    change_info = c_request.get(query={'sys_id': record['parent']['value']}, stream=True).first()
    change_number = change_info['number']
    change_state = change_info['state']
    change_short_desc = change_info['short_description']
    change_start_date = change_info['start_date']
    change_end_date = change_info['end_date']
    if change_state == '2':
        change_state = 'Work in progress'
    elif change_state == '3':
        change_state = 'closed'
    elif change_state == '710':
        change_state = 'review'
    elif change_state == '910':
        change_state = 'Cancelled'
    elif change_state == '340':
        change_state = 'Scheduled'
    elif change_state == '120':
        change_state = 'Draft'
    elif change_state == '210':
        change_state = 'Requested'

    if change_state == 'Scheduled':
        x.add_row([change_number, change_state, ctask_number, change_start_date, change_end_date, task_assigned_to])
        # x.add_row([change_number,change_state,ctask_number,change_short_desc,change_start_date,change_end_date,
        # task_assigned_to])

x.sortby = 'Change Number'
x.align["Short Description"] = "l"
print(x)
