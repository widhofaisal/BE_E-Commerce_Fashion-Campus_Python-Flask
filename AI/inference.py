# this file is for handling inference process in term of input and output prediction
import numpy as np
import torch
import torch.nn.functional as F


class Inference:
    def __init__(self, model, input_prep):
        self.model = model
        self.input_prep = input_prep

    def infer(self):
        with torch.no_grad():
            # self.model.eval()
            logits = self.model(self.input_prep)
            probabilitas = F.sigmoid(logits)
            # ps = torch.exp(logits)
            conf, classes = torch.max(probabilitas, 1)
            print("done predicting")
            print("ps :", conf, "pred :", classes)
        return classes
