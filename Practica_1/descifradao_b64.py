import base64

from tkinter.filedialog import askopenfilename

from Crypto.Util.Padding import unpad
from Crypto.Cipher import DES

BLOCK_SIZE = 32

# Lectura del archivo a cifrar
dir_archivo = askopenfilename(
    title='Archivo a descifrar',
    filetypes=(('Archivo de texto', '*.txt'), )
)

# Lectura del contenido cifrado
archivo = open(dir_archivo, 'r')
nombre_archivo = archivo.name.split('.')[0]
contenido = archivo.read()
archivo.close()

# Lectura de la llave
dir_archivo_llave = askopenfilename(
    title='Llave para descifrar',
    filetypes=(('Archivo de texto', '*.txt'), )
)

archivo_llave = open(dir_archivo_llave, 'rb')
# Separamos la cadena de bytes de la llave y el vector de inicialización
llave = archivo_llave.read()
archivo_llave.close()

# Descifrado del contenido
cifrador = DES.new(llave, DES.MODE_ECB)

bytes_cifrados = base64.b64decode(contenido)

#contenido_descifrado = cifrador.decrypt(contenido)
contenido_descifrado = cifrador.decrypt(bytes_cifrados)

salida = unpad(contenido_descifrado, BLOCK_SIZE)

print(salida.decode('utf-16'))

# Escritura del archivo con contenido cifrado
"""archivo_descifrado = open(nombre_archivo + '_D.txt', 'wb')
archivo_descifrado.write(salida)
archivo_descifrado.close()"""