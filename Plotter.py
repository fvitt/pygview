#! /usr/bin/env python

from Tkinter import *
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.colors import LogNorm

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

from MetaData import metadata
from ListBox import listbox

from DataSlice import dataslice
from LevelsSelector import levelsselector

class plotter(Tk):
    def __init__(self, parent, filepath, title='Map Plot'):
        Tk.__init__(self,None)
        self.filepath = filepath
        self.title(title)
        self.parent = parent
        self.initialize()
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def initialize(self):
        self.fig = plt.figure(figsize=(10,5),dpi=80)
        self.ax = self.fig.add_subplot(111)

        self.map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                           llcrnrlon=0,urcrnrlon=360,resolution='c',ax=self.ax )

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.metadata = metadata(self.filepath)

        self.varname = self.metadata.vars_list[0]

        varsbox = listbox(self, 'Variables', self.metadata.vars_list, self.var_selection, setfirst=True)
        varsbox.pack(side=LEFT)

        if hasattr(self.metadata,'levs'):
            self.levndx = len(self.metadata.levs_list)-1
            self.levsbox = listbox(self, 'Levels',    self.metadata.levs_list, self.lev_selection, setlast=True)
            self.levsbox.pack(side=LEFT)
        else:
            self.levndx = None

        #if (self.metadata.datetimes):
        if hasattr(self.metadata,'datetimes'):
            self.timndx = 0
            self.timestr = self.metadata.datetimes[0]
            timesbox = listbox(self, 'Dates/Times',    self.metadata.datetimes, self.time_selection, setfirst=True)
            timesbox.pack(side=LEFT)
        else:
            self.timndx = None
            self.timestr = ''

        f = Frame(self)

        self.levselect = levelsselector(f)
        self.levselect.pack(side=TOP, fill=BOTH, expand=1)

        b1 = Button(f, text="Set levels", command=self.setlevels)
        b1.pack(side=LEFT)

        b2 = Button(f, text="Clear levels",  command=self.clearlevels)
        b2.pack(side=LEFT)

        f.pack(side=LEFT)

        self.logscale = IntVar(master=self)
        self.cbut = Checkbutton(f, text="Log Scale", variable=self.logscale)
        self.cbut.pack(side=LEFT)
        self.logscale.trace_variable("w", self.log_scale_update)

        self.text = self.fig.suptitle('')

        # create a toplevel menus
        menubar = Menu(self)

        menubar.add_command(label="Quit!", command=self.quit)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="help", command=self.help)
        helpmenu.add_command(label="about", command=self.about)

        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.config(menu=menubar)

        self.levels=None

        self.ax.format_coord = self.format_coord

    def get_value(self, lon, lat ):

        lons = self.dslice.lon
        lats = self.dslice.lat
        d = self.dslice.data
        if len(d.shape) == 1 : # unstructured grid
            r = (lons-lon)**2 + (lats-lat)**2
            idx = r.argmin()
            return d[idx]
        else : # reg lat/lon grid
            lonidx = (np.abs(lons-lon)).argmin()
            latidx = (np.abs(lats-lat)).argmin()

    def format_coord(self, lon, lat):
        try:
            z = self.get_value(lon, lat)
            return 'val=%1.4e, lon=%1.2f, lat=%1.2f'%(z, lon, lat)
        except:
            return 'click a variable to plot'

    def setlevels(self):
        self.levels = self.levselect.get_levels(log_scale=self.logscale.get())
        self.draw_plot()

    def clearlevels(self):
        self.levselect.clear()
        self.levels=None
        self.draw_plot()

    def help(self):
        print "help!"

    def about(self):
        print "about... "

    def log_scale_update(self,*args):
        self.draw_plot()

    def update(self, lons, lats, z, title, canvas_title=None):

        # draw coastlines, country boundaries, fill continents.
        self.map.drawcoastlines(linewidth=0.75)

        # draw the edge of the map projection region (the projection limb)
        self.map.drawmapboundary(fill_color='lightgray')
        # draw lat/lon grid lines every 30 degrees.
        self.map.drawmeridians(np.arange(0,360,45),  labels=[False,False,False,True])
        self.map.drawparallels(np.arange(-90,90,30), labels=[True,False,False,False])

        latlon = False
        tri = False

        if len(z.shape) == 1 : # unstructured grid
            tri = True
            x = lons; y = lats
        else : # reg lat/lon grid
            latlon = True
            x, y = np.meshgrid(lons,lats)

        if self.logscale.get() :
            self.cs = self.map.contourf( x,y, z, norm=LogNorm(), levels=self.levels, latlon=latlon, tri=tri )
        else:
            self.cs = self.map.contourf( x,y, z, levels=self.levels, latlon=latlon, tri=tri )

        self.cb = self.map.colorbar(mappable=self.cs)
        self.ax.set_title(title)
        self.ax.text(-30.0, -115.0, self.filepath, fontsize=10 )

        maxval = str(np.amax(z))
        minval = str(np.amin(z))

        self.ax.text(-40.0, 110.0, 'min : '+minval, fontsize=12 )
        self.ax.text(-40.0, 100.0, 'max : '+maxval, fontsize=12 )

        if canvas_title :
            self.text.set_text(canvas_title)

        self.canvas.show()

    def clear(self):
        self.ax.clear()
        self.fig.delaxes(self.fig.axes[1])

    def dest(self):
        self.quit()
        #self.destroy()
        #sys.exit()
 
    def var_selection( self, event ):
        index = int(event.widget.curselection()[0])
        value = event.widget.get(index)
        self.varname = value
        self.draw_plot()

    def lev_selection( self, event ):
        if self.levsbox.enabled:
            index = int(event.widget.curselection()[0])
            value = event.widget.get(index)
            self.levndx = index
            self.draw_plot()

    def time_selection( self, event ):
        index = int(event.widget.curselection()[0])
        value = event.widget.get(index)
        self.timndx = index
        self.timestr = value
        self.draw_plot()

    def draw_plot( self ):

        try:
            self.clear()
        except:
            pass

        self.dslice = dslice = dataslice( self.filepath, self.varname, time_ndx=self.timndx, level_ndx=self.levndx )

        title = self.timestr

        if hasattr(self.metadata,'levs'):
            if dslice.levdep : 
                title += ' (' + "{:6.2f}".format( float(self.metadata.levs_list[self.levndx]) ) + ' mbar)'
                self.levsbox.enable()
            else :
                self.levsbox.disable()

        if hasattr(dslice,'units'):
            self.update( dslice.lon, dslice.lat, dslice.data, self.varname+' ('+dslice.units+')', canvas_title=title  )
        else:
            self.update( dslice.lon, dslice.lat, dslice.data, self.varname, canvas_title=title  )


if __name__ == '__main__':

    filepath = '../pygview_test_data/se_ne5np4_test.cam.h0.0000-01-01-00000.nc'

    plotter1 = plotter(None, filepath, title=filepath)
    plotter1.mainloop()

#    filepath = '/Users/fvitt/cam_output_data/fv_10x15_test.cam.h0.0000-01-01-00000.nc'
#    filepath = '/glade/scratch/fvitt/archive/sdchem_ne30_10pctovrwrt_01/atm/hist/sdchem_ne30_10pctovrwrt_01.cam.h2.2006-01-01-00000.nc'
#    plotter2 = plotter(None, filepath, title=filepath)
#    plotter2.mainloop()
