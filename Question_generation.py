from AllMatrixAndVectorOperations import *
import random
from numpy import *
import math
import time

M = Matrix()
V = Vector()

class Questions():

    def printMatricesOrVectors(self,A,B,s):
        print("A = ")
        print(np.mat(A))
        print("B = ")
        print(np.mat(B))
        w = "Find A{}B"
        print(w.format(s))
    
    def inputAnswer(self,name):
        while True:
            try:
                s = "Input {} : "
                answer = float(input((s.format(name))))
                break
            except ValueError:
                print("Invalid data type\nInput integer or float only\n")
        return answer
    
    def generateRandomNumForQuestion(self):
        return random.randint(1,12)

    def printCorrectWord(self):
        x = V.generateRandomNumber()
        if x == 2:
            return "perpendicular"
        elif x == 3:
            return "shortest"

    def determineWhichQuestionToCreate(self):
        print("===========================================")
        u = self.generateRandomNumForQuestion()
        if u == 1:
            return self.multiplyMatricesQuestion()
        elif u == 2:
            return self.addMatricesQuestion()
        elif u == 3:
            return self.subtractMatricesQuestion()
        elif u == 4:
            return self.DetQuestion()
        elif u == 5:
            return self.InverseQuestion()
        elif u == 6:
            return self.dotProductQuestion()
        elif u == 7:
            return self.crossProductQuestion()
        elif u == 8:
            return self.shortestDistanceBetweenSkewLinesQuestion()
        elif u == 9:
            return self.shortestDistanceBetweenLineAndPlaneQuestion()
        elif u == 10:
            return self.angleBetweenTwoLinesQuestion()
        elif u == 11:
            return self.angleBetweenLineAndPlaneQuestion()
        elif u == 12:
            return self.planeParametricToCartesianFormQuestion()

    #Matrix questions

    #1
    def multiplyMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"")
        result = M.multiplyMatrix(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Correct!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
    
    #2
    def addMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"+")
        result = M.add(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Correct!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
            return False

    #3
    def subtractMatricesQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            A = M.create2x2Matrix()
            B = M.create2x2Matrix()
        elif x == 3:
            A = M.create3x3Matrix()
            B = M.create3x3Matrix()
        self.printMatricesOrVectors(A,B,"-")
        result = M.subtract(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if x == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, result):
            print("Great!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(result)
            return False
    #4  
    def DetQuestion(self):
        x = M.generateRandomNumber()
        if x == 2:
            m = M.create2x2Matrix()
        elif x == 3:
            m = M.create3x3Matrix()
        print(np.mat(m))
        det = M.DetOfMatrix(m)
        print("Calculate the determinant of the above matrix")
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,det):
            print("Well done!")
            return True
        else:
            print("Incorrect!\nThe answer was :",det)
            return False
        
    #5
    def InverseQuestion(self):
        inverseMatrix = M.createInverseMatrix()
        inverseMatrix = np.around(inverseMatrix, decimals=2, out=None)
        v = len(inverseMatrix)
        print("Find the inverse matrix")
        print("Give the following values to",2,"decimal places where appropriate")
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answer = np.mat([[a,b],[c,d]])
        if v == 3:
            e = self.inputAnswer("e")
            f = self.inputAnswer("f")
            g = self.inputAnswer("g")
            h = self.inputAnswer("h")
            i = self.inputAnswer("i")
            answer = np.mat([[a,b,c],[d,e,f],[g,h,i]])
        if M.checkIfMatricesAreEqual(answer, inverseMatrix):
            print("Fantastic!")
            return True
        else:
            print("Incorrect!\nThe correct answer is : ")
            print(inverseMatrix)
            return False

    #Vector questions
    #6
    def dotProductQuestion(self):
        z = V.generateRandomNumber()
        if z == 2:
            A = V.createVector2D()
            B = V.createVector2D()
        elif z == 3:
            A = V.createVector3D()
            B = V.createVector3D()
        self.printMatricesOrVectors(A,B,"∙")
        result = V.dotProduct(A,B)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer, result):
            print("Good work!")
            return True
        else:
            print("Wrong answer!\nThe correct answer is : ",result)
            return False

    #7
    def crossProductQuestion(self):
        A = V.createVector3D()
        B = V.createVector3D()
        self.printMatricesOrVectors(A,B,"×")
        result = V.crossProduct(A,B)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        answer = np.mat([a,b,c]).T
        if V.checkIfVectorsAreEqual(answer,result):
            print("Great!")
            return True
        else:
            print("That's incorrect!\nThe correct answer is : ",result)
            return False

    #8
    def shortestDistanceBetweenSkewLinesQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        word = self.printCorrectWord()
        print("L1 :")
        print(a1, "+ λ",b1)
        print("L2 :")
        print(a2, "+ μ",b2)
        print("Find the",word,"distance between the skew lines L1 and L2\nGive your answers to",2,"decimal places")
        result = V.getShortestDistaceBetweenLines(a1,b1,a2,b2)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Fantastic!")
            return True
        else:
            print("That's wrong!\nThe correct answer is : ",result,"units")
            return False

    #9
    def shortestDistanceBetweenLineAndPlaneQuestion(self):
        A = V.createVector3D() #point
        n = V.createVector3D() #direction vector
        d = V.generateRandomNumber() #the non x coefficient
        print("The plane π has equation :")
        print("r ∙",n,"=",d)
        print("The point A has position vector :",A)
        word = self.printCorrectWord()
        print("Find the",word,"distance between A and the plane π\nGive your answer to",2,"decimal places")
        result = V.getShortestDistaceBetweenPointAndPlane(A,n,d)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Splendid!")
            return True
        else:
            print("That's the wrong answer!\nThe correct answer is : ",result,"units")
            return False

    #10
    def angleBetweenTwoLinesQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        print("L1 :")
        print(a1, "+ λ",b1)
        print("L2 :")
        print(a2, "+ μ",b2)
        print("Find the acute angle between the lines L1 and L2\nGive your answer in degrees to",2,"decimal places")
        result = V.angleBetween2LinesOr2Planes(b1,b2)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(result,answer):
            print("Good!")
            return True
        else:
            print("Not correct!\nThe correct answer is : ",result,"degrees")
            return False

    #11   
    def angleBetweenLineAndPlaneQuestion(self):
        a1 = V.createVector3D()
        b1 = V.createVector3D()
        a2 = V.createVector3D()
        b2 = V.createVector3D()
        n1 = V.createVector3D() #direction vector
        d1 = V.generateRandomNumber() #the non x coefficient
        print("The plane π has equation :")
        print("r ∙",n1,"=",d1)
        print("L :")
        print(a1, "+ λ",b1)
        print("Find the acute angle between the plane π and the line L\nGive your answer in degrees to",2,"decimal places")
        result = V.angleBetween1LineAnd1Plane(n1,b1)
        answer = self.inputAnswer("answer")
        if M.checkIfAnswerIsCorrect(answer,result):
            print("Excellent!")
            return True
        else:
            print("Not right!\nThe correct answer is : ",result,"degrees")
            return False

    #12
    def planeParametricToCartesianFormQuestion(self):
        a = V.createVector3D()
        b = V.createVector3D()
        c = V.createVector3D()
        print("The plane π has equation :")
        print(a,"+ s",b,"+ t",c)
        print("Given that the cartesian form is ax + by + cz = d, where a, b, c, and d are constants\nConvert this plane in parametric form to cartesian form")
        n = V.crossProduct(b,c)
        answerD = V.dotProduct(n,a)
        a = self.inputAnswer("a")
        b = self.inputAnswer("b")
        c = self.inputAnswer("c")
        d = self.inputAnswer("d")
        answerA = np.array([a,b,c]).T
        if M.checkIfMatricesAreEqual(answerA,n) and M.checkIfAnswerIsCorrect(d, answerD):
            print("Great job!")
            return True
        else:
            print("Not correct!\nThe correct answer is : ",end = "")
            print(n[0],"x +",n[1],"y +",n[2],"z =",answerD)
            return False

