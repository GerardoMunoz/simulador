from Matrix import Matrix
import array
import random
class Perceptron:
    def __init__(self, name_or_input_size, output_size=None):
        if isinstance(name_or_input_size,str):
            self.weights = Matrix.load_file(name_or_input_size)
        else:
            self.weights = Matrix(name_or_input_size+1, output_size+1,  [random.random() for _ in range((name_or_input_size+1) * (output_size+1))])  

    def predict(self, inputs):
        tail=False
        if inputs.n==self.weights.m-1:
            result = Matrix.untail(Matrix.tail(inputs) * self.weights)
        else:
            result = inputs * self.weights
        return result

    def train(self, inputs, labels, learning_rate=0.01, epochs=1):
        if inputs.n==self.weights.m-1:
            inputs=Matrix.tail(inputs)
        if labels.n==self.weights.n-1:
            labels=Matrix.tail(labels)
        for epoch in range(epochs):
            predictions = self.predict(inputs)
            
            error = labels - predictions
            self.weights=self.weights.add_tail(  inputs.T() * error * learning_rate)
            
    def save_file(self,name):
        self.weights.save_file(name)

# Example usage
if __name__ == "__main__":
    from Car import Car
    from Speedway import Speedway
    import tkinter as tk


    master = tk.Tk()
    
    perceptron = Perceptron(name_or_input_size=7, output_size=2)    
    
    train=True
    repeat=True
    
    speedway = Speedway(master)
    car = Car()
    speedway.add_car(car)

    def aumentar_velocidad_izquierda(event):
        car.v_l_up()

    def disminuir_velocidad_izquierda(event):
        car.v_l_down()

    def aumentar_velocidad_derecha(event):
        car.v_r_up()

    def disminuir_velocidad_derecha(event):
        car.v_r_down()

    def enter(event):
        global train
        train=not(train)
        print('train: ',train)
        perceptron.save_file("car.txt")
        
    def load(event):
        global perceptron
        perceptron = Perceptron("car.txt") 
        print('load: ',load)
       


    master.bind("<Up>", aumentar_velocidad_izquierda)
    master.bind("<Down>", disminuir_velocidad_izquierda)
    master.bind("<KeyPress-w>", aumentar_velocidad_derecha)
    master.bind("<KeyPress-s>", disminuir_velocidad_derecha)
    master.bind("<Return>", enter)
    master.bind("<space>", load)

    def train_control():
      global cont_train,repeat
      if repeat:
       
        floor_colors = Matrix(1,7,speedway.read_floor_color_gray(car.get_sensors_coord()))
        if train:
            master.after(30,train_control)
            maxval=0
            index_maxval=11
            for i in range(7):
                if floor_colors[0,i]>maxval:
                    maxval=floor_colors[0,i]
                    index_maxval=i-4
            car.v_i=5 - index_maxval/3
            car.v_d=5 + index_maxval/3
            motors_vel= Matrix(1,2,[car.v_i,car.v_d])

            cont_train +=1
            if cont_train%100==0:
                print(cont_train,perceptron.predict(floor_colors*(1/255))*5-motors_vel)
            if cont_train==10000:
                repeat=False

            perceptron.train(floor_colors*(1/255), motors_vel*(1/5))
        else:
            master.after(10,train_control)
            prediction=perceptron.predict(floor_colors*(1/255))*5
            car.v_i = prediction[0,0]
            car.v_d = prediction[0,1]
            #print('predic', prediction)
                
    cont_train =0
    speedway.anim()
    train_control()
    master.mainloop()

#     # Example usage
#     # Define training data (inputs) and their respective labels (labels)
#     inputs = Matrix(2,3, [0, 0, 1, 
#                            1, 0, 0])
#     labels = Matrix(2, 2, [0, 1,
#                            1, 0])
# 
# 
#     # Create a perceptron with 2 inputs and 2 outputs
#     perceptron = Perceptron(input_size=inputs.n, output_size=labels.n)
# 
#     # Define training data (inputs) and their respective labels (labels)
#     inputs = Matrix(2, 3, [0, 0, 1,0,1,0])
#     labels = Matrix(2, 2, [0, 1,1,0])
# 
#     # Train the perceptron
#     perceptron.train(inputs, labels,epochs=100)
# 
#     # Make predictions
#     print("Predictions after training:")
#     for i in range(inputs.m):
#         input_i=inputs[i:i+1,:]#[i*inputs.n:(i+1)*inputs.n]
#         prediction = perceptron.predict(input_i)
#         print(f"Inputs: {input_i} -> Prediction: {prediction}")




