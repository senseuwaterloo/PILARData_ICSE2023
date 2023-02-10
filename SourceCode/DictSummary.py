import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import gaussian_kde

def DictEvaluate(objectdict):
    valuedict = dict()
    for v in objectdict.values():
        if v in valuedict:
            valuedict[v] = valuedict[v] + 1
        else:
            valuedict[v] = 1
    values = []
    for v in valuedict.keys():
        values.append(v)
    values.sort()
    appearence = []
    for v in values:
        appearence.append(valuedict[v])
    print(values)
    print(appearence)

def DictPrint(objectdict):
    values = []
    for v in objectdict.keys():
        values.append(v)
    values.sort()
    appearence = []
    entropy = []
    for v in values:
        appearence.append(objectdict[v])
        entropy.append(float(v))

    print(entropy)
    print(appearence)

def DictDensity(objectdict, file):
    output = open(file, 'w')
    values = []
    for v in objectdict.values():
        output.write(str(v))
        output.write(',')