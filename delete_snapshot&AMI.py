
from datetime import datetime, timedelta, timezone
from dateutil import parser
from tracemalloc import Snapshot
import boto3

def lambda_handler(event, context):  
    try:
        image= boto3.client("ec2", region_name='us-east-1')
        ec2= boto3.resource("ec2")
        snapshots=ec2.snapshots.filter (Filters=[
                    {
                        'Name': 'tag:tr:application-asset-insight-id',
                        'Values': ["203700"]
                    }
               ] )
        amis = image.describe_images(Filters=[
                    {
                        'Name': 'tag:tr:application-asset-insight-id',
                        'Values': ["203700"]
                    }
               ] )      
        
        for ami in amis['Images']:
            create_date = ami['CreationDate']
            date = parser.parse(create_date)
            dereg_time = datetime.now(tz=timezone.utc) - timedelta(days=30)
            ami_id = ami['ImageId']
            if dereg_time > date:           
                ec2.deregister_image(ImageId=ami_id)
                print ('AMI with Id = {} is deregistered'.format(ami["ImageId"]))

        for snapshot in snapshots:
            start_time = snapshot.start_time
            delete_time = datetime.now(tz=timezone.utc) - timedelta(days=30)
            if delete_time > start_time:
                #print('fmt_start_time = {} And fmt_delete_time = {}'.format(start_time,delete_time))
                snapshot.delete()
                print ('Snapshot with Id = {} is deleted'.format(snapshot.snapshot_id))
    except BaseException as e:
       print('Failed to delete snapshot: ' + str(e))
