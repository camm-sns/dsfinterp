'''
Created on Jan 6, 2014

@author: jbq
'''

class Channel(object):
  '''
  A dynamical channel defined by momentum transfer Q and energy E
  '''

  def __init__(self, phasepoint):
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

  #def InitializeInterpolator(self, fseries):
    ''' Initialize the interpolator for this channel
    '''
  #  if len(fseries) != len(self.signalseries):
      