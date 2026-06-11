from q2_word_usage import get_most_used, get_valid_chars
import time

# Lista não exaustiva de caracteres que podem aparecer nas palavras mais comuns
# list("abcdefghijklmnopqrstuvwxyzçáàâãäªéèêẽëíìîĩïóòôõöºúùũûüñ")       
VALID_CHARS = get_valid_chars()                                 # idx to char
LOOKUP = { VALID_CHARS[i]:i for i in range(len(VALID_CHARS))}   # char to idx


class TrieNode:
    def __init__(self, is_terminal=False):
        self.children = [None] * len(VALID_CHARS)
        self.terminal = is_terminal


class Trie:
    def __init__(self, words=[]):
        self.root = TrieNode()
        for w in words:
            self.insert(w)

    # Questão 2.1 
    def insert(self, word):
        if not word:
            raise ValueError("Invalid word. Canot include word with length 0 in the trie")
        try:
            self._insert_rec(self.root, word.lower())
        except:
            print(f"Caractere inválido na palavra: {word}")

    # Questap 2.2
    def search(self, word):
        # return self._as_nodes(word)
        return self._search_rec(self.root, word.lower())

    # Questão 2.3
    def remove(self, word):
        word = word.lower()
        nodes = self._as_nodes(word)
        if not nodes:
            return

        nodes[-1].terminal = False
        for i in range(len(nodes)-1, -1, -1):
            node = nodes[i]
            if node.terminal:
                return
            if any( x is not None for x in node.children ):
                return
            
            if i==0:
                self.root.children[0] = None
            else:
                nodes[i-1].children[LOOKUP[word[i]]] = None

    # Questao 2.5
    def autocomplete(self, word):
        nodes = self._as_nodes(word.lower())
        if not nodes:
            return None
        if nodes[-1].terminal:
            return word
        return word + self._nearest_terminal_path(nodes[-1])

    # PRIVATE METHODS

    # Questão 2.4
    def __str__(self):
        strs = []
        return "\n".join( self._get_words(self.root) )
        
    def _get_words(self, node, prefix=""):
        arr = []
        if node.terminal:
            arr.append(prefix)

        for key in range(len(VALID_CHARS)):
            if node.children[key] != None:
                rec = self._get_words( node.children[key], prefix+VALID_CHARS[key])
                arr.extend( rec )

        return arr

    def _insert_rec(self, node, str):
        if len(str) < 1:
            node.terminal = True
            return
        
        idx = LOOKUP[str[0]]
        if not node.children[idx]:
            node.children[idx] = TrieNode()
        
        self._insert_rec( node.children[idx], str[1:])

    def _search_rec(self, node, word):
        if node.terminal and not word:
            return True
        
        if not word:
            return False

        idx = LOOKUP[word[0]]
        if not node.children[idx]:
            return False

        return self._search_rec(node.children[idx], word[1:])
        
    def _as_nodes(self, word, node=None):
        "Retorna um array de nodes onde cada um representa um caracter da palavra fornescida"
        node = self.root if not node else node
        if not word:
            return []

        idx = LOOKUP[word[0]]
        if not node.children[idx]:
            return None
        
        following = self._as_nodes(word[1:], node.children[idx])  
        return [ node.children[idx], *following ] if following is not None else None

    def _nearest_terminal_path(self, node):
        to_visit = self._children_path(node, "")

        while len(to_visit) > 0:
            path, nd = to_visit[0]
            if nd.terminal:
                return path

            to_visit = [ *to_visit[1:], *self._children_path(nd, path) ]
        
    def _children_path(self, node, prefix=""):
        "Retorna uma lista contendo os filhos não nulos e seus respectivos caminhos (strings), incluindo o prefixo"
        return [ 
            (prefix + VALID_CHARS[idx], child) 
            for idx, child in enumerate(node.children) 
            if child is not None
        ]


# Questao 2.7
def test(name, size, iterations, busca, autocomplete):

    print(f"\n_______________________________________")
    print(f"INICIANDO TESTES: {name}")
    print(f"- Montando Trie com as {size} palavras mais usadas na lingua portuguesa.")
    palavras = get_most_used(size)
    t = Trie(palavras)
    print(f"- A palavra '{busca}' está entre elas? \t\t {t.search(busca)}")
    a = t.autocomplete(autocomplete)
    print(f"- Resultado do autocomplete para '{autocomplete}'   : \t '{a}'")
    print(f"- Removendo palavra '{a}' ...")
    t.remove(a)
    print(f"- Resultado do autocomplete para '{autocomplete}'   : \t '{t.autocomplete(autocomplete)}'")
    
    inicio = time.time()
    for i in range(iterations):
        t.search(palavras[-1]) # presume-se aqui que plavras menos utilizadas tendem a ser maiores (e por tanto mais demoram mais para serem encontradas)
    delta = time.time() - inicio
    print(f"- Tempo para buscar uma palavra {iterations} vezes : \t {(delta*100):.2f} s")

    return t
    

if __name__ == "__main__":  
    iterations = 10000
    t = test("1", 10, 10000, "você", "e")
    print(f"10 palavras mais utilizadas : \t { ', '.join(str(t).split('\n')) }")
    t = test("2", 100, 10000,"agora", "va")
    t = test("3", 1000, 10000, "ouro", "far")
    t = test("4", 10000, 10000, "python", "compu")

