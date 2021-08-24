from flask import Flask, render_template,redirect,url_for,request,jsonify
import json,random


import random
import botocore
from operator import is_not
import http.client
import time
import json
import statistics
import boto3
import math
from functools import partial
import paramiko
from boto.manage.cmdshell import sshclient_from_instance
from paramiko import SSHClient

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

app=Flask(__name__)

risk_val=[]
val=[]
def creating_istance():
    try:
        print ("Creating EC2 instance")
        resource_ec2 = boto3.client("ec2",region_name='us-east-1',aws_access_key_id="ASIA5OSMFRWOPPQV5MN5",
            aws_secret_access_key="Lo7SUetIphlPLsNxIsry9I4qKkX4ippLBlujDT4t",aws_session_token='FwoGZXIvYXdzEO3//////////wEaDIKch3I1+R8Vr5cVCyLIAUCCidkrMjRegrxXvLAyM8vxP02x1/x3X0dUTOMWghENcB1wwd1OoyX0gaqxU/JeqxPiLT3ZzeVNoo4r9a7zeMqWFpCaa5sS75J0zqQltZwpjhV+cg9QKq5ExKGUSrO4UzFS1jPTHb90AsfIDevMmMli0/sFL0qQoIBUxPjO0R00rSDc2Povyyc7r5HstDfxcwG8jULJg2oeLE9JEU311HxSyqG5x/q02hSIQuwAJhCxFuFxwDFABWK1rESg7SasZ3gSh3/oeg8mKOeDjokGMi2Hme7+4jFTQ70+Ufe0bzJeLhFh9elD1WcXFOfMWLArJ7seUOgjc7Y9ZnMLpdE=',)
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
        
def define_ec2():
    instance_ids = []
    try:
        print ("Defining EC2 instance")
        resource_ec2 = boto3.client("ec2",region_name='us-east-1',aws_access_key_id="ASIA5OSMFRWOPPQV5MN5",
            aws_secret_access_key="Lo7SUetIphlPLsNxIsry9I4qKkX4ippLBlujDT4t",aws_session_token='FwoGZXIvYXdzEO3//////////wEaDIKch3I1+R8Vr5cVCyLIAUCCidkrMjRegrxXvLAyM8vxP02x1/x3X0dUTOMWghENcB1wwd1OoyX0gaqxU/JeqxPiLT3ZzeVNoo4r9a7zeMqWFpCaa5sS75J0zqQltZwpjhV+cg9QKq5ExKGUSrO4UzFS1jPTHb90AsfIDevMmMli0/sFL0qQoIBUxPjO0R00rSDc2Povyyc7r5HstDfxcwG8jULJg2oeLE9JEU311HxSyqG5x/q02hSIQuwAJhCxFuFxwDFABWK1rESg7SasZ3gSh3/oeg8mKOeDjokGMi2Hme7+4jFTQ70+Ufe0bzJeLhFh9elD1WcXFOfMWLArJ7seUOgjc7Y9ZnMLpdE=',)
        for i in resource_ec2.describe_instances()["Reservations"]:

            print(i["Instances"][0]["InstanceId"])
            instance_ids.append(i["Instances"][0]["InstanceId"])
        
        print("DONE")

        # print(resource_ec2.describe_instances()["Reservations"][0]["Instances"][0]["InstanceId"])
        return instance_ids
    except Exception as e:
        print(e)
        
def get_public_ip(ins):
    ec2_client = boto3.client("ec2", region_name="us-east-1",aws_access_key_id="ASIA5OSMFRWOPPQV5MN5",
            aws_secret_access_key="Lo7SUetIphlPLsNxIsry9I4qKkX4ippLBlujDT4t",aws_session_token='FwoGZXIvYXdzEO3//////////wEaDIKch3I1+R8Vr5cVCyLIAUCCidkrMjRegrxXvLAyM8vxP02x1/x3X0dUTOMWghENcB1wwd1OoyX0gaqxU/JeqxPiLT3ZzeVNoo4r9a7zeMqWFpCaa5sS75J0zqQltZwpjhV+cg9QKq5ExKGUSrO4UzFS1jPTHb90AsfIDevMmMli0/sFL0qQoIBUxPjO0R00rSDc2Povyyc7r5HstDfxcwG8jULJg2oeLE9JEU311HxSyqG5x/q02hSIQuwAJhCxFuFxwDFABWK1rESg7SasZ3gSh3/oeg8mKOeDjokGMi2Hme7+4jFTQ70+Ufe0bzJeLhFh9elD1WcXFOfMWLArJ7seUOgjc7Y9ZnMLpdE=',)
    reservations = ec2_client.describe_instances(InstanceIds=[ins]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))
            if instance.get("PublicIpAddress") == None:
                continue
            else:    
                return instance.get("PublicIpAddress")

def get_values(host,CC_MinHistory,CC_shots):
    CC_MinHistory=int(CC_MinHistory)
    CC_shots=int(CC_shots)
    
    print(host)
    user="ubuntu"
    key=paramiko.RSAKey.from_private_key_file("./cloud_project_LSA.pem")
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    client.connect(host, username=user,pkey=key)
    # client.bind(('localhost', 5000))
    stdin, stdout, stderr = client.exec_command(f'cd /home/ubuntu/ && cd Data-Science/ && python3 EC2.py {CC_MinHistory} {CC_shots} {1}')
    print ("stderr: ", stderr.readlines())
    #for i,item in enumerate(stdout.readlines()):
       # print(i)
        #print(item)

    vals = stdout.readlines()[1]
    print ("output: ", vals)

    return vals
def stop_instance(instanceid):
    try:
        print ("Stopping EC2 instance")
        # instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client("ec2")
        resource_ec2.stop_instances(InstanceIds=[instanceid])
        print(f"{instanceid} STOPPED")
    except Exception as e:
        print(e)
        
def get_values(host,CC_MinHistory,CC_shots):
    
    CC_shots=int(CC_shots)
    CC_MinHistory=int(CC_MinHistory)
    print("I am here",host)
    user="ubuntu"
    key=paramiko.RSAKey.from_private_key_file("./cloud_project_LSA.pem")
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    client.connect(host, username=user,pkey=key)
    # client.bind(('localhost', 5000))
    stdin, stdout, stderr = client.exec_command(f'cd /home/ubuntu/ && cd Data-Science/ && python3 EC2.py {CC_MinHistory} {CC_shots} {1}')
    print ("stderr: ", stderr.readlines())
    #for i,item in enumerate(stdout.readlines()):
       # print(i)
        #print(item)

    vals = stdout.readlines()[1]
    print ("output: ", vals)

    return vals

def EC2_instace(CC_resources,CC_MinHistory,CC_shots):
    #for i in range(CC_resources):
        #creating_istance()
    #time.sleep(120)
    
    instanceId = define_ec2()
    print(instanceId)
    
    instanceIPaddress = []
    
    for ins in instanceId:
        
        ip_address = get_public_ip(ins)
        print("ip_addressajajdjas",ip_address)
        instanceIPaddress.append(ip_address)
    for i in instanceId:
        stop_instance(i)
        
    for i in instanceIPaddress:
        print(i)
        if i is not None:
            print(i)
            my_values = get_values(i,CC_MinHistory,CC_shots)
            print("my_values valto count",my_values)
            risk_val.append([my_values,i])
            val.append(my_values)
    
    return  risk_val,val  
    

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        CC_services = request.form['Services']
        CC_resources = int(request.form['resources'])
        CC_MinHistory = request.form['MinHistory']
        CC_shots = request.form['shots']
        CC_scale = request.form['digits']
        print("Service used: ", CC_services)
        print("Resources used: ", CC_resources)
        print("Shots used: ", CC_shots)
        print("Digits used: ", CC_scale)
        
        risk,values=EC2_instace(CC_resources,CC_MinHistory,CC_shots)
        print("valuesadhakhk",values)
        
        elpsed=[]
        for i in val:
            h=json.loads(i)
            elpsed.append(float(h['Elp_time']))
        elpsed_time=elpsed[0]+elpsed[1]/2
        print("elpsed_time",elpsed_time)
        all=[]
        for i in values:
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
               
        print("datestesaus",date)
        
        print("vakeufaskfisdfhkdf",list_95)
        estimated_risk_val_95=list_95[-1]
        estimated_risk_val_99=list_99[-1]
        return render_template('graph.html', resource_type=CC_services, resource_type2=CC_resources,CC_MinHistory=CC_MinHistory,resource_type3=CC_shots,resource_type4=CC_scale,list_95=list_95,list_99=list_99,date=date,elpsed_time=elpsed_time,estimated_risk_val_95=estimated_risk_val_95,estimated_risk_val_99=estimated_risk_val_99)
    else:
        return render_template('home.html')
    

if __name__ == "__main__":
    app.run(debug=True)



