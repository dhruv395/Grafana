from __future__ import division
from requests.exceptions import ConnectionError
import json
import requests
import boto3
import smtplib

def main():
    # aws credentials
    aws_access_key_id="aws_access_key_id"
    aws_secret_access_key="aws_secret_access_key"
    # aws credentials end

    TargetGroupArn = 'arn:aws:elasticloadbalancing:us-west-2:***********:targetgroup/DBCheck/db139a9e7****'

    # list of influxdb machines
    influxdb_machine_1 = "i-0**43b******"
    influxdb_machine_2 = "i-0****e86616472"
    influxdb_machine_3 = "i-0*****6079af321"
    # end of machines

    machines_tuple = (influxdb_machine_1, influxdb_machine_2)

    client = boto3.client('elbv2',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name='us-west-2')

    def get_current_active_machine(TargetGroupArn):
        response = client.describe_target_health(TargetGroupArn=TargetGroupArn)
        for i in response['TargetHealthDescriptions']:
            if i['TargetHealth']['State'] == "draining":
                continue
            return i['Target']['Id']


    def get_next_machine(current_machine_id):
        return machines_tuple[(machines_tuple.index(current_machine_id)+1)%len(machines_tuple)]


    current_machine = get_current_active_machine(TargetGroupArn)
    register_machine = get_next_machine(current_machine)
    unregister_machine = [i for i in machines_tuple if i !=register_machine]

    for unregister in unregister_machine:
        client.deregister_targets(TargetGroupArn=TargetGroupArn,Targets=[{'Id': unregister,}])

    client.register_targets(TargetGroupArn=TargetGroupArn,Targets=[{'Id': register_machine}])
    print "done.."
    send_email("Influxdb machine with id %s is down"%(current_machine))


def send_email(body,recipient=['user1@gmail.com','user2@gmail.com'],user="cloud.alerts@gmail.com", pwd="Password",
            subject="Influxdb machine down!!"):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"




def check_connection():
    try:
        status_code = requests.get("http://influxdb-1160877343.us-west-2.elb.amazonaws.com:8086",timeout=10).status_code
    except ConnectionError as e:
        print e
        status_code = 500
    if status_code >= 500:
        print "switching machines"
        main()
    else:
        print "status ok"


def lambda_handler(event, context):
    main()
    print event
    print dir(context)
    check_connection()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    check_connection()
