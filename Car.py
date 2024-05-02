from Matrix import Matrix
import array
import random


import math

class Car:
    def __init__(self,color='blue'):
        self.color=color
        self.mov_d =5
        self.mov_r =3
        self.angle_car=0
        self.posi_car=Matrix(1,3,[0,0,1])
        

        # Coordenadas originales del triángulo del carrito
        car_d =10
        self.vertices_car = Matrix(3,3,[0,-car_d, 1,
                                         3*car_d,0,1,
                                        0,car_d, 1])
        self.vertices_car_absol = self.vertices_car.copy()

        self.sensors = Matrix(7,3,[
                                    3*car_d,-1.5*car_d,1,
                                    3*car_d,-1*car_d,1,
                                    3*car_d,-0.5*car_d,1,
                                    3*car_d,0,1,
                                    3*car_d,0.5*car_d,1,
                                    3*car_d,1*car_d,1,
                                    3*car_d,1.5*car_d,1,
                                    ])


        # Controles del carrito
        self.v_i = 0
        self.v_d = 0


            
    def get_sensors_coord(self):
        return self.sensors*  Matrix.rot2D(self.angle_car)*Matrix.tras2D(self.posi_car[0,0],self.posi_car[0,1])

    def get_vertices_car(self):
        return self.vertices_car* Matrix.rot2D(self.angle_car)*Matrix.tras2D(self.posi_car[0,0],self.posi_car[0,1])
            
    
    def get_color(self):
        return self.color

    def set_color(self,color):
        self.color =color

        
    def v_l_up(self):
        self.v_i += 0.1
        self.actualizar_labels()

    def v_l_down(self):
        self.v_i -= 0.1
        self.actualizar_labels()

    def v_r_up(self):
        self.v_d += 0.1
        self.actualizar_labels()

    def v_r_down(self):
        self.v_d -= 0.1
        self.actualizar_labels()

    def actualizar_labels(self):
        print("actualizar",self.v_i,self.v_d,self.posi_car,self.angle_car)
        

            
    def mov(self,t):
        x=self.mov_r*(self.v_d+self.v_i)/2*t
        y=0
        angle=self.mov_r/self.mov_d*(self.v_d-self.v_i)/2*t
        desp = Matrix(1,3,[x,y,1])*Matrix.rot2D(self.angle_car)
        self.posi_car +=desp
        self.angle_car+=angle
        self.vertices_car_absol=self.get_vertices_car()
        return self.vertices_car_absol
        
        
        

    
