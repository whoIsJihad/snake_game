import pygame
import time
import random
from constants import *
class Game:
    def __init__(self,food,grid,snake):
       self.food=food 
       self.grid=grid 
       self.snake=snake

    def check_collision(self):
        snake_head=self.snake.segments[0]
        # checking collision with walls
        if snake_head[0]<0 or snake_head[0]>GRID_ROWS-1:
            return True
        elif snake_head[1]<0 or snake_head[1]>GRID_COLS-1:
            return True
        
        unique_elements = set(self.snake.segments)
        
        return len(unique_elements) != len(self.snake.segments)
    def check_food_hit(self):
        snake_head=self.snake.segments[0]
        foods=self.food.food_position_set
        print(snake_head,foods)
        if snake_head in foods:
            foods.remove(snake_head)
            # add another food
            added=False
            while not added:
                
                rand_x=random.randint(0,GRID_ROWS-1)
                rand_y=random.randint(0,GRID_COLS-1)
                if not (rand_x,rand_y) in self.snake.segments_set:
                    foods.add((rand_x,rand_y))
                    added=True
            self.food.food_position=list(foods)
            self.snake.segments.append(self.snake.last_tail_position)
            self.snake.segments_set.add(self.snake.last_tail_position)
            self.snake.score=self.snake.score+1
class Food:
    def __init__(self):
        self.food_position=[(random.randint(0,GRID_ROWS-1),random.randint(0,GRID_ROWS-1)) for _ in range(NUM_FOODS)]
        self.color=GREEN
        self.size = CELL_SIZE-5
        self.food_position_set=set(self.food_position)


    def render(self,window):
        for i in range(len(self.food_position)):
            pygame.draw.rect(window,self.color,(self.food_position[i][0]*CELL_SIZE, self.food_position[i][1]*CELL_SIZE,self.size,self.size))
    



class Grid:
    def __init__(self):
        self.ROWS=GRID_ROWS
        self.COLS=GRID_COLS
        self.CELL_SIZE=CELL_SIZE
        self.color= GREY
    

    def render(self,window):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                pygame.draw.rect(window,self.color,(j*(self.CELL_SIZE),i*(self.CELL_SIZE),self.CELL_SIZE-1,self.CELL_SIZE-1))



class Snake:
    def __init__(self,initial_position):
        self.color=BLUE
        self.size= CELL_SIZE-5
        self.segments=[]+initial_position
        self.segments_set=set(self.segments)
        self.direction=RIGHT
        self.score=0
        self.last_tail_position=()

    def render(self,window):
        for (i,j) in self.segments:
            pygame.draw.rect(window,self.color,(i*(CELL_SIZE),j*(CELL_SIZE),self.size,self.size))

    
    def update_position(self):
        n=len(self.segments)

        self.last_tail_position=self.segments[n-1]

        for i in range(n-1,0,-1):
            self.segments[i]=self.segments[i-1]
        
        if self.direction == DOWN:
            self.segments[0] = (self.segments[0][0], self.segments[0][1] + 1)

        elif self.direction ==UP :

            self.segments[0]=(self.segments[0][0],self.segments[0][1]-1)

        elif self.direction== LEFT:
            self.segments[0]=(self.segments[0][0]-1,self.segments[0][1])

        elif self.direction ==RIGHT:
            self.segments[0]=(self.segments[0][0]+1,self.segments[0][1])
            
        self.segments_set=set(self.segments)

    def handle_input(self,event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and self.direction!=DOWN and self.direction!=UP:
                self.direction=DOWN
            elif event.key==pygame.K_UP and self.direction!=DOWN and self.direction!=UP:
                self.direction=UP

            elif event.key==pygame.K_LEFT and self.direction!=RIGHT and self.direction!=LEFT:
                self.direction=LEFT
            elif event.key==pygame.K_RIGHT  and self.direction!=RIGHT and self.direction!=LEFT:
                self.direction=RIGHT
            else :
                return
    

def game_init():
    initial_position=[(1,1),(1,2)]
    game_board=Grid()
    snake = Snake(initial_position=initial_position)
    food= Food()
    game=Game(food=food,grid=game_board,snake=snake)
    return game

def game_render(game,window):
    game.grid.render(window=window)
    game.snake.render(window=window)
    game.food.render(window=window)

def terminate_render(game,window,score):
    font = pygame.font.Font(None, 50)
    ended = font.render("GAME ENDED ", True,BLACK)
    score = font.render(f"SCORE : {score} ", True,BLACK)
    window.blit(ended, (200, 240))
    window.blit(score, (200, 280))
# initializing imported module
pygame.init()
game=game_init()
window=pygame.display.set_mode((WINDOW_SIZE,WINDOW_SIZE))
window.fill((255,255,255))   # white background
running = True
clock=pygame.time.Clock()
elapsed=0
interval=400
while running:
    dt=clock.tick(60)
    for event in pygame.event.get():
        
        # if event is of type quit then 
        # set running bool to false
        if event.type == pygame.QUIT:
            running = False
        else :
            game.snake.handle_input(event)
    if elapsed>interval :
        elapsed=0
        interval=interval*0.99
        game.snake.update_position()
    else :
        elapsed+=dt

    game.check_food_hit()
    game_render(game,window)
    if game.check_collision()==True:
        terminate_render(game,window,game.snake.score)
        pygame.display.update()
        time.sleep(3)
        running=False
    pygame.display.update()

    