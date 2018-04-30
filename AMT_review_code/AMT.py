import boto3


MTURK_SANDBOX = 'https://mturk-requester.us-east-1.amazonaws.com'
#MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = "***************",
   aws_secret_access_key = "**************",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)
print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my account")


# Example of using qualification to restrict responses to Workers who have had
# at least 80% of their assignments approved. See:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html#ApiReference_QualificationType-IDs
worker_requirements = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [90],
    'RequiredToPreview': True,
}]

question = open('questions.xml',mode='r').read()
new_hit = mturk.create_hit(
   Title = 'Image marking - Electronics components (5-20min depending on the image)',
   Description = 'Mark all the electronics components with polygons or rectangles. See the instructions please. (WARNING! Can be completed only with mouse. No touchscreen devices.)',
   Keywords = 'contours, image labeling, draw, image marking, image annotation, image',
   Reward = '1.00',
   MaxAssignments = 1,
   LifetimeInSeconds = 864000, # 10 days
   AssignmentDurationInSeconds = 7200,
   AutoApprovalDelayInSeconds = 1728000, # 20 days
   Question = question,
   QualificationRequirements=worker_requirements,
)
print("A new HIT has been created. You can preview it here:")
# workersandbox.mturk.com
print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITTypeId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=