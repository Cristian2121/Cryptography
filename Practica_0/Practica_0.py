from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

# 32 bytes * 8 = 256 bits
llave = get_random_bytes(32)
# La información debe estar codificada a bytes
info_a_cifrar = 'Esto es texto plano'
# Es importante codificar la info a bytes
info = info_a_cifrar.encode('utf-8')

#------------ CIFRAR ------------#
# Cipher FeedBack
objeto_cipher = AES.new(llave, AES.MODE_CFB)
bytes_cifrados = objeto_cipher.encrypt(info)

# Esta es nuestra información
# Initialization Vector
iv = objeto_cipher.iv
info_cifrada = bytes_cifrados

print("Cadena cifrada: {}".format(info_cifrada))

#------------ DESCIFRAR ------------#
# Se conoce la llave, la info cifrada y el iv
objeto_cipher_desc = AES.new(llave, AES.MODE_CFB, iv=iv)
bytes_descifrados = objeto_cipher_desc.decrypt(info_cifrada)

info_descifrada = bytes_descifrados.decode('utf-8')

print("Cadena descifrada: {}".format(info_descifrada))

# Permite realizar comprobaciones, si la expresión es False lanza una excepción
assert info_a_cifrar == info_descifrada, 'La información original no coincide.'




