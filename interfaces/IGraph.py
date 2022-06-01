import json
from .ILink import ILink
from .INode import INode

class IGraph:
    def __init__(self, _nodes : list[INode], _links : list[ILink], _data = {}) -> None:
        self.nodes = _nodes
        self.links = _links
        self.data = _data
        
    def __str__(self) -> str:
        return f"[IGraph] Nodes: {' '.join([str(node) for node in self.nodes])}" + '\n' + f"Links: {' '.join([str(link) for link in self.links])}"
    
    def add_node(self, node : INode) -> None:
        self.nodes.append(node)
        
    def add_link(self, link : ILink) -> None:
        self.links.append(link)
    
    def update_data(self, _data : dict) -> None:
        self.data.update(_data)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)    