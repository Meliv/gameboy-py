from hypothesis import given
from hypothesis.strategies import integers

from src.cpu import CPU
import unittest

class BC_Test(unittest.TestCase):
    @given(integers(min_value=256, max_value=65535))
    def test_setter(self, bc):
        cpu = CPU()

        cpu.BC = bc
        
        self.assertEqual(cpu.BC, bc)
        self.assertEqual(cpu.B, ((255 << 8) & bc) >> 8)
        self.assertEqual(cpu.C, 255 & bc)
        
        
        
    @given(integers(min_value=0, max_value=255), integers(min_value=0, max_value=255))
    def test_getter(self, b, c):
        cpu = CPU()
        
        cpu.B = b
        cpu.C = c
        
        self.assertEqual(cpu.BC, (b << 8) | c)
        self.assertEqual(cpu.B, b)        
        self.assertEqual(cpu.C, c)        
        