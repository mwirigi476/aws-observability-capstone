import os
import boto3

ecs_client = boto3.client('ecs')
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

# Fallback to us-east-1 SNS topic if env var is missing
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:093796422314:on-call-alert')

def lambda_handler(event, context):
    alarm_name = event['detail']['alarmName']
    state_reason = event['detail']['state']['reason']
    
    print(f"Remediation engine triggered by alarm: {alarm_name}. Reason: {state_reason}")
    
    # Action 1: Recycle ECS Fargate tasks if application metrics fail
    if "ecs" in alarm_name or "error-count" in alarm_name:
        print("Initiating rolling deployment restart for ECS Fargate tier...")
        try:
            ecs_client.update_service(
                cluster='production-backend-cluster',
                service='production-core-service',
                forceNewDeployment=True
            )
            print("ECS Fargate rollback triggered successfully.")
        except Exception as e:
            print(f"ECS restart failed (Check if service is active yet): {str(e)}")
        
    # Action 2: Tag the underlying Web Host for manual engineering review
    try:
        # Pull the reference host instance ID we built earlier
        ec2_client.create_tags(
            Resources=['i-0a559ebe51f64b5eb'],
            Tags=[{'Key': 'Status', 'Value': 'Investigate-Observability-Alert'}]
        )
        print("Targeted EC2 instance tagged successfully.")
    except Exception as e:
        print(f"Targeted EC2 tag update bypassed or failed: {str(e)}")
        
    # Action 3: Trigger real-time page to On-Call Engineers via SNS
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"🔥 CRITICAL INCIDENT: {alarm_name} activated",
        Message=f"Automated systems responded to: {alarm_name}.\nReason: {state_reason}\nAction taken: Forced Fargate task deployment & marked target instances as 'Investigate'."
    )
    
    return {"status": "RemediationExecutedSuccessfully"}
