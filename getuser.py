import pysnow

import pysnow
import getpass

def pick_instance():
  ans = input("""Select serviceNOW instance:
    1. hmsprod
    2. hmstest
    3. hmsdev

    Your Choice[1]: """)
  if ans == '1' or ans =="":
    instance = "hmsprod"
  elif ans == '2':
    instance = "hmstest"
  elif ans == '3':
    instance = "hmsdev"
  else:
    print("Bad choice")

  return instance

myinstance = pick_instance()

myusername = input("username: ")
mypassword = getpass.getpass()

c = pysnow.Client(instance=myinstance, user=myusername, password=mypassword)

user = c.resource(api_path='/table/sys_user')
response = user.get(query={'sys_id':'e8640e8d6f24b500886324dfae3ee4e4'}).one()
print(response)


#for record in response.all():
#  print(record)
