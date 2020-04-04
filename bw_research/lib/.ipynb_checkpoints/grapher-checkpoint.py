import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Grapher:
    def __init__(self, figsize=(20,25), fontsize=26):
        self.font = fontsize
        self.figsize = figsize
    
    def graph(self, obj, title='Title', combine=False):
        obj_class = str(obj.__class__.__name__)
        fig, axs = None, None
        
        # List can be a list of holder objects
        if obj_class == 'list':
            self.graphList(obj, combine, title)
        
        elif obj_class == 'DataHolder':
            fig, axs = plt.subplots(1, figsize=self.figsize)
            fig.suptitle(title, fontsize=self.font)
            self.graphHolder(obj, axs)
        
        else:
            print('Input was not a list or holder')
            return
    
    def graphList(self, l, combine, title):
        size = len(l)
        if combine:
            fig, axs = plt.subplots(1, figsize=self.figsize)
        else:
            fig, axs = plt.subplots(size, figsize=self.figsize)
        fig.suptitle(title, fontsize=self.font)
        
        i = 0
        while(i < size):
            if not combine:
                self.graphHolder(l[i], axs[i])
            else:
                self.graphHolder(l[i], axs)
            i += 1
    
    def graphHolder(self, holder, axs):
        (rates, res) = holder.getResults()
        rates = np.array([r/60 for r in rates])
        means = np.array([r[0] for r in res])
        stds = np.array([r[1] for r in res])
        
        #axs.plot(rates, means)
        axs.errorbar(rates, means, yerr=stds, capsize=4, fmt='-o')
        axs.fill_between(rates, means-stds, means+stds, alpha=0.2)