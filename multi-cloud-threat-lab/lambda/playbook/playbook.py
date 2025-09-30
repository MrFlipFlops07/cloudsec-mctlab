#!/usr/bin/env python3
import json, boto3, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')
iam = boto3.client('iam')

def stop_instance(instance_id):
    try:
        resp = ec2.stop_instances(InstanceIds=[instance_id])
        logger.info("Stopped instance: %s result: %s", instance_id, resp)
        return True
    except Exception as e:
        logger.exception("Failed to stop instance: %s", e)
        return False

def revoke_access_key(username, access_key_id):
    try:
        iam.update_access_key(UserName=username, AccessKeyId=access_key_id, Status='Inactive')
        logger.info("Revoked access key %s for %s", access_key_id, username)
        return True
    except Exception as e:
        logger.exception("Failed to revoke access key: %s", e)
        return False

def lambda_handler(event, context):
    logger.info("Playbook triggered with event: %s", event)
    action = event.get('action')
    evidence = event.get('evidence', {})
    # If we find instance id in evidence, stop it
    instance_id = evidence.get('instanceId') or evidence.get('instance_id') or event.get('instance_id')
    if instance_id:
        stop_instance(instance_id)
        return {"stopped": instance_id}
    # If evidence shows accessKeyId and user, revoke
    ak = evidence.get('requestParameters', {}).get('accessKeyId') or event.get('accessKeyId')
    user_arn = evidence.get('userIdentity', {}).get('arn')
    if ak and user_arn:
        # try to extract username from arn if possible
        if ":" in user_arn:
            username = user_arn.split("/")[-1]
        else:
            username = user_arn
        revoke_access_key(username, ak)
        return {"revoked": ak, "user": username}
    logger.info("No actionable artifact in evidence")
    return {"status": "noaction"}
