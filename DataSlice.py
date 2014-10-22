#! /usr/bin/env python

import netCDF4 as nc
import mpl_toolkits.basemap as bm
import numpy

class dataslice():

    def __init__( self, filename, varname, time_ndx=0, level_ndx=0 ):

        fh = nc.Dataset(filename, 'r', format='NETCDF4')

        dims = fh.dimensions

        if dims.has_key('time') :

            self.units = fh.variables[varname].units
            
            if dims.has_key('ncol') :

                if fh.variables[varname].ndim == 3 :
                    self.data = numpy.ravel(fh.variables[varname][time_ndx,level_ndx,:])
                    self.levdep = True
                else:
                    self.data = numpy.ravel(fh.variables[varname][time_ndx,:])
                    self.levdep = False

                self.lon = numpy.ravel(fh.variables["lon"][:])
                self.lat = numpy.ravel(fh.variables["lat"][:])
                self.structured = False

            if dims.has_key('lon') and dims.has_key('lat') :

                if fh.variables[varname].ndim == 4 :
                    self.data = fh.variables[varname][time_ndx,level_ndx,:,:]
                    self.levdep = True
                else:
                    self.data = fh.variables[varname][time_ndx,:,:]
                    self.levdep = False

                self.lon = fh.variables["lon"][:]
                self.lat = fh.variables["lat"][:]
                self.structured = True

                # Add longitude cyclic point
                self.data,self.lon = bm.addcyclic(self.data,self.lon)

        else :

            if dims.has_key('ncol') :
                if fh.variables[varname].ndim == 2 :
                    self.data = numpy.ravel(fh.variables[varname][level_ndx,:])
                    self.levdep = True
                else:
                    self.data = numpy.ravel(fh.variables[varname][:])
                    self.levdep = False

                self.lon = numpy.ravel(fh.variables["lon"][:])
                self.lat = numpy.ravel(fh.variables["lat"][:])
                self.structured = False

            if dims.has_key('lon') and dims.has_key('lat') :
                if fh.variables[varname].rank == 3 :
                    self.data = fh.variables[varname][level_ndx,:,:]
                    self.levdep = True
                else:
                    self.data = fh.variables[varname][:,:]
                    self.levdep = False

                self.lon = fh.variables["lon"][:]
                self.lat = fh.variables["lat"][:]
                self.structured = True

                # Add longitude cyclic point
                self.data,self.lon = bm.addcyclic(self.data,self.lon)

        fh.close

def test():

    filepath = '../pygview_test_data/se_ne5np4_test.cam.h0.0000-01-01-00000.nc'

    dslice = dataslice( filepath, 'T', time_ndx=0, level_ndx=8 )

    print '         filepath : '+filepath
    print 'dslice.data.shape : ',dslice.data.shape
    print 'dslice.structured : ',dslice.structured
    print '     dslice.units : ',dslice.units
    print '  dslice.lon.size : ',dslice.lon.size
    print '  dslice.lat.size : ',dslice.lat.size
    print '  dslice.lon : ',dslice.lon
    print '  dslice.lat : ',dslice.lat

    print '     dslice.lon.min, dslice.lon.max   : ',dslice.lon.min(), dslice.lon.max()

    print '     dslice.lon.min, dslice.lon.max   : ',numpy.amin(dslice.lon), numpy.amax(dslice.lon)
    print '     dslice.lat.min, dslice.lat.max   : ',numpy.amin(dslice.lat), numpy.amax(dslice.lat)
    print '     dslice.data.min,dslice.data.max  : ',numpy.amin(dslice.data), numpy.amax(dslice.data)

    filepath = '../pygview_test_data/fv_10x15_test.cam.h0.0000-01-01-00000.nc'

    dslice = dataslice( filepath, 'V', time_ndx=0, level_ndx=18 )
    
    print '         filepath : '+filepath
    print 'dslice.data.shape : ',dslice.data.shape
    print 'dslice.structured : ',dslice.structured
    print '     dslice.units : ',dslice.units
    print '     dslice.lon   : ',dslice.lon
    print '     dslice.lat   : ',dslice.lat
    print '     dslice.data  : ',dslice.data.min(),dslice.data.max()

if __name__ == '__main__':
    test()
