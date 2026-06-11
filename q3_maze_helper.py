

from PIL import Image, ImageEnhance

IMAGE_PATH = "q3_maze.png"

def load_to_matrix(image_path, threshold=200, contrast_factor=2.0):
    # Função criada com auxilio de IA
    # Prompt utilizado:
    # """
    #   Give me a python script that contains a function that loads 
    #   a png and returns a 2d vector containing booleans. 
    #   0 for black pixels, 1 for white pixels 
    # """
    
    # Open the image and convert it to grayscale ('L' mode: 0-255)
    with Image.open(image_path) as img:
        grayscale_img = img.convert('L')

        # A melhoria de contraste foi adicionada separadamente para melhorar a performance da matris gerada
        # Para a imagem em fornescida em especifico, um treshold de 200 e um contrast_factor de 2 foi o ideal
        enhancer = ImageEnhance.Contrast(grayscale_img)
        grayscale_img = enhancer.enhance(contrast_factor)

        width, height = grayscale_img.size
        
        # Get flat pixel data
        pixels = list(grayscale_img.getdata())
        
        # Convert flat list into a 2D grid of booleans
        # True (1) if pixel is bright/white, False (0) if dark/black
        boolean_matrix = [
            [pixels[y * width + x] >= threshold for x in range(width)]
            for y in range(height)
        ]
        
        return boolean_matrix

# Funções criadas com auxilio de IA
# Prompt utilizado:
# """ 
#   python. Supose that i have a 2d  vector of booleans. implement the following functions:
#   evaluate_column -> says weather or not a given column is equal to the column on the right.
#   evaluate_row -> says weather or not a given row is equal to the row below
#   remove_column -> recieves a 2d array and returns a 2d array with that column removed
#   remove_row -> recieves a 2d array and returns a 2d array with that row removed
#   reduce_matrix -> iteratively evaluates and removes all rows and columns until the matrix (2d array) 
#   can no longer be reduced. then return the reduced matrix 
# """


def evaluate_column(matrix, col_idx):
    if not matrix or col_idx >= len(matrix[0]) - 1:
        return False
    return all(row[col_idx] == row[col_idx + 1] for row in matrix)


def evaluate_row(matrix, row_idx):
    if not matrix or row_idx >= len(matrix) - 1:
        return False
    return matrix[row_idx] == matrix[row_idx + 1]


def remove_column(matrix, col_idx):
    return [row[:col_idx] + row[col_idx + 1:] for row in matrix]


def remove_row(matrix, row_idx):
    return matrix[:row_idx] + matrix[row_idx + 1:]


def reduce_matrix(matrix):
    mat = [row[:] for row in matrix]
    changed = True
    
    while changed:
        changed = False
        
        # Reduce rows
        for r in range(len(mat) - 2, -1, -1):
            if evaluate_row(mat, r):
                mat = remove_row(mat, r)
                changed = True
                
        # Reduce columns
        if mat and mat[0]:
            for c in range(len(mat[0]) - 2, -1, -1):
                if evaluate_column(mat, c):
                    mat = remove_column(mat, c)
                    changed = True         
    return _trim(mat)


# As funções a seguir foram escritas pelo aluno:

def _trim(data):
    mat = [row[:] for row in data]
    changed = True
    
    while changed:
        changed = False
        # Tira espaço vazio na primeira e ultima linha
        if all(mat[0]):
            mat = remove_row(mat, 0)
            changed = True
        if all(mat[-1]):
            mat = remove_row(mat, len(mat)-1)
            changed = True
        
        # Tira espaçõ vazio na primeira e ultima coluna
        if all([ x[0] for x in mat] ):
            mat = remove_column(mat, 0)
            changed = True
        if all([ x[-1] for x in mat]):
            mat = remove_column(mat, len(mat[0])-1 )
            changed = True
    return mat

def get_start_finish(data):
    start = None
    end = None
    for i in range(1, len(data[0])):
        if data[0][i]:
            start = (0, i)

    for i in range(1, len(data[-1])):
        if data[-1][i]:
            end = (len(data[-1])-1, i )

    return start, end
    

def print_maze(data, char_map=None, path="  ", wall="██"):
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            if char_map and char_map.get((i, j)):
                print(char_map.get((i, j)), end="")
            elif row[j]:
                print(path, end="")
            else:
                print(wall, end="")
        print()

def print_matrix(matrix):
    print("   \t", end="")
    for j in range(len(matrix[0])):
        print(f"{j}"[0], end="  ")
    print()
    print("   \t", end="")
    for j in range(len(matrix[0])):
        print(f"{j}"[-1], end="  ")
    print()
    print()
    for i in range(len(matrix)):
        print(f"{i}:\t", end="")
        for j in range(len(matrix[i])):
            print( 1 if matrix[i][j] else 0, end=" |")
        print()
        

def get_maze():
    maze = load_to_matrix(IMAGE_PATH)
    return reduce_matrix(maze)



if __name__ == "__main__":
    maze = get_maze()
    start, end = get_start_finish(maze)

    PRINT_MAP={
        "start": "⭐" ,
        "finish": "🔴",
    }

    print("Renderizando labitinto...")
    print("Start: ", start)
    print("Finish: ", end)
    print_matrix(maze)
    # print_maze(maze, {}, start, end)