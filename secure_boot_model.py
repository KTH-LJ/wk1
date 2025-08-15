import hmac
import hashlib
import os

class SecureBootComponent:
    def __init__(self, name, key, valid_prefix=None):
        self.name = name
        self.key = key  
        self.is_verified = False
        self.memory = {}  
        self.valid_prefix = valid_prefix 

    def generate_hmac(self, data):
        return hmac.new(self.key, data, hashlib.sha256).digest()

    def verify_hmac(self, data, received_hmac):
        expected_hmac = self.generate_hmac(data)
        self.is_verified = hmac.compare_digest(expected_hmac, received_hmac)
        return self.is_verified

    def is_microcode_valid(self, microcode):
        if self.valid_prefix is None:
            return True  
        return microcode.startswith(self.valid_prefix)

    def load_microcode(self, microcode, microcode_hmac):
        if not self.is_microcode_valid(microcode):
            print(f"[{self.name}] Microcode is invalid by content!")
            return False
        if self.verify_hmac(microcode, microcode_hmac):
            print(f"[{self.name}] Microcode verified successfully.")
            self.memory["microcode"] = microcode
            return True
        else:
            print(f"[{self.name}] Microcode verification failed!")
            return False

    def execute_microcode(self):
        if self.is_verified and "microcode" in self.memory:
            print(f"[{self.name}] Executing verified microcode...")
            print(f"Microcode snippet: {self.memory['microcode'][:20]}...")
            return True
        else:
            print(f"[{self.name}] Cannot execute unverified microcode.")
            return False

    def read_protected_memory(self, address, is_verified):
        if is_verified and address in self.memory:
            return self.memory[address]
        else:
            print(f"[{self.name}] Unauthorized access to protected memory at {address}!")
            return None

class SecureBootPipeline:
    def __init__(self, root_key, bootloader_key=None, kernel_key=None):
        self.root_component = SecureBootComponent("Root", root_key, valid_prefix=b'root_microcode_valid_')
        self.bootloader_component = SecureBootComponent("Bootloader", bootloader_key if bootloader_key else os.urandom(32))
        self.kernel_component = SecureBootComponent("Kernel", kernel_key if kernel_key else os.urandom(32))

    def boot(self, root_microcode, bootloader_microcode, kernel_microcode):
    
        print("=== Starting Secure Boot Pipeline ===")

        root_hmac = self.root_component.generate_hmac(root_microcode)
        if not self.root_component.load_microcode(root_microcode, root_hmac):
            return False

        bootloader_hmac = self.bootloader_component.generate_hmac(bootloader_microcode)
        if not self.bootloader_component.load_microcode(bootloader_microcode, bootloader_hmac):
            return False

        kernel_hmac = self.kernel_component.generate_hmac(kernel_microcode)
        if not self.kernel_component.load_microcode(kernel_microcode, kernel_hmac):
            return False

        self.root_component.execute_microcode()
        self.bootloader_component.execute_microcode()
        self.kernel_component.execute_microcode()

        print("=== Secure Boot Pipeline Completed Successfully ===")

        return True
