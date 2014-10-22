#! /usr/bin/env python

from Tkinter import *

class listbox(LabelFrame):

    def __init__(self,parent,title,items_list,bind_function, setfirst=False, setlast=False):

        LabelFrame.__init__(self,parent, text=title, padx=5, pady=5)
        self.parent = parent
        self.title = title
        self.items_list = items_list
        self.bind_function = bind_function
        self.initialize(setfirst, setlast)

    def initialize(self, setfirst, setlast):

        s = Scrollbar(self, orient=VERTICAL)
        self.lb = Listbox(self, yscrollcommand=s.set,height=8, width=20, exportselection=0)
        s.config(command=self.lb.yview)
        s.pack(side=RIGHT, fill=Y)
        for i in self.items_list:
            self.lb.insert(END,i)
        self.lb.pack(side=LEFT, fill=BOTH, expand=1)

        last=len(self.items_list)-1

        if setfirst :
            self.lb.selection_set( first=0 )
            self.lb.activate( 0 )
            self.lb.see(0)

        if setlast :
            self.lb.selection_set( first=last )
            self.lb.activate( last )
            self.lb.see(last)

        self.lb.bind('<<ListboxSelect>>', self.bind_function )

        self.enabled = True

    def disable(self):
        self.lb.configure(state=DISABLED)
        self.enabled = False

    def enable(self):
        self.lb.configure(state=NORMAL)
        self.enabled = True

#    def disable(self):
#        help(lb)
#        lb.configure(state=DISABLED)

def color_bind_function(e):
    try:
        index = int(e.widget.curselection()[0])
        value = e.widget.get(index)
        print 'You selected color %d: "%s"' % (index, value)
    except:
        pass

def number_bind_function(e):
    index = int(e.widget.curselection()[0])
    value = e.widget.get(index)
    print 'You selected number %d: "%s"' % (index, value)

def test():
    
    print 'Begin TEST'

    win = Tk()
    win.title("TEST List Boxes")

    colors = listbox(win,'Colors',['red','orange','yellow','green','blue','purple'], color_bind_function)
    colors.pack(side=LEFT)
    colors.disable()

    numbers =  listbox(win,'Numbers',['zero','one','two','three','four','five','six'], number_bind_function)
    numbers.pack(side=LEFT)
    numbers.disable()
    numbers.enable()

    win.mainloop()

    print 'END TEST'

if __name__ == '__main__':
    test()
