


from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webbrowser
from tkinter import messagebox

# Facilitan el acceso al tipo de estado ya que unicamente funcionan en base a un código, es decir, estados[0] -> Inicializandose.
estados = ["Inicializandose", "Preparado", "Suspendido", "Terminado"]

# Permite generar advertencias y errores en base a un código y donde ocurrio el problema
def advertencias_errores(id_adverr, lugar):
        if id_adverr == "A01":
            messagebox.showerror("Advertencia A01:", f"No has ingresado un valor más que el por defecto en {lugar}.")            
        elif id_adverr == "E01":
            messagebox.showerror("Error E01:", f"Has ingresado un tipo de dato erroneo en {lugar}.")    



class Proceso:
    '''
        La clase proceso permite que un proceso almacene los siguientes datos:
            - nombre -> Es el nombre del proceso
            - tiempo de ejecución -> El tiempo de procesamiento del proceso.
            - tiempo restante de ejecución -> El tiempo restanto por procesar del proceso. (Causado por posible suspensión del mismo)
            - prioridad -> La prioridad del proceso. (Se asume que 0 es la prioridad más alta)
            - PID -> Identificador del proceso
            - estado -> Es el estado en el que se encuentra actualmente el proceso dado por un número
    '''
    
    # Contructor del proceso.    
    def __init__ (self, nombre, tiempo_ejecucion, prioridad, PID):
        self.nombre = nombre
        self.tiempo_ejecucion = tiempo_ejecucion        
        self.prioridad = prioridad
        self.PID = PID
        self.tiempo_restante = tiempo_ejecucion
        self.estado = 0
        
    # Devuelve información del proceso.
    def __str__(self):        
        return f"PID: {self.PID} | Proceso: {self.nombre} | Prioridad: {self.prioridad} | Tiempo de ejecución: {self.tiempo_ejecucion} | Tiempo restante de ejecución: {self.tiempo_restante} | Estado: {estados[(int)(self.estado)]}"               
        
    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre
    def set_tiempo_ejecucion(self, tiempo_ejecucion):
        self.tiempo_ejecucion = tiempo_ejecucion
    def set_tiempo_restante(self, tiempo_restante):
        self.tiempo_restante = tiempo_restante
    def set_prioridad(self, prioridad):
        self.prioridad = prioridad;
    def set_PID(self, PID):
        self.PID = PID
    def set_estado(self, estado):
        self.estado = estado
        
    # Getters
    def get_nombre(self):
        return self.nombre
    def get_tiempo_ejecucion(self):
        return self.tiempo_ejecucion
    def get_tiempo_restante(self):
        return self.tiempo_restante
    def get_prioridad(self):
        return self.prioridad
    def get_PID(self):
        return self.PID
    def get_estado(self):
        return self.estado  
    

class Administrador:
    '''
    La clase administrador contiene todas los métodos que se requieren para interactuar con los procesos tales como:
        - Crear proceso -> Crea un proceso nuevo.
        - Ejecutar Procesos -> Comienza el procesamiento de todos los procesos con fin de suspension manual.
        - ejecutar proceso auto -> Comienza el procesamiento de todos los procesos con fin de suspension automática.
        - Renudar -> Reanuda un proceso suspendido
        - Matar Proceso -> Finaliza un proceso en ejecución
        - Ver lista de todos los procesos -> Devuelve la lista de todos los procesos
        - Ver lista de los procesos preparados -> Devuelve la lista de los procesos preparados
        - Ver lista de los procesos suspendidos -> Devuelve la lista de los procesos suspendidos
        - to_preparado -> Permite la migración de los procesos recien creados a estar preparados.
        - ver_terminados -> Devuelve la lista de los procesos terminados
        - salir -> funciona como un Garbage Collector
        - buscar_proceso -> busca un proceso dado el PID del mismo
        - eliminar_proceso_lista -> elimina un proceso de una lista dado el PID del mismo
        - eliminar_proceso -> elimina un proceso recientemente ingresado
        - vaciar -> vacia la lista de procesos terminados
        - ordenar -> ordena una lista dado un código tanto por prioridad como por PID
        - evaluar_salida -> reestablece el valor del PID cuando un proceso finaliza
        - set_tiempos -> establecen los tiempos tanto para el tiempo máximo de procesamiento como para el tiempo de suspendido máximo.
        
    Por otra parte, sus atributos son:
        - procesos_todos -> una lista con todos los procesos menos los finalizados
        - procesos_preparados -> una lista con todos los procesos preparados
        - procesos_suspendidos -> una lista con todos los procesos suspendidos
        - procesos_terminados -> una lista con todos los procesos terminados
        - PID -> identificador de cuantos procesos existen en el programa sin haber finalizado
        - tiempo_max -> tiempo máximo de ejecución del aplicativo
        - tiempo_restante -> tiempo restante del máximo de ejecucion del aplicativo
        - tiempo_suspendido -> tiempo máximo de suspensión de un proceso
        - tiempo_suspendido_restante -> tiempo restante del máximo de suspensión de un proceso
    '''
    # Constructor
    def __init__(self):
        # Las listas presentes almacenarán todos los procesos que se crearán.
        self.procesos_todos = []
        self.procesos_preparados = []
        self.procesos_suspendidos = []   
        self.procesos_terminados = []
        # Se refiere al código que tendrá cada proceso
        self.PID = 0      
        # Tiempos de procesamiento
        self.tiempo_max = 0
        self.tiempo_restante = 0
        # Tiempos de suspensión máximo
        self.tiempo_suspendido = 0
        self.tiempo_suspendido_restante = 0            
    
    # Crea un proceso y lo agrega a la lista de todos los procesos
    def crear_proceso(self, nombre, tiempo_ejecucion, prioridad):
        proceso = Proceso(nombre, tiempo_ejecucion, prioridad, self.PID)
        self.procesos_todos.append(proceso)
        self.PID += 1            
        
    # Inicia la ejecución de los procesos con fin de suspendido automatico
    def ejecutar_proceso_auto(self):
        # Mueve todos los procesos a preparado si se encuentran en la lista inicial
        self.to_preparado()
        # Comienza la ejecución de todos los procesos
        while(True):
            try:
                # Se toma el proceso con prioridad más alta
                proceso_ejecucion = self.procesos_preparados.pop()
            except:
                if len(self.procesos_suspendidos) > 0:
                    self.reanudar(self.procesos_suspendidos[0].get_PID())
                    continue
                else:
                    break                
            # Se muestra le proceso en ejecucion en el GUI
            mostrar_proceso(proceso_ejecucion.get_nombre())
            # Se ejecuta el proceso
            for x in range(self.tiempo_max+1):
                # Si el tiempo de suspendido llega a 0 y existe un proceso suspendido, se procede a enviarlo a preparado
                if len(self.procesos_suspendidos) != 0:
                    self.tiempo_suspendido_restante -= 1
                    if self.tiempo_suspendido_restante == 0:
                        self.reanudar(self.procesos_suspendidos[0].get_PID())
                        self.tiempo_suspendido_restante = self.tiempo_suspendido
                # Si el tiempo de ejecución por proceso máximo termina y el proceso aún no, procede a suspenderse
                if(self.tiempo_restante == 0 and proceso_ejecucion.get_tiempo_restante() > 0):
                    proceso_ejecucion.set_estado(2)
                    self.procesos_suspendidos.append(proceso_ejecucion)
                    self.tiempo_restante = self.tiempo_max
                    break
                # Si el proceso termina sin que el proceso de ejecución máximo termine, el proceso termina
                elif proceso_ejecucion.get_tiempo_restante() == 0:
                    proceso_ejecucion.set_estado(3)                    
                    self.procesos_terminados.append(proceso_ejecucion)                    
                    self.eliminar_proceso_lista(proceso_ejecucion)
                    self.evaluar_salida(proceso_ejecucion.get_PID())
                    break
                # Se aumenta un contador al tiempo
                self.tiempo_restante -= 1
                proceso_ejecucion.set_tiempo_restante(proceso_ejecucion.get_tiempo_restante()-1)
                set_tiempos(self.tiempo_restante, proceso_ejecucion.get_tiempo_restante())   
            
    # Inicia la ejecución de los procesos con fin de suspensión manual
    def ejecutar_proceso(self):
        # Mueve todos los procesos a preparado si se encuentran en la lista inicial
        self.to_preparado()
        # Comienza la ejecución de todos los procesos
        while(True):
            try:
                # Se toma el proceso con prioridad más alta
                proceso_ejecucion = self.procesos_preparados.pop()
            except:
                break
                
            # Se muestra le proceso en ejecucion en el GUI
            mostrar_proceso(proceso_ejecucion.get_nombre())
            # Se ejecuta el proceso
            for x in range(self.tiempo_max+1):
                # Si el tiempo de ejecución por proceso máximo termina y el proceso aún no, procede a suspenderse
                if(self.tiempo_restante == 0 and proceso_ejecucion.get_tiempo_restante() > 0):
                    proceso_ejecucion.set_estado(2)
                    self.procesos_suspendidos.append(proceso_ejecucion)
                    self.tiempo_restante = self.tiempo_max
                    break
                # Si el proceso termina sin que el proceso de ejecución máximo termine, el proceso termina
                elif proceso_ejecucion.get_tiempo_restante() == 0:
                    proceso_ejecucion.set_estado(3)
                    self.procesos_terminados.append(proceso_ejecucion)
                    self.eliminar_proceso_lista(proceso_ejecucion)
                    self.evaluar_salida(proceso_ejecucion.get_PID())
                    break
                # Se aumenta un contador al tiempo
                self.tiempo_restante -= 1
                proceso_ejecucion.set_tiempo_restante(proceso_ejecucion.get_tiempo_restante()-1)
                set_tiempos(self.tiempo_restante, proceso_ejecucion.get_tiempo_restante())       
            
    def to_preparado(self):
        for x in self.procesos_todos:
            if x.get_estado() == 0:
                x.set_estado(1)
                self.procesos_preparados.append(x)                          
        self.ordenar(self.procesos_preparados)
        
    
    # Reanuda un proceso suspendido dado su PID
    def reanudar(self, PID):
        proceso = self.buscar_proceso(PID, 2)
        proceso.set_estado(1)
        self.eliminar_proceso_lista(proceso,2)
        self.procesos_todos[PID-1].set_estado(1)
        self.procesos_preparados.append(proceso)
        self.ordenar(self.procesos_preparados)
    
    # Finaliza un proceso dado su PID
    def matar_proceso(self, PID, nivel):
        proceso_ejecucion = self.buscar_proceso(PID, nivel)
        proceso_ejecucion.set_estado(3)
        self.procesos_terminados.append(proceso_ejecucion)
        self.eliminar_proceso_lista(proceso_ejecucion)
        self.evaluar_salida(proceso_ejecucion.get_PID())
        
        #proceso_ejecucion = self.buscar_proceso(PID, nivel)
        #proceso_ejecucion.set_estado(3)        
        #self.procesos_terminados.append(proceso_ejecucion)
        #self.eliminar_proceso_lista(proceso_ejecucion, nivel)        
        #self.eliminar_proceso_lista(proceso_ejecucion)
        #self.evaluar_salida(PID)
    
    # Devuelve la lista de todos los procesos
    def ver_lista(self):
        return self.procesos_todos
    
    # Devuelve la lsita de los procesos preparados
    def ver_preparados(self):
        return self.procesos_preparados
    
    # Devuelve la lista de los proceso suspendidos
    def ver_suspendidos(self):
        return self.procesos_suspendidos;
    
    # Devuelve la lista de los procesos acabados
    def ver_terminados(self):
        return self.procesos_terminados;
    
    # Elimina toda la información de los procesos
    def salir(self):
        self.procesos_todos = []
        self.procesos_preparados = []
        self.procesos_suspendidos = [] 
        self.procesos_terminados = [] 
                
    # Función que localiza el proceso con mayor prioridad
    def buscar_prioridad_mayor(self):
        '''
        Se debe tener en cuenta que se asume que la prioridad máxima es 0
        '''       
        if len(self.procesos_todos) == 0:
            proceso_temp = Proceso("", 0, 0, -1)
            return proceso_temp
         # Almacena la priorisdad máxima encontrada
        prioridad_max = self.procesos_todos[0].get_prioridad()
        proceso_PID = self.procesos_todos[0].get_PID()
        for x in range(len(self.procesos_todos)):
            if self.procesos_todos[x].get_prioridad() < prioridad_max:
                prioridad_max = self.procesos_todos[x].get_prioridad
                proceso_PID = self.procesos_todos[x].get_PID()
        proceso_deseado = self.buscar_proceso(proceso_PID)
        return proceso_deseado
    
    # Busca y devuelve un proceso en una lista dada
    def buscar_proceso(self, PID, lista = 0):
        # Busca un proceso en la lista de todos los procesos
        if lista == 0:
            for x in self.procesos_todos:
                if x.get_PID() == PID:
                    return x
        # Busca un proceso en la lista de procesos preparados
        elif lista == 1:
            for x in self.procesos_preparados:
                if x.get_PID() == PID:
                    return x
        # Busca un proceso en la lista suspendidos
        else:
            for x in self.procesos_suspendidos:
                if x.get_PID() == PID:
                    return x
    
    # Elimina el proceso de una lista.
    def eliminar_proceso_lista(self, proceso, lista = 0):
        # Elimina un proceso en la lista de todos los procesos
        if lista == 0:
            self.procesos_todos.remove(proceso)
        # Elimina un proceso en la lista preparados
        elif lista == 1:
            self.procesos_preparados.remove(proceso)
        # Elimina un proceso en la lista suspendidos
        else:
            self.procesos_suspendidos.remove(proceso)
            
    def eliminar_proceso(self, PID):
        val = False
        self.PID -= 1
        for x in self.procesos_todos:
            if x.get_PID() == PID:
                self.procesos_todos.remove(x)
                val = True
        if val != True:
            for x in self.procesos_preparados:
                if x.get_PID() == PID:
                    self.procesos_preparados.remove(x)
                    val = True
        if val != True:
            for x in self.procesos_suspendidos:
                if x.get_PID() == PID:
                    self.procesos_suspendidos.remove(x)   
                    
    # Vacia la lista de procesos terminados
    def vaciar(self):
        self.procesos_terminados=[]
        
    # Ordena una lista por la prioridad
    def ordenar(self, lista, orden = 0):
        # Ordenar por prioridad mayor a menor (mayor == 0)
        if orden == 0:
            for i in range(len(lista)):
                for j in range(len(lista[1:])):
                    if lista[i].get_prioridad() > lista[j].get_prioridad():
                        temp = lista[i]
                        lista[i] = lista[j]
                        lista[j] = temp   
        # ORdenar por PID menor a mayor (menor == 0)
        elif orden == 1:
            for i in range(len(lista)):
                for j in range(len(lista[1:])):
                    if lista[i].get_PID() < lista[j].get_PID():
                        temp = lista[i]
                        lista[i] = lista[j]
                        lista[j] = temp
                    
    def evaluar_salida(self, PID):
        self.procesos_preparados = []
        self.procesos_suspendidos = []
        self.PID -= 1
        if self.PID == 0:
            self.procesos_todos[0].set_PID(0)
        for x in range(self.PID):            
            if x >= PID:                
                self.procesos_todos[x].set_PID(x)
        for x in self.procesos_todos:
            if x.get_estado() == 1:
                self.procesos_preparados.append(x)
            elif x.get_estado() == 2:
                self.procesos_suspendidos.append(x)      
                
    def set_tiempos(self, tiempo_max, tiempo_suspendido):
        self.tiempo_max = tiempo_max
        self.tiempo_suspendido = tiempo_suspendido
        self.tiempo_restante = self.tiempo_max
        self.tiempo_suspendido_restante = self.tiempo_suspendido


# Permite abrir una página web para conocer más del proyecto
def conocer_mas():
    webbrowser.open("https://thesteppenwolf.github.io/Proyecto-Sistemas-Operativos-Simulador-de-Procesos/", new=2, autoraise=True)
    
# Permite abrir una página web para mostrar el listado de errores y advertencias
def adverr():
    webbrowser.open("https://github.com/TheSteppenwolf/Proyecto-Sistemas-Operativos-Simulador-de-Procesos/blob/main/Advertencias%20y%20errores.md", new=2, autoraise=True)
    
# Permite la salida del programa
def salir():
    administrador.salir()
    global window
    window.destroy()    



# Muestra los procesos creados en diferentes listas
def mostrar_procesos():
    administrador.to_preparado()
    procesos_lst.delete(0, END)
    procesos_lst.insert('0', *administrador.ver_lista())
    preparado_lst.delete(0, END)    
    preparado_lst.insert('0', *administrador.ver_preparados()[::-1])
    suspendido_lst.delete(0, END)
    suspendido_lst.insert('0', *administrador.ver_suspendidos())    
    
# Muestra el proceso que se encuentra en ejecución
def mostrar_proceso(proceso):
    proceso_ejecutado_txt.delete(0, END)
    proceso_ejecutado_txt.insert('0', proceso)
    mostrar_procesos()
    
# Comienza la ejecución de los procesos
def simulacion_empieza_auto():
    # Control ingreso de tipo de dato al tiempo maximo de procesamiento
    tiempo_max = 0
    while True:
        try:
            tiempo_max = tiempo_max_var.get()
        except:
            advertencias_errores("E01", "tiempo maximo de procesamiento")
        finally:
            break
    # Control ingreso de tipo de dato al tiempo maximo de suspensión
    tiempo_sus = 0
    while True:
        try:
            tiempo_sus = tiempo_suspendido.get()
        except:
            advertencias_errores("E01", "tiempo maximo de suspendido")
        finally:
            break
    # Advertencia si se mantiene el valor por defecto del tiempo máximo de procesamiento
    if tiempo_max == 0:
        advertencias_errores("A01", "tiempo máximo de procesamiento")
    else:
        administrador.set_tiempos(tiempo_max, tiempo_sus)
        administrador.ejecutar_proceso_auto()
        mostrar_procesos()

# Comienza la ejecución de los procesos
def simulacion_empieza():  
    # Control ingreso de tipo de dato al tiempo maximo de procesamiento
    tiempo_max = 0
    while True:
        try:
            tiempo_max = tiempo_max_var.get()
        except:
            advertencias_errores("E01", "tiempo maximo de procesamiento")
        finally:
            break
    # Control ingreso de tipo de dato al tiempo maximo de suspensión
    tiempo_sus = 0
    while True:
        try:
            tiempo_sus = tiempo_suspendido.get()
        except:
            advertencias_errores("E01", "tiempo maximo de suspendido")
        finally:
            break
    # Advertencia si se mantiene el valor por defecto del tiempo máximo de procesamiento
    if tiempo_max == 0:
        advertencias_errores("A01", "tiempo máximo de procesamiento")
    else:
        administrador.set_tiempos(tiempo_max, tiempo_sus)
        administrador.ejecutar_proceso()
        mostrar_procesos()

# Establece el nuevo tiempo restante
def set_tiempos(tiempo_total, tiempo_proceso):
    tiempo_ejecucion_txt2.delete(0, END)
    tiempo_ejecucion_txt2.insert('0', tiempo_total)
    proceso_tiempo_txt.delete(0, END)    
    proceso_tiempo_txt.insert('0', tiempo_proceso)
    
# Reanuda una tarea suspendida
def reanudar():
    administrador.reanudar((int)(suspendido_lst.get(suspendido_lst.curselection()).split()[1]))
    mostrar_procesos()
    
# Finaliza un proceso
def finalizar():
    if suspendido_lst.curselection():
        administrador.matar_proceso((int)(suspendido_lst.get(suspendido_lst.curselection()).split()[1]), 2)
    elif preparado_lst.curselection():
        administrador.matar_proceso((int)(preparado_lst.get(preparado_lst.curselection()).split()[1]), 1)
    mostrar_procesos()



# Función que agrega un nuevo proceso a partir del botón agregar de la subventana avanzado
def agregar_proceso_btn():
    # Control de ingreso del nombre de los procesos
    nombre = nombre_entry.get()
    if nombre == "":
        advertencias_errores("A01", "nombre del proceso")
    # Control de ingreso de la prioridad de los procesos
    prioridad = 0
    while True:
        try:
            prioridad = prioridad_entry.get()
        except:
            advertencias_errores("E01", "prioridad del proceso")
        finally:
            break
    # Control de ingreso del tiempo de ejecución de los procesos
    tiempo_ejecucion = 0
    while True:
        try:
            tiempo_ejecucion = tiempo_ejecucion_entry.get()
        except:
            advertencias_errores("E01", "tiempo de ejecución del proceso")
        finally:
            break        
    administrador.crear_proceso(nombre, tiempo_ejecucion, prioridad)
    mostrar_procesos_avanzada()
    vaciar()
    
# Elimina un proceso ingresado
def eliminar_proceso_btn():
    administrador.eliminar_proceso((int)(procesos_avanzado_lst.get(procesos_avanzado_lst.curselection()).split()[1]))
    mostrar_procesos_avanzada()
    vaciar()
    
# Muestra todos los procesos creados en una lista
def mostrar_procesos_avanzada():
    procesos_avanzado_lst.delete(0, END)
    procesos_avanzado_lst.insert('0', *administrador.ver_lista())
    procesos_acabados_lst.delete(0, END)
    procesos_acabados_lst.insert('0', *administrador.ver_terminados())
    
# Vacia el texto en los textbox de ingreso de datos
def vaciar():
    nombre_txt.delete(0, END)
    tiempo_ejecucion_txt.delete(0, END)
    prioridad_txt.delete(0, END)
    
# Vacia la lista de procesos terminados
def vaciar_lista():
    procesos_acabados_lst.delete(0, END)
    administrador.vaciar()
    
# Inicializa la subventana avanzada
def ini_avanzada(event):
    vaciar()
    mostrar_procesos_avanzada()
    mostrar_procesos()



# Creación del menu del aplicativo
def creacion_menu():    
    menubar = Menu(window)
    window.config(menu=menubar)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Iniciar simulación con reanudación automática", command=simulacion_empieza_auto)
    filemenu.add_command(label="Iniciar simulación con reanudación manual", command=simulacion_empieza)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=salir)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_command(label="Advertencias y Errores", command=adverr)
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...", command=conocer_mas)

    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)



# Creación del GUI
window = tk.Tk()
window.title("Simulador de Procesos")
window.resizable(False, False)

# Variables que almacenan los datos ingresados para los procesos
nombre_entry = tk.StringVar()
tiempo_ejecucion_entry = tk.IntVar()
prioridad_entry = tk.IntVar()
tiempo_max_var = tk.IntVar()
tiempo_suspendido = tk.IntVar()

# Se inicializa el administrador general
administrador = Administrador()

# Creación del menu del aplicativo
creacion_menu()
# Creación de subventanas
tabControl = ttk.Notebook(window)
# Subventana procesos
procesos_tab = ttk.Frame(tabControl)
tabControl.add(procesos_tab, text="Procesos")
# Subventana avanzado
avanzado_tab = ttk.Frame(tabControl)
tabControl.add(avanzado_tab, text="Avanzado")

# Desarrollo en la subventana de procesos
procesos_txt = Label(procesos_tab, text="Procesos")
procesos_lst = Listbox(procesos_tab, width="50", height="20")
tiempo_max_lb = Label(procesos_tab, text="Tiempo máximo")
tiempo_max_txt = Entry(procesos_tab, width="20", textvariable=tiempo_max_var)
tiempo_ejecucion_lb = Label(procesos_tab, text="Tiempo en ejecución")
tiempo_ejecucion_txt2 = Entry(procesos_tab, width="20")
proceso_ejecutado_lb = Label(procesos_tab, text="Proceso en ejecución")
proceso_ejecutado_txt = Entry(procesos_tab, width="20")
proceso_tiempo_lb = Label(procesos_tab, text="Tiempo restante proceso")
proceso_tiempo_txt = Entry(procesos_tab, width="20")
preparado_txt = Label(procesos_tab, text="Preparado")
preparado_lst = Listbox(procesos_tab, width="55", height="20")
suspendido_txt = Label(procesos_tab, text="Suspendido")
suspendido_tiempo_lb = Label(procesos_tab, text="Tiempo suspendido:")
suspendido_tiempo_txt = Entry(procesos_tab, width="10", textvariable=tiempo_suspendido)
suspendido_lst = Listbox(procesos_tab, width="55")
empezar_simulacion = Button(procesos_tab, text="Simulación automática", command=simulacion_empieza_auto)
detener_simulacion = Button(procesos_tab, text="Simulación manual", command=simulacion_empieza)
finalizar_tarea = Button(procesos_tab, text="Finalizar tarea", command=finalizar)
reanudar_tarea = Button(procesos_tab, text="Reanudar tarea", command=reanudar)

# Ubicación de los elementos de la subventana procesos
procesos_txt.grid(column=0, row=0, padx = 5, pady=5, sticky=W)
procesos_lst.grid(column=0, row=1, padx=5, pady=5, sticky=N)
tiempo_max_lb.grid(column=0, row=2, padx=10, pady=5, sticky=W)
tiempo_max_txt.grid(column=0, row=3, padx=5, pady=5, sticky=NW)
tiempo_ejecucion_lb.grid(column=0, row=2, padx=10, pady=5, sticky=E)
tiempo_ejecucion_txt2.grid(column=0, row=3, padx=5, pady=5, sticky=NE)
proceso_ejecutado_lb.grid(column=0, row=3, padx=5, pady=5, sticky=W)
proceso_ejecutado_txt.grid(column=0, row=3, padx=5, pady=5, sticky=E)
proceso_tiempo_lb.grid(column=0, row=3, padx=5, pady=50, sticky=SW)
proceso_tiempo_txt.grid(column=0, row=3, padx=5, pady=50, sticky=SE)
preparado_txt.grid(column=1, row=0, padx = 5, pady=5, sticky=W)
preparado_lst.grid(column=1, row=1, padx=5, pady=5)
suspendido_txt.grid(column=1, row=2, padx = 5, pady=5, sticky=W)
suspendido_tiempo_lb.grid(column=1, row=2, padx=75, pady=5, sticky=E)
suspendido_tiempo_txt.grid(column=1, row=2, padx=5, pady=5, sticky=E)
suspendido_lst.grid(column=1, row=3, padx=5, pady=5)
empezar_simulacion.grid(column=0, row=5, padx=5, pady=5, sticky=W)
detener_simulacion.grid(column=0, row=5, padx=150, pady=5, sticky=W, columnspan=2)
finalizar_tarea.grid(column=1, row=5, padx=5, pady=5, sticky=E)
reanudar_tarea.grid(column=1, row=5, padx=5, pady=5)

# Desarrollo en la subventana de avanzado
procesos_avanzado = Label(avanzado_tab, text="Agregar proceso")
nombre_lb = Label(avanzado_tab, text="Nombre:")
nombre_txt = ttk.Entry(avanzado_tab, width="20", textvariable=nombre_entry)
prioridad_lb = Label(avanzado_tab, text="Prioridad:")
prioridad_txt = ttk.Entry(avanzado_tab, width="20", textvariable=prioridad_entry)
tiempo_ejecucion_lb = Label(avanzado_tab, text="Tiempo ejecución:")
tiempo_ejecucion_txt = ttk.Entry(avanzado_tab, width="20", textvariable=tiempo_ejecucion_entry)
procesos_avanzado_lb = Label(avanzado_tab, text="Todos los procesos")
procesos_avanzado_lst = Listbox(avanzado_tab, width="65", height="20")
agregar_btn = Button(avanzado_tab, text="Agregar proceso", command=agregar_proceso_btn)
eliminar_btn = Button(avanzado_tab, text="Eliminar proceso", command=eliminar_proceso_btn)
texto_lb = Label(avanzado_tab, text="Lista de procesos finalizados")
procesos_acabados_lst = Listbox(avanzado_tab, width="100", height="10")
vaciar_acabados_btn = Button(avanzado_tab, text="Vaciar lista", command=vaciar_lista)

# Ubicación de los elementos de la subventana avanzado
procesos_avanzado.grid(column=0, row=0, padx=5, pady=5, sticky=W, columnspan=2)
nombre_lb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
nombre_txt.grid(column=1, row=1, padx=5, pady=5, sticky=W)
prioridad_lb.grid(column=0, row=2, padx=5, pady=5, sticky=W)
prioridad_txt.grid(column=1, row=2, padx=5, pady=5, sticky=W)
tiempo_ejecucion_lb.grid(column=0, row=3, padx=5, pady=5, sticky=W)
tiempo_ejecucion_txt.grid(column=1, row=3, padx=5, pady=5, sticky=W)
procesos_avanzado_lb.grid(column=2, row=0, padx=5, pady=5, sticky=W)
procesos_avanzado_lst.grid(column=2, row=1, padx=5, pady=5, rowspan=4)
agregar_btn.grid(column=0, row=4, padx=5, pady=5)
eliminar_btn.grid(column=1, row=4, padx=5, pady=5)
texto_lb.grid(column=0, row=5, padx=5, pady=5, columnspan=2)
procesos_acabados_lst.grid(column=0, row=6, padx=5, pady=5, columnspan=3, sticky=S)
vaciar_acabados_btn.grid(column=2, row=7, padx=5, pady=5, sticky=E)


# Using pack to make the control visible inside the GUI
tabControl.pack(expand=1, fill="both")
# Permite generar un evento cuando se seleccione una nueva subventana
tabControl.bind("<<NotebookTabChanged>>", ini_avanzada)
window.mainloop()


