import boto3
import json
import os

MTURK_SANDBOX = 'https://mturk-requester.us-east-1.amazonaws.com'
#MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   aws_access_key_id = "xxxxxxxxxxxxxxxxxxxxxxx",
   aws_secret_access_key = "xxxxxxxxxxxxxxxxxxx",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

# TODO: DANGER / IMPORTAND: Always check if this is False before running, unless setting to True deliberately. !!!!!!!!!!!!!!!!!
delete_all_results = False
auto_approve = False

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
print("=====================================================================================")
print("=====================================================================================")
print("=====================================================================================\n\n")
print("Number of hits HITs, only published: " + str(len(hit_list)))

submitted = []
approved = []
rejected = []
other = []

for hitId in hit_list:
    if delete_all_results:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Number of assignments :" + str(mturk.list_assignments_for_hit(HITId=hitId)['NumResults']))
        print("WARNING! Deleting result :" + str(mturk.list_assignments_for_hit(HITId=hitId)))
        #mturk.update_hit_review_status(HITId=hitId, Revert=True)
        if auto_approve:
            for assignment in mturk.list_assignments_for_hit(HITId=hitId)['Assignments']:
                try:
                    mturk.approve_assignment(AssignmentId=assignment['AssignmentId'],
                                             RequesterFeedback='Thank you! Your work has been approved.')
                except:
                    print("ERROR: Assignment could not be approved. It is possible the it has already been approved.")
                # mturk.reject_assignment(AssignmentId='string', RequesterFeedback='Sorry! Your work was not accepted.')
        mturk.delete_hit(HITId=hitId)
    else:

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
    #print(assignment['HITId'])
    print("=============================================================\n")
    # try:
    #     mturk.delete_hit(HITId=assignment['HITId'])
    # except:
    #     print("Could not delete approved Hit")

print("\n=============================================================")
print("\n=============================================================")
print("\nNumber of Rejected assignments: ", len(rejected))
for assignment in rejected:
    print("Rejected Assignment :" + str(assignment))
    assignmentId = assignment['AssignmentId']
    workerId = assignment['WorkerId']
    results = assignment['Answer'].split("<Answer><QuestionIdentifier>"
                                         "results</QuestionIdentifier><FreeText>")[1].split(
        "</FreeText></Answer></QuestionFormAnswers>")[0]
    print("RESULTS: ", results)
    # try:
    #     labels = json.loads(results)
    #     labels["assignment_id"] = assignmentId
    #     labels["worker_id"] = workerId
    #     image_filename = labels["image_filename"]
    #     print(labels)
    #     print(image_filename)
    #     filename_prefix = image_filename.split(".")[0]
    #     full_filename = filename_prefix + "_labels.json"
    #     file_path = 'rejected_labels/' + full_filename
    #     print(file_path)
    #     with open(file_path, 'w') as outfile:
    #         json.dump(labels, outfile)
    # except:
    #     print("Could not save the labels.json file")
    # print("=============================================================\n")


print("\n=============================================================")
print("\n=============================================================")
print("\nNumber of Submitted assignments: ", len(submitted))
for assignment in submitted:
    print("Submitted Assignment :" + str(assignment))
    assignmentId = assignment['AssignmentId']
    workerId = assignment['WorkerId']
    results = assignment['Answer'].split("<Answer><QuestionIdentifier>"
                                         "results</QuestionIdentifier><FreeText>")[1].split(
        "</FreeText></Answer></QuestionFormAnswers>")[0]
    print("RESULTS: ", results)
    labels = json.loads(results)
    labels["assignment_id"] = assignmentId
    labels["worker_id"] = workerId
    image_filename = labels["image_filename"]
    print(labels)
    print(image_filename)
    filename_prefix = image_filename.split(".")[0]
    full_filename = filename_prefix + "_labels.json"
    file_path = 'labels/' + full_filename
    print(file_path)
    with open(file_path, 'w') as outfile:
        json.dump(labels, outfile)
    print("=============================================================\n")
