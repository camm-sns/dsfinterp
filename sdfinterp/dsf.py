'''
Created on Jan 7, 2014

@author: jbq
'''
from logger import vlog

class Dsf(object):
  '''
  This class implements a dynamic structure factor
  '''


  def __init__(self):
    '''
    fvalue: value of the external parameter
    intensities: actual values of the structure factor
    errors: associated errors of the intensities. Mostly for experimentally-derived data
    shape: shape of the intensities array
    '''
    self.fvalue = None
    self.intensities = None
    self.errors = None

  def Shape(self):
    return self.intensities.shape
  shape = property( fget = Shape )

  def ExtractIntensity(self, index ):
    return self.intensities.ravel()[ index ]

  def ExtractError(self, index ):
    if self.errors:
      return self.errors.ravel()[ index ]
    else:
      return None