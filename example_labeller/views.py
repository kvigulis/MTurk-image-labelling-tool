import os, datetime

from django.shortcuts import render, get_object_or_404

from django.conf import settings

from image_labelling_tool import labelling_tool
from image_labelling_tool import models as lt_models
from image_labelling_tool import labelling_tool_views
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from . import models
import json

import logging


logger = logging.getLogger(__name__)


def home(request):
    #print("request META:", request.META)
    #request_str = "request - 'USERNAME':" + request.META['USERNAME'] + "; REMOTE_ADDR:" +  request.META['REMOTE_ADDR']
    #logger.info(request.META)
    # Force Log out the user if his browser has save the session data and he is being automatically logged in.
    logout(request)
    logged_in = False
    query_string = ''
    assignmentId = 'NOT_SET'
    preview_mode = True

    mturk_urls = ['workersandbox.mturk.com', 'worker.mturk.com']

    try:
        # Check if the request comes from either Sandbox or the production Mturk.
        if any(x in request.META['HTTP_REFERER'] for x in mturk_urls):
            query_string = request.META['QUERY_STRING']
            assignmentId = query_string.split('assignmentId=')[1].split('&')[0]
            log_str = "assignmentId:" + assignmentId
            logger.info(log_str)
            try:
                if 'ASSIGNMENT_ID_NOT_AVAILABLE' not in assignmentId:
                    workerId = query_string.split('workerId=')[1].split('&')[0]
                    log_str = "workerId:" + workerId
                    logger.info(log_str)
                    preview_mode = False
                    if not User.objects.filter(username=workerId).exists():
                        logger.info("New user was created")
                        user = User.objects.create_user(username=workerId, password='Frusciante11')
                        user.save()
                        user = authenticate(username=workerId, password='Frusciante11')
                        login(request, user)
                        logged_in = True
                    else:
                        logger.info("User was logged in")
                        user = authenticate(username=workerId, password='Frusciante11')
                        login(request, user)
                        logged_in = True

            except:
                logger.warning("Something went wrong with user authentication")
    except:
        logger.warning("The request from a non AMT address was made.")

    image_descriptors = [labelling_tool.image_descriptor(
            image_id=img.id, url=img.image.url,
            width=img.image.width, height=img.image.height) for img in models.ImageWithLabels.objects.all()]

    # Convert the label class tuples in `settings` to `labelling_tool.LabelClass` instances
    label_classes = [labelling_tool.LabelClass(*c) for c in settings.LABEL_CLASSES]

    #list example / demonstration images
    image_path = os.path.join(settings.STATIC_ROOT, 'example_images')
    image_dir_files = os.listdir(image_path)

    context = {
        'label_classes': [c.to_json() for c in label_classes],
        'image_descriptors': image_descriptors,
        'initial_image_index': 0,
        'labelling_tool_config': settings.LABELLING_TOOL_CONFIG,
        'example_images': image_dir_files,
        'assignmentId': assignmentId,
        'preview_mode': preview_mode,
        'logged_in': logged_in,
    }
    return render(request, 'index.html', context)


def visualizer(request):
    logged_in = True
    image_descriptors = [labelling_tool.image_descriptor(
            image_id=img.id, url=img.image.url,
            width=img.image.width, height=img.image.height) for img in models.ImageWithLabels.objects.all()]

    # Convert the label class tuples in `settings` to `labelling_tool.LabelClass` instances
    label_classes = [labelling_tool.LabelClass(*c) for c in settings.LABEL_CLASSES]

    # list example / demonstration images
    image_path = os.path.join(settings.STATIC_ROOT, 'example_images')
    image_dir_files = os.listdir(image_path)


    context = {
        'label_classes': [c.to_json()   for c in label_classes],
        'image_descriptors': image_descriptors,
        'initial_image_index': 0,
        'labelling_tool_config': settings.LABELLING_TOOL_CONFIG,
        'example_images': image_dir_files,
        'logged_in': logged_in,

    }
    return render(request, 'visualizer.html', context)



class LabellingToolAPI (labelling_tool_views.LabellingToolViewWithLocking):
    '''Inherits from 'LabellingToolViewWithLocking'. Found in Python sitd-packages'''

    def get_labels(self, request, image_id_str, *args, **kwargs):
        image = get_object_or_404(models.ImageWithLabels, id=image_id_str)
        return image.labels

    def get_next_unlocked_image_id_after(self, request, current_image_id_str, *args, **kwargs):
        unlocked_labels = lt_models.Labels.objects.unlocked()
        unlocked_imgs = models.ImageWithLabels.objects.filter(labels__in=unlocked_labels)
        unlocked_img_ids = [img.id for img in unlocked_imgs]
        print("unlocked_img_ids(child class):", unlocked_img_ids)
        try:
            index = unlocked_img_ids.index(int(current_image_id_str))
            print("Image index: ", index)
        except ValueError:
            print("Image selection ERROR: No unlocked images found")
            return None
        index += 1
        if index < len(unlocked_img_ids):
            print("unlocked image name (returned):",unlocked_img_ids[index])
            return unlocked_img_ids[index]
        else:
            return None


    def get_unlocked_image_ids(self, request, *args, **kwargs):
        '''Overridden method called in the parents get() method'''
        unlocked_labels = lt_models.Labels.objects.unlocked()
        unlocked_imgs = models.ImageWithLabels.objects.filter(labels__in=unlocked_labels)
        unlocked_img_ids = [img.filename() for img in unlocked_imgs]
        unlocked_img_ids = {"unlocked_ids": unlocked_img_ids}
        return unlocked_img_ids


