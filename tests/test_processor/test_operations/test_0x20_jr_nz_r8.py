from hypothesis import given
from hypothesis.strategies import integers

from processor.cpu import CPU
from processor.operations import jr_nz_r8

import unittest

class JR_NZ_R8_Test(unittest.TestCase):
    def test_jr_nz_r8_Z(self):

        cpu = CPU([])
        
        cpu.F_Z = 1
        
        cycles = jr_nz_r8(cpu, cpu.M)

        self.assertEqual(cycles, 8)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 1)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, 1)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])
        
    @given(integers(min_value=0x00, max_value=0xff))
    def test_jr_nz_r8_NZ(self, r8):

        memory = [0x20, r8]
        cpu = CPU(memory)
        
        cpu.F_Z = 0
        
        cycles = jr_nz_r8(cpu, cpu.M)

        self.assertEqual(cycles, 12)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F_Z, 0)
        self.assertEqual(cpu.F_N, 0)
        self.assertEqual(cpu.F_H, 0)
        self.assertEqual(cpu.F_C, 0)
        
        self.assertEqual(cpu.B, 0)
        self.assertEqual(cpu.C, 0)
        self.assertEqual(cpu.D, 0)
        self.assertEqual(cpu.E, 0)
        self.assertEqual(cpu.H, 0)
        self.assertEqual(cpu.L, 0)
        
        self.assertEqual(cpu.BC, 0)
        self.assertEqual(cpu.DE, 0)
        self.assertEqual(cpu.HL, 0)
        
        self.assertEqual(cpu.PC, r8)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, memory)