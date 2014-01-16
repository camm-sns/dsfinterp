'''
Created on Jan 6, 2014

@author: jbq
'''
import numpy
from logger import vlog

class Interpolator(object):
  '''
  Evaluate the structure factor at a particular phase point for any
  value of the external parameters
  '''


  def __init__(self, fseries, signalseries, errorseries=None, running_regr_type = 'linear' ):
    '''
    Arguments:
      fseries: list of values for the external parameter
      signalseries: values of the structure factor as a function of the external parameter
      [errorseries]: associated errors of the structure factor
      [running_regr_type]: method for the local, runnig regression
    
    Attributes:
      range: minimum and maximum of the fseries
      fitted: values of the structure factor at the external parameter values after the running regression
      errors: errorseries or estimated errors at the external parameter values from the running regression
      y: interpolator object for the struc ture factor (cubic spline)
      e: interpolator object for the error (linear)
      running_regr_type: type of running regression
    '''
    # Deal with possible errors
    if len( fseries ) != len( signalseries ):
      vlog.error( 'signal and external parameter series have different lenght!' )

    self.running_regr_type = running_regr_type
    self.range = ( fseries[ 0 ], fseries[ -1 ] )
    # Do running regression and estimate errors
    if running_regr_type == 'linear':
      from scipy.stats import linregress
      windowlength = 5 # important to be odd number
      if len( fseries ) < windowlength:
        vlog.error( 'series has to contain at least {0} members'.format( windowlength ) )
      else:
        # Lower boundary, the first three values
        x = fseries[ : windowlength ]
        y = self.signalseries[ : windowlength ]
        slope, intercept, r_value, p_value, std_err = linregress( x, y )
        linF = lambda xx: intercept + slope * xx
        self.fitted = [ linF( x[0] ), linF( x[1] ), linF( x[2] ) ]
        self.errors = [ std_err, std_err, std_err ]
        # Continue until hitting the upper boundary
        index = 1 # lower bound of the regression window
        while ( index + windowlength < len( fseries ) ):
          x = fseries[ index : index + windowlength ]
          x = self.signalseries[ index : index + windowlength ]
          slope, intercept, r_value, p_value, std_err = linregress( x, y )
          linF = lambda xx: intercept + slope * xx
          self.fitted.append( linF( x[2] ))
          self.errors.append( std_err )
          # Resolve the upper boundary
          if index + windowlength +1 == len( fseries ):
            self.fitted += [ linF( x[3] ), linF( x[4] ) ]
            self.errors += [ std_err, std_err ]
    else:
      vlog.warning( 'Only the running linear regression has been implemented to date' )

    if errorseries:
      self.errors = errorseries

    # Interpolators for fitted and errors
    from scipy.interpolate import interp1d, UnivariateSpline
    x = numpy.array( self.fvalues )
    y = numpy.array( self.fitted )
    e = numpy.array( self.errors )
    w = 1.0 / e
    self.y = UnivariateSpline( x, y, w=w, s=len( fseries ) )
    self.e = interp1d(x, e, kind='linear')


  def __call__(self, fvalue):
    ''' Evalue the interpolators for the particular value of the external parameter '''
    if self.range[0] <= fvalue <= self.range[1]:
      x = numpy.array( [fvalue,] )
      return self.y(x)[0], self.e(x)[0]
    else:
      vlog.error( 'Value outside of interpolating bounds' )
      return ( float( 'inf' ), float( 'inf' ) )