'''
Created on Jan 14, 2014

@author: Jose Borreguero
'''
import unittest
from dsfload import DsfLoaderMantidWorkspace2D

try:
  import mantid.simpleapi as mapi
except ImportError:
  print 'mantid library not found!'
  raise

class DsfLoadTest(unittest.TestCase):

  def test_DsfLoaderMantidWorkspace2D(self):
    ''' Load a Nexus file containing a workspace2D with data '''
    ws = mapi.LoadNexus(Filename='./data/exp100K.nxs') #workspace with 9 Q-values and 700-Evalues
    loader = DsfLoaderMantidWorkspace2D()
    intensities,errors = loader.Load(ws)
    nQ, nE = intensities.shape
    self.assertEqual(nQ, 9)
    self.assertEqual(nE, 700)
    self.assertEqual(intensities[4][321], 0.0302994) #just one simple example
    self.assertEqual(errors[4][321], 0.001094)

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(DsfLoadTest))
  return suite

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(suite())