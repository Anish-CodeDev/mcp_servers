from cryptography.fernet import Fernet
import os

def encrypt_files(folder,extension):
    key = Fernet.generate_key()

    cipher = Fernet(key)

    for file in os.listdir(folder):
        if file.endswith(extension):
            path = os.path.join(folder,file)

            with open(path,'rb') as f:
                data = f.read()
            
            encrypted = cipher.encrypt(data)

            with open(path + ".enc",'wb') as f:
                f.write(encrypted)
    
    return key

def encrypt_file(path):
    key = Fernet.generate_key()
    cipher = Fernet(key)

    with open(path,'rb') as f:
        data = f.read()
    
    encrypted = cipher.encrypt(data)

    with open(path + '.enc','wb') as f:
        f.write(encrypted)
    
    return key