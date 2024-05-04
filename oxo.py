class TreeNode:
    def __init__(self,datas,parent=None,deep=0,result=''):
        self.datas=datas
        self.children=[]
        self.parent=parent
        self.deep=deep
        self.result = result

    def add_child(self,datas):
        for data in datas:
            child = TreeNode(data,self,self.deep+1,self.result)
            self.children.append(child)


def get_moves(grid):
    r=[]
    for i in range(9):
        if grid[i]==".":
            r.append(i)
    return r

def game_status(grid):
    #vérifie les lignes horizontales
    for i in range(3):
        if grid[i*3]==grid[i*3+1]==grid[i*3+2]!=".":
            return grid[i*3]
    
    #vérifie les lignes vérticales
    for i in range(3):
        if grid[i]==grid[i+3]==grid[i+6]!=".":
            return grid[i]

    #vérifie la première diag
    if grid[0]==grid[4]==grid[8]!=".":
        return grid[0]
    
    #vérifie le seconde diag
    if grid[2]==grid[4]==grid[6]!=".":
        return grid[2]
    
    #vérifie si nul
    if not "." in grid:
        return "."

    return False






def main(grid,oxo,bot,player):
    #vérifie si position gagnante ou perdante
    #renvoi le symbole du gagnant
    status = game_status(grid)
    if status:
        oxo.result=status
        return status
    #ajoute les coup d'après
    moves = get_moves(grid)
    oxo.add_child(moves)

    #tente les coups
    for child in oxo.children:
        #joue le coup en fonction du joueur à qui c'est le tour
        
        if child.deep%2==0:
            grid[child.datas]="X"
        else:
            grid[child.datas]="0"
        
        main(grid,child,bot,player)

        if child.deep%2==0:
            grid[child.datas]="."
        else:
            grid[child.datas]="."
        
    #détérmine le result en fonction des fils
    children_result = []
    for child in oxo.children:
        children_result.append(child.result)
    
    bot_deep = 0
    if bot=="0":
        bot_deep=1

    #si prochain coup au joueur
    if oxo.deep%2==bot_deep:
        if player in children_result:
            oxo.result=player
        elif "." in children_result:
            oxo.result="."
        else:
            oxo.result=bot
    else:
        if bot in children_result:
            oxo.result=bot
        elif "." in children_result:
            oxo.result="."
        else:
            oxo.result=player
        

def print_grid(grid):
    print(f"{grid[0]} {grid[1]} {grid[2]}\n{grid[3]} {grid[4]} {grid[5]}\n{grid[6]} {grid[7]} {grid[8]}")



#partie
grid = [".",".",".",".",".",".",".",".","."]
x = input("qui commence la partie?\n1 pour vous\n0 pour nous ").replace(" ","")
while x!="1" and x!="0":
    x = input("qui commence la partie?\n1 pour vous\n0 pour nous ")

if x=="1":
    bot = "0"
    player = "X"
    move=input("où voulez vous placer votre X\n0 1 2\n3 4 5\n6 7 8\n")
    while not move.isdigit and 0<=int(move)<9:
        move=input("où voulez vous placer votre X\n0 1 2\n3 4 5\n6 7 8\n")
    
else:
    bot = "X"
    player = "0"
    move="4"

move=int(move)

grid[move]="X"
oxo = TreeNode(move)



main(grid,oxo,bot,player)


for i in range(1,10):
    print_grid(grid)
    game_statu = game_status(grid)
    if game_statu:
        if game_statu==bot:
            print("le bot a gagné")
        elif game_statu==player:
            print("vous avez gagné???")
        else:
            print("vous avez survécu,\nsurement un coup de chance LOL")
        break
    player_turn = "X"
    if i%2==1:
        player_turn = "0"

    #tour du joueur
    if player_turn==player:
        x=input("choisissez l'emplecement: ")
        while not x.isdigit() or not 0<=int(x)<=8 or not grid[int(x)]==".":
            x= input("choisissez un emplecement valide: ")
        x=int(x)
        #trouvle la branche dans l'arbre
        temp=None
        for child in oxo.children:
            if child.datas==x:
                temp=child
        oxo=temp
    #tour du bot
    else:
        temp=None
        for child in oxo.children:
            if child.result==bot:
                temp=child
        if temp==None:
            for child in oxo.children:
                if child.result==".":
                    temp=child
        x=temp.datas
        oxo=temp
        print(f"on joue {x}:")
    
    grid[x]=player_turn
    