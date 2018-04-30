import boto3
import json
import os

MTURK_SANDBOX = 'https://mturk-requester.us-east-1.amazonaws.com'
#MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   aws_access_key_id = "xxxxxxxxxxxxxxxxxx",
   aws_secret_access_key = "xxxxxxxxxxxxxxxxxxxxxxx",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

#hitId = "3Q7TKIAPOTAWOTH4YJVLJVPDW7UDLW"


print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my account\n")
print("Number of hits HITs from incl. preview: " + str(mturk.list_hits(MaxResults=100)['NumResults']))
hit_list = []
for x in mturk.list_hits(MaxResults=100)['HITs']:
    print("+++++++++++++++++++++++++")

    print("HIT status: ", x['HITStatus'], " HIT review status: ", x['HITReviewStatus'], x)
    # Delete all preview hits and make a list of real HITs
    if x['HITStatus'] == 'Unassignable':
        print("Unassignable HIT encountered. This will not be included in the HIT list for approvals")
    else:
        hit_list.append(x['HITId'])

submitted = []
approved = []
rejected = []
other = []

print("=====================================================================================")
print("=====================================================================================")
print("=====================================================================================\n\n")
print("Number of hits HITs, only published: " + str(len(hit_list)))

for hitId in hit_list:
   for assignment in mturk.list_assignments_for_hit(HITId=hitId)['Assignments']:

      if assignment['AssignmentStatus'] == 'Submitted':
         submitted.append(assignment)
      elif assignment['AssignmentStatus'] == 'Approved':
         approved.append(assignment)
      elif assignment['AssignmentStatus'] == 'Rejected':
         rejected.append(assignment)
      else:
         other.append(assignment)


print("\n=============================================================")
print("\n=============================================================")
print("\nNumber of Approved assignments: ", len(approved))
for assignment in approved:
    print("Approved Assignment :" + str(assignment))
    assignmentId = assignment['AssignmentId']
    workerId = assignment['WorkerId']
    results = assignment['Answer'].split("<Answer><QuestionIdentifier>"
                                         "results</QuestionIdentifier><FreeText>")[1].split(
        "</FreeText></Answer></QuestionFormAnswers>")[0]
    print("RESULTS: ", results)
    print("Hit ID: ", assignment['HITId'])
    try:
        #mturk.delete_hit(HITId=assignment['HITId'])
        print("HIT: ", assignment['HITId'], " deleted.")
    except:
        ("Delete HIT ID:", assignment['HITId'], " failed." )
    print("=============================================================\n")


