'''
Created on Jan 16, 2014

@author: Jose Borreguero
'''
import unittest
import numpy

from interpolator import Interpolator

class TestInterpolator(unittest.TestCase):

  def ServeInput(self):
    ''' Helper method to serve data for the test cases '''
    size = 100
    function = numpy.sin(2*numpy.pi*numpy.arange(size)*0.01)
    noise = 0.2*numpy.random.rand(size)
    signalseries = function + noise
    errorseries = 0.2*numpy.random.rand(size)
    fseries = 1.0*numpy.arange(size)
    return signalseries, errorseries, fseries

  def test___init__(self):
    signalseries, errorseries, fseries = self.ServeInput()
    interpolator = Interpolator(signalseries, errorseries, fseries)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(TestInterpolator))
  return suite

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(suite())