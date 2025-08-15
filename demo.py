from secure_boot_model import SecureBootPipeline
import os

# 生成根密钥
root_key = os.urandom(32)
# 有效根微码（要以模型中指定的有效前缀开头，这里是 b'root_microcode_valid_'）
valid_root_microcode = b'root_microcode_valid_123'
valid_bootloader_microcode = b'bootloader_microcode_456'
valid_kernel_microcode = b'kernel_microcode_789'

# 初始化安全启动流程
pipeline = SecureBootPipeline(root_key)

# 执行启动
print("--- Demo 1: Valid Secure Boot ---")
if pipeline.boot(valid_root_microcode, valid_bootloader_microcode, valid_kernel_microcode):
    print("Secure Boot Demo 1 Successful!")
else:
    print("Secure Boot Demo 1 Failed!")

# 无效根微码示例（不以 b'root_microcode_valid_' 开头）
invalid_root_microcode = b'invalid_root_microcode_123'

print("\n--- Demo 2: Invalid Root Microcode ---")
if pipeline.boot(invalid_root_microcode, valid_bootloader_microcode, valid_kernel_microcode):
    print("Secure Boot Demo 2 Successful!")
else:
    print("Secure Boot Demo 2 Failed!")