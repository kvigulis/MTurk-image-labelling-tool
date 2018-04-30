import boto3
import json
import os

MTURK_SANDBOX = 'https://mturk-requester.us-east-1.amazonaws.com'
#MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client('mturk',
   aws_access_key_id = "xxxxxxxxxxxx",
   aws_secret_access_key = "xxxxxxxxxxxxxxxxxxx",
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

assignment_ID = '3P4RDNWND569NY6KDEPLJXNJ8BVJI8'
#requesterFeedback='Your work has been approved, but please try to be a bit more precise. Carefully watching the video and example images at the bottom of the webpage might help. Thank you.'
requesterFeedback='Thank you for your work! It has been approved. Keep it up.'
#requesterFeedback='Excellent! Your work has been approved. Keep it up.'
#requesterFeedback='Please try to mark around SMT resistors and capactiors more closely with the box tool.'
#requesterFeedback='Thank you for the brilliant quality work! Note: You don\'t need to mark PCB holes. Please, GOOGLE some images to see what I mean by PCB holes. Your work has been approved.'
#requesterFeedback='Thank you for the brilliant quality work! Your work has been approved.'
#requesterFeedback='Thank you! Your work has been approved. But please try to be more precise next time. Watching the examples at the end of the video might help.'
#requesterFeedback='Sorry. The work was not precise enough and there were too many errors. Carefully watching the video and example images at the bottom of the webpage might help. Thank you.'
#requesterFeedback='Sorry. The work was not precise enough and there were too many errors. Some of the components are marked correctly but more than half ' \
#                  'are not up to the required quality standard. Please see all the example images at the bottom of the page and watch the whole video.'
#                   'Also, when marking the pins of the components with less than 5 pins, include them all in the same polygon. ' \
#                   'Try zooming in and out using the mouse wheel for easier tracing, to increase the precision.'
# requesterFeedback='Sorry. The work was not precise enough. For squere components try to use "Draw box" tool. Few of the components are marked correctly but more than half ' \
#                 'are not up to the required quality standard. Please see all the example images at the bottom of the page. '\
#                  'Try using the Draw polygon tool.'
#requesterFeedback='Sorry. The result you sent was empty. (No work was done) This could happen due to server errors. If you think this rejection is unjustified or is a mistake, please send a screenshot of your work to karlis.vigulis@city.ac.uk.'
#requesterFeedback='Recalled rejection. It is possible that there was a mistake produced by our system, thus although empty your work is approved.'
#requesterFeedback='Please try to mark around SMT resistors and capactiors more closely with the box tool. An example of WRONG labelling can be seen at 2:41 in the video and of CORRECT at 3:05. If the future work does not get improved, it might get rejected.'
#requesterFeedback='Rejection reason. Too many components were left unlabelled or were labelled wrong.'
try:
    # TODO: check if the function is set to approve_assignment() or reject_assignment().#requesterFeedback= 'Sorry. Although I can see you have tried, the work was not done correctly. Please try to mark around the SMT resistors and capactiors more closely with the box tool. Watching the examples at the end of the video might help.'


    mturk.approve_assignment(AssignmentId=assignment_ID,
                            RequesterFeedback=requesterFeedback) # .approve_assignment(OverrideRejection=True) for reverting rejection
    # (OverrideRejection=True)
    print("Assignment : ", assignment_ID, " has been reviewed.")
except:
    print("ERROR: Assignment could not be approved. It is possible the it has already been approved.")