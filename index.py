from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime
import time
import schedule
from docx import Document
import pandas as pd

date = datetime.date.today()
fecha = date.strftime("%d/%m/%y")
month = date.strftime('%m')
Horas = datetime.datetime.now()
hora = Horas.hour
minute = Horas.minute
seconds = Horas.second
numFactura = 0

class Product:

    def __init__(self, window):
        self.wind = window
        self.wind.title('Sistema de inventarios')
        ANCHO = 900
        ALTO = 690
        POSY = 0
        POSX = 230

        anchoAlto = str(ANCHO) + 'x' + str(ALTO)
        posicionX = '+' + str(POSX)
        posicionY = '+' + str(POSY)

        self.wind.geometry(anchoAlto+posicionX+posicionY)
        
        #creacion del frame
        frame = Frame(self.wind, bg='SteelBlue2')
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        #elementos pantalla principal
        Label(frame, text='Sistema de inventario casa linda', bg='SteelBlue2', width=40, font=('Segoe UI', 30)).grid(row=0, column=0, pady=10)

        Label(frame, text='¡Bienvenido!', bg='SteelBlue2', width=20, font=('Segoe UI', 25)).grid(row=1, column=0, pady=5)

        #frame para los botones pantalla principal
        frameBotones = Frame(self.wind, pady=10, bg='SteelBlue2')
        frameBotones.grid(row=2, column=0, columnspan=3, pady=10)

        Button(frameBotones, text='Inventario de maquinas', width=30, pady=30, border=2, bg='SteelBlue3',command=self.Inventario_Maquinas, font=('Segoe UI',13)).grid(row=0, column=0, pady=10, padx=10)
        Button(frameBotones, text='Inventario de insumos', width=30, pady=30, border=2, bg='SteelBlue3', command=self.inventario_herramientas ,font=('Segoe UI',13)).grid(row=0, column=1, pady=10, padx=10)
        Button(frameBotones, text='Inventario de produccion', width=30, pady=30, border=2, bg='SteelBlue3',command=self.Inventario_produccion,font=('Segoe UI',13)).grid(row=2, column=0, pady=10, padx=10)
        Button(frameBotones, text='Productos terminados', width=30, pady=30, bg='SteelBlue3', font=('Segoe UI',13), command=self.Terminados).grid(row=2, column=1, pady=10, padx=10)
        Button(frameBotones, text='Ingresos', width=30, pady=30, bg='SteelBlue3', font=('Segoe UI',13), command=self.Ingresos).grid(row=3, column=0, pady=10, padx=10)
        Button(frameBotones, text='Gastos', width=30, bg='SteelBlue3', pady=30, font=('Segoe UI',13), command=self.Gastos).grid(row=3, column=1, pady=10, padx=10)
        Button(frameBotones, text='Facturas', width=30, command=self.Facturas, bg='SteelBlue3', pady=30, font=('Segoe UI',13)).grid(row=4, column=0)
        Button(frameBotones, text='Historial de ventas', width=30, command=self.Historial, bg='SteelBlue3', pady=30, font=('Segoe UI',13)).grid(row=4, column=1)

    class inventario_herramientas():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=500, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 1620
            ALTO = 830
            POSY = 11
            POSX = 0

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Inventario de Insumos', pady=20, padx=20, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=1)

            #form para registrar productos
            Label(self.top_level, text='Nombre producto', pady=1, bg='SteelBlue2').grid(row=2, column=0)
            self.name = Entry(self.top_level, width=35, name='nombre')
            self.name.grid(row=3, column=0, ipady=4, pady=(0, 20))

            Label(self.top_level, text='Cantidad producto', pady=1, bg='SteelBlue2').grid(row=2, column=1)
            self.cantidad = Entry(self.top_level, width=35, name='cantidad')
            self.cantidad.grid(row=3, column=1, ipady=4, pady=(0, 20))

            Label(self.top_level, text='Precio producto', pady=1, bg='SteelBlue2').grid(row=2, column=2)
            self.precio = Entry(self.top_level, width=35, name='precio')
            self.precio.grid(row=3, column=2, padx=(46,46),ipady=4, pady=(0, 20))

            Label(self.top_level, text='Fecha de ingreso', pady=1, bg='SteelBlue2').grid(row=4, column=0)
            self.ingreso = Entry(self.top_level, width=35, name='ingreso')
            self.ingreso.grid(row=5, column=0, ipady=4)

            Label(self.top_level, text='Fecha de vencimiento', pady=1, bg='SteelBlue2').grid(row=4, column=1)
            self.vencimiento = Entry(self.top_level, width=35, name='vencimiento')
            self.vencimiento.grid(row=5, column=1, ipady=4)

            Label(self.top_level, text='Detalles', pady=1, bg='SteelBlue2').grid(row=4, column=2)
            self.detalles = Entry(self.top_level, width=35, name='detalles')
            self.detalles.grid(row=5, column=2, padx=(46,46),ipady=4)

            self.button = Button(self.top_level, text='Registrar', width=30, height=2, bg='SteelBlue3',command=self.add_product)
            self.button.grid(row=8, column=0, pady=20)

            Label(self.top_level, text='Tus insumos disponibles', font=('Segoe UI', 20), bg='SteelBlue2').grid(row= 12, column=0)

            self.busqueda = Entry(self.top_level, width=35)
            self.busqueda.grid(row=13, column=1, ipady=4)
            Button(self.top_level, text='Buscar insumo', width=20, height=1, bg='SteelBlue3', command=self.Buscador).grid(row=14, column=1, pady=10, ipady=3)

            self.tabla = ttk.Treeview(self.top_level, columns=('price', 'Mount', 'dateAdmission', 'dateExpiration', 'total', 'description', 'id'))
            self.tabla.grid(row=16, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Nombre', anchor=CENTER)
            self.tabla.heading('#1', text='Precio', anchor=CENTER)
            self.tabla.heading('#2', text='Cantidad', anchor=CENTER)
            self.tabla.heading('#3', text='Fecha de ingreso', anchor=CENTER)
            self.tabla.heading('#4', text='Fecha de vencimiento', anchor=CENTER)
            self.tabla.heading('#5', text='Total', anchor=CENTER)
            self.tabla.heading('#6', text='Descripcion', anchor=CENTER)
            self.tabla.heading('#7', text='Id', anchor=CENTER)

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=16, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)

            self.get_products()

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2,command=self.delete_products, bg='SteelBlue3' )
            self.btn_eliminar.grid(row=17, column=0, pady=20)

            self.btn_actualizar = Button(self.top_level, text='Actualizar', width=30, height=2, command=self.Ventana_Actulizar, bg='SteelBlue3')
            self.btn_actualizar.grid(row=17, column=1, pady=20)

            Entry(self.top_level, textvariable=StringVar(self.top_level, self.total), font=20, width=20, justify='center').grid(row=18, column=2, ipady=10)

            Button(self.top_level, text='Informe general', width=30, height=2, bg='SteelBlue3', command=self.InformeGeneral).grid(row=18, column=1)
            Button(self.top_level, text='Informe mensual', width=30, height=2, bg='SteelBlue3', command=self.InformeMensual).grid(row=17, column=2)

            self.total = 0
        
        def Buscador(self):
            total_insumos = []
            query = "SELECT * FROM Productos WHERE Nombre = ?"
            datos = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            query_2 = 'SELECT Total FROM Productos WHERE Nombre = ?'
            precios = self.run_query(query_2, (self.busqueda.get().upper().strip(), ))
            for precio in precios:
                preciototal = int(''.join(map(str, precio)))
                total_insumos.append(preciototal)
            total = sum(total_insumos)
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 'end',text= row[1], values=(row[3], row[2], row[4], row[5], row[7], row[6], row[0]))
            messagebox.showinfo(title='Total', message=f'Total: {"{:,}".format(total)}')

        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result
        
        def InformeGeneral(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Cantidad, Precio, Total, Ingreso, Vencimiento, Detalles FROM Productos', cnx)
            writer = pd.ExcelWriter('Informe general insumos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe general insumos', index=False)
            writer.save()
        
        def InformeMensual(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Cantidad, Precio, Total, Ingreso, Vencimiento, Detalles FROM Productos WHERE substr(Ingreso, 4, 2) = "{0}"'.format(month), cnx)
            writer = pd.ExcelWriter('Informe mensual insumos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe mensual insumos', index=False)
            writer.save()

        def Total_Insumos(self):
            maquinas_precio = []
            query_maquinas = 'SELECT Total FROM Productos'
            total_maquinas = self.run_query(query_maquinas, ( ))
            for total in total_maquinas:
                precio_maquina = int(''.join(map(str, total))) 
                maquinas_precio.append(precio_maquina)
            total_precio_maquina = sum(maquinas_precio)
            formatted_num = "{:,}".format(total_precio_maquina)
            self.total = formatted_num

        def get_products(self):          
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Productos ORDER BY Nombre ASC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 'end',text= row[1], values=(row[3], row[2], row[4], row[5], row[7], row[6], row[0]))
            self.Total_Insumos()

        def validation(self):
            return len(self.name.get()) != 0 and len(self.cantidad.get()) != 0 and len(self.precio.get()) != 0

        def add_product(self):
            if self.validation():
                total = float(self.cantidad.get()) * int(self.precio.get())
                query = 'INSERT INTO productos VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)'
                parameters = (self.name.get().upper().strip(), self.cantidad.get().upper().strip(), self.precio.get().upper().strip(), self.ingreso.get().upper().strip(), self.vencimiento.get().upper().strip(), self.detalles.get().upper().strip(), total)
                self.run_query(query, parameters)
                self.name.delete(0, END)
                self.cantidad.delete(0, END)
                self.precio.delete(0, END)
                self.ingreso.delete(0, END)
                self.vencimiento.delete(0, END)
                self.detalles.delete(0, END)
            else:
                messagebox.showinfo(title='Verificacion', message='No se pueden registrar valores vacios\nSe deben llenar los campos de nombre, cantidad y precio')
            self.get_products()
        
        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            nombre_product = self.tabla.item(self.tabla.selection())['text']
            id = self.tabla.item(self.tabla.selection())['values'][6]
            query = 'DELETE FROM Productos WHERE Nombre = ? AND Id = ?'
            self.run_query(query, (nombre_product, id))
            self.get_products()
        
        def Ventana_Actulizar(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            cantidad = self.tabla.item(self.tabla.selection())['values'][1]
            fechaIngreso = self.tabla.item(self.tabla.selection())['values'][2]
            fechaVencimiento = self.tabla.item(self.tabla.selection())['values'][3]
            description = self.tabla.item(self.tabla.selection())['values'][5]
            
            self.EditProduct = Toplevel()
            self.EditProduct.config(bg='SteelBlue2')
            Label(self.EditProduct, text='Actualizar productos', pady=10, font=('Segoe UI',20), bg='SteelBlue2').grid(column=1, row=1, columnspan=1)

            Label(self.EditProduct, text='Nombre', bg='SteelBlue2').grid(column=0, row=4)
            self.newName = Entry(self.EditProduct, name='name', width=30, textvariable=StringVar(self.EditProduct,value=name))
            self.newName.grid(column=0, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Precio', bg='SteelBlue2').grid(column=1, row=4)
            self.newPrice = Entry(self.EditProduct, name='precio', width=30, textvariable=StringVar(self.EditProduct,value=precio))
            self.newPrice.grid(column=1, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Cantidad', bg='SteelBlue2').grid(column=2, row=4)
            self.newCount= Entry(self.EditProduct, name='cantidad', width=30, textvariable=StringVar(self.EditProduct,value=cantidad))
            self.newCount.grid(column=2, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha ingreso', bg='SteelBlue2').grid(column=0, row=6)
            self.newDateadmission = Entry(self.EditProduct, name='admission', width=30, textvariable=StringVar(self.EditProduct,value=fechaIngreso))
            self.newDateadmission.grid(column=0, row=7, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha vencimiento', bg='SteelBlue2').grid(column=1, row=6)
            self.newDateexpiration = Entry(self.EditProduct, name='expiration', width=30, textvariable=StringVar(self.EditProduct,value=fechaVencimiento))
            self.newDateexpiration.grid(column=1, row=7, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Descripcion', bg='SteelBlue2').grid(column=1, row=8)
            self.newDescription = Entry(self.EditProduct, width=50 ,textvariable=StringVar(self.EditProduct, value=description))
            self.newDescription.grid(column=1, row=9, columnspan=1, padx=20, pady=20, ipadx=10, ipady=5)
            
            Button(self.EditProduct, text='Actualizar', width=20, command= lambda : self.actualizar_producto(name, self.newName.get().upper().strip(),self.newPrice.get().upper().strip(), self.newCount.get().upper().strip(), self.newDateadmission.get().upper().strip(), self.newDateexpiration.get().upper().strip(), self.newDescription.get().upper().strip()), bg='SteelBlue3').grid(column=0, row=10, columnspan=6, ipadx=5, ipady=5, pady=10)

        def actualizar_producto(self, name, newname, newprice, newcount, newadmission, newexpiration, newdescripcion):
            if len(self.newName.get()) != 0 and len(self.newPrice.get()) != 0 and len(self.newCount.get()) != 0:
                total = float(newcount) * int(newprice)
                query = 'UPDATE productos SET Nombre = ?, Cantidad = ?, Precio = ?, Ingreso = ?, Vencimiento = ?, Detalles = ?, Total = ? WHERE Nombre = ?'
                parametros = (newname, newcount, newprice, newadmission, newexpiration, newdescripcion, total, name)
                self.run_query(query, parametros)
                self.EditProduct.destroy()
                self.get_products()
            else:
                messagebox.showerror(title='error', message='No se pueden enviar valores vacios')

    class Inventario_produccion():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=550, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 1220
            ALTO = 750
            POSY = 1
            POSX = 180

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Inventario de produccion', pady=20, padx=20, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=1)

            #form para registrar productos
            Label(self.top_level, text='Nombre producto', pady=1, bg='SteelBlue2').grid(row=2, column=0)
            self.name = Entry(self.top_level, width=35, name='nombre')
            self.name.grid(row=3, column=0, ipady=4)
            
            Label(self.top_level, text='Fecha inicio', bg='SteelBlue2').grid(row=2, column=2)
            self.fecha_inicio = Entry(self.top_level, width=35, name='fecha inicio')
            self.fecha_inicio.grid(row=3, column=2, ipady=4)

            Label(self.top_level, text='Fecha final', pady=1, bg='SteelBlue2').grid(row=4, column=0, pady=(20, 0))
            self.fecha_final = Entry(self.top_level, width=35, name='fecha final')
            self.fecha_final.grid(row=5, column=0, ipady=4)

            Label(self.top_level, text='Cantidad', pady=1, bg='SteelBlue2').grid(row=2, column=1)
            self.cantidad = Entry(self.top_level, width=35, name='cantidad')
            self.cantidad.grid(row=3, column=1, ipady=4)

            self.button = Button(self.top_level, text='Registrar', width=30, height=2, command=self.add_product, bg='SteelBlue3')
            self.button.grid(row=5, column=1)

            Label(self.top_level, text='Tus producciones', font=('Segoe UI', 20), bg='SteelBlue2').grid(row= 10, column=0, pady=(10, 10))

            self.busqueda = Entry(self.top_level, width=35)
            self.busqueda.grid(row=12, column=1, ipady=4)
            Button(self.top_level, text='Buscar produccion', width=20, height=1, bg='SteelBlue3', command=self.Buscador).grid(row=13, column=1, pady=10, ipady=3)

            self.tabla = ttk.Treeview(self.top_level, columns=('price','date','Mount', 'DateInit', 'id'))
            self.tabla.config()
            self.tabla.grid(row=14, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Nombre')
            self.tabla.heading('#1', text='Precio')
            self.tabla.heading('#2', text='Fecha Inicio')
            self.tabla.heading('#3', text='Fecha final')
            self.tabla.heading('#4', text='Cantidad')
            self.tabla.heading('#5', text='Id')

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=14, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2,command=self.delete_products, bg='SteelBlue3')
            self.btn_eliminar.grid(row=15, column=0, pady=20)
            self.btn_actualizar = Button(self.top_level, text='Actualizar', width=30, height=2,command=self.Ventana_Actulizar, bg='SteelBlue3')
            self.btn_actualizar.grid(row=15, column=1, pady=20)
            self.btn_view = Button(self.top_level, text='Ver producto', width=30, height=2,command=self.viewProduct, bg='SteelBlue3')
            self.btn_view.grid(row=15, column=2, pady=20)
            self.btn_terminado = Button(self.top_level, text='Terminado', width=30, height=2, command=self.terminado, bg='SteelBlue3')
            self.btn_terminado.grid(row=16, column=0)
            Button(self.top_level, text='Informe mensual', width=30, height=2, bg='SteelBlue3', command=self.InformeMensual).grid(row=16, column=1)
            Button(self.top_level, text='Informe general', width=30, height=2, bg='SteelBlue3', command=self.InformeGeneral).grid(row=16, column=2)

            self.get_products()
        
        def Buscador(self):
            query = "SELECT * FROM Produccion WHERE Nombre = ?"
            datos = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 0, text= row[0], values=(row[1], row[3], row[4], row[2], row[5]))

        def InformeGeneral(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Precio, Cantidad, FechaInicio, FechaFinal FROM Produccion', cnx)
            writer = pd.ExcelWriter('Informe general produccion.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe general producion', index=False)
            writer.save()
        
        def InformeMensual(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Precio, Cantidad, FechaInicio, FechaFinal FROM Produccion WHERE substr(FechaInicio, 4, 2) = "{0}"'.format(month), cnx)
            writer = pd.ExcelWriter('Informe mensual produccion.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe mensual produccion', index=False)
            writer.save()
            
        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Produccion ORDER BY Nombre DESC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 0, text= row[0], values=(row[1], row[3], row[4], row[2], row[5]))

        def validation(self):
            return len(self.name.get()) != 0 and len(self.cantidad.get()) != 0

        def add_product(self):
            if self.validation():
                query = 'INSERT INTO produccion VALUES(?, ?, ?, ?, ?, NULL)'
                parameters = (self.name.get().upper().strip(), '', self.cantidad.get().upper().strip(), self.fecha_inicio.get().upper().strip(), self.fecha_final.get().upper().strip())
                self.run_query(query, parameters)
                self.name.delete(0, END)
                self.fecha_inicio.delete(0, END)
                self.fecha_final.delete(0, END)
                self.cantidad.delete(0,  END)
            else:
                messagebox.showinfo(title='Verificacion', message='No se pueden registrar valores vacios\nSe deben llenar los campos nombre y cantidad')
            self.get_products()
        
        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            nombre_product = self.tabla.item(self.tabla.selection())['text']
            id = self.tabla.item(self.tabla.selection())['values'][4]
            query = 'DELETE FROM Produccion WHERE Nombre = ? AND Id = ?'
            self.run_query(query, (nombre_product, id))
            delete = 'DELETE FROM VerProducto WHERE Nombre = ? AND IdProducto = ?'
            self.run_query(delete, (nombre_product, id))
            self.get_products()
        
        def Ventana_Actulizar(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            cantidad = self.tabla.item(self.tabla.selection())['values'][3]
            fechaInicio = self.tabla.item(self.tabla.selection())['values'][1]
            FechaFinal = self.tabla.item(self.tabla.selection())['values'][2]
            id = self.tabla.item(self.tabla.selection())['values'][4]

            self.EditProduct = Toplevel()
            self.EditProduct.resizable(0,0)
            self.EditProduct.config(bg='SteelBlue2')
            Label(self.EditProduct, text='Actualizar produccion', pady=20, font=('Segoe UI',20), bg='SteelBlue2').grid(column=1, row=1, columnspan=1) 

            Label(self.EditProduct, text='Nombre', bg='SteelBlue2').grid(column=0, row=2)
            self.newName = Entry(self.EditProduct, name='name', width=30, textvariable=StringVar(self.EditProduct, value=name))
            self.newName.grid(column=0, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Precio', bg='SteelBlue2').grid(column=1, row=2)
            self.newPrice = Entry(self.EditProduct, name='precio', width=30,textvariable=StringVar(self.EditProduct, value=precio))
            self.newPrice.grid(column=1, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Cantidad', bg='SteelBlue2').grid(column=2, row=2)
            self.newCount= Entry(self.EditProduct, name='cantidad', width=30, textvariable=StringVar(self.EditProduct, value=cantidad))
            self.newCount.grid(column=2, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha de inico', bg='SteelBlue2').grid(column=0, row=4)
            self.newDateinit = Entry(self.EditProduct, name='estado', width=30, textvariable=StringVar(self.EditProduct, value=fechaInicio))
            self.newDateinit.grid(column=0, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha final', bg='SteelBlue2').grid(column=1, row=4)
            self.newDatefinit = Entry(self.EditProduct, name='dateFinit', width=30, textvariable=StringVar(self.EditProduct, value=FechaFinal))
            self.newDatefinit.grid(column=1, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Button(self.EditProduct, text='Actualizar', width=20, bg='SteelBlue3',command= lambda : self.actualizar_producto(name, self.newName.get().upper().strip(), self.newPrice.get().upper().strip(), self.newCount.get().upper().strip(), self.newDateinit.get().upper().strip(), self.newDatefinit.get().upper().strip(), id)).grid(column=1, row=7, columnspan=1, ipadx=5, ipady=5, pady=10)

        def actualizar_producto(self, name, newname, newprice, newcount, newdateinit, newdatefinit, id):
            if len(self.newName.get()) != 0 and len(self.newPrice.get()) != 0 and len(self.newCount.get()) != 0:
                query = 'UPDATE produccion SET Nombre = ?, Precio = ?, Cantidad = ?, FechaInicio = ?, FechaFinal = ? WHERE Nombre = ? AND Id = ?'
                parametros = (newname, newprice, newcount, newdateinit, newdatefinit, name, id)
                self.run_query(query, parametros)
                self.EditProduct.destroy()
                self.get_products()
            else:
                messagebox.showerror(title='error', message='No se pueden enviar valores vacios')
            query_delete = 'DELETE FROM Terminado WHERE Nombre = ?'
            self.run_query(query_delete, (name, ))
        
        def terminado(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            cantidad = self.tabla.item(self.tabla.selection())['values'][3]
            fechaInicio = self.tabla.item(self.tabla.selection())['values'][1]
            fechaFinal = self.tabla.item(self.tabla.selection())['values'][2]
            id = self.tabla.item(self.tabla.selection())['values'][4]

            def ProductoTerminado():
                if(int(self.Produccion.get()) < int(self.terminado.get())):
                    messagebox.showinfo(title='Advertencia', message='No hay suficientes unidades de este producto')
                else:
                    if(len(fechaFinal) != 0): 
                            query_cant_product = 'SELECT Cantidad FROM Produccion WHERE Nombre = ? AND Id = ?'
                            consultaCant = self.run_query(query_cant_product, (name, id))
                            for Cant in consultaCant:
                                res = int(''.join(map(str, Cant)))
                                terminados = int(self.terminado.get()) - res
                                positivo = abs(terminados)
                                query_restar = 'UPDATE Produccion SET Cantidad = ? WHERE Nombre = ? AND Id = ?'
                                self.run_query(query_restar, (positivo, name, id))
                                query_update = 'UPDATE Terminado SET Cantidad = ? WHERE FechaIngreso = ? AND Id = ?'
                                self.run_query(query_update, (self.terminado.get(), name, id))
                            query_2 = 'SELECT Gasto FROM VerProducto WHERE Nombre = ? AND IdProducto = ?'
                            query_gasto = self.run_query(query_2, (name, id))
                            listaGasto = []
                            for gasto in query_gasto:
                                res = int(''.join(map(str, gasto)))
                                listaGasto.append(res)
                            GastoTotalProduct = sum(listaGasto)
                            query = 'INSERT INTO Terminado VALUES (?,?,?,?,?,?,?,?,?,NULL)'
                            parametros = (fecha, name, precio, GastoTotalProduct * int(self.terminado.get()), '' , '' , self.terminado.get(), '', '')
                            query_cant_product = 'SELECT Cantidad FROM Produccion WHERE Nombre = ? AND Id = ?'
                            consultaCant = self.run_query(query_cant_product, (name, id))
                            for Cant in consultaCant:
                                res = int(''.join(map(str, Cant)))
                                if(res == 0):
                                    self.run_query('DELETE FROM VerProducto WHERE Nombre = ? AND IdProducto = ?', (name, id))
                                    query_delete = 'DELETE FROM Produccion WHERE Nombre = ? AND Id = ?'
                                    self.run_query(query_delete, (name, id))
                            self.run_query(query, parametros)
                            self.topLevel.destroy()
                            self.get_products()
                
            self.topLevel = Toplevel()
            self.topLevel.config(bg='SteelBlue2')

            Label(self.topLevel, text='Productos terminados', bg='SteelBlue2', font=('Segoe UI', 20)).grid(row=2, column=1, pady=20)

            Label(self.topLevel, text='Nombre', bg='SteelBlue2').grid(row=3, column=0)
            Entry(self.topLevel, textvariable=StringVar(self.topLevel, name), name='name', width=35).grid(row=4, column=0, ipady='5', ipadx='5')

            Label(self.topLevel, text='En produccion', bg='SteelBlue2').grid(row=3, column=1)
            self.Produccion = Entry(self.topLevel, textvariable=StringVar(self.topLevel, cantidad), name='cantidad', width=35)
            self.Produccion.grid(row=4, column=1, ipady='5', ipadx='5')

            Label(self.topLevel, text='Terminados', bg='SteelBlue2').grid(row=3, column=2, padx=5)
            self.terminado = Entry(self.topLevel, name='terminado', width=35)
            self.terminado.grid(row=4, column=2, ipady='5', ipadx='5')

            Button(self.topLevel, text='Producto terminado', command=ProductoTerminado, bg='SteelBlue3').grid(row=10, column=1, ipady=5, ipadx=5, pady=20)

        def viewProduct(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            wind = Toplevel()
            wind.title('Sistema de inventarios')
            wind.resizable(0,0)
            wind.config(bg='SteelBlue2')

            ANCHO = 1200
            ALTO = 630
            POSY = 20
            POSX = 100

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            wind.geometry(anchoAlto+posicionX+posicionY)

            name = self.tabla.item(self.tabla.selection())['text']
            id = self.tabla.item(self.tabla.selection())['values'][4]
            cantidad_producto = self.tabla.item(self.tabla.selection())['values'][3]
            
            def run_query(query, parametrs = {}):
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    result = cursor.execute(query, parametrs)
                    conn.commit()
                return result
                
            def TraerValores():
                query = 'SELECT Nombre FROM Productos'
                consulta = run_query(query, ( ))
                Products = ['PRODUCTOS DISPONIBLES']
                for producto in consulta:
                    pro = ''.join(map(str, producto))
                    Products.append(pro)
                return Products
            
            Label(wind, text='' + name, font=('Segoe UI',20), bg='SteelBlue2').grid(column=1, row=1, columnspan=1, pady=20)

            var = StringVar(self.top_level)
            var.set('Escoja un producto')
            OptionMenu(wind, var, *TraerValores()).grid(row=3, column=0, ipady=4, padx=20)

            Label(wind, text='Insumos gastados', padx=90, bg='SteelBlue2').grid(column=0, row=2)
            insumosgastados = Entry(wind, width=30, textvariable=var)
            insumosgastados.grid(column=1, row=3, ipadx=10, ipady=5)

            Label(wind, text='Cantidad insumos', padx=90, bg='SteelBlue2').grid(column=2, row=2)
            cantidadgastados = Entry(wind, width=30)
            cantidadgastados.grid(column=2, row=3, ipadx=10, ipady=5, pady=20)

            def validation():
                return len(insumosgastados.get()) != 0 and len(cantidadgastados.get()) != 0

            def Gastottotal():
                query_2 = 'SELECT Gasto FROM VerProducto WHERE Nombre = ? AND IdProducto = ?'
                query_gasto = self.run_query(query_2, (name, id))
                listaGasto = []
                for gasto in query_gasto:
                    res = int(''.join(map(str, gasto)))
                    listaGasto.append(res)
                GastoTotalProduct = sum(listaGasto)
                queryPrice = 'UPDATE Produccion SET Precio = ? WHERE Nombre = ? AND Id = ?'
                run_query(queryPrice, (GastoTotalProduct, name, id))
                formatted_num = "{:,}".format(GastoTotalProduct)
                return formatted_num

            def add_product():
                query_2 = 'SELECT Cantidad FROM Productos WHERE Nombre = ?'
                consultaCant = run_query(query_2, (insumosgastados.get().upper(), ))
                for alert in consultaCant:
                    res = float(''.join(map(str, alert)))
                    if(insumosgastados.get().upper() == 'MANO DE OBRA'):
                            query_precio = 'SELECT Precio FROM Productos WHERE Nombre = ?'
                            consultaPrice = run_query(query_precio, (insumosgastados.get()))
                            precio = 0
                            for price in consultaPrice:
                                res = int(''.join(map(str, price)))
                                precio = res
                            gasto = float(cantidadgastados.get()) * int(precio)
                            if validation():
                                query = 'INSERT INTO verproducto VALUES(NULL, ?, ?, ?, ?, ?, ?)'
                                parameters = (insumosgastados.get().upper(), precio, cantidadgastados.get().upper(), gasto, name, id)
                                run_query(query, parameters)
                            get_products()
                    else:
                        condicion =  res - float(cantidadgastados.get())
                        if(condicion >= 0):
                            query_precio = 'SELECT Precio FROM Productos WHERE Nombre = ?'
                            consultaPrice = run_query(query_precio, (insumosgastados.get(), ))
                            precio = 0
                            for price in consultaPrice:
                                res = int(''.join(map(str, price)))
                                precio = res
                            gasto = float(cantidadgastados.get()) * int(precio)
                            if validation():
                                query = 'INSERT INTO verproducto VALUES(NULL, ?, ?, ?, ?, ?, ?)'
                                parameters = (insumosgastados.get().upper(), precio, cantidadgastados.get().upper(), gasto, name, id)
                                run_query(query, parameters)
                                query_2 = 'SELECT Cantidad FROM Productos WHERE Nombre = ?'
                                consultaCant = run_query(query_2, (insumosgastados.get().upper(), ))
                                for cant in consultaCant:
                                    res = float(''.join(map(str, cant)))
                                    NuevaCant = res - float(cantidadgastados.get().upper()) * cantidad_producto
                                    query_update = 'UPDATE Productos SET Cantidad = ? WHERE Nombre = ?'
                                    parametrso = (NuevaCant, insumosgastados.get().upper(), )
                                    run_query(query_update, parametrso)
                                query_total_insumos = 'SELECT Cantidad FROM Productos WHERE Nombre = ?'
                                query_total_insumos_2 = 'SELECT Precio FROM Productos WHERE Nombre = ?'
                                cantidad_inusmo = run_query(query_total_insumos, (insumosgastados.get(), ))
                                precio_insumo = run_query(query_total_insumos_2, (insumosgastados.get(), ))
                                for Cant in cantidad_inusmo:
                                    resCant = float(''.join(map(str, Cant)))
                                    for Price in precio_insumo:
                                        resPrice = int(''.join(map(str, Price)))
                                        total = resCant * resPrice
                                        query_actualizar_total = 'UPDATE Productos SET Total = ? WHERE Nombre = ?'
                                        run_query(query_actualizar_total, (total, insumosgastados.get(), ))
                                insumosgastados.delete(0, END)
                                cantidadgastados.delete(0, END)
                                Gastottotal()
                                get_products()
                        else:
                            messagebox.showerror(message='El producto ' + insumosgastados.get() + ' no tiene unidades suficientes, UNIDADES DISPONIBLES ' + str(res))
                    if(res <= 5):
                        messagebox.showinfo(message='El producto ' + insumosgastados.get().upper() + ' se esta agotando, UNIDADES DISPONIBLES ' + str(res), title='Agotamiento de producto')

            Button(wind, text='Registrar', width=30, height=2, command=add_product, bg='SteelBlue3').grid(column=1, row=4)

            Label(wind, text='Insumos gastados', font=('Segoe UI',20), bg='SteelBlue2').grid(row=5, column=0, pady=10)

            tabla_product = ttk.Treeview(wind, columns=('price','date','Mount', 'id', 'product'))
            tabla_product.config()
            tabla_product.grid(row=6, column=0, columnspan=3, pady=20)
            tabla_product.heading('#0', text='Insumos Gastados')
            tabla_product.heading('#1', text='Precio de insumos')
            tabla_product.heading('#2', text='Cantidad de insumos')
            tabla_product.heading('#3', text='Gasto total')
            tabla_product.heading('#4', text='Id insumo')
            tabla_product.heading('#5', text='Id producto')

            scrooll_ver = ttk.Scrollbar(wind, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=6, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)
            
            def get_products():
                #borrar todos los elementos antes de posicionar los nuevamente
                records = tabla_product.get_children()
                for element in records:
                    tabla_product.delete(element)
                #listar los elementos en la tabla de la base de datos
                query = 'SELECT * FROM VerProducto WHERE Nombre = ? AND IdProducto = ?'
                parametros = (name, id)
                db_results = run_query(query, parametros)
                for row in db_results:
                    tabla_product.insert('', 0, text= row[1], values=(row[2], row[3], row[4], row[0], row[6]))
                Gastottotal()
                TraerValores()

            def delete_products():
                try:
                    tabla_product.item(tabla_product.selection())['values'][3]
                except IndexError:
                    messagebox.showerror(message='Selecciona un producto para eliminar')

                id_product = tabla_product.item(tabla_product.selection())['values'][3]
                cant_product = tabla_product.item(tabla_product.selection())['values'][1]
                name_product = tabla_product.item(tabla_product.selection())['text']

                if(name_product == 'MANO DE OBRA'):
                    query = 'DELETE FROM VerProducto WHERE Id = ?'
                    run_query(query, (id_product, ))
                    get_products()
                else:
                    query_2 = 'SELECT Cantidad FROM Productos WHERE Nombre = ?'
                    consultaCant = run_query(query_2, (name_product, ))
                    for cant in consultaCant:
                        res = float(''.join(map(str, cant)))
                        NuevaCant = 0
                        NuevaCant = res + float(cant_product)
                        query_update = 'UPDATE Productos SET Cantidad = ? WHERE Nombre = ?'
                        parametrso = (NuevaCant, name_product)
                        run_query(query_update, parametrso)
                    query_total_insumos = 'SELECT Cantidad FROM Productos WHERE Nombre = ?'
                    query_total_insumos_2 = 'SELECT Precio FROM Productos WHERE Nombre = ?'
                    cantidad_inusmo = run_query(query_total_insumos, (name_product, ))
                    precio_insumo = run_query(query_total_insumos_2, (name_product, ))
                    for Cant in cantidad_inusmo:
                        resCant = float(''.join(map(str, Cant)))
                    for Price in precio_insumo:
                        resPrice = int(''.join(map(str, Price)))
                        total = resCant * resPrice
                        query_actualizar_total = 'UPDATE Productos SET Total = ? WHERE Nombre = ?'
                        run_query(query_actualizar_total, (total, name_product))
                    query = 'DELETE FROM VerProducto WHERE Id = ?'
                    run_query(query, (id_product, ))
                    get_products()

            Button(wind, text='Eliminar', width=30, height=2, command=delete_products, bg='SteelBlue3').grid(row=7, column=1, pady=20)

            Entry(wind, textvariable=IntVar(wind, Gastottotal()), width=20, font=1, justify='center').grid(row=7, column=2, ipady='10')
            
            get_products()

    class Inventario_Maquinas():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=650, height=580, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 1420
            ALTO = 720
            POSY = 10
            POSX = 170

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Inventario de maquinaria', pady=20, padx=20, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=1)

            #form para registrar productos
            Label(self.top_level, text='Nombre maquina', pady=1, bg='SteelBlue2').grid(row=2, column=0, pady=7)
            self.name = Entry(self.top_level, width=35)
            self.name.grid(row=3, column=0, ipady=4)

            Label(self.top_level, text='Precio', pady=1, bg='SteelBlue2').grid(row=2, column=1)
            self.precio = Entry(self.top_level, width=35, name='precio')
            self.precio.grid(row=3, column=1, ipady=4)

            Label(self.top_level, text='Cantidad', pady=1, bg='SteelBlue2').grid(row=2, column=2)
            self.cantidad = Entry(self.top_level, width=35, name='cantidad')
            self.cantidad.grid(row=3, column=2, ipady=4)

            Label(self.top_level, text='Estado', pady=1, bg='SteelBlue2').grid(row=5, column=0, pady=7)
            self.estado = Entry(self.top_level, width=35, name='estado')
            self.estado.grid(row=6, column=0, ipady=4)

            Label(self.top_level, text='Detalles de la maquina', pady=1, bg='SteelBlue2').grid(row=5, column=1)
            self.description = Entry(self.top_level, width=35, name='detalles')
            self.description.grid(row=6, column=1, ipady=4)

            self.button = Button(self.top_level, text='Registrar', width=30, height=2,command=self.add_product, bg='SteelBlue3')
            self.button.grid(row=6, column=2)

            self.busqueda = Entry(self.top_level, width=35)
            self.busqueda.grid(row=12, column=1, ipady=4)
            Button(self.top_level, text='Buscar maquina', width=20, height=1, bg='SteelBlue3', command=self.Buscador).grid(row=13, column=1, pady=10, ipady=3)

            Label(self.top_level, text='Tus maquinas', font=('Segoe UI', 20), bg='SteelBlue2').grid(row= 10, column=0, pady=(0, 10))

            self.tabla = ttk.Treeview(self.top_level, columns=('price', 'state', 'mount', 'description', 'total', 'id'))
            self.tabla.grid(row=14, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Nombre')
            self.tabla.heading('#1', text='Precio')
            self.tabla.heading('#2', text='Cantidad')
            self.tabla.heading('#3', text='Estado')
            self.tabla.heading('#4', text='Total')
            self.tabla.heading('#5', text='Detalles')
            self.tabla.heading('#6', text='Id')

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=14, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2,command=self.delete_products, bg='SteelBlue3')
            self.btn_eliminar.grid(row=15, column=0, pady=5)

            self.btn_actualiza = Button(self.top_level, text='Actualizar', width=30, height=2,command=self.Ventana_Actulizar, bg='SteelBlue3')
            self.btn_actualiza.grid(row=15, column=1, pady=5)

            self.total = Entry(self.top_level, width=20, font=1, textvariable=IntVar(self.top_level, self.Total_Maquinas()), justify='center')
            self.total.grid(row=15, column=2, ipady=10)

            Button(self.top_level, text='Informe general', bg='SteelBlue3', width=30, height=2, command=self.InformeGeneral).grid(row=16, column=1)

            self.get_products()

        def Buscador(self):
            precios_maquinas = []
            query = "SELECT * FROM Maquinas WHERE Nombre = ?"
            datos = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            query = 'SELECT Total FROM Maquinas WHERE Nombre = ?'
            precios = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            for precio in precios:
                precio_maquina = int(''.join(map(str, precio)))
                precios_maquinas.append(precio_maquina)
            total_maquinas = sum(precios_maquinas)
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 0, text= row[0], values=(row[1], row[3], row[2], row[5], row[4], row[6]))
            messagebox.showwarning(title='Total', message=f'Total: {"{:,}".format(total_maquinas)}')

        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result
        
        def InformeGeneral(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Precio, Estado, Cantidad, Descripcion, Total FROM Maquinas', cnx)
            writer = pd.ExcelWriter('Informe general maquinas.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe general maquinas', index=False)
            writer.save()

        def Total_Maquinas(self):
            maquinas_precio = []
            query_maquinas = 'SELECT Total FROM Maquinas'
            total_maquinas = self.run_query(query_maquinas, ( ))
            for total in total_maquinas:
                precio_maquina = int(''.join(map(str, total))) 
                maquinas_precio.append(precio_maquina)
            total_precio_maquina = sum(maquinas_precio)
            formatted_num = "{:,}".format(total_precio_maquina) 
            return formatted_num
        
        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Maquinas ORDER BY Nombre DESC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 0,text= row[0], values=(row[1], row[3], row[2], row[5], row[4], row[6]))
        
        def validation(self):
            return len(self.name.get()) != 0 and len(self.precio.get()) != 0 and len(self.cantidad.get()) != 0

        def add_product(self):
            if self.validation():
                total = int(self.cantidad.get()) * int(self.precio.get())
                query = 'INSERT INTO maquinas VALUES(?, ?, ?, ?, ?, ?, NULL)'
                parameters = (self.name.get().upper().strip(), self.precio.get().upper().strip(), self.estado.get().upper().strip(), self.cantidad.get().upper().strip(), self.description.get().upper().strip(), total)
                self.run_query(query, parameters)
                self.name.delete(0, END)
                self.precio.delete(0, END)
                self.estado.delete(0, END)
                self.cantidad.delete(0, END)
                self.description.delete(0, END)
            else:
                messagebox.showinfo(title='Verificacion', message='No se pueden registrar valores vacios\nSe deben llenar los campos de nombre, cantidad y precio')
            self.get_products()
            self.Total_Maquinas()

        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            id = self.tabla.item(self.tabla.selection())['values'][5]
            query = 'DELETE FROM Maquinas WHERE Id = ?'
            self.run_query(query, (id, ))
            self.get_products()

        def Ventana_Actulizar(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            cantidad = self.tabla.item(self.tabla.selection())['values'][1]
            estado = self.tabla.item(self.tabla.selection())['values'][2]
            description = self.tabla.item(self.tabla.selection())['values'][4]
            id = self.tabla.item(self.tabla.selection())['values'][5]

            self.EditProduct = Toplevel()
            self.EditProduct.config(bg='SteelBlue2')
            Label(self.EditProduct, text='Actualizar maquinas', pady=20, font=('Segoe UI',20), bg='SteelBlue2').grid(column=0, row=1, columnspan=2)

            Label(self.EditProduct, text='Nombre actual', bg='SteelBlue2').grid(column=0, row=2)
            self.newName = Entry(self.EditProduct, name='name', textvariable=StringVar(self.EditProduct, value=name))
            self.newName.grid(column=0, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Precio actual', bg='SteelBlue2').grid(column=1, row=2)
            self.newPrice = Entry(self.EditProduct, name='price',textvariable=StringVar(self.EditProduct, value=precio))
            self.newPrice.grid(column=1, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Cantidad actual', bg='SteelBlue2').grid(column=0, row=4)
            self.newCount = Entry(self.EditProduct, name='mount', textvariable=StringVar(self.EditProduct, value=cantidad))
            self.newCount.grid(column=0, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Estado actual', bg='SteelBlue2').grid(column=1, row=4)
            self.newState = Entry(self.EditProduct, name='state',textvariable=StringVar(self.EditProduct, value=estado))
            self.newState.grid(column=1, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Descripcion', bg='SteelBlue2').grid(column=0, row=6)
            self.newDescription = Entry(self.EditProduct, width=50 ,textvariable=StringVar(self.EditProduct, value=description))
            self.newDescription.grid(column=0, row=7, columnspan=2, padx=20, pady=20, ipadx=10, ipady=5)

            Button(self.EditProduct, text='Actualizar', width=20, command= lambda : self.actualizar_producto(id, self.newName.get().upper(),self.newPrice.get().upper(), self.newCount.get().upper(), self.newState.get().upper(), self.newDescription.get().upper()), bg='SteelBlue3').grid(column=0, row=8, columnspan=2, ipadx=5, ipady=5, pady=10)

        def actualizar_producto(self, newname, newprice, newcount, newstate, newdescripcion, id):
            if len(self.newName.get()) != 0 and len(self.newPrice.get()) != 0 and len(self.newCount.get()) != 0 and len(self.newState.get()) != 0:
                """ print(id, newprice, newstate, newcount, newdescripcion) """
                Total_maq = int(newstate) * int(newcount)
                query = 'UPDATE maquinas SET Nombre = ?, Precio = ?, Estado = ?, Cantidad = ?, Descripcion = ?, Total = ? WHERE Id = ?'
                parametros = (newprice, newcount, newdescripcion, newstate, id, Total_maq, newname)
                self.run_query(query, parametros)
                self.EditProduct.destroy()
                self.get_products()
            else:
                messagebox.showerror(title='error', message='No se pueden enviar valores vacios')

    class Ingresos():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=500, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 1220
            ALTO = 730
            POSY = 30
            POSX = 90

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)
            self.top_level.geometry(anchoAlto+posicionX+posicionY)
            
            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Ingresos', pady=20, padx=20, width=30, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=0, columnspan=3)
                    
            Label(self.top_level, text='Producto', bg='SteelBlue2').grid(row=2, column=0)
            self.var = StringVar(self.top_level)
            self.var.set('Escoja una opcion')
            OptionMenu(self.top_level, self.var, *self.TraerValores()).grid(row=3, column=0, ipady=4, padx=5)

            Label(self.top_level, text='Cantidad', bg='SteelBlue2').grid(row=2, column=1)
            self.cantidad = Entry(self.top_level, width=35,name='cantidad')
            self.cantidad.grid(row=3, column=1, ipady=4)

            Label(self.top_level, text='Id producto', bg='SteelBlue2').grid(row=2, column=2)
            self.id_product = Entry(self.top_level, width=35, name='id')
            self.id_product.grid(row=3, column=2, ipady=4)

            self.button = Button(self.top_level, text='Registrar', width=30, height=2, command=self.add_product, bg='SteelBlue3')
            self.button.grid(row=4, column=1, pady=10)

            Label(self.top_level, text='Tus ingresos', font=('Segoe UI', 20), bg='SteelBlue2').grid(row= 8, column=0)

            self.busqueda = Entry(self.top_level, width=35)
            self.busqueda.grid(row=9, column=1, ipady=4)
            Button(self.top_level, text='Buscar ingreso', width=20, height=1, bg='SteelBlue3', command=self.Buscador).grid(row=10, column=1, pady=10, ipady=3)

            self.tabla = ttk.Treeview(self.top_level, columns=('Date', 'valorUnit', 'Valortoal', 'Mount', 'id'))
            self.tabla.grid(row=11, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Nombre', anchor=CENTER)
            self.tabla.heading('#1', text='Fecha ingreso', anchor=CENTER)
            self.tabla.heading('#2', text='Cantidad', anchor=CENTER)
            self.tabla.heading('#3', text='Valor unitario', anchor=CENTER)
            self.tabla.heading('#4', text='Valor total', anchor=CENTER)
            self.tabla.heading('#5', text='Id', anchor=CENTER)

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=11, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)

            self.get_products()

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2, command=self.delete_products, bg='SteelBlue3')
            self.btn_eliminar.grid(row=12, column=0, pady=20)
            Entry(self.top_level, textvariable=IntVar(self.top_level,self.CalValorTotal()), width=20, font=1, justify='center').grid(row=12, column=2, ipady=10)
            Button(self.top_level, text='Informe mensual', bg='SteelBlue3', width=30, height=2, command=self.InformeMensual).grid(row=12, column=1)
            Button(self.top_level, text='Informe general', bg='SteelBlue3', width=30, height=2, command=self.InformeGeneral).grid(row=13, column=1)
        
        def Buscador(self):
            ingresos = []
            query = "SELECT * FROM Ingresos WHERE Nombre = ?"
            datos = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            query = 'SELECT Total FROM Ingresos WHERE Nombre = ?'
            precios = self.run_query(query, (self.busqueda.get().upper().strip(), ))
            for precio in precios:
                precio_maquina = int(''.join(map(str, precio)))
                ingresos.append(precio_maquina)
            sum_ingreso = sum(ingresos)
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 'end', text= row[0], values=(row[5], row[1], row[2], row[3], row[4]))
            messagebox.showinfo(title='Total', message=f'Total: {"{:,}".format(sum_ingreso)}')

        def CalValorTotal(self):
            query_total = 'SELECT Total FROM Ingresos'
            ValorTotal = self.run_query(query_total, ( ))
            Valores = []
            for Total in ValorTotal:
                res = int(''.join(map(str, Total)))
                Valores.append(res)
            resultado = sum(Valores)
            formatted_num = "{:,}".format(resultado)
            return formatted_num
        
        def TraerValores(self):
                query = 'SELECT Nombre FROM Terminado'
                consulta = self.run_query(query, ())
                Products = ['PRODUCTOS TERMINADOS']
                for producto in consulta:
                    pro = ''.join(map(str, producto))
                    Products.append(pro)
                return Products

        def TraerValorUnitario(self):
            query_valorUnit = 'SELECT ValorMercado FROM Terminado WHERE Nombre = ? AND Id = ?'
            ValorUni = self.run_query(query_valorUnit, (self.var.get().upper(), self.id_product.get()))
            valorUnitario = 0
            for ValorUnidad in ValorUni:
                res = int(''.join(map(str, ValorUnidad)))
                valorUnitario = res
            return valorUnitario

        def TraerCantidad(self):
            query_valorUnit = 'SELECT Cantidad FROM Terminado WHERE Nombre = ? AND Id = ?'
            ValorUni = self.run_query(query_valorUnit, (self.var.get().upper(), self.id_product.get()))
            valorUnitario = 0
            for ValorUnidad in ValorUni:
                res = int(''.join(map(str, ValorUnidad)))
                valorUnitario = res
            return valorUnitario
        
        def InformeGeneral(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Cantidad, ValorUnitario, Total, FechaIngreso FROM Ingresos', cnx)
            writer = pd.ExcelWriter('Informe general ingresos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe general ingresos', index=False)
            writer.save()
        
        def InformeMensual(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT Nombre, Cantidad, ValorUnitario, Total, FechaIngreso FROM Ingresos WHERE substr(FechaIngreso, 4, 2) = "{0}"'.format(month), cnx)
            writer = pd.ExcelWriter('Informe mensual ingresos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe mensual ingresos', index=False)
            writer.save()

        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Ingresos ORDER BY Nombre ASC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 'end', text= row[0], values=(row[5], row[1], row[2], row[3], row[4]))
            self.CalValorTotal()
            self.TraerValores()

        def validation(self):
            return len(self.var.get()) != 0 and len(self.cantidad.get()) != 0 and len(self.id_product.get()) != 0
        
        def add_product(self):
            query_cant = 'SELECT Cantidad FROM Terminado WHERE Nombre = ? AND Id = ?'
            consultaCant = self.run_query(query_cant, (self.var.get().upper(), self.id_product.get().strip()))
            for Cant in consultaCant:
                res = int(''.join(map(str, Cant)))
                consumo = res - int(self.cantidad.get())
                if(int(self.cantidad.get()) > res):
                    messagebox.showinfo(title='Sin unidades', message='Solo quedan, ' + str(res) + ' unidades de este producto, se deben producir mas')
                else:
                    queryupdate = 'UPDATE Terminado SET Cantidad = ? WHERE Nombre = ? AND Id = ?'
                    self.run_query(queryupdate, (consumo, self.var.get(), self.id_product.get().strip()))
                    ingreso = int(self.cantidad.get()) * int(self.TraerValorUnitario())
                    if self.validation():
                        query = 'INSERT INTO Ingresos VALUES(?, ?, ?, ?, NULL, ?)'
                        parameters = (self.var.get().upper(), self.cantidad.get(), self.TraerValorUnitario(), ingreso, fecha)
                        self.run_query(query, parameters)
                        self.get_products()
                        queryCant = 'SELECT Cantidad FROM Terminado WHERE Nombre = ? AND Id = ?'
                        consulta = self.run_query(queryCant, (self.var.get(), self.id_product.get().strip()))
                        for cantidad in consulta:
                            res = int(''.join(map(str, cantidad)))
                            if(res == 0):
                                query_delete = 'DELETE FROM Terminado WHERE Nombre = ? AND Id = ?'
                                self.run_query(query_delete, (self.var.get(), self.id_product.get().strip()))
                    else:
                        messagebox.showinfo(title='Verificacion', message='No se pueden registrar valores vacios\nSe deben llenar los campos nombre, cantidad e id')
                    self.get_products()
                    self.cantidad.delete(0, END)
                    self.id_product.delete(0, END)

        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            fecha_product = self.tabla.item(self.tabla.selection())['values'][4]
            query = 'DELETE FROM Ingresos WHERE Id = ?'
            self.run_query(query, (fecha_product, ))
            self.get_products()

    class Gastos():
        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 820
            ALTO = 730
            POSY = 10
            POSX = 280

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Gastos',pady=20, padx=20, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=0, columnspan=4)

            #form para registrar productos
            Label(self.top_level, text='Valor gasto', pady=1, bg='SteelBlue2').grid(row=2, column=0)
            self.valor = Entry(self.top_level, width=35, name='nombre')
            self.valor.grid(row=3, column=0, ipady=4, padx=20)

            Label(self.top_level, text='Fecha gasto', pady=1, bg='SteelBlue2').grid(row=2, column=1)
            self.fecha = Entry(self.top_level, width=35, name='fecha')
            self.fecha.grid(row=3, column=1, ipady=4)

            Label(self.top_level, text='Tipo de gasto', pady=1, bg='SteelBlue2').grid(row=2, column=2)
            opciones = ['Pago de servicios publicos', 'Gastos varios']
            self.var = StringVar(self.top_level)
            self.var.set('Escoja una opcion')
            OptionMenu(self.top_level, self.var, *opciones).grid(row=3, column=2, ipady=4, padx=20)

            Label(self.top_level, text='Detalles del gasto', pady=1, bg='SteelBlue2').grid(row=5, column=0)
            self.detalle = Entry(self.top_level, width=35, name='detalle')
            self.detalle.grid(row=6, column=0, ipady=4)

            self.button = Button(self.top_level, text='Registrar', width=30, height=2,command=self.add_product, bg='SteelBlue3')
            self.button.grid(row=6, column=1)

            Label(self.top_level, text='Tus Gastos', font=('Segoe UI', 20), bg='SteelBlue2').grid(row= 8, column=0)

            opciones = ['Pago de servicios publicos', 'Gastos varios']
            self.busqueda = StringVar(self.top_level)
            self.busqueda.set('Escoja una opcion')
            OptionMenu(self.top_level, self.busqueda, *opciones).grid(row=9, column=1, ipady=4, padx=20)

            Button(self.top_level, text='Buscar gasto', width=20, height=1, bg='SteelBlue3', command=self.Buscador).grid(row=10, column=1, pady=10, ipady=3)

            self.tabla = ttk.Treeview(self.top_level, columns=('Date', 'type', 'details'))
            self.tabla.grid(row=11, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Valor', anchor=CENTER)
            self.tabla.heading('#1', text='Fecha', anchor=CENTER)
            self.tabla.heading('#2', text='Tipo de gasto', anchor=CENTER)
            self.tabla.heading('#3', text='Detalle gasto', anchor=CENTER)

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=11, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2, command=self.delete_products, bg='SteelBlue3')
            self.btn_eliminar.grid(row=12, column=0, pady=20)
            self.btn_eliminar = Button(self.top_level, text='Actualizar', width=30, height=2, command=self.Ventana_Actulizar, bg='SteelBlue3')
            self.btn_eliminar.grid(row=12, column=1, pady=20)
            Entry(self.top_level, textvariable=IntVar(self.top_level, self.CalValorTotal()), width=20, font=1, justify='center').grid(row=13, column=2, ipady=10)
            Button(self.top_level, text='Informe mensual', bg='Steelblue3', width=30, height=2,command=self.InformeMensual).grid(row=12, column=2)
            Button(self.top_level, text='Informe general', bg='Steelblue3', width=30, height=2, command=self.InformeGeneral).grid(row=13, column=1)

            self.get_products()
        
        def Buscador(self):
            query = "SELECT * FROM Gastos WHERE Tipo = ?"
            datos = self.run_query(query, (self.busqueda.get().upper(), ))
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 'end', text= row[0], values=(row[2], row[1], row[3]))

        def CalValorTotal(self):
            query = 'SELECT Valor FROM Gastos'
            consulta = self.run_query(query, ( ))
            Valores = []
            for gasto in consulta:
                res = int(''.join(map(str, gasto)))
                Valores.append(res)
            resultado = sum(Valores)
            formatted_num = "{:,}".format(resultado)
            return formatted_num

        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Gastos ORDER BY Valor ASC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 'end', text= row[0], values=(row[2], row[1], row[3]))

        def validation(self):
            return len(self.valor.get()) != 0 and len(self.fecha.get()) != 0

        def add_product(self):
            if self.validation():
                query = 'INSERT INTO Gastos VALUES(?, ?, ?, ?)'
                parameters = (self.valor.get().upper(), self.var.get().upper(), self.fecha.get().upper(), self.detalle.get().upper())
                self.run_query(query, parameters)
                self.valor.delete(0, END)
                self.fecha.delete(0, END)
                self.detalle.delete(0, END)
            else:
                messagebox.showinfo(title='Verificacion', message='No se pueden registrar valores vacios\nSe deben llenar los campos tipo de gasto, valor y fecha')
            self.get_products()
        
        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            nombre_product = self.tabla.item(self.tabla.selection())['text']
            query = 'DELETE FROM Gastos WHERE Valor = ?'
            self.run_query(query, (nombre_product, ))
            self.get_products()
        
        def InformeGeneral(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT * FROM Gastos', cnx)
            writer = pd.ExcelWriter('Informe general gastos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe general gastos', index=False)
            writer.save()
        
        def InformeMensual(self):
            cnx = sqlite3.connect('Database.db')
            df = pd.read_sql('SELECT * FROM Gastos WHERE substr(Fecha, 4, 2) = "{0}"'.format(month), cnx)
            writer = pd.ExcelWriter('Informe mensual gastos.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Informe mensual gastos', index=False)
            writer.save()

        def Ventana_Actulizar(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            details = self.tabla.item(self.tabla.selection())['values'][2]

            self.EditProduct = Toplevel()
            self.EditProduct.config(bg='SteelBlue2')
            Label(self.EditProduct, text='Actualizar Gastos', pady=15, font=('Segoe UI',20), bg='SteelBlue2').grid(column=0, row=1, columnspan=2)

            Label(self.EditProduct, text='Nombre gasto', bg='SteelBlue2').grid(column=0, row=2)
            self.newName = Entry(self.EditProduct, textvariable=StringVar(self.EditProduct, value=name))
            self.newName.grid(column=0, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha actual', bg='SteelBlue2').grid(column=1, row=2)
            self.newPrice = Entry(self.EditProduct, textvariable=StringVar(self.EditProduct, value=precio))
            self.newPrice.grid(column=1, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Tipo de gasto', pady=1, bg='SteelBlue2').grid(row=4, column=1)
            opciones = ['Compra de insumos', 'Pago de servicios publicos', 'Gastos varios']
            var = StringVar(self.top_level)
            var.set('Escoja una opcion')
            OptionMenu(self.EditProduct, var, *opciones).grid(row=5, column=1, ipady=4, padx=20)

            Label(self.EditProduct, text='Tipo de gasto', bg='SteelBlue2').grid(column=0, row=4)
            self.newCount = Entry(self.EditProduct, textvariable=var)
            self.newCount.grid(column=0, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Detalles', bg='SteelBlue2').grid(column=0, row=6)
            self.details = Entry(self.EditProduct, textvariable=StringVar(self.EditProduct, value=details))
            self.details.grid(column=0, row=7, padx=20, pady=20, ipadx=10, ipady=5)            

            Button(self.EditProduct, text='Actualizar', bg='SteelBlue3', width=20, command= lambda : self.actualizar_producto(precio, self.newName.get().upper(), self.newPrice.get().upper(), self.newCount.get().upper(), self.details.get().upper())).grid(column=0, row=8, columnspan=2, ipadx=5, ipady=5, pady=10)

        def actualizar_producto(self, price, newname, newprice, newDate, details):
            if len(self.newName.get()) != 0 and len(self.newPrice.get()) != 0 and len(self.newCount.get()) != 0:
                query = 'UPDATE Gastos SET Valor = ?, Tipo = ?, Fecha = ?, Detalle = ? WHERE Fecha = ?'
                parametros = (newname, newDate, newprice, details, price)
                self.run_query(query, parametros)
                self.EditProduct.destroy()
                self.get_products()
            else:
                messagebox.showerror(title='error', message='No se pueden enviar valores vacios')

    class Terminados():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=500, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 2020
            ALTO = 440
            POSY = 80
            POSX = 0

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()

        def widgets_ventana2(self):

            #titulo de la ventana
            Label(self.top_level, text='Productos terminados',pady=20, padx=20, font=('Segoe UI',20), bg='SteelBlue2').grid(row=0, column=0, columnspan=4)

            self.tabla = ttk.Treeview(self.top_level, columns=('Date', 'type', 'mercado', 'costototal', 'valormargen','ganancias','unidad', 'margen', 'id'))
            self.tabla.grid(row=9, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Fecha de ingreso', anchor=CENTER)
            self.tabla.heading('#1', text='Nombre', anchor=CENTER)
            self.tabla.heading('#2', text='Costo unitario', anchor=CENTER)
            self.tabla.heading('#3', text='Cantidad', anchor=CENTER)
            self.tabla.heading('#4', text='Costo total', anchor=CENTER)
            self.tabla.heading('#5', text='Margen', anchor=CENTER)
            self.tabla.heading('#6', text='Valor Margen', anchor=CENTER)
            self.tabla.heading('#7', text='Valor mercado', anchor=CENTER)
            self.tabla.heading('#8', text='Ganancias', anchor=CENTER)
            self.tabla.heading('#9', text='Id Producto', anchor=CENTER)

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=9, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)
            
            self.get_products()

            self.btn_eliminar = Button(self.top_level, text='Eliminar', width=30, height=2, command=self.delete_products, bg='SteelBlue3')
            self.btn_eliminar.grid(row=12, column=0, pady=20)

            self.btn_actualizar = Button(self.top_level, text='Añadir margen', width=30, height=2, command=self.Ventana_Actulizar, bg='SteelBlue3')
            self.btn_actualizar.grid(row=12, column=1, pady=20)

        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Terminado ORDER BY Nombre ASC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 'end', text= row[0], values=(row[1], row[2], row[6], row[3], row[7], row[8], row[4], row[5], row[9]))
                
        def delete_products(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para eliminar')
            nombre_product = self.tabla.item(self.tabla.selection())['values'][8]
            query = 'DELETE FROM Terminado WHERE Id = ?'
            self.run_query(query, (nombre_product, ))
            self.get_products()
        
        def Ventana_Actulizar(self):
            try:
                self.tabla.item(self.tabla.selection())['text'][0]
            except IndexError:
                messagebox.showerror(message='Selecciona un producto para actualizar')
                return

            name = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            cantidad = self.tabla.item(self.tabla.selection())['values'][1]
            fechaIngreso = self.tabla.item(self.tabla.selection())['values'][2]
            fechaVencimiento = self.tabla.item(self.tabla.selection())['values'][4]
            description = self.tabla.item(self.tabla.selection())['values'][3]
            id = self.tabla.item(self.tabla.selection())['values'][8]

            self.EditProduct = Toplevel()
            self.EditProduct.config(bg='SteelBlue2')
            Label(self.EditProduct, text='Actualizar productos', font=('Segoe UI',20), bg='SteelBlue2').grid(column=1, row=1, columnspan=5)

            Label(self.EditProduct, text='Nombre', bg='SteelBlue2').grid(column=3, row=2)
            self.newName = Entry(self.EditProduct, name='name', textvariable=StringVar(self.top_level, value=precio))
            self.newName.grid(column=4, row=2, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Costo unitario', bg='SteelBlue2').grid(column=3, row=3)
            self.newCostoUni = Entry(self.EditProduct, name='precio', textvariable=StringVar(self.top_level, value=cantidad))
            self.newCostoUni.grid(column=4, row=3, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Cantidad', bg='SteelBlue2').grid(column=3, row=4)
            self.newCantidad= Entry(self.EditProduct, name='cantidad', textvariable=StringVar(self.top_level, value=fechaIngreso))
            self.newCantidad.grid(column=4, row=4, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Fecha de ingreso', bg='SteelBlue2').grid(column=3, row=5)
            self.newDateadmission = Entry(self.EditProduct, name='admission', textvariable=StringVar(self.top_level, value=name))
            self.newDateadmission.grid(column=4, row=5, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Costo total', bg='SteelBlue2').grid(column=3, row=6)
            self.newCostoTotal = Entry(self.EditProduct, name='costo', textvariable=StringVar(self.top_level, value=description))
            self.newCostoTotal.grid(column=4, row=6, padx=20, pady=20, ipadx=10, ipady=5)

            Label(self.EditProduct, text='Margen Producto', bg='SteelBlue2').grid(column=3, row=7)
            self.ValorMercado = Entry(self.EditProduct, name='mercado', textvariable=StringVar(self.top_level, ))
            self.ValorMercado.grid(column=4, row=7, padx=20, pady=20, ipadx=10, ipady=5)
            
            self.button = Button(self.EditProduct, text='Añadir', bg='SteelBlue3', width=20, command = lambda : self.actualizar_producto(precio, self.ValorMercado.get(), id))
            self.button.grid(column=1, row=8, columnspan=6, ipadx=5, ipady=5, pady=10)

        def actualizar_producto(self, name, margen, id):
            margen = int(self.ValorMercado.get()) * int(self.newCostoTotal.get())
            valomercado = margen // 100
            valormargen = int(self.newCostoTotal.get()) + int(valomercado) 
            ganancia = int(self.newCostoTotal.get()) - int(valormargen)
            positivo = abs(ganancia)
            if len(self.newCostoTotal.get()) != 0 and len(self.ValorMercado.get()) != 0:
                query = 'UPDATE Terminado SET ValorMercado = ?, Ganancias = ?, valormargen = ? WHERE Nombre = ? AND Id = ?'
                parametros = (valormargen, positivo, valomercado, name, id)
                self.run_query(query, parametros)
                query_margen = 'UPDATE Terminado SET margen = ? WHERE Nombre = ? AND Id = ?'
                parametrs = (self.ValorMercado.get(), name, id)
                self.run_query(query_margen, parametrs)
                self.EditProduct.destroy()
                self.get_products()
            else: 
                messagebox.showerror(title='error', message='No se pueden enviar valores vacios')
    
    class Facturas():
        
        db_name =  'Database.db'
        num_factura = 0

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=500, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            self.widgets_ventana2()
        
        def widgets_ventana2(self):

            Label(self.top_level, text='Facturas', font=('Segoe UI', 20), bg='SteelBlue2').grid(column=1, row=1, pady=10)

            Label(self.top_level, text='Cliente', bg='SteelBlue2').grid(column=0, row=3, pady=10)
            self.cliente = Entry(self.top_level, width=30)
            self.cliente.grid(row=4, column=0, padx=10, ipady=2)

            Label(self.top_level, text='Nit', bg='SteelBlue2').grid(column=1, row=3)
            self.nit = Entry(self.top_level, width=30)
            self.nit.grid(row=4, column=1, padx=10, ipady=2)

            Label(self.top_level, text='Direccion', bg='SteelBlue2').grid(column=2, row=3)
            self.direccion = Entry(self.top_level, width=30)
            self.direccion.grid(row=4, column=2, padx=10, ipady=2)

            Label(self.top_level, text='Ciudad', bg='SteelBlue2').grid(column=0, row=5)
            self.ciudad = Entry(self.top_level, width=30)
            self.ciudad.grid(row=6, column=0, padx=10, ipady=2)

            Label(self.top_level, text='Telefono', bg='SteelBlue2').grid(column=1, row=5, pady=10)
            self.telefono = Entry(self.top_level, width=30)
            self.telefono.grid(row=6, column=1, ipady=2, padx=10)

            Label(self.top_level, text='Barrio', bg='SteelBlue2').grid(column=2, row=5, pady=10)
            self.barrio = Entry(self.top_level, width=30)
            self.barrio.grid(row=6, column=2, ipady=2, padx=10)

            Label(self.top_level, text='Fecha vencimiento', bg='Steelblue2').grid(row=7, column=0, pady=10)
            self.vencimiento = Entry(self.top_level, width=30)
            self.vencimiento.grid(row=8, column=0, ipady=2)

            Label(self.top_level, text='Forma de pago', bg='SteelBlue2').grid(row=7, column=1)
            self.formadepago = Entry(self.top_level, width=30)
            self.formadepago.grid(row=8, column=1, ipady=2)

            Label(self.top_level, text='Descuento', bg='SteelBlue2').grid(column=2, row=7, pady=10)
            self.descuento = Entry(self.top_level, width=30)
            self.descuento.grid(row=8, column=2, ipady=2, padx=10)

            Button(self.top_level, text='Imprimir', command=self.Imprimir, width=20, bg='SteelBlue3').grid(row=10, column=1, pady=20, ipadx=10, ipady=3)

            Button(self.top_level, text='Agregar productos', bg='SteelBlue3', command=self.AgregarProductos).grid(row=10, column=0, pady=20, ipadx=10, ipady=3)

        productosVendidos = []
        
        def AgregarProductos(self):

            self.agregarproductos = Toplevel()
            self.agregarproductos.config(bg='SteelBlue2')

            Label(self.agregarproductos, text='Aregar Productos', font=('Segoe UI', 20), bg='SteelBlue2').grid(row=3, column=1)

            Label(self.agregarproductos, text='Producto', bg='SteelBlue2').grid(column=0, row=4)
            self.valor = Entry(self.agregarproductos, width=30)
            self.valor.grid(row=5, column=0, ipady=4, padx=5) 

            Label(self.agregarproductos, text='Precio', bg='SteelBlue2').grid(column=1, row=4, pady=10)
            self.precio = Entry(self.agregarproductos, width=30)
            self.precio.grid(row=5, column=1, ipady=4, padx=10)

            Label(self.agregarproductos, text='Cantidad', bg='SteelBlue2').grid(column=2, row=4, pady=10)
            self.cantidad = Entry(self.agregarproductos, width=30)
            self.cantidad.grid(row=5, column=2, ipady=4, padx=10)

            def Addproduct():
                producto = (self.valor.get().upper(), int(self.cantidad.get()), int(self.precio.get()))
                self.productosVendidos.append(producto)
                messagebox.showinfo(message=f'Producto {self.valor.get().upper()} agregado')
                self.valor.delete(0, END)
                self.precio.delete(0, END)
                self.cantidad.delete(0, END)

            Button(self.agregarproductos, text='Agregar', bg='SteelBlue3', command=Addproduct, width=20).grid(column=1, row=6, pady=10, ipady=5)

        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def NumFactura(self):
            numero = self.run_query('SELECT Num FROM NumFactura')
            for num in numero:
                return int(num[0])
        
        def Imprimir(self):
            
            def ProductosVendidos(productos):
                width = 28
                total = 0
                Descuento = 0

                if(self.descuento.get() == ''):
                    Descuento = 0
                else:
                    Descuento = int(self.descuento.get())
                
                items = [
                    
                ]

                for name, price, count in productos:
        
                    total += int(price)*int(count) 

                    print()

                    all_price = str(price*count)

                    msg = f'{name}'.ljust(width-len(all_price), ' ')
                    msg += all_price

                    if(type(count) is int and count >= 2):
                        msg += f'\n {price} x {"{:,}".format(count)}'
                    elif type(count) is float:
                        msg += f'\n {"{:,}".format(count)} x {price}'
        
                    items.append(msg)
                totalnuevo = total - int(Descuento)
                total = str("{:,}".format(totalnuevo))
                items.append("---------------------------------------------")
                items.append("SUBTOTAL: ".ljust(width-len(total) + 1) + total)

                return '\n'.join(items)

            doc = Document()
            factura = doc.add_paragraph(f'TALLER CASALINDA A.N.L\nNIT: 57478574\nCALLE 14 N° 8A, APTO 1, AV. NUÑEZ\nTELEFONO: 474738234\nLa Union - Colombia\nNO RESPONSABLE DE I.V.A\n\nFACTURA POR CONTINGENCIA No: FV 0{self.NumFactura()}\nFECHA:  {datetime.date.today().strftime("%d/%m/%Y")}\nHORA:  {hora}:{minute}:{seconds}\nLE ATENDIO:  TALLER CASALINDA\nCAJERO No: 1\n---------------------------------------------\nCLIENTE:  {self.cliente.get().upper()}\nNIT:   {self.nit.get()}\nDIRECCION:  {self.direccion.get().upper()}\nTELEFONO: {self.telefono.get().upper()}\nCIUDAD:  {self.ciudad.get()}\nBARRIO:  {self.barrio.get().upper()}\n---------------------------------------------\nDETALLE DE LA VENTA:\n {ProductosVendidos(self.productosVendidos)}\nDESCUENTO:               {"{:}".format(self.descuento.get())}\nIVA: \nNETO: \n---------------------------------------------\nFORMA DE PAGO:  {self.formadepago.get().upper()}\nVENCE: {self.vencimiento.get().upper()} INT: 0%\nCLIENTE:  {self.cliente.get().upper()}\n\nFIRMA: ____________________\nNo DOC. ID: \n\nGRACIAS POR SU COMPRA\n\n------ *** FIN FACTURA *** ------\n\n\n')
            factura.style.font.name = 'Arial Century'
            factura.runs[0].bold = True
            doc.save('Factura.docx')
            
            numerosFactura = self.run_query('SELECT Num FROM NumFactura')
            for numero in numerosFactura:
                self.run_query('UPDATE NumFactura SET Num = ?', (int(numero[0]) + 1, ))
            self.run_query('SELECT * FROM NumFactura', ())

            self.productosVendidos = []

    class Historial():

        db_name =  'Database.db'

        def __init__(self):
            self.top_level = Toplevel(window)
            self.top_level.title("Sistema de inventarios")
            self.top_level.config(width=600, height=500, bg='SteelBlue2')
            self.top_level.resizable(0,0)

            ANCHO = 1220
            ALTO = 470
            POSY = 10
            POSX = 75

            anchoAlto = str(ANCHO) + 'x' + str(ALTO)
            posicionX = '+' + str(POSX)
            posicionY = '+' + str(POSY)

            self.top_level.geometry(anchoAlto+posicionX+posicionY)

            self.widgets_ventana2()
        
        def widgets_ventana2(self):
            
            Label(self.top_level, text='Historial de ventas', font=('Segoe UI',20), bg='SteelBlue2').grid(row=2, column=1, pady=(10, 20))

            Button(self.top_level, text='Buscar', width=10, bg='SteelBlue3', command=self.Buscador).grid(row=4, column=1, pady=(15,0))
            self.search = Entry(self.top_level, width=30)
            self.search.grid(row=3, column=1, ipady=2)

            self.tabla = ttk.Treeview(self.top_level, columns=('Date', 'valorUnit', 'Valortoal', 'Mount', 'id'))
            self.tabla.grid(row=6, column=0, columnspan=3, pady=20)
            self.tabla.heading('#0', text='Nombre', anchor=CENTER)
            self.tabla.heading('#1', text='Fecha ingreso', anchor=CENTER)
            self.tabla.heading('#2', text='Cantidad', anchor=CENTER)
            self.tabla.heading('#3', text='Valor unitario', anchor=CENTER)
            self.tabla.heading('#4', text='Valor total', anchor=CENTER)
            self.tabla.heading('#5', text='Id', anchor=CENTER)

            scrooll_ver = ttk.Scrollbar(self.top_level, orient="vertical", command=self.tabla.yview)
            scrooll_ver.grid(row=6, column=3, sticky='nsw')
            self.tabla.configure(yscrollcommand=scrooll_ver.set)
        
            self.get_products()
        
        #conexion con la base de datos
        def run_query(self, query, parametrs = {}):
                    with sqlite3.connect(self.db_name) as conn:
                        cursor = conn.cursor()
                        result = cursor.execute(query, parametrs)
                        conn.commit()
                    return result

        def get_products(self):
            #borrar todos los elementos antes de posicionar los nuevamente
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #listar los elementos en la tabla de la base de datos
            query = 'SELECT * FROM Historial ORDER BY Nombre ASC'
            db_results = self.run_query(query)
            for row in db_results:
                self.tabla.insert('', 'end', text= row[0], values=(row[1], row[2], row[3], row[5], row[4]))
            
        def Buscador(self):
            query = "SELECT * FROM Historial WHERE substr(Total, 4, 2) = ? ORDER BY Nombre ASC"
            datos = self.run_query(query, (self.search.get(), ))
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            for row in datos:
                self.tabla.insert('', 'end', text= row[0], values=(row[1], row[2], row[3], row[5], row[4]))

if __name__ == '__main__':
    window = Tk()
    window.resizable(0,0)
    window.config(bg='SteelBlue2')
    aplication = Product(window)
    window.mainloop()

def transfer_data():
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Historial')
    cursor.execute('INSERT INTO Historial SELECT * FROM Ingresos')
    conn.commit()
    conn.close()
    print("Data transferred successfully at: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Schedule the transfer_records function to run every 5 minutes
schedule.every(1).minutes.do(transfer_data)

while True:
    schedule.run_pending()
    time.sleep(60)
