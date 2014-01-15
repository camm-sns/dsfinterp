'''
Created on Jan 14, 2014

@author: jbq
'''
import unittest

try:
  import mantid
except ImportError:
  print 'mantid library not found!'
  raise

class DsfLoadTest(unittest.TestCase):

  def testDsfLoaderMantidWorkspace2D(self):
    from dsfload import DsfLoaderMantidWorkspace2D
    ws = mantid.LoadNexus('data/exp100K.nxs') #workspace with 9 Q-values and 700-Evalues
    loader = DsfLoaderMantidWorkspace2D()
    intensities,errors = loader.Load(ws)
    nQ, nE = intensities.shape
    self.assertEqual(nQ, 9)
    self.assertEqual(nE, 700)
    self.assertEqual(intensities[4][321],0.0302994) #just one simple example

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()