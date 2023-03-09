import shlex
import string
import subprocess
import re
import os
import pandas as pd

# Declaration
file = "C:/Users/11014494/Downloads/AD_user_Dover/Coverity/Data/3rdeye.xlsx"
cmd = 'curl -X POST "https://api.crowdstrike.com/oauth2/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "client_id=c188c8de1a9046d3a17f0d90c06ad497&client_secret=WUNG67aJY9P0XLnCr3wIhvZjAR4f5182FbsdgpeT"'
number_of_host = 5       #input ("Enter number host :")      Taking input as number of host need to get
args = shlex.split(cmd)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
s = str(stdout)
res = s.split(' ')[2]
token = re.findall(r'"([^"]*)"', res)
#print(token)
OauthToken = (' '.join(token))
#print(OauthToken)
c = 'curl -X GET "https://api.crowdstrike.com/detects/queries/detects/v1?offset=0&limit='
d= '&sort=last_behavior%7Casc" -H "accept: application/json" -H "authorization: bearer'+ ' '+ OauthToken
cmd1 = c+str(number_of_host)+d
#print(cmd1)
output = subprocess.check_output(cmd1, shell=True)
op = str(output)
#print(output)
# formatting all identified host id to get more details
api = re.findall(r'"ldt:.*?"', op)
api1 = (' '.join(api))
api2 = "[%s]" % ', '.join(map(str, api1))
api3 = re.sub(r'" "', '","', api1)
api4 = re.sub(r'"',r'\"', api3)





# Formatting host id to check from opco asset inventory
ldt = re.findall(r'(ldt:\w*)', op )
ldtdata = '[%s]' % ', '.join(map(str, ldt))
#print(ldtdata)
new_str = ldtdata.replace('ldt:', '')
#print(new_str)
df = pd.read_excel(file, sheet_name=0)
test_list = df['AID'].tolist()
#print(test_list)
#Formating excel to json file name
name = re.findall('[^/]*.xlsx',file)
name1 = str(name)[2 : -2]
Opco_name = name1.replace('.xlsx','')
t = 0
tup = []
result = []
b = set()
#Host id check from inventory excel
for i in range(int(number_of_host)):
    x = new_str.split(',')[i]
    y = re.sub(r'\W+', '', x)

    for j in test_list:
           if (y == j) :
               t += 1
               #print(j)
               reg = re.findall('"ldt:' + j + '.*?"', api3)
               reg1 = (' '.join(reg))
               reg2 = re.sub(r'" "', '","', reg1)
               reg3 = re.sub(r'"',r'\"', reg2,)
               tup += (reg3,)


# Formating identified opco specific host id to get details
result = [element for element in tup
                     if not (tuple(element) in b
                             or b.add(tuple(element)))]


dd = str(result)
df = str(dd)[1 : -1]
ts =  df.replace('\\"','\"')
ts1 = ts.replace("'","")
ts2 = ts1.replace(", ",",")
ts3 = ts2.__add__(','+ts2)
#print(ts3)

print('Number of matched host id from asset inventory of '+ Opco_name + ' is '+str(t))


#Opco spefic run
opco_spe = 'curl -X POST "https://api.crowdstrike.com/detects/entities/summaries/GET/v1" -H "accept: application/json" -H "authorization: bearer '+ OauthToken
cific_run = '" -H "Content-Type: application/json" -d "{ \\"ids\\": ' + '['+' '+ ts3 + ']}' # ts3  for opco specific identified can be used
opco_specific_run = opco_spe + cific_run

# running command storing data specific to opco host data
opco = os.popen(opco_specific_run).read()
file2 = open(Opco_name+".json","w+")
file2.write(opco)

file3 = open("file.txt", "a+")
file3.write(api4)

with open("D:/pycharm/CrowdStrike/file.txt", "r+") as f :
    b1 = f.readlines()
    c1 = str(b1)
    line1 = []
    a1 = re.findall(r'(\\\\"ldt:.*?")', c1)
    rmv_duplicate = list(set(a1))
with open("D:/pycharm/CrowdStrike/Unique_ldt.txt", "w+") as f1 :

    rmv_duplicate2 = re.sub(r'(\\\\\\)', '', str(rmv_duplicate))
    rmv_duplicate3 = re.sub('\'', '', rmv_duplicate2)
    rmv_duplicate4 = re.sub('\[|\]| ', '', rmv_duplicate3)
    f1.write(str(rmv_duplicate4))
    # print(rmv_duplicate4) # final out put removing duplicates

# running api to get data of all host id
c = 'curl -X POST "https://api.crowdstrike.com/detects/entities/summaries/GET/v1" -H "accept: application/json" -H "authorization: bearer '+ OauthToken
m = '" -H "Content-Type: application/json" -d "{ \\"ids\\": ' + '['+' '+ rmv_duplicate4 + ']}' # rmv_duplicate4 or api4 for all identified be used
cm = c+m

# running command storing all host data
abc = os.popen(cm).read()

# writing to json file for all
file1 = open("myfile.json","w+")
file1.write(abc)






