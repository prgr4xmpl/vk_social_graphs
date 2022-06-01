import json

class ILink:
    def __init__(self, _source : int, _target : int, _data = {}) -> None:
        self.source = _source
        self.target = _target
        self.data = _data
    
    def __str__(self) -> str:
        return f"[ILink]{self.source} -> {self.target}, {self.data}"
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)
    