from enum import Enum

class Engine(Enum):
    Unity = 'Unity' 
    
    def __str__(self):
        return self.value