from PIL import Image
import torchvision

import warnings
import torch

import random
import numpy as np
import cv2


def filter(output):
    boxes = []
    labels = []
    scores = []

    for i in range(len(output['scores'])):
        if output['scores'][i] >= 0.5:
            boxes.append(output['boxes'][i].int().cpu().numpy())
            labels.append(output['labels'][i].cpu().numpy())
            scores.append(output['scores'][i].cpu().numpy())
        
    return boxes, labels, scores
    
    
def categories_from_txt(path):
    categories = []
    with open(path, 'r') as file:
        for line in file:
            categories.append(line.strip())

    return categories
    
    
def segmented_image(img, boxes, labels, scores):
    categories = categories_from_txt('../data/categories.txt')
        
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in categories]
        
    result_image = np.array(img)
        
    for box, label, score, in zip(boxes, labels, scores):
        color = random.choice(colors)
        tl = round(0.002 * max(result_image.shape[0:2])) + 1
        c1, c2 = (box[0], box[1]), (box[2], box[3])
        cv2.rectangle(result_image, c1, c2, color, thickness=tl)
        display_txt = "%s: %.1f%%" % (categories[label], 100*score)
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(display_txt, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(result_image, c1, c2, color, -1)
        cv2.putText(result_image, display_txt, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    
    return Image.fromarray(result_image.astype(np.uint8))


def segmentation(path):
    img = Image.open(path)
    
    torch.set_grad_enabled(False)
    warnings.filterwarnings("ignore")
    pretrained_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    pretrained_model = pretrained_model.eval().cpu()

    img_tensor = torchvision.transforms.functional.to_tensor(img).cpu()
    output = pretrained_model([img_tensor])[0]
    
    boxes, labels, scores = filter(output)

    return segmented_image(img, boxes, labels, scores)
