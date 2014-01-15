'''
Created on Jan 7, 2014

@author: jbq
'''

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

  def Load(self, container ):
    ''' Load intensities and errors from an object or reference
    '''
    from dsfload import DsfLoaderFactory
    loader_factory = DsfLoaderFactory()
    for datatype in loader_factory.datatypes:
      try:
        loader = loader_factory.Instantiate(datatype)
        self.intensities, self.errors = loader.Load(container)
        return self.intensities
      except:
        pass
    return None
