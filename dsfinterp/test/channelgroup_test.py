'''
Created on Jan 17, 2014

@author: Jose Borreguero
'''
import unittest
import numpy

from logger import tr
from channelgroup import ChannelGroup
from dsfgroup_test import LoadDsfGroup

class TestChannelGroup(unittest.TestCase):
  
  def test_InitFromDsfGroup(self):
    dsfgroup, fseries = LoadDsfGroup()
    channelgroup = ChannelGroup()
    channelgroup.InitFromDsfGroup(dsfgroup)

    channel_index = 700*4+321 # select one channel
    channel = channelgroup[channel_index]

    series = channel.signalseries
    self.assertAlmostEqual(series[0], 0.0302994, places=6)
    self.assertAlmostEqual(series[-1], 0.0289113, places=6)

    series = channel.errorseries
    self.assertAlmostEqual(series[0], 0.001094, places=6)
    self.assertAlmostEqual(series[-1], 0.00107701, places=6)


def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(loader.loadTestsFromTestCase(TestChannelGroup))
  return suite

if __name__ == "__main__":
  unittest.TextTestRunner(verbosity=2).run(suite())