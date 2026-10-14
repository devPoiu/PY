def xor(text, key):
    result = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        print(f'{char}-{ord(char):08b}')

        key_char = key[i % key_length]
        print(f'{key_char}-{ord(key_char):08b}')

        cipher_char = chr(ord(char) ^ ord(key_char))
        print(' ','-'*8)
        print(f'  {ord(cipher_char):08b}\n')

        result.append(cipher_char)
        
    return "".join(result)

message = "Hello, World!"
secret_key = "CODE"

encrypted = xor(message, secret_key)
print(f"Зашифровано: {encrypted.encode('utf-8').hex()}") 

decrypted = xor(encrypted, secret_key)
print(f"Расшифровано: {decrypted}")
