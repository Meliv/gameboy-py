from src.cpu import CPU

from src.operations import nop
import unittest

class NOP_Test(unittest.TestCase):
    def test_nop(self):
        cpu = CPU(memory=[])

        cycles = nop(cpu)

        self.assertEqual(cycles, 4)
        
        self.assertEqual(cpu.A, 0)
        self.assertEqual(cpu.F, 0)
        
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
        