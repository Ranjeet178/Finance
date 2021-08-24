import boto3
import botocore
from operator import is_not
from functools import partial
import paramiko
from paramiko import SSHClient
from boto.manage.cmdshell import sshclient_from_instance
import json 

# cloud_project_LSA
user_data = '''#!/bin/bash
sudo apt-get update &&
sudo apt-get install python3 &&
cd /home/ubuntu/ &&
git clone https://github.com/pujariakshayk/Data-Science &&
cd Data-Science
sudo apt install --yes python3-pip &&
pip install -r requirements.txt
'''

def create_ec2_instance():
    try:
        print ("Creating EC2 instance")
        resource_ec2 = boto3.client("ec2",region_name='us-east-1',aws_access_key_id="ASIA5OSMFRWOCQHBWU6L",
            aws_secret_access_key="RWPpdW6meWpJH6wfl5/WBrjxIKH45NXiVlgx7sng",aws_session_token='FwoGZXIvYXdzEH4aDDYkgKtpXFmHTP0a4CLIAaRH3L2GDoLbMzckmHRzJRuSMApz8F0WiGm0Y+Gr0eQeDpl0CgJkGpmiGCciOvEz82LVdBYlGD6/czzCnK8qChYWIBraT87UgJ/i1VSpLA+NSWzsgjtzQGwnojXxLc4jGRiI3Ysd1vFsP16ByUhAqyUBNg+G3Yt5xnT+41IW+uJJRa5LYfnCs4c+Q8fn1LinaHAkn+He6mcZV4FWo/N6kgzpCmXZTRS0l7P9U7BkX7NFEDOau3ncZbktCMq/6CsmUQpPAFbr2n9EKPHU9YgGMi3IHq8/H8I3djc6lU9Aoa+Xm4ZQlyd86EdFSOk4TGRVL2zjzznSFqMWVjjJMRg=',)
        resource_ec2.run_instances(
            ImageId="ami-09e67e426f25ce0d7",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            UserData=user_data, 
            KeyName="cloud_project_LSA",
            #sg-0494724ab8ec5858e
            SecurityGroupIds=['sg-0494724ab8ec5858e'],
            
        )
        print("end of request")
    except Exception as e:
        print(e)
        
def describe_ec2_instance():
    instance_ids = []
    try:
        print ("Describing EC2 instance")
        resource_ec2 = boto3.client("ec2",region_name='us-east-1',aws_access_key_id="ASIA5OSMFRWOCQHBWU6L",
            aws_secret_access_key="RWPpdW6meWpJH6wfl5/WBrjxIKH45NXiVlgx7sng",aws_session_token='FwoGZXIvYXdzEH4aDDYkgKtpXFmHTP0a4CLIAaRH3L2GDoLbMzckmHRzJRuSMApz8F0WiGm0Y+Gr0eQeDpl0CgJkGpmiGCciOvEz82LVdBYlGD6/czzCnK8qChYWIBraT87UgJ/i1VSpLA+NSWzsgjtzQGwnojXxLc4jGRiI3Ysd1vFsP16ByUhAqyUBNg+G3Yt5xnT+41IW+uJJRa5LYfnCs4c+Q8fn1LinaHAkn+He6mcZV4FWo/N6kgzpCmXZTRS0l7P9U7BkX7NFEDOau3ncZbktCMq/6CsmUQpPAFbr2n9EKPHU9YgGMi3IHq8/H8I3djc6lU9Aoa+Xm4ZQlyd86EdFSOk4TGRVL2zjzznSFqMWVjjJMRg=',)
        for i in resource_ec2.describe_instances()["Reservations"]:

            print(i["Instances"][0]["InstanceId"])
            instance_ids.append(i["Instances"][0]["InstanceId"])
        
        print("DONE")

        # print(resource_ec2.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"])
        return instance_ids
    except Exception as e:
        print(e)

def stop_ec2_instance(instance_id):
    try:
        print ("Stopping EC2 instance")
        # instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client("ec2",region_name='us-east-1',aws_access_key_id="ASIA5OSMFRWOCQHBWU6L",
            aws_secret_access_key="RWPpdW6meWpJH6wfl5/WBrjxIKH45NXiVlgx7sng",aws_session_token='FwoGZXIvYXdzEH4aDDYkgKtpXFmHTP0a4CLIAaRH3L2GDoLbMzckmHRzJRuSMApz8F0WiGm0Y+Gr0eQeDpl0CgJkGpmiGCciOvEz82LVdBYlGD6/czzCnK8qChYWIBraT87UgJ/i1VSpLA+NSWzsgjtzQGwnojXxLc4jGRiI3Ysd1vFsP16ByUhAqyUBNg+G3Yt5xnT+41IW+uJJRa5LYfnCs4c+Q8fn1LinaHAkn+He6mcZV4FWo/N6kgzpCmXZTRS0l7P9U7BkX7NFEDOau3ncZbktCMq/6CsmUQpPAFbr2n9EKPHU9YgGMi3IHq8/H8I3djc6lU9Aoa+Xm4ZQlyd86EdFSOk4TGRVL2zjzznSFqMWVjjJMRg=',)
        resource_ec2.stop_instances(InstanceIds=[instance_id])
        print(f"{instance_id} STOPPED")
    except Exception as e:
        print(e)

def get_public_ip(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1",aws_access_key_id="ASIA5OSMFRWOCQHBWU6L",
            aws_secret_access_key="RWPpdW6meWpJH6wfl5/WBrjxIKH45NXiVlgx7sng",aws_session_token='FwoGZXIvYXdzEH4aDDYkgKtpXFmHTP0a4CLIAaRH3L2GDoLbMzckmHRzJRuSMApz8F0WiGm0Y+Gr0eQeDpl0CgJkGpmiGCciOvEz82LVdBYlGD6/czzCnK8qChYWIBraT87UgJ/i1VSpLA+NSWzsgjtzQGwnojXxLc4jGRiI3Ysd1vFsP16ByUhAqyUBNg+G3Yt5xnT+41IW+uJJRa5LYfnCs4c+Q8fn1LinaHAkn+He6mcZV4FWo/N6kgzpCmXZTRS0l7P9U7BkX7NFEDOau3ncZbktCMq/6CsmUQpPAFbr2n9EKPHU9YgGMi3IHq8/H8I3djc6lU9Aoa+Xm4ZQlyd86EdFSOk4TGRVL2zjzznSFqMWVjjJMRg=',)
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))
            if instance.get("PublicIpAddress") == None:
                continue
            else:    
                return instance.get("PublicIpAddress")


def get_values_from_ec2(host):
    
    
    print(host)
    user="ubuntu"
    key=paramiko.RSAKey.from_private_key_file("./cloud_project_LSA.pem")
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    client.connect(host, username=user,pkey=key)
    # client.bind(('localhost', 5000))
    stdin, stdout, stderr = client.exec_command(f'cd /home/ubuntu/ && cd Data-Science/ && python3 EC2.py {200} {1000} {1}')
    print ("stderr: ", stderr.readlines())
    #for i,item in enumerate(stdout.readlines()):
       # print(i)
        #print(item)

    vals = stdout.readlines()[1]
    print ("output: ", vals)

    return vals

#for i in (0,3):
    #create_ec2_instance()

instance_ids = describe_ec2_instance()
print(instance_ids)

instance_ip_address = []

for instance in instance_ids:
    
    ip_address = get_public_ip(instance)
    instance_ip_address.append(ip_address)
    


print("The IPs: ",instance_ip_address)

risk_val=[]
val=[]
for i in instance_ip_address:
    if i is not None:
        my_values = get_values_from_ec2(i)
        print("my_values valto count",my_values)
        risk_val.append([my_values,i])
        val.append(my_values)

print("gasdygdasgdjasdguasdguadg",risk_val)
test_list=[]
print(len(risk_val))
#for i in instance_ids:
    #stop_ec2_instance(i)
for i in risk_val:
    #print(type(i))
    #print(i)
    #json1_data = json.loads(i)[0]
    #print(json1_data)
    for j in i:
        test_list.append(j)
        
print("testtsthgashhas",test_list)       

json_list = []
#json_list.append(json.loads(JSON_STRING))
#json.dumps(json_list)
#for i in test_list:

#print(test_list)
print("tetsttcdtcgctdtctctdtctdtctcttdtcc",test_list[0][0])
f_list_1=json.loads(test_list[0])
    #f_list_2=json.loads(test_list[1])
print("flistshdb",f_list_1['val_risk'])
#for i in test_list:
#    print("hhhhhhzcgjzdgzgcjhg",i) 

print("fshgfjsgfjsgfjsdfjsdfgjsdfgjsfgsjdfgahflsf",val)

all=[]
for i in val:
    h=json.loads(i)
    for i in h['val_risk']:
        
        all.append(i)
        
list_95=[]
list_99=[]
date=[]
data = all
for i in range(0, len(data)-1):
    for j in range(i+1, len(data)-1):
        if data[i][0]==data[j][0]:
            list_95.append(data[i][1]+data[j][1]/2)
            list_99.append(data[i][2]+data[j][2]/2)
            date.append(data[i][0])

print("vakeufaskfisdfhkdf",list_95)


