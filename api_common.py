from enum import Enum

class Role(Enum):
    UNKNOWN = 0
    HUMAN = 1
    ARTIFICIAL_INTELLIGENCE = 2    
        
    def __str__(self) -> str:
        if self == Role.ARTIFICIAL_INTELLIGENCE:
            return "AI"
        elif self == Role.HUMAN:
            return "HUMAN"
        else:
            return "UNKNOWN"

def role_from_str(str):
        if str == 'HUMAN':
            return Role.HUMAN
        elif str == "AI" or str == "artificial intelligence":
            return Role.ARTIFICIAL_INTELLIGENCE
        else:
            return Role.UNKNOWN