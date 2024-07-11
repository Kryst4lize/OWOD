import csv
import split as splt
import masking as mk
import instance as ins 
import select as slt

T1_COCO_CLASS_NAMES = [
    "airplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "dining table", "dog", "horse", "motorcycle", "person",
    "potted plant", "sheep", "couch", "train", "tv"
]
T2_CLASS_NAMES = [
    "truck", "traffic light", "fire hydrant", "stop sign", "parking meter",
    "bench", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase",
    "microwave", "oven", "toaster", "sink", "refrigerator"
]
T3_CLASS_NAMES = [
    "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake"
]
T4_CLASS_NAMES = [
    "bed", "toilet", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl"
]

min_images_required = 20000
max_images_required = 20000
annotation_path =    '../annotations/instances_train2017.json'
destination_path =   '../json_coco_file/'
spliting_file_name = ["T1_instances_train2017_split.json","T2_instances_train2017_split.json","T3_instances_train2017_split.json","T4_instances_train2017_split.json"]
Class = [T1_COCO_CLASS_NAMES,T2_CLASS_NAMES,T3_CLASS_NAMES,T4_CLASS_NAMES]
Image_list = [destination_path+'image_list_blank.json', 
              destination_path+'image_list_task1.json',
              destination_path+'image_list_task2.json',
              destination_path+'image_list_task3.json',
              destination_path+'image_list_task4.json']
"""
slt.process_coco_annotations_task(annotation_path,Image_list[1], 35000, 35000, Class[0], Image_list[0])
slt.process_coco_annotations_task(annotation_path,Image_list[2], min_images_required, max_images_required, Class[1], Image_list[1])
slt.process_coco_annotations_task(annotation_path,Image_list[3], min_images_required, max_images_required, Class[2], Image_list[2])
slt.process_coco_annotations_task(annotation_path,Image_list[4], min_images_required, max_images_required, Class[3], Image_list[3])
"""
slt.get_unique_images(annotation_path, Image_list, destination_path+'image_list_task0.json')
# All comment below are for testing, validate and give an example of how to use the function

# mk.masking_json(annotation_path, destination_path+spliting_file_name[1], Class[1], num_images= 3000) 
# slt.filter_and_select_images(destination_path+spliting_file_name[1], '../json_coco_file/T2_instances_train2017_split_revised.json', [20000, 50000], Class[1])
# ins.count_categories('../json_coco_file/T2_instances_train2017_split_revised.json')
# ins.count_categories('../json_coco_file/T2_instances_train2017_split.json')
# ins.total_images_check(destination_path+spliting_file_name[1],destination_file_path=destination_path, classes=Class[1].append("unknown"), file_name='T2_total_images.csv')
# ins.count_annotation(destination_path+spliting_file_name[1], destination_file_path =destination_path, file_name='T2_annotation.csv')
# slt.process_coco_annotations_task(annotation_path,destination_path+'image_list_task1.json', min_images_required, max_images_required, T1_COCO_CLASS_NAMES)