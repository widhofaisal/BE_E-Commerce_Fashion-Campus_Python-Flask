# initialize model

import torch
import torch.nn as nn
import torchvision
from collections import OrderedDict


class Model:
    model = torchvision.models.mobilenet_v2(pretrained=True)

    for param in model.parameters():
        param.requires_grad = False

    newClassifier = nn.Sequential(
        OrderedDict([
            ('0', nn.Dropout(p=0.2, inplace=False)),
            ('1', nn.Linear(in_features=1280, out_features=11, bias=True))
        ])
    )

    model.classifier = newClassifier

    def __init__(self):
        self.load_model()

    def load_model(self):
        self.model.load_state_dict(torch.load(
            "AI/model_terbaruNew.pt", map_location=torch.device('cpu')))  # torch
        self.model.eval()

    @property
    def get_model(self):
        return self.model
