class Stack():

    def reverseStack(self,x):
        return x.reverse()
    
    def push(self,x,item):
        return x.append(item)
    
    def pop(self,x):
        self.reverseStack(x)
        return x.remove(x[0])
        self.reverseStack(x)

    def peek(self,items):
        return items[0]

    
