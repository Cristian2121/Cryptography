import base64

from tkinter.filedialog import askopenfilename

from Crypto.Util.Padding import pad
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 32

dir_archivo = askopenfilename(
    title='Archivo a cifrar',
    filetypes=(('Archivo de texto', '*.txt'), )
)

archivo = open(dir_archivo, 'r')
nombre_archivo = archivo.name.split('.')[0]
contenido = archivo.read()
archivo.close()

# Cifrado del contenido
llave = get_random_bytes(8)
cifrador = DES.new(llave, DES.MODE_ECB)
contenido_cifrado = cifrador.encrypt(pad(contenido.encode('utf-8'), BLOCK_SIZE))

# Convirtiendo a base64
b64_cifrado = base64.b64encode(contenido_cifrado).decode()

# Escritura del archivo con la llave y el iv
archivo_llave = open(nombre_archivo + '_llave.txt', 'wb')
archivo_llave.write(llave)
archivo_llave.close()

# Escritura del archivo con contenido cifrado
archivo_cifrado = open(nombre_archivo + '_C.txt', 'w')
#archivo_cifrado.write(contenido_cifrado)
archivo_cifrado.write(b64_cifrado)
archivo_cifrado.close()