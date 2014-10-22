#! /usr/bin/env python

import netCDF4 as nc
from datetime import datetime

class metadata:
    def __init__(self, filepath):

        f = nc.Dataset(filepath, 'r', format='NETCDF4')

        dims = f.dimensions
        vars = f.variables

        self.vars_list = []

        for v in vars.keys():
            if vars[v].dimensions.__contains__('lev') or \
               vars[v].dimensions.__contains__('lon') or \
               vars[v].dimensions.__contains__('lat') or \
               vars[v].dimensions.__contains__('ncol') :
                self.vars_list.append(v)

        self.vars_list.sort()

        if vars.has_key('lat'):
            self.lats = vars['lat']
            self.lats_list = []
            for l in self.lats:
                self.lats_list.append(str(l))
        if vars.has_key('lon'):
            self.lons = vars['lon']
            self.lons_list = []
            for l in self.lons:
                self.lons_list.append(str(l))

        if dims.has_key('lat'):
            self.nlats = dims['lat']
        if dims.has_key('lon'):
            self.nlons = dims['lon']
        if dims.has_key('ncol'):
            self.ncols = dims['ncol']

        if dims.has_key('lev'):
            self.nlevs = dims['lev']
            self.levs = vars['lev']
            self.levs_list = []
            for l in self.levs:
                self.levs_list.append(str(l))

        if dims.has_key('time'):

            self.datetimes = []

            dates = vars['date']
            datesec = vars['datesec']

            self.ntimes = dates.size

            for t in range(0,self.ntimes):
                year = int( dates[t]/10000 )
                month = int( (dates[t]-year*10000)/100 )
                day = dates[t]-year*10000-month*100

                hr = int(datesec[t]/3600)
                min = int( (datesec[t] - hr*3600)/60 )
                sec = int(datesec[t] - hr*3600 - min*60)

                date = datetime(2000,month,day,hr,min,sec )

                
                datestr = str(year) + date.strftime(' %b %d %H:%M:%S')

                self.datetimes.append( datestr )

def test():

    mdata = metadata('../pygview_test_data/se_ne5np4_test.cam.h0.0000-01-01-00000.nc')

    print 'levs : ',mdata.levs_list

    print 'datetimes: ',mdata.datetimes
    print 'variables: ',mdata.vars_list

    if hasattr(mdata,'nlats') : print ' nlats : ', mdata.nlats
    if hasattr(mdata,'nlons') : print ' nlons : ', mdata.nlons
    if hasattr(mdata,'ncols') : print ' ncols : ', mdata.ncols
    if hasattr(mdata,'nlevs') : print ' nlevs : ', mdata.nlevs
    if hasattr(mdata,'ntimes'): print ' ntimes: ', mdata.ntimes

if __name__ == '__main__':
    test()
