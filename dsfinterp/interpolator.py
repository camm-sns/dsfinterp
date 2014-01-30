'''
Created on Jan 6, 2014

@author: jbq
'''
import numpy
from logger import vlog, tr
import copy

class Interpolator(object):
  '''
  Evaluate the structure factor at a particular phase point for any
  value of the external parameters
  '''


  def __init__(self, fseries, signalseries, errorseries=None, running_regr_type = 'linear' ):
    '''
    Arguments:
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
    # Do running regression, and if neccessary estimate errors
    if running_regr_type == 'linear':
      from scipy.stats import linregress
      windowlength = 5 # important to be odd number
      if len( fseries ) < windowlength:
        vlog.error( 'series has to contain at least {0} members'.format( windowlength ) )
      else:
        # Lower boundary, the first three values
        x = fseries[ : windowlength ]
        y = signalseries[ : windowlength ]
        slope, intercept, r_value, p_value, std_err = linregress( x, y )
        linF = lambda xx: intercept + slope * xx
        self.fitted = [ linF(x[0]), linF(x[1]), linF(x[2]) ]
        residuals = numpy.square(numpy.vectorize(linF)(x) - y)
        residual = numpy.sqrt( numpy.mean(residuals)) #average residual
        self.errors = [ residual, residual, residual]
        # Continue until hitting the upper boundary
        index = 1 # lower bound of the regression window
        while ( index + windowlength <= len( fseries ) ):
          x = fseries[ index : index + windowlength ]
          y = signalseries[ index : index + windowlength ]
          slope, intercept, r_value, p_value, std_err = linregress( x, y )
          linF = lambda xx: intercept + slope * xx
          self.fitted.append(linF(x[2]))
          residuals = numpy.square(numpy.vectorize(linF)(x) - y)
          residual = numpy.sqrt( numpy.mean(residuals)) #average residual
          self.errors.append(residual)
          # Resolve the upper boundary
          if index + windowlength +1 == len( fseries ):
            self.fitted += [ linF(x[3]), linF(x[4]) ]
            self.errors += [ residual, residual ]
          index += 1
    elif running_regr_type == 'quadratic':
      from numpy import polyfit
      windowlength = 5 # important to be odd number
      if len( fseries ) < windowlength:
        vlog.error( 'series has to contain at least {0} members'.format( windowlength ) )
      else:
        # Lower boundary, the first three values
        x = fseries[ : windowlength ]
        y = signalseries[ : windowlength ]
        coeffs, residuals, rank, singular_values, rcond= polyfit(x,y,2, full=True) #second order polynomial
        quadF = lambda xx: coeffs[0]*xx*xx + coeffs[1]*xx + coeffs[2]
        self.fitted = [ quadF(x[0]), quadF(x[1]), quadF(x[2]) ]
        residual = numpy.sqrt(numpy.mean( residuals )) #average residual
        self.errors = [ residual, residual, residual]
        # Continue until hitting the upper boundary
        index = 1 # lower bound of the regression window
        while ( index + windowlength <= len( fseries ) ):
          x = fseries[ index : index + windowlength ]
          y = signalseries[ index : index + windowlength ]
          coeffs, residuals, rank, singular_values, rcond = polyfit(x,y,2, full=True) #second order polynomial
          quadF = lambda xx: coeffs[0]*xx*xx + coeffs[1]*xx + coeffs[2]
          self.fitted.append(quadF(x[2]))
          residuals = numpy.square(numpy.vectorize(quadF)(x) - y)
          residual = numpy.sqrt( numpy.mean(residuals)) #average residual
          self.errors.append(residual)
          # Resolve the upper boundary
          if index + windowlength +1 == len( fseries ):
            self.fitted += [ quadF(x[3]), quadF(x[4]) ]
            self.errors += [ residual, residual ]
          index += 1
    else:
      vlog.warning( 'Requested regression type not recogized' )

    if errorseries is not None:
      self.errors = errorseries
    # Interpolators for fitted and errors
    from scipy.interpolate import interp1d, UnivariateSpline
    x = numpy.array( fseries )
    y = numpy.array( self.fitted )
    e = numpy.array( self.errors )
    if e.any():
      min_nonzero_error = numpy.min(e[numpy.nonzero(e)]) # smallest non-zero error
      e = numpy.where(e >=min_nonzero_error, e, min_nonzero_error) # substitute zero errors with the smallest non-zero error
      w = 1.0 / e
      s = len( fseries ) 
    else: # in the improbable case of no errors, force the spline to pass through all points
      w = 1.0
      s = 0
    self.y = UnivariateSpline( x, y, w=w, s=s )
    self.e = interp1d(x, e, kind='linear')


  def __call__(self, fvalue):
    ''' Evalue the interpolators for the particular value of the external parameter '''
    if self.range[0] <= fvalue <= self.range[1]:
      return self.y(fvalue), float(self.e(fvalue))
    else:
      vlog.error( 'Value outside of interpolating bounds' )
      return ( float( 'inf' ), float( 'inf' ) )