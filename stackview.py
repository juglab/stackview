import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('qt5agg') # only good backend available!
from matplotlib import text
import sys

class Stack(object):
    """
    Quick and dirty viewer for ndarrays with ndim>2.
    Hold down the number of the dimension you want to cycle, eg '1', '2', ...
    Move forwards/backwards with k/j
    'F' = Faster
    'S' = Slower
    'A' = toggle auto contrast
    """
    def press(self, event):
        sys.stdout.flush()
        if event.key == 'i': # Up
            dimlen = self.stack.shape[self.zdim]
            pt = self.idx[self.zdim]
            if dimlen > 10:
                pt += 1*self.mul
            else:
                pt += 1
            pt %= dimlen
            self.idx[self.zdim] = pt
            print('\r Slice: '+str(self.idx)+' '*5, end="")
        elif event.key == 'j': # Down
            dimlen = self.stack.shape[self.zdim]
            pt = self.idx[self.zdim]
            if dimlen > 10:
                pt -= 1*self.mul
            else:
                pt -= 1
            pt %= dimlen
            self.idx[self.zdim] = pt
            print('\r Slice: '+str(self.idx)+' '*5, end="")
        elif event.key in {'1', '2', '3'}:
            self.zdim = int(event.key)-1
            print('\r'+'idx:', self.idx, 'zdim:', self.zdim, 'mul:', self.mul, 'autocolor:', self.autocolor, end="")
        elif event.key == 'F': # Faster
            self.mul += 1
        elif event.key == 'S': # Slower
            self.mul -= 1
        elif event.key == 'A':
            self.autocolor = not self.autocolor
        elif event.key == 'V':
            assert False
        elif event.key == 'R':
            # cyclic permutation of last three (non-color) dimensions
            p = np.arange(self.stack.ndim)
            if self.stack.shape[-1]==3:
                temp = p[-4]
                p[-4] = p[-3]
                p[-3] = p[-2]
                p[-2] = temp
            else:
                temp = p[-3]
                p[-3] = p[-2]
                p[-2] = p[-1]
                p[-1] = temp
            self.stack = self.stack.transpose(p)
            if self.idx[self.zdim] >= self.stack.shape[0]:
            	self.idx[self.zdim] = 0
            	print('\r Slice: '+str(self.idx)+' '*5, end="")

        # elif event.key == 'W':
        #     self.w = int(input('gimme a w: '))
        
        if self.autocolor:
            img = self.stack[tuple(self.idx)]
            mn, mx = img.min(), img.max()
            self.fig.gca().images[0].set_clim(mn, mx)
            # print(mn, mx)

        # print('idx:', self.idx, 'zdim:', self.zdim, 'mul:', self.mul, 'autocolor:', self.autocolor)
        
        if self.w > 0:
            zpos = self.idx[1]
            # a = max(zpos-self.w, 0)
            b = min(zpos+self.w, self.stack.shape[1])
            ss = list(self.idx)
            ss[1] = slice(zpos, b)
            data = self.stack[tuple(ss)]
            if decay:
                decay = np.exp(-np.arange(data.shape[0])/2).reshape((-1,1,1))
                data = (data*decay).mean(0)
        else:
            ss = tuple(self.idx)
            data = self.stack[ss]
        
        self.fig.gca().images[0].set_data(data)
        self.fig.canvas.draw()

    def __init__(self, stack, customclick=None, colorchan=False, w=0, decay=False, norm=True):
        if type(stack)==list:
            stack = np.stack(stack).astype(np.float)
            print(stack.dtype)
        self.zdim = 0
        # TODO: this will give a bug when we have 3channel color imgs.
            
        if colorchan:
            if stack.shape[-1]==2:
                stack = np.stack([stack[...,0], 0.5*stack[...,1], 0.5*stack[...,1]], axis=-1)
            self.idx = np.array([0]*(stack.ndim-3))
            self.ndim = stack.ndim-3
        else:
            self.idx = np.array([0]*(stack.ndim-2))
            self.ndim = stack.ndim-2
        self.stack = stack
        # self.overlay = np.zeros(stack.shape[-3:] + (4,), dtype='float')
        # self.overlay[:100, :50] = 4
        # self.overlay[100:, :50] = 1

        fig = plt.figure()
        fig.gca().imshow(stack[tuple(self.idx)], interpolation='nearest')
        print('\r Slice: '+str(self.idx)+' '*5, end="")
        fig.gca().set_aspect('equal', 'datalim')
        fig.gca().set_position([0, 0, 1, 1])
        
        fig.canvas.mpl_connect('key_press_event', self.press)
        remove_keymap_conflicts({'k'})
        # fig.gca().imshow(self.overlay[self.idx[-1]])

        print(fig, self.idx)
        self.fig = fig
        self.mul = 1
        self.autocolor = True
        self.w = w
        self.img = self.fig.axes[0].images[0]

def remove_keymap_conflicts(new_keys_set):
    """
    from https://www.datacamp.com/community/tutorials/matplotlib-3d-volumetric-data
    """
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)
