import pysnow
import getpass
mypassword = getpass.getpass()

c = pysnow.Client(instance='hmsprod', user='e006487', password=mypassword)
c_request = c.resource(api_path='/table/change_request')

change_num = 'CHG0027362'

out = c_request.get(query={'number':change_num}).one()
print(out)
