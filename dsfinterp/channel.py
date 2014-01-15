'''
Created on Jan 6, 2014

@author: jbq
'''

from logger import vlog
from interpolator import Interpolator
class Channel( object ):
  '''
  A dynamical channel defined by momentum transfer Q and energy E
  '''

  def __init__( self ):
    '''
    Attributes:
      signalseries: the values that the structure factor for this channel
        takes for the different values of the external parameter
      errorseries: associated errors for the signalseries. Mostly applicable
        to experimental signalseries
      interpolator: evaluates the structure factor for this channel and estimation
        of error for a particular value of the external parameter 
    '''
    self.signalseries = None
    self.erorrseries = None
    self.interpolator = None

  def SetSignalSeries(self, signalseries):
    ''' Initialize the signalseries '''
    self.signalseries = signalseries

  def SetErrorSeries(self, errorseries):
    ''' Initialize the errorseries '''
    self.errorseries = errorseries

  def InitializeInterpolator(self, fseries, running_regr_type = 'linear'):
    ''' Initialize the interpolator for this channel
    
    Arguments:
      fseries: list of external parameter values
      running_regr_type: the type of the local, running regression

    Returns:
      None if error found
      interpolator attribute if success
    '''
    # Handle errors first
    if not self.signalseries:
      vlog.error( 'Signal series not set!' )
      return None
    if len( fseries ) != len( self.signalseries ):
      vlog.error( 'signal and external parameter series have different lenght!' )
      return None

    self.interpolator = Interpolator( fseries, self.signalseries, errorseries = self.erorrseries, running_regr_type = running_regr_type)
    return self.interpolator


  def __call__(self, fvalue ):
    ''' Evaluates the interpolator for the fvalue mimicking a function call'''
    return self.interpolator( fvalue )