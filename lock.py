# lock.py
# Created by Ghost In A Jar

'''
Usage:

lock.py [action] <target directory>

Actions:

-e (encrypt)
-d (decrypt)
'''

import os
import sys
import shutil
import subprocess
import getpass

def clear_password(password):
    password[:] = b'\x00' * len(password)

def genrand(byte_length):
    return os.urandom(byte_length).hex()

def encrypt_file(filename, password, out_dir):
    random_name = genrand(4)
    enc_filename = random_name + ".gpg"
    
    subprocess.run(["gpg", "--batch", "--yes", "--pinentry-mode", "loopback", "--passphrase-fd", "0",
                    "-o", os.path.join(out_dir, enc_filename), "-c", filename], input = password, check = True)
                    
def decrypt_file(filename, password, out_dir):
    subprocess.run(["gpg", "--batch", "--yes", "--pinentry-mode", "loopback", "--passphrase-fd", "0",
                    "--use-embedded-filename", filename], input = password, cwd = out_dir, check = True)
                    
def walk_encrypt_path(src_dir, password):
    ENC_DIR = "enc"
    
    if not os.path.exists(ENC_DIR):
        os.mkdir(ENC_DIR)

    for dirpath, _, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(".gpg"):
                continue
            file_path = os.path.join(src_dir, filename)
            encrypt_file(file_path, password, ENC_DIR)
            
def walk_decrypt_path(src_dir, password):
    OUT_DIR = "unlocked"
    
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)

    for dirpath, _, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(".gpg"):
                decrypt_file_path = os.path.join("..", src_dir, filename)
                decrypt_file(decrypt_file_path, password, OUT_DIR)
                delete_file_path = os.path.join(src_dir, filename)
                os.remove(delete_file_path)
            
if __name__ == "__main__":
    password_str = getpass.getpass("Enter Password: ")
    confirm_password_str = getpass.getpass("Confirm Password: ")

    password = bytearray(password_str, "utf-8")
    del password_str
    
    confirm_password = bytearray(confirm_password_str, "utf-8")
    del confirm_password_str
    
    if password != confirm_password:
        print("The passwords do not match")
        sys.exit(1)
    elif bool(password) == False or bool(confirm_password) == False:
        print("Password should not be empty")
        sys.exit(1)
        
    clear_password(confirm_password)
    
    try:
        src_dir = sys.argv[2]
        if sys.argv[1] == "-e":
            walk_encrypt_path(src_dir, password)
        elif sys.argv[1] == "-d":
            walk_decrypt_path(src_dir, password)
    finally:
        clear_password(password)
        
