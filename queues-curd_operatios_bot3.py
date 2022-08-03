import boto3

session = boto3.Session(profile_name='connectit')
client = session.client('connect')


def get_instance_id(instance_name):
    
    response = client.list_instances()
    for i in response.pop('InstanceSummaryList'):
        if i['InstanceAlias']==instance_name:
            return i['Id']

def check_queue(instance_id,queue_name,hours_id,queue_type):
    response = client.list_queues(
    InstanceId=instance_id,
    )
    for i in response.pop('QueueSummaryList'):
        if i['QueueType']==queue_type:
            if i['Name']==queue_name:
                try:
                    # return i['Id']
                    update_queue_id= i['Id']
                    q=update_queue(instance_id,hours_id,update_queue_id,queue_type,queue_name)
                    return q
                except Exception as qnot:
                    return qnot
    else:
        try:
            qc=create_queue(instance_id,queue_name,hours_id)
            return qc
        except Exception as qcnot:
            return qcnot

def update_queue(instance_id,hours_id,update_queue_id,queue_type,queue_name):
    response = client.update_queue_hours_of_operation(
    InstanceId=instance_id,
    QueueId=update_queue_id,
    HoursOfOperationId=hours_id,
    )
    response = client.list_queues(
    InstanceId=instance_id,
    )
    for i in response.pop('QueueSummaryList'):
        if i['QueueType']==queue_type:
            if i['Name']==queue_name:
                return i['Id']
    

def create_queue(instance_id,queue_name,hours_id):

    response = client.create_queue(
        InstanceId=instance_id,
        Name=queue_name,
        # Description='string',
        HoursOfOperationId=hours_id,
        Tags={
            'Name': 'QueueCreation'
        }
    )
    return response['QueueId']

def create_hours_operations(instance_id,hours_name):

    response = client.create_hours_of_operation(
        InstanceId=instance_id,
        Name=hours_name,
        TimeZone='Asia/Kolkata',
        Config=[
        {
            'Day': 'WEDNESDAY',
            'StartTime': {
                'Hours': 4,
                'Minutes': 00
            },
            'EndTime': {
                'Hours': 5,
                'Minutes': 00
            }
        },
    ],
    )
    return response['HoursOfOperationId']

def update_hours_of_operation(instance_id,hours_name,update_hours_id):
    
    response = client.update_hours_of_operation(
    InstanceId=instance_id,
    HoursOfOperationId=update_hours_id,
    Name=hours_name,
    Description='Updation Of Hours_Of_Operation',
    TimeZone='Asia/Kolkata',
    Config=[
        {
            'Day': 'THURSDAY',
            'StartTime': {
                'Hours': 11,
                'Minutes': 00
            },
            'EndTime': {
                'Hours': 12,
                'Minutes': 00
            }
        },
    ]
    )
    # print(response)
    response = client.list_hours_of_operations(
        InstanceId=instance_id,
    )
    for j in response.pop('HoursOfOperationSummaryList'):
        if j['Name']==hours_name:
            return j['Id']
    


def check_hours_of_operation(instance_id,hours_name):

    response = client.list_hours_of_operations(
        InstanceId=instance_id,
    )
    # print(response)
    for i in response.pop('HoursOfOperationSummaryList'):
            if i['Name']==hours_name:
                try:
                    # print(i)
                    update_hours_id= i['Id']
                    s=update_hours_of_operation(instance_id,hours_name,update_hours_id)
                    return s
                except Exception as e:
                    return e
    else:
        try:
            u=create_hours_operations(instance_id,hours_name)
            return u
        except Exception as d:
            return d

# def delete_hours_of_operation(list,instance_id):

#     response = client.delete_hours_of_operation(
#         InstanceId=instance_id,
#         HoursOfOperationId=list
#     )
#     return response




instance_name='epam-awsconnect'
instance_id=get_instance_id(instance_name)
print('instanceID=',instance_id)
hours_name='Basic Hours1'
hours_id=check_hours_of_operation(instance_id,hours_name)
print('hoursID=',hours_id)
# y=delete_hours_of_operation(list,instance_id)
queue_name='myqueue-12'
queue_type='STANDARD'
queue_id=check_queue(instance_id,queue_name,hours_id,queue_type)
print('queueID=',queue_id)