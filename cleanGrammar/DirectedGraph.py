class DirectedGraph:
    ''' G = (E, V) '''
    def __init__(self):
        self.adj = dict()

    '''
    def exists_node(node): 
        def decorator(fun):
            def wrapper(*args, **kwargs):
                assert node in self.adj
                result = fun(*args, **kwargs)
                return result
            return wrapper
        return decorator
    '''

    def edges(self):
        conjunto = set()
        for a in self.adj:
            for b in self.adj[a]:
                conjunto.add((a, b))
        return conjunto 

    def vertices(self):
        return self.adj.keys()

    def remove_edge(self, u, v):
        assert u in self.adj
        if v in self.adj[u]: 
            self.adj[u].remove(v) 

    def add_edge(self, u, v = None):
        if u not in self.adj: 
            self.adj[u] = list() 
        if v != None: 
            if not v in self.adj:
                self.adj[v] = list()
            self.adj[u].append(v) 

    def has_edge(self, u, v):
        assert u in self.adj
        return v in self.adj[u]

    def out_edges(self, u):
        assert u in self.adj
        return self.adj[u]

    def in_edges(self, u):
        edges = list()
        for key in self.adj:
            if u in self.adj[key]: 
                edges.append(key) 
        return edges

    def has_next(self, u):
        assert u in self.adj
        return len(self.adj[u]) > 0

    def loop(self, u):
        assert u in self.adj
        return u in self.adj[u]

    def vertices_forward(self, u):
        vertices = set()
        visited = { x: False for x in self.adj }

        def helper(v):
            for value in self.adj[v]:
                vertices.add(value)
                if self.has_next(value) and not visited[value]: 
                    visited[value] = True
                    helper(value)

        assert u in self.adj
        helper(u)
        return vertices - set(u)