from Matrix import Matrix
from Perceptron import Perceptron
import array
import random

class Reinforcement:
  def __init__(self,n_in, n_out, list_outs,f_error):
    """
    n_in, n_out : number of inputs and outputs
    list_outs : a Matrix of spected outputs. each row is one output
    f_error : input -> realnumber that represents the error of that input

    """
    self.n_in = n_in
    self.n_out = n_out
    self.list_outs = list_outs
    self.f_error = f_error
    self.control = Perceptron( n_in, n_out)
    self.model = Percepton(n_in + n_out, n_in)
    self.input_old =None
    self.output_old =None



  def predict(self, input_):

    output =self.control.predict(input_)
    
    self.train(self.input_old,self.output_old,input_,output)

    self.input_old=input_
    self.output_old=output
    return pred
     
  
  def train(self , input_old ,  output_old , input_ , output):
      model.train(input_old & output_old,input_)
      out_selected=None
      min_error=None
      for out_i in self.list_outs:
          in_predic = model.predict(input_ & out_i)
          error_pred = f_error(in_predic)
          if (error_predic < min_error) or (None == min_error):
              min_error = error_predic
              out_selected= out_i
      control.train(input_,out_selected)        
          
     