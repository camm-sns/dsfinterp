'''
Created on Jan 7, 2014

@author: jbq
'''

import numpy
from channel import Channel

class ChannelGroup(object):
  '''
  This class implements a group of channels
  representing a group of dynamic structure factors
  '''

  def __init__(self):
    '''
    Attributes:
      fseries: list of external parameter values
      channels: series of channels, one for each point of the dynamical domain.
    '''
    self.fseries = None
    self.channels = None
    self.shape = None

  def Nchannels(self):
    if self.shape is None:
      return 0
    return numpy.prod(self.shape)
  nchannels = property( fget = Nchannels )

  def InitFromDsfGroup(self, dsfg ):
    ''' Load a group of dynamic structure factors into a channel group '''
    self.fseries = dsfg.fseries
    self.shape = dsfg.shape
    # Instantiate the channels
    grid = numpy.empty( self.nchannels, dtype = object )
    vChannel = numpy.vectorize(Channel)
    self.channels[:,:] = vChannel( grid )
    # fill the channels.
    for i in range( self.nchannels ):
      self.channels[i].SetSignalSeries( dsfg.ExtractSignalSeries(i) )
      self.channels[i].SetErrorSeriess( dsfg.ExtractErrorSeries(i) )

  def InitializeInterpolator(self, running_regr_type = 'linear'):
    ''' Create the spline interpolator for each channel '''
    def initInterp(channel):
      channel.InitializeInterpolator( self.fseries, running_regr_type = running_regr_type)
      return channel
    vinitInterp = numpy.vectorize( initInterp ) # faster than the classic "for" loop
    self.channels[:,:] = vinitInterp( self.channels )