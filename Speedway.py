from Matrix import Matrix
import array
import random


import tkinter as tk
import math



class Speedway:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador de Carrito")

        self.canvas_width = 400
        self.canvas_height = 300
        self.cars_list=[]
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        

        # Función para calcular el color de fondo en escala de grises
        self.color_func = self.calcular_color

        # Dibujar el fondo en escala de grises
        step_box=5
        for y in range(0,self.canvas_height,step_box):
            for x in range(0,self.canvas_width,step_box):
                color = self.color_func(x+step_box/2, y+step_box/2)
                self.canvas.create_rectangle(x, y, x+step_box, y+step_box, fill=color, outline="")


    def calcular_color(self, x, y):
        # Ejemplo de una función que devuelve un color en escala de grises
        # Devuelve un tono de gris basado en la coordenada 
        x=x/self.canvas_width*4 -2
        y=y/self.canvas_height*4 -2
        r2=x**2+y**2
        if r2<1:
            gray_value= int(r2*256)
        else:
            gray_value= int(256/r2)
        #print(x,y,r2,gray_value)
        return "#{:02x}{:02x}{:02x}".format(gray_value, gray_value, gray_value)
    


    def read_floor_color(self,sensors):
        #sensors = coords*Matrix.rot2D(self.angle_car)*Matrix.tras2D(self.posi_car[0,0],self.posi_car[0,1])
        sensors_values=[]
        for i in range(sensors.m):
            hex_color = self.calcular_color(sensors[i,0],sensors[i,1])[1:]
            sensors_values.append(hex_color)
        return sensors_values

    def read_floor_color_gray(self,sensors):
        sensors_values=[]
        for i in range(sensors.m):
            hex_color = self.calcular_color(sensors[i,0],sensors[i,1])[1:]

            # Convert hexadecimal string to RGB tuple
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            # Calculate grayscale value
            gray_value = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

            sensors_values.append(gray_value)
        return sensors_values
            
            
        

    def actualizar_labels(self):
        pass
#         self.label_izquierda.config(text="Velocidad Izquierda: {}".format(self.v_i))
#         self.label_derecha.config(text="Velocidad Derecha: {}".format(self.v_d))
#         self.label_sensors.config(text="Sensores: {}".format(self.read_sensors()))
       
        

    def add_car(self,car,labels=None):
        car.posi_car=Matrix(1,3,[self.canvas_width/2,self.canvas_height/2,1]);
        
        car_d={
            'car':car,
            #'pos':self.orig,
            'labels':labels,
            'canvas_poligon':   self.canvas.create_polygon( Matrix.untail(car.get_vertices_car()), fill=car.get_color())

            
        }
        self.cars_list.append(car_d)





            
        
    def anim(self):    
        self.canvas.after(10,self.anim)
        # Dibujar el carrito como un triángulo
        for car_d in self.cars_list:
            vert =car_d['car'].mov(1)            
            #print(Matrix.untail(vert))
            self.canvas.coords(car_d['canvas_poligon'], Matrix.untail(vert))
        #self.actualizar_labels()
        
        

    

if __name__ == "__main__":
    from Car import Car
    

    master = tk.Tk()
    speedway = Speedway(master)
    car = Car()
    speedway.add_car(car)
    car2 = Car(color='red')
    speedway.add_car(car2)
    
    def aumentar_velocidad_izquierda2(self):
        car2.v_l_up()

    def disminuir_velocidad_izquierda2(self):
        car2.v_l_down()

    def aumentar_velocidad_derecha2(self):
        car2.v_r_up()

    def disminuir_velocidad_derecha2(self):
        car2.v_r_down()

    def aumentar_velocidad_izquierda(self):
        car.v_l_up()

    def disminuir_velocidad_izquierda(self):
        car.v_l_down()

    def aumentar_velocidad_derecha(self):
        car.v_r_up()

    def disminuir_velocidad_derecha(self):
        car.v_r_down()


    # Crear las teclas para subir y bajar la velocidad de cada rueda
    master.bind("<Up>", aumentar_velocidad_izquierda)
    master.bind("<Down>", disminuir_velocidad_izquierda)
    master.bind("<KeyPress-w>", aumentar_velocidad_derecha)
    master.bind("<KeyPress-s>", disminuir_velocidad_derecha)

    
    master.bind("<Right>", aumentar_velocidad_izquierda2)
    master.bind("<Left>", disminuir_velocidad_izquierda2)
    master.bind("<KeyPress-d>", aumentar_velocidad_derecha2)
    master.bind("<KeyPress-a>", disminuir_velocidad_derecha2)
    
    
    
    
    speedway.anim()
    master.mainloop()


