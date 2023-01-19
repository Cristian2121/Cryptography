from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

class ModoDeOperacion():
    def __init__(self, modo, llave: bytes, iv: bytes, datos_img: bytes):
        self.modo = modo
        self.llave = llave
        self.iv = iv
        self.datos_img = datos_img

    def cifrar_datos(self) -> bytes:
        try:
            if self.modo == DES.MODE_ECB:
                cifrador = DES.new(self.llave, self.modo)
                bytes_imagen_cifrada = cifrador.encrypt(pad(self.datos_img, DES.block_size))
            else:
                cifrador = DES.new(self.llave, self.modo, iv=self.iv)
                bytes_imagen_cifrada = cifrador.encrypt(pad(self.datos_img, DES.block_size))
        
            return bytes_imagen_cifrada
        except:
            return self.datos_img

    def descifrar_datos(self) -> bytes:
        if self.modo == DES.MODE_ECB:
            cifrador = DES.new(self.llave, self.modo)
            bytes_imagen_descifrada = cifrador.decrypt(self.datos_img)
        else:
            cifrador = DES.new(self.llave, self.modo, iv=self.iv)
            bytes_imagen_descifrada = cifrador.decrypt(self.datos_img)
        
        return bytes_imagen_descifrada