from hypothesis import given
from hypothesis.strategies import booleans

from processor.cpu import CPU

import unittest

class Register_F_Z_Test(unittest.TestCase):
    @given(booleans(), booleans(), booleans(), booleans())
    def test_register_F_Z(self, z, n, h, c):
        cpu = CPU(memory=[])
        
        cpu.F_Z = int(z)
        cpu.F_N = int(n)
        cpu.F_H = int(h)
        cpu.F_C = int(c)

        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, int(z))
        self.assertEqual(cpu.F_N, int(n))
        self.assertEqual(cpu.F_H, int(h))
        self.assertEqual(cpu.F_C, int(c))
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 0)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])