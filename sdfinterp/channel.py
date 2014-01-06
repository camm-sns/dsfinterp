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

  def __init__( self, phasepoint ):
    '''
    Attributes:
      p: the domain of the dynamical channel, the (Q,E) pair
      signalseries: the values that the structure factor for this channel
        takes for the different values of the external parameter
      interpolator: evaluates the structure factor for this channel and estimation of error for a particular value of the external parameter 
    '''
    self.p = phasepoint
    self.signalseries = None
    self.interpolator = None

  def SetSignalSeries(self, signalseries):
    self.signalseries = signalseries

  def InitializeInterpolator(self, fseries, running_interp_type = 'linear'):
    ''' Initialize the interpolator for this channel
    
    Arguments:
      fseries: list of external parameter values
      running_interpolation: the type of the local, running interpolation

    Returns:
      None if error found
      interpolator attribute if success
    '''
    # Handle errors first
    if not self.signalseries:
      vlog.error("Signal series not set!")
      return None
    if len( fseries ) != len( self.signalseries ):
      vlog.error("signal and external parameter series have different lenght!")
      return None

    self.interpolator = Interpolator( fseries, self.signalseries, errorseries=None, running_interp_type = running_interp_type)
    return self.interpolator

  def __call__(self, fvalue ):
    ''' Evaluates the interpolator for the fvalue mimicking a function call'''
    return self.interpolator( fvalue )