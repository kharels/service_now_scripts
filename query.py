import pysnow
import getpass
import json

def pick_instance():
  ans = input("""Select serviceNOW instance: 
    1. hmsprod
    2. hmstest
    3. hmsdev

    Your Choice[1]: """)
  if ans == '1' or ans =="":
    myinstance = "hmsprod"
  elif ans == '2':
    myinstance = "hmstest"
  elif ans == '3':
    myinstance = "hmsdev"
  else:
    print("Bad choice")

  return myinstance

myinstance = pick_instance()

myusername = input("username: ")
mypassword = getpass.getpass()

c = pysnow.Client(instance=myinstance, user=myusername, password=mypassword)

def my_ctask(ctask_num):
    ctask = c.resource(api_path='/table/change_task')
    response = ctask.get(query={'number': ctask_num })
    change_id = response.one_or_none()['parent']['value']
    return change_id

change_id = my_ctask('CTASK0091687')
qb = (
    pysnow.QueryBuilder()
    .field('sys_id').equals(change_id))

crequest = c.resource(api_path='/table/change_request')
response = crequest.get(query=qb, stream=True).first()

ctask = c.resource(api_path='/table/change_task')

cnum = 'CHG0026883'
change_sys_id = crequest.get(query={'number': cnum}).one()['sys_id']

qb = (
   pysnow.QueryBuilder()
   .field('parent').equals(change_sys_id))


response = ctask.get(query=qb, stream=True).all()
print(response)








