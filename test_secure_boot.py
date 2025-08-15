import unittest
from secure_boot_model import SecureBootPipeline
import os

class TestSecureBoot(unittest.TestCase):
    def setUp(self):
        self.root_key = os.urandom(32)
        self.valid_root_microcode = b'root_microcode_valid_123'
        self.valid_bootloader_microcode = b'bootloader_microcode_456'
        self.valid_kernel_microcode = b'kernel_microcode_789'
        self.invalid_root_microcode = b'invalid_root_microcode_123'

    def test_valid_secure_boot(self):
        pipeline = SecureBootPipeline(self.root_key)
        self.assertTrue(pipeline.boot(self.valid_root_microcode, self.valid_bootloader_microcode, self.valid_kernel_microcode))

    def test_invalid_root_microcode(self):
        pipeline = SecureBootPipeline(self.root_key)
        self.assertFalse(pipeline.boot(self.invalid_root_microcode, self.valid_bootloader_microcode, self.valid_kernel_microcode))

if __name__ == '__main__':
    unittest.main()