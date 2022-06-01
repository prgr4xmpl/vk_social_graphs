import json

class INode:
    def __init__(self, _id : int, _data = {}) -> None:
        self.id = _id
        self.data = _data
    
    def __str__(self) -> str:
        return f"[INode]{self.id}, {self.data}"
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)