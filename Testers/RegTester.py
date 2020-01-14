import torch.nn as nn
import Dataloaders
from torch.optim.optimizer import Optimizer
from utils import progress_bar
import torch
import os
import json
from .BaseTester import BaseTester 
from Attacker import Attacker


#with open('config.json') as config_file: # Reading the Config File 
#    config = json.load(config_file)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class RegTester(BaseTester):
    def __init__(self, model, testdataloader, optimizer, criterion, classes, n_epoch, testbatchsize, expid, checkepoch, pres, stepsize, k, atmeth, c_1, c_2, eps, dataname, nstep, **kwargs):
        super().__init__(self, model, testdataloader, optimizer, criterion, classes, n_epoch, testbatchsize, expid, checkepoch, pres, stepsize, k, atmeth, c_1, c_2, eps, dataname, nstep, **kwargs)
        self.pert = []
        self.best_acc = 0
        self.startepoch = 0
        self.attacker = Attacker(self.eps, self.model, self.stepsize, self.optimizer, self.criterion, self.c_1, self.c_2, self.nstep, self.dataname)
    def test_minibatch(self, batch_idx):
        (I, _), targets = self.testdataloader[batch_idx]
        I, targets = I.to(device), targets.to(device)
        targets = targets.long()

        if self.atmeth == "PGD":
            I , self.pert = attacker.PGDattack(I.cpu().numpy(),targets.cpu(),self.optimizer)
            I = torch.from_numpy(I)
            I = I.to(device)
    
        if self.atmeth == "FGSM":
            I = attacker.FGSMattack(I.cpu().numpy(),targets.cpu(),self.optimizer)
            I = torch.from_numpy(I)
            I = I.to(device)

        self.optimizer.zero_grad()
        outputs = self.model(I)
        loss = self.criterion(outputs, targets)
        _,predicted = outputs.max(1)
        return loss.item(), predicted.eq(targets).sum().item(), targets.size(0)

