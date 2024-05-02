from Matrix import Matrix
import array
import random
class Perceptron:
    def __init__(self, input_size, output_size):
      # each row is an input or an output
        self.weights = Matrix(input_size, output_size,  [random.random() for _ in range(input_size * output_size)])  # Initialize weights randomly
        self.bias = Matrix( 1,output_size, [random.random() for _ in range(output_size)])  # Initialize biases randomly

    def predict(self, inputs):
        # Weighted sum of inputs with weights plus biases
        result = inputs * self.weights  + self.bias.repeat_vertically(inputs.m)
        # Apply activation function (in this case, step function)
        return result#Matrix(result.m, result.n, [[1 if val > 0 else 0 for val in row] for row in result.data])

    def train(self, inputs, labels, learning_rate=0.01, epochs=1):
        for epoch in range(epochs):
            # Make a prediction
            predictions = self.predict(inputs)
            
            # Calculate the error
            error = labels - predictions
            # Update weights and biases using error and learning rate
            self.weights += inputs.T() * error * learning_rate
            #print('train',inputs,labels,predictions,self.weights)
            for i in range(error.m):
                self.bias += error[i:i+1,:] * learning_rate

if __name__ == "__main__":
    from Car import Car
    from Speedway import Speedway
    import tkinter as tk


    master = tk.Tk()
    
    perceptron = Perceptron(input_size=7, output_size=2)
    
    history_max=1000
    history_write_index=0
    history_inputs = Matrix(history_max,7)# 7 sensors
    history_labels = Matrix(history_max,2)# v_i, v_d
    
    error=1000
    error_umbral=1
    
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
        
    def loop(event):
        global repeat
        print('loop')
        repeat=False


    # Crear las teclas para subir y bajar la velocidad de cada rueda
    master.bind("<Up>", aumentar_velocidad_izquierda)
    master.bind("<Down>", disminuir_velocidad_izquierda)
    master.bind("<KeyPress-w>", aumentar_velocidad_derecha)
    master.bind("<KeyPress-s>", disminuir_velocidad_derecha)
    master.bind("<Return>", enter)
    master.bind("<space>", loop)

    
    

    
    def train_control():
      global cont_train,repeat
      if repeat:
       
        floor_colors = Matrix(1,7,speedway.read_floor_color_gray(car.get_sensors_coord()))
        if train:#history_write_index < history_max:
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

            #print(car.v_i,car.v_d,index_maxval)
            perceptron.train(floor_colors*(1/255), motors_vel*(1/5))
        else:
            master.after(10,train_control)
            prediction=perceptron.predict(floor_colors*(1/255))*5
            car.v_i = prediction[0,0]
            car.v_d = prediction[0,1]
            print('predic', prediction)
                
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




