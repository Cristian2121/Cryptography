"""
    Módulos:
    Crypto. Primitivas criptográficas.
    PKCS115_SigScheme. Sirve para crear un objeto de firma digital que permitirá firmar y verificar una firma.
    RSA. Permite generar par de llaves y crear los objetos llave correspondientes.
    get_random_bytes. Función para obtener bytes aleatorios, usada por el algoritmo RSA.
    SHA256. Para hacer hash criptografico a un mensaje.
"""

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, showerror

from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def elegir_archivo() -> tuple:
    """
        Permite elegir un archivo del explorador de archivos del
        usuario, este puede ser el archivo original o el firmado.

        Retorno:
        datos_f: cadena con el contenido del txt
        nombre_archivo: cadena del nombre correspondiente al archivo txt
    """

    ruta_archivo = askopenfilename(
        title="Elegir archivo",
        filetypes=(("Archivo de texto", "*.txt"), )
    )

    with open(ruta_archivo, "r") as f_e:
        datos_f = f_e.read()
        nombre_archivo = f_e.name.split('.')[0]
        f_e.close()

    return (datos_f, nombre_archivo)

def elegir_llave() -> bytes:
    """
        Permite elegir la llave (pública o privada) del explorador de 
        archivos del usuario.

        Retorno:
        datos_llave: bytes del contenido del archivo pem 
    """

    ruta_llave = askopenfilename(
        title="Elegir llave",
        filetypes=(("Archivo de llave", "*.pem"), )
    )

    with open(ruta_llave, "rb") as f_e:
        datos_llave = f_e.read()
        f_e.close()

    return datos_llave

def firmar_archivo() -> None:
    """
        Permite firmar el archivo elegido por el usuario, además
        escribe el archivo después de firmarlo en la ruta del proyecto.
    """

    datos_archivo, nombre_archivo = elegir_archivo()
    datos_privada = elegir_llave()

    # Crea la llave con el objeto RSA
    llave = RSA.importKey(datos_privada)

    # Creamos el digesto de 256 bit del contenido original
    h = SHA256.new(datos_archivo.encode())

    # Creación del objeto firma a partir de la llave privada
    # firma del digesto
    firma = PKCS115_SigScheme(llave).sign(h)

    with open(nombre_archivo + "_firmado.txt", "w") as f:
        # Concatenación de los datos originales, el separador y la firma
        f.write(datos_archivo + "-|-|" + firma.hex())
        f.close()

def verificacion_firma() -> None:
    """
        Permite verificar si la firma de algún archivo corresponde
        con una llave determinada, tanto el archivo firmado como la
        llave es seleccionada por el usuario.
    """

    datos_archivo_firmado, nombre_archivo = elegir_archivo()
    datos_publica = elegir_llave()

    # Separar firma y mensaje
    separador = datos_archivo_firmado.find('-|-|')
    msj = datos_archivo_firmado[0:separador]
    firma = datos_archivo_firmado[separador + 4:]

    # Crea la llave con el objeto RSA
    llave = RSA.importKey(datos_publica)

    # Creamos el digesto de 256 bit del contenido original
    h = SHA256.new(msj.encode())

    # Objeto firma creado a partir de la llave pública
    verificador = PKCS115_SigScheme(llave)

    try:
        verificador.verify(h, bytes(bytearray.fromhex(firma)))
        showinfo('Verificación', 'La firma es auténtica.')
    except (ValueError, TypeError):
        showerror('Verificación', 'La firma no es auténtica.')

def generar_llave(nombre: str) -> None:
    """
        Permite crear una pareja de llaves, y las escribe
        de manera separada.

        Parámetros:
        nombre: cadena que ayuda a diferenciar a quién pertenecen las llaves
    """

    # Generar pareja de llaves de longitud 1024
    llave = RSA.generate(1024, get_random_bytes)

    # Exportamos la clave privada
    llave_privada = llave.export_key()

    # Guardamos la clave privada en un fichero
    with open("privada_" + nombre + ".pem", "wb") as f:
        f.write(llave_privada)
        f.close()

    # Obtenemos la clave pública
    llave_publica = llave.publickey().export_key()

    # Guardamos la clave pública en un fichero
    with open("publica_" + nombre + ".pem", "wb") as f:
        f.write(llave_publica)
        f.close()

if __name__ == "__main__":
    # Primera parte: generar llaves
    """generar_llave('Alicia')
    generar_llave('Betito')
    generar_llave('Candy')"""

    # Segunda parte: firmar archivo
    #firmar_archivo()

    # tercer parte: verificacion
    #verificacion_firma()

    # Verificar que las llaves sean diferentes
    with open('privada_Alicia.pem', 'rb') as f:
        publica_alicia = f.read()
        f.close()

    with open('privada_Betito.pem', 'rb') as f:
        publica_betito = f.read()
        f.close()

    with open('privada_Candy.pem', 'rb') as f:
        publica_candy = f.read()
        f.close()

    if publica_alicia==publica_betito:
        print('son iguales')
    else:
        print('no son iguales')