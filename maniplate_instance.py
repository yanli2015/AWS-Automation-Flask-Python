import boto3
import datetime
import time

session = boto3.session.Session(
    aws_access_key_id='key',
    aws_secret_access_key='key',
    region_name="us-east-1")

ec2 = session.resource(service_name='ec2')

COST_CONFIG = {"'m4.large": "20", "t2.micro": "10"}


def launch_an_instance():
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}])
    for instance in instances:
        if instance.id:
            print(instance.id)
            return False
    instances = ec2.create_instances(
        ImageId='ami-9be6f38c',
        MinCount=1,
        MaxCount=1,
        KeyName="key",
        InstanceType="t2.micro",

    )
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'pending']}])
    for instance in instances:
        if instance.id:
            return True
        else:
            return False


def terminate_an_instance(id):
    ec2.instances.filter(InstanceIds=[id]).terminate()
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['terminated', 'shutting-down', 'pending']}])
    flag = False
    for instance in instances:
        if instance.id == id:
            flag = True
    return flag


def get_instances_info():
    utc_now = datetime.datetime.utcnow()
    dd = str(utc_now)[0:19]
    pp = '%Y-%m-%d %H:%M:%S'
    epoch_current_time = float(time.mktime(time.strptime(dd, pp)))
    print("epoch current timestamp: " + str(epoch_current_time))
    dic = {}
    sub_dic = {}
    count = 0
    running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    for instance in running_instances:
        count = count + 1
        d = str(instance.launch_time)[0:19]
        p = '%Y-%m-%d %H:%M:%S'
        epoch_launch_time = float(time.mktime(time.strptime(d, p)))
        time_used = (epoch_current_time - epoch_launch_time) / 3600
        sub_dic["Instance_id"] = instance.id
        sub_dic['Instance_type'] = instance.instance_type
        sub_dic['Instance_state'] = instance.state['Name']
        dic['Instance#' + str(count)] = sub_dic
        sub_dic['Epoch launch timeStamp'] = str(epoch_launch_time)
        sub_dic['Epoch used time'] = str(time_used)
    for key in dic.keys():
        print(key + "->" + str(dic[key]))
        print('\n')
    return dic

# get_instances_info()
