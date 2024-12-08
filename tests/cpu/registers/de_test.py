from hypothesis import given
from hypothesis.strategies import integers

from src.cpu import CPU

import unittest

class DE_Test(unittest.TestCase):
    @given(integers(min_value=256, max_value=65535))
    def test_setter(self, de):
        cpu = CPU()

        cpu.DE = de
        
        self.assertEqual(cpu.DE, de)
        self.assertEqual(cpu.D, ((255 << 8) & de) >> 8)
        self.assertEqual(cpu.E, 255 & de)
        
        
        
    @given(integers(min_value=0, max_value=255), integers(min_value=0, max_value=255))
    def test_getter(self, d, e):
        cpu = CPU()
        
        cpu.D = d
        cpu.E = e
        
        self.assertEqual(cpu.DE, (d << 8) | e)
        self.assertEqual(cpu.D, d)        
        self.assertEqual(cpu.E, e)        
        