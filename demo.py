from secure_boot_model import SecureBootPipeline
import os


root_key = os.urandom(32)
valid_root_microcode = b'root_microcode_valid_123'
valid_bootloader_microcode = b'bootloader_microcode_456'
valid_kernel_microcode = b'kernel_microcode_789'

pipeline = SecureBootPipeline(root_key)

print("--- Demo 1: Valid Secure Boot ---")
if pipeline.boot(valid_root_microcode, valid_bootloader_microcode, valid_kernel_microcode):
    print("Secure Boot Demo 1 Successful!")
else:
    print("Secure Boot Demo 1 Failed!")

invalid_root_microcode = b'invalid_root_microcode_123'

print("\n--- Demo 2: Invalid Root Microcode ---")
if pipeline.boot(invalid_root_microcode, valid_bootloader_microcode, valid_kernel_microcode):
    print("Secure Boot Demo 2 Successful!")
else:

    print("Secure Boot Demo 2 Failed!")
