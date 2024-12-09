from src.cpu import CPU

from src.operations import stop
import unittest

class STOP_Test(unittest.TestCase):
    def test_stop(self):

        cpu = CPU([])
        
        cycles = stop(cpu)

        self.assertEqual(cycles, 4)
        
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
        
        self.assertEqual(cpu.PC, 2)
        self.assertEqual(cpu.SP, 0)
        
        self.assertEqual(cpu.M, [])        