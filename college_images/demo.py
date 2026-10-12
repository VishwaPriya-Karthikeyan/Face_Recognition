WORKSPACE_PATH = 'Users\muthu\RealTimeObjectDetection\Tensorflow\workspace'
SCRIPTS_PATH = 'Users\muthu\RealTimeObjectDetection\Tensorflow\scripts'
APIMODEL_PATH = 'Users\muthu\RealTimeObjectDetection\Tensorflow\models'
ANNOTATION_PATH = WORKSPACE_PATH+'\annotations'
IMAGE_PATH = WORKSPACE_PATH+'\images'
MODEL_PATH = WORKSPACE_PATH+'\models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'\pre-trained-models'
CONFIG_PATH = MODEL_PATH+'\my_ssd_mobnet\pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'\my_ssd_mobnet'

import os

labels = [
    {'name':'Hello', 'id':1},
    {'name':'Yes', 'id':2},
    {'name':'No', 'id':3},
    {'name':'Thank You', 'id':4},
    {'name':'I Love You', 'id':5}
]

# Define the annotation path (make sure this is correct for your system)
ANNOTATION_PATH = 'Users\\muthu\\RealTimeObjectDetection\\Tensorflow\\workspace\\annotations'

# Create the directory if it doesn't exist
os.makedirs(ANNOTATION_PATH, exist_ok=True)

# Write label_map.pbtxt
with open(ANNOTATION_PATH + '\\label_map.pbtxt', 'w') as f:
    for label in labels:
        f.write('item {\n')
        f.write('\tname: \'{}\'\n'.format(label['name']))
        f.write('\tid: {}\n'.format(label['id']))
        f.write('}\n')


!python {SCRIPTS_PATH + '/generate_tfrecord.py'} -x {IMAGE_PATH + '/train'} -l {ANNOTATION_PATH + '/label_map.pbtxt'} -o {ANNOTATION_PATH + '/train.record'}
!python {SCRIPTS_PATH + '/generate_tfrecord.py'} -x {IMAGE_PATH + '/test'} -l {ANNOTATION_PATH + '/label_map.pbtxt'} -o {ANNOTATION_PATH + '/test.record'}
