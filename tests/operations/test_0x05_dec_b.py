from hypothesis import given
from hypothesis.strategies import integers
from src.cpu import CPU

from src.operations import dec_b
import unittest

class DEC_B_Test(unittest.TestCase):
    @given(
        integers(min_value=0x00, max_value=0xff)
    )
    def test_inc_b(self, b):

        cpu = CPU([])
        cpu.B = b
        
        cycles = dec_b(cpu)

        self.assertEqual(cycles, 4)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, int(b - 1 == 0))
        self.assertEqual(cpu.F_N, 1)
        self.assertEqual(cpu.F_H, int((b & 0x0f) - 1 > 0xff))
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, b-1 & 0xff)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, ((b-1 & 0xff) << 8) | cpu.C)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])        