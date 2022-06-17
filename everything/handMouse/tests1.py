class Portal:
 
    # Defining __init__ method
    def __init__(self):
        self.__name =''
     
    # Using @property decorator
    # @property
     
    # # Getter method
    # def name(self):
    #     return self.__name
     
    # # Setter method
    # @name.setter
    # def name(self, val):
    #     self.__name = val
 
    # # Deleter method
    # @name.deleter
    # def name(self):
    #    del self.__name
 
# Creating object
p = Portal()
 
# Setting name
p.__name = 'GeeksforGeeks'

print(p.__name)