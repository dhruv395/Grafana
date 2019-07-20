from __future__ import division
from requests.exceptions import ConnectionError
import json
import requests
import boto3
import smtplib

def main():
    # aws credentials
    aws_access_key_id="............."
    aws_secret_access_key=".............."
    # aws credentials end

    TargetGroupArn = 'arn:aws:elasticloadbalancing:us-west-2:4..........8:targetgroup/DBCheck/d.......8'

    # list of influxdb machines
    influxdb_machine_1 = "i-0.......3"
    influxdb_machine_2 = "i-0........2"
    influxdb_machine_3 = "i-0.........1"
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


def send_email(body,recipient=['email.id','email.id'],user="email.alerts@officeid.com", pwd="psword",
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
