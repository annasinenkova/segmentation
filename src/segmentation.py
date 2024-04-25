from PIL import Image
import torchvision

import warnings
import torch


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


def segmentation():
    path = 'St5FF-zqLHE.jpg'
    img = Image.open(path)
    
    torch.set_grad_enabled(False)
    warnings.filterwarnings("ignore")
    pretrained_model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    pretrained_model = pretrained_model.eval().cpu()

    img_tensor = torchvision.transforms.functional.to_tensor(img).cpu()
    output = pretrained_model([img_tensor])[0]
    
    boxes, labels, scores = filter(output)

