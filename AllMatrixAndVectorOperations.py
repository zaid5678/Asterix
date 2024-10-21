import numpy as np
import math
import random
from Stack import *
St = Stack()

class Matrix():
    
    def generateRandomNumber(self):
        return random.randint(2,3)

    def generateRandomMatrixNumber(self):
        return random.randint(-50,50)

    def add(self,A,B):
        if len(A) == 2:
            a = A[0][0] + B[0][0]
            b = A[0][1] + B[0][1]
            c = A[1][0] + B[1][0]
            d = A[1][1] + B[1][1]
            values = [[a, b],[c, d]]
        elif len(A) == 3:
            a = A[0][0] + B[0][0]
            b = A[0][1] + B[0][1]
            c = A[0][2] + B[0][2]
            d = A[1][0] + B[1][0]
            e = A[1][1] + B[1][1]
            f = A[1][2] + B[1][2]
            g = A[2][0] + B[2][0]
            h = A[2][1] + B[2][1]
            i = A[2][2] + B[2][2]
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return np.mat(values)

    def subtract(self,A,B):
        if len(A) == 2:
            a = A[0][0] - B[0][0]
            b = A[0][1] - B[0][1]
            c = A[1][0] - B[1][0]
            d = A[1][1] - B[1][1]
            values = [[a, b],[c, d]]
        elif len(A) == 3:
            a = A[0][0] - B[0][0]
            b = A[0][1] - B[0][1]
            c = A[0][2] - B[0][2]
            d = A[1][0] - B[1][0]
            e = A[1][1] - B[1][1]
            f = A[1][2] - B[1][2]
            g = A[2][0] - B[2][0]
            h = A[2][1] - B[2][1]
            i = A[2][2] - B[2][2]
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return np.mat(values)

    def create3x3Matrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        e = self.generateRandomMatrixNumber()
        f = self.generateRandomMatrixNumber()
        g = self.generateRandomMatrixNumber()
        h = self.generateRandomMatrixNumber()
        i = self.generateRandomMatrixNumber()
        values = [[a, b, c], [d, e, f], [g, h, i]]
        return values

    def create2x2Matrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        values = [[a, b],[c, d]]
        return values
    
    def createRandomMatrix(self):
        a = self.generateRandomMatrixNumber()
        b = self.generateRandomMatrixNumber()
        c = self.generateRandomMatrixNumber()
        d = self.generateRandomMatrixNumber()
        e = self.generateRandomMatrixNumber()
        f = self.generateRandomMatrixNumber()
        g = self.generateRandomMatrixNumber()
        h = self.generateRandomMatrixNumber()
        i = self.generateRandomMatrixNumber()
        s = self.generateRandomNumber()
        if s == 2:
            values = [[a, b],[c, d]]
        elif s == 3:
            values = [[a, b, c], [d, e, f], [g, h, i]]
        return values
        
    def createInverseMatrix(self):
        determinant = 0
        while determinant == 0:
            m = self.createRandomMatrix()
            print(np.mat(m))
            determinant = self.DetOfMatrix(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return np.mat([[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]])
        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.DetOfMatrix(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(m)):
            for c in range(len(m)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors

    def transposeMatrix(self,m):
        return [[row[i] for row in m] for i in range(len(m[0]))]
            
    def getMatrixMinor(self,m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def DetOfMatrix(self,m):
        if len(m) == 2:
            return(m[0][0]*m[1][1])-(m[0][1]*m[1][0])
        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*self.DetOfMatrix(self.getMatrixMinor(m,0,c))
        return determinant

    def multiplyMatrix(self,a,b):
      result=[]
      result1=[]
      while len(a)>0:     
        d=0    
        a1=a[:1:]    
        c=True
        while d<len(a1):
          for x in b:
            for x1 in x:
              St.push(result,x1*a1[0][d])
            d=d+1
        a.pop(0)    
      result=[result[i:i+len(b[0])] for i in range(0, len(result), len(b[0]))]     
      total=0      
      while len(result)>0:
        for X in range(len(result[0])):
          for Y in range(len(b)):
            total=total+result[Y][X]
          St.push(result1,total)
          total=0 
        for s in range(len(b)):
          result.pop(0)  
      result1=[result1[i:i+len(b[0])] for i in range(0, len(result1), len(b[0]))] 
      return (np.mat(result1))

    def checkIfMatricesAreEqual(self,a,b):
        if np.array_equal(a, b):
            return True
        else:
            return False

    def checkIfAnswerIsCorrect(self,a,b):
        if a == b:
            return True
        else:
            return False

class Vector():
    def generateRandomNumber(self):
        return random.randint(2,3)

    def generateRandomVectorNumber(self):
        return random.randint(-50,50)
        
    def createVector2D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        return np.array([a,b]).T

    def createVector3D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        c = self.generateRandomVectorNumber()
        return np.array([a,b,c]).T

    def distanceBetween(self,a,b,c):
        return math.sqrt(a**2 + b**2 + c**2)

    def getShortestDistaceBetweenLines(self,a1,b1,a2,b2):
        c = self.crossProduct(b1,b2)
        numerator = self.dotProduct((a2-a1),c)
        d = self.distanceBetween(c[0],c[1],c[2])
        result = round((numerator/d),2)
        if result < 0:
            result = result * -1
        return result

    def getShortestDistaceBetweenPointAndPlane(self,A,n,d):
        denominator = self.distanceBetween(n[0],n[1],n[2])
        numerator = ((A[0]*n[0]) + (A[1]*n[1]) + (A[2]*n[2])) - d
        if numerator < 0:
            numerator = numerator * -1
        return round(numerator/denominator,2)

    def createVector3D(self):
        a = self.generateRandomVectorNumber()
        b = self.generateRandomVectorNumber()
        c = self.generateRandomVectorNumber()
        return np.array([a,b,c]).T
        
    def dotProduct(self,A,B):
        result = 0
        for i in range(0,len(A)):
            result += (A[i] * B[i])
        return result

    def crossProduct(self,A,B):
      dimension = len(A)
      c = []
      for i in range(dimension):
        c.append(0)
        for j in range(dimension):
          if j != i:
            for k in range(dimension):
              if k != i:
                if k > j:
                  c[i] += A[j]*B[k]
                elif k < j:
                  c[i] -= A[j]*B[k]
      c[1] *= -1
      return c

    def cosInverse(self,x):
        if x < 0:
            x = x * -1
        a = math.acos(x)
        return math.degrees(a)

    def sinInverse(self,x):
        if x < 0:
            x = x * -1
        a = math.asin(x)
        return math.degrees(a)
    
    def angleBetween2LinesOr2Planes(self,b1,b2):
        magA = self.distanceBetween(b1[0],b1[1],b1[2])
        magB = self.distanceBetween(b2[0],b2[1],b2[2])
        aDotb = self.dotProduct(b1,b2)
        angle = self.cosInverse(aDotb/(magA*magB))
        return round(angle,2)

    def angleBetween1LineAnd1Plane(self,b1,b2):
        magA = self.distanceBetween(b1[0],b1[1],b1[2])
        magB = self.distanceBetween(b2[0],b2[1],b2[2])
        aDotb = self.dotProduct(b1,b2)
        angle = self.sinInverse(aDotb/(magA*magB))
        return round(angle,2)

    def checkIfVectorsAreEqual(self,A,B):
        for i in range(0,len(A)-1):
            if A[i] != B[i]:
                return False
        return True
                      
class SortAndSearch():
    def msort(self, x):
        num_lines = sum(1 for line in open('AllScores.txt'))
        result = []
        if num_lines < 20:
            return sorted(x)
        mid = int(num_lines / 2)
        y = msort(x[:mid])
        z = msort(x[mid:])
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        return result

    def hashFunction(self,name):
        return hashlib.sha244(x).hexdigest()                           
        

