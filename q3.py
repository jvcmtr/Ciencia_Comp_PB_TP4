from q3_maze_helper import get_maze, get_start_finish, print_maze
from time import perf_counter


class Graph:
    def __init__(self, edges, USE_OPTIMIZATION=False):
        """
        'node' aqui pode ser qualquer tipo hasheavel.
        'edges' deve ser uma lista de tuplas, cada item da tupla sendo um node. 
        'USE_OPTIMIZATION' omite/remove nodes que possuam duas ou menos conexões
        """
        self.data = {}
        for e in edges:
            self.add_edge(e)
        if USE_OPTIMIZATION:
            self._optimize()

    def _optimize(self):
        # Não iterar sobre o array original pois vamos alteralo durante a iteração
        items = [*self.data.items()]

        for k, v in items:
            if len(v) == 2:
                # Pegar valores atualizados
                true_val = self.data[k]
                self.remove_node(k)
                self.add_edge(list(true_val))
        # Se nessa função nós removessemos todos os nodes com 1 conexão (becos sem saida), com
        # exeção do inicio e do fim, resolveriamos o labirinto. Apesar de ser uma forma bem ineficiente 

    def remove_node(self, node):
        self.data.pop(node)
        for k, v in self.data.items():
            self.data[k] = set([x for x in v if x != node])

    def add_edge(self, e):
        if not self.data.get(e[0]):
            self.data[e[0]] = set()
        if not self.data.get(e[1]):
            self.data[e[1]] = set()

        self.data[e[0]].add(e[1])
        self.data[e[1]].add(e[0])
        
    def get_conected(self, node):
        return self.data[node]

    def bfs(self, start, finish):
        # Identico ao DFS, mas é LIFO em vez de FIFO
        seen = {}
        to_see = [ (start, [])  ] # (node, caminho)
        
        while len(to_see) > 0:
            node, path = to_see.pop()
            seen[node] = True

            if node == finish:
                return path, len(seen.items())

            discovered = self.get_conected(node) 
            to_see.extend([
                (x, [*path, node]) for x in discovered
                if seen.get(x) == None
            ])

        return None, len(seen.items())

    def dfs(self, start, finish):
        # Identico ao BFS, mas é FIFO em vez de LIFO (fila em vez de pilha)
        seen = {}
        to_see = [ (start, [])  ] # (node, caminho)
        
        while len(to_see) > 0:
            node, path = to_see[0]
            to_see = to_see[1:]
            seen[node] = True

            if node == finish:
                return path, len(seen.items())

            discovered = self.get_conected(node) 
            
            to_see.extend([
                (x, [*path, node]) for x in discovered
                if seen.get(x) == None
            ])

        return None, len(seen.items())

    def get_all_edges(self, complement=True):
        e = {}
        for k, v in self.data.items():
            for node in v:
                if e.get((node, k)) and not complement:
                    continue
                e[(k, node)] = True
 
        return [ k for k, v in e.items()]

    def get_all_nodes(self):
        return [k for k,v in self.data.items() ]



def matrix_to_edges_list(data):
    edges = []

    def get_in_bound(row, col):
        if not ( row>=0 and row<len(data)):
            return False
        if not( col>=0 and col<len(data[row])):
            return False
        return (row, col) if data[row][col] else False

    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            cell = get_in_bound(i, j)
            right = get_in_bound(i, j+1)
            down = get_in_bound(i+1, j)
            if right and cell:
                edges.append( (cell, right) )
            if down and cell:
                edges.append( (cell, down) )
    return edges


# TESTE E EXIBIÇÃO

def timed(calable):
    start = perf_counter()
    result = calable()
    end = perf_counter() - start
    return result, end

def test_graph(graph, start, finish, name):
    print("____________________________________________")
    print(f"-------  {name}  -----")
    
    print(f"+ Num edges \t: {len(graph.get_all_edges(False))}")  
    print(f"+ Num nodes \t: {len(graph.get_all_nodes())}") 
    (bfs, bfs_seen), bfs_delta = timed(lambda: graph.bfs(start, finish))
    (dfs, dfs_seen), dfs_delta = timed(lambda: graph.dfs(start, finish))
    print(f"+ BFS solution \t: {len(bfs)} nodes")
    print(f"+ DFS solution \t: {len(dfs)} nodes")
    
    print(f"+ BFS seen \t: {bfs_seen} nodes seen during search")
    print(f"+ DFS seen \t: {dfs_seen} nodes seen during search")

    print(f"+ BFS duration\t: {bfs_delta*1000:6f} ms")
    print(f"+ DFS duration\t: {dfs_delta*1000:6f} ms")

    # print(" --------------------------------------------- ")

    return bfs, bfs_delta, dfs_delta,  
      


if __name__ == "__main__":
    print("______________________________________")
    
    matrix = get_maze()
    start, finish = get_start_finish(matrix)
    edges = matrix_to_edges_list(matrix)
    graph = Graph(edges)
    graph_o = Graph(edges, True)
    path = graph.bfs(start, finish)

    def print_map(name = "MAZE", allnodes="  ", optimized_nodes="  ", ipath="  ", ifinish="⭐", istart="🔵",):   

        print("______________________________________")
        print(f" ---- {name} ----")

        CHAR_MAP={
            **{k:allnodes for k in graph.get_all_nodes()}, 
            **{k:optimized_nodes for k in graph_o.get_all_nodes()}, 
            **{k:ipath for k in path}, 
            start: istart,
            finish: ifinish ,
        }
        print_maze(matrix, CHAR_MAP)
        print("-----------------------------------------")

    path, a,b = test_graph(graph, start, finish, "TESTE COM MAPA NÃO OTIMIZADO")
    
    path_o, a,b = test_graph(graph_o, start, finish, "TESTE COM MAPA OTIMIZADO")
    
    print_map("NODES NA VERSAO OTIMIZADA", optimized_nodes="🔴")
    print_map("RESOLUÇÃO", ipath="🔴")

    

