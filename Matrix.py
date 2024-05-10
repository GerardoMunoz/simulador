import array
import random
from math import cos,sin

class Matrix:
    def __init__(self, m, n, data=None):
        self.m = m  # number of rows
        self.n = n  # number of columns
        if data is None:
            self.data = array.array('f', [0.0] * (n * m))
        else:
            if len(data) != n * m:
                raise ValueError("Incorrect data length")
            self.data = array.array('f', data)
            
    def copy(self):
        return Matrix(self.m,self.n,self.data[:])

    def __getitem__(self, index):
        if isinstance(index,tuple):
      
           i, j = index
           if isinstance(i,int) and isinstance(j,int):
                if 0 <= i < self.m and 0 <= j < self.n:
                    return self.data[i * self.n + j]
                else:
                    raise IndexError("Matrix indices out of range",i,j)
           if isinstance(i,int) and isinstance(j,slice):
             raise IndexError("One slice is not allow yet ")
           if isinstance(i,slice) and isinstance(j,int):
             raise IndexError("One slice is not allow yet ")
           if isinstance(i,slice) and isinstance(j,slice):
                 start_i, stop_i, step_i = i.indices(self.m)
                 start_j, stop_j, step_j = j.indices(self.n)
                 if step_i!=1 or step_j!=1:
                     raise IndexError("Step must be one")
                 sliced_data = [self.data[r * self.n + c] for r in range(start_i, stop_i, step_i) for c in range(start_j, stop_j, step_j)]
                 return Matrix(stop_i - start_i, stop_j - start_j, sliced_data)
           else:
                 raise IndexError("i,j indices are required")
        else:
            raise ValueError("i,j indices are required")

    def __setitem__(self, index, value):
        i, j = index
        if 0 <= i < self.m and 0 <= j < self.n:
            self.data[i * self.n + j] = value
        else:
            raise IndexError("Matrix indices out of range",i,j)

    def __add__(self, other):
        #print('add',self.m,self.n,other.m,other.n)
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] + other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be added",self.m,self.m,other.m,other.n)

    def __sub__(self, other):
        #print('sub',self.m,self.n,other.m,other.n)
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] - other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be subtracted",self.m,self.m,other.m,other.n)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] * other
            return result
        elif isinstance(other, Matrix):
            #print('mul',self.m,self.n,other.m,other.n)
            if self.n != other.m:
                raise ValueError("Number of columns of first matrix must be equal to number of rows of second matrix")
            result = Matrix(self.m, other.n)
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        result[i, j] += self[i, k] * other[k, j]
            return result
        else:
            raise ValueError("Multiplication not defined for these data types")

    def T(self):
        transposed_data = array.array('f', [0.0] * (self.n * self.m))
        for i in range(self.m):
            for j in range(self.n):
                transposed_data[j * self.m + i] = self.data[i * self.n + j]
        return Matrix(self.n, self.m, transposed_data)
    
    def __or__(self,other):
        """
        concatenate vertically
        """
        if isinstance(other, Matrix) and self.n == other.n :
            return Matrix(self.m + other.m, self.n,self.data+other.data)
        else:
            raise ValueError("Matrices of different dimensions cannot be added")

    def __and__(self, other):
        """
        Concatenate two matrices horizontally.

        Args:
            other (Matrix): The second matrix to concatenate.

        Returns:
            Matrix: The resulting matrix after horizontal concatenation.
        """
        if self.m != other.m:
            raise ValueError("Matrices must have the same number of rows to concatenate horizontally")
        
        concatenated_data = []
        for i in range(self.m):
            concatenated_data.extend(self.data[i*self.n : (i+1)*self.n])
            concatenated_data.extend(other.data[i*other.n : (i+1)*other.n])

        return Matrix(self.m, self.n + other.n, concatenated_data)

    def repeat_vertically(self,n):
         return Matrix(self.m *n, self.n,self.data *n)

    def rot2D(a):
        return Matrix(3,3,[cos(a),sin(a), 0,
                           -sin(a), cos(a), 0,
                           0     , 0     , 1])
    
    def tras2D(x,y):
        return Matrix(3,3,[1, 0, 0,
                           0, 1, 0,
                           x, y, 1])
   
    def untail(m):
       return Matrix(m.m,m.n-1,[m.data[i] for i in range(len(m.data))  if i%m.n != m.n-1])
    
    def tail(m):
       return Matrix(m.m,m.n+1,[(m.data[i * m.n + j] if j != m.n else 1) for i in range(m.m) for j in range(m.n+1)  ])
    
    
    
    

    def __str__(self):
        output = ""
        for i in range(self.m):
            row_str = " ".join(str(self[i, j]) for j in range(self.n))
            output += row_str + "\n"
        return output
    
    def save_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"{self.m} {self.n}\n")
            for i in range(self.m):
                for j in range(self.n):
                    file.write(str(self.data[i * self.n + j]) + ' ')
                file.write('\n')

    @classmethod
    def load_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            rows, cols = map(int, file.readline().split())
            data = []
            for _ in range(rows):
                row = list(map(float, file.readline().split()))
                data.extend(row)
            return cls(rows, cols, data)




