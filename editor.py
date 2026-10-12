from prompt_toolkit import prompt

class Editor:
    def __init__(self):
        self.pila_principal = []
        self.pila_auxiliar = []
        self.pos = 1

    @staticmethod
    def limpiar_terminal() -> None:
        import os
        os.system("cls" if os.name == "nt" else "clear")

    def _renderizar(self):
        self.limpiar_terminal()
        if self.pila_principal:
            for i, linea in enumerate(self.pila_principal):
                print(f"{i+1} >>> : {linea}")

    def entrada(self):
        while True:
            self._renderizar()
            linea = input(f"{self.pos} >>> : ")
            self.pos += 1
            try:

                if linea == "":
                    break

                elif linea.strip().lower() == "break":
                    break

                elif linea.lower().startswith("edit "):
                    self._edit(linea)

                elif linea.lower().startswith("insert "):
                    self._insert(linea)

                elif linea.lower().startswith("del "):
                    self._del(linea)

                elif linea.strip().lower() == "clear":
                    self._clear()

                else:
                    self.pila_principal.append(linea)

            except Exception as error:
                print(f"Error: {error}.")
                input()

        return self.pila_principal
    
    def _edit(self, linea):
        self._procesar_comando(linea, self._logica_edit)
        
    def _insert(self, linea):
        self._procesar_comando(linea, self._logica_insert)
        
    def _del(self, linea):
        numero_linea = self._procesar_linea(linea)
        self.pila_principal.pop(numero_linea - 1)
        self.pos -= 1
        
    def _clear(self):
        self.pila_principal = []
        self.pos = 1

    def _procesar_comando(self, linea_comando, logica_comando):
        numero_linea = self._procesar_linea(linea_comando)
        while self.pila_principal and numero_linea <= len(self.pila_principal):
            self.pila_auxiliar.append(self.pila_principal.pop())
        nueva_linea = logica_comando(numero_linea)
        self.pila_auxiliar.append(nueva_linea)
        while self.pila_auxiliar:
            self.pila_principal.append(self.pila_auxiliar.pop())

    def _procesar_linea(self, linea_comando):
        linea_format = linea_comando.split()
        self.pos -= 1
        if len(linea_format) == 2 and linea_format[1].isdigit():
            numero_linea = int(linea_format[1])
            if numero_linea > 0 and numero_linea <= len(self.pila_principal):
                return numero_linea
            else:
                raise Exception(f"La línea [ {numero_linea} ] no existe")
        else:
            raise Exception(f"El comandó [ {linea_comando} ] no es válido")

    def _logica_edit(self, numero_linea):
        texto = self.pila_auxiliar.pop()
        linea_editada = prompt(f"{numero_linea} >>> : ", default=texto)
        return linea_editada
    
    def _logica_insert(self, numero_linea):
        nueva_linea = input(f"{numero_linea} >>> : ")
        self.pos += 1
        return nueva_linea
    
editor = Editor()
lineas = editor.entrada()
print(lineas)

