from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror

class App():
    def __init__(self, raiz):
        #------------------VARIABLES------------------#
        self.ek = StringVar()
        self.dk = StringVar()

        #------------------BOTONES Y LABELS------------------#
        frame_principal = ttk.Frame(raiz)
        frame_principal.pack()

        lbl_n = ttk.Label(frame_principal, text='Ingresa la variable n:')
        lbl_n.grid(row=0, column=0)
        lbl_alfa = ttk.Label(frame_principal, text='Ingresa la variable ' + chr(945) + ':')
        lbl_alfa.grid(row=1, column=0)
        lbl_beta = ttk.Label(frame_principal, text='Ingresa la variable ' + chr(946) + ":")
        lbl_beta.grid(row=2, column=0)

        self.ent_n = ttk.Entry(frame_principal, justify='center')
        self.ent_n.grid(row=0, column=1)
        self.ent_alfa = ttk.Entry(frame_principal, justify='center')
        self.ent_alfa.grid(row=1, column=1)
        self.ent_beta = ttk.Entry(frame_principal, justify='center')
        self.ent_beta.grid(row=2, column=1)

        btn_calcular = ttk.Button(frame_principal, text='Calcular', command=self.validar_datos)
        btn_calcular.grid(row=3, columnspan=2)

        for child in frame_principal.winfo_children():
            child.grid_configure(padx=5, pady=5)

        #------------------LABELS SALIDA------------------#
        frame_secundario = ttk.Frame(raiz)
        frame_secundario.pack()

        lbl_ek = ttk.Label(frame_secundario, text='Ek:')
        lbl_ek.grid(row=0, column=0)
        lbl_ek_calculado = ttk.Label(frame_secundario, textvariable=self.ek)
        lbl_ek_calculado.grid(row=0, column=1)
        lbl_dk = ttk.Label(frame_secundario, text='Dk:')
        lbl_dk.grid(row=1, column=0)
        lbl_dk_calculado = ttk.Label(frame_secundario, textvariable=self.dk)
        lbl_dk_calculado.grid(row=1, column=1)

        for child in frame_secundario.winfo_children():
            child.grid_configure(padx=5, pady=5)

    #---------------------FUNCIONES---------------------#        
    def validar_datos(self):
        try:
            alfa = int(self.ent_alfa.get())
            beta = int(self.ent_beta.get())
            n = int(self.ent_n.get())

            # Validar que alfa, beta < n & alfa, beta no sean negativos
            alfa_correcto = self.validar_alfa_beta(alfa, n)
            beta_correcto = self.validar_alfa_beta(beta, n)

            # Validar que gcd(alfa, n) = 1
            if self.euclidean_algorithm(alfa, n) == 1:
                # Valores calculados para la función Dk
                g, x, y = self.gcdExtended(alfa_correcto, n)
                beta_inversa = self.validar_alfa_beta(beta_correcto * -1, n)
                
                if x < 0:
                    alfa_inversa = self.validar_alfa_beta(x, n)
                else:
                    alfa_inversa = x

                self.ek.set(f"C = {alfa_correcto}m + {beta_correcto} mod {n}")
                self.dk.set(f"D = {alfa_inversa}[C + {beta_inversa}] mod {n}")
            else:
                showerror(
                    'GCD inválido', 
                    f"GCD({alfa}, {n}) = {self.euclidean_algorithm(alfa, n)}, por lo que no se cumple la regla GCD(a, n)=1. Prueba con otros datos."
                )

            #print(F"gcd({alfa}, {n}) = {self.euclidean_algorithm(alfa, n)}")
        except ValueError:
            showerror('Datos inválidos', 'Por favor, ingrese datos enteros en todas las casillas.')

    def euclidean_algorithm(self, a, n):
        while n > 0:
            r = a % n
            a = n
            n = r

        return a

    def gcdExtended(self, a, b):
        # Base Case
        if a == 0:
            return b, 0, 1
    
        gcd, x1, y1 = self.gcdExtended(b % a, a)
    
        # Update x and y using results of recursive
        # call
        x = y1 - (b//a) * x1
        y = x1
    
        return gcd, x, y

    def validar_alfa_beta(self, a, n):
        if a < 0:
            # Para convertir el negativo a positivo.
            a = a * -1

            # Si el valor sobrepasa a n, entonces calcular mod n
            if a > n:
                a = a % n

                a = n - a
            # si ya es menor, entonces restar del modulo n
            else:
                a = n - a
        elif a > n:
            a = a % n

        return a

#---------------------MAIN---------------------#
raiz = Tk()
raiz.title('Función Afín')
raiz.resizable(0, 0)

App(raiz)

raiz.mainloop()