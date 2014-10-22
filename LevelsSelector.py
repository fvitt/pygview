#! /usr/bin/env python

from Tkinter import *
import numpy as np

class levelsselector(Frame):

   def __init__(self,parent):
      Frame.__init__(self,parent)
      self.parent = parent

      self.initialize()


   def initialize(self):

      self.levslab = Label(self, text="Levels: ")
      self.levslab.grid(row=0, sticky=E)

      self.minlab = Label(self, text="Min level: ")
      self.minlab.grid(row=1, sticky=E)

      self.maxlab = Label(self, text="Max level: ")
      self.maxlab.grid(row=2, sticky=E)

      self.nlvlab = Label(self, text="Num edges: ")
      self.nlvlab.grid(row=3, sticky=E)


      self.levse = Entry(self)
      self.levse.grid(row=0, column=1)

      self.mine = Entry(self)
      self.mine.grid(row=1, column=1)

      self.maxe = Entry(self)
      self.maxe.grid(row=2, column=1)

      self.nlvse = Entry(self)
      self.nlvse.grid(row=3, column=1)

   def clear(self):
      self.levse.delete(0,END)
      self.mine.delete(0,END)
      self.maxe.delete(0,END)
      self.nlvse.delete(0,END)

   def get_levels(self,log_scale):

      levels = None
      try:
         ulevs = self.levse.get().split()
         if len(ulevs) > 1 :
            levels = []
            for l in ulevs:
               levels.append( float(l) )
         else:

            maxval = float(self.maxe.get())
            minval = float(self.mine.get())

            nlevs = int(self.nlvse.get())

            if log_scale :

               maxval = np.ceil( np.log10(maxval))
               minval = np.floor(np.log10(minval))
               levels = np.logspace(minval,maxval,nlevs)
            else:
               dx = (maxval-minval)/(nlevs-1)
               levels = np.arange(minval,maxval+dx,dx)
      except:
         levels = None

      return levels

if __name__ == '__main__':

   root = Tk()
   levs = levelsselector(root)
   levs.pack()

   def get_button():
      print 'button pushed'
      newlevs = levs.get_levels(log_scale=False)
      print 'New levels : ',newlevs

      newlevs = levs.get_levels(log_scale=True)
      print 'New levels : ',newlevs

   def clear_button():
      levs.clear()

   button = Button(root, text="Get New Levels", command=get_button)
   button.pack(side=LEFT)

   button = Button(root, text="Clear Levels", command=clear_button)
   button.pack(side=LEFT)

   root.title('Levels Selector Test')

   root.mainloop()

