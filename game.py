
import random
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_TAIL = (255, 153, 153)
BLUE = (0, 0, 255)
BLUE_TAIL = (153, 153, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 0, 127)

class GridObject:
    def __init__(self, x, y, game, color):
        self.game = game
        self.active = True
        self.color = color
        self.x = x
        self.y = y

    def handle_event(self, event):
        pass

    def draw(self):
        block_size = self.game.block_size
        pygame.draw.rect(self.game.display, self.color, [self.x*block_size, self.y*block_size, block_size, block_size])

class Player1(GridObject):
    dx = 0
    dy = 0

    def __init__(self, x, y, game, color):
        self.color = color
        super().__init__(x, y, game, self.color)
        self.direction = ''

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.dx = -1
                self.dy = 0
                self.direction = 'W'
            elif event.key == pygame.K_d:
                self.dx = 1
                self.dy = 0
                self.direction = 'E'
            elif event.key == pygame.K_w:
                self.dy = -1
                self.dx = 0
                self.direction = 'N'
            elif event.key == pygame.K_s:
                self.dy = 1
                self.dx = 0
                self.direction = 'S'

class Player2(GridObject):
    dx = 0
    dy = 0

    def __init__(self, x, y, game, color):
        self.color = color
        super().__init__(x, y, game, self.color)
        self.direction = ''

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dx = -1
                self.dy = 0
                self.direction = 'W'
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
                self.dy = 0
                self.direction = 'E'
            elif event.key == pygame.K_UP:
                self.dy = -1
                self.dx = 0
                self.direction = 'N'
            elif event.key == pygame.K_DOWN:
                self.dy = 1
                self.dx = 0
                self.direction = 'S'

class Food(GridObject):
    colors = [GREEN, PINK, YELLOW]

    def __init__(self, game):
        self.color = random.choice(Food.colors)
        x = random.randint(game.blank+1, game.n_cols+game.blank-2)
        y = random.randint(game.blank+1, game.n_rows+game.blank-2)
        super().__init__(x, y, game, self.color)


class Game:
    block_size = 10

    def __init__(self, n_rows, n_cols, blank):
        pygame.init()
        self.start_time = pygame.time.get_ticks()
        self.display = pygame.display.set_mode(((n_cols+blank*2)*self.block_size, (n_rows+blank*2)*self.block_size))
        self.display_x, self.display_y = (n_cols+blank*2)*self.block_size, (n_rows+blank*2)*self.block_size
        self.blank = blank
        self.n_rows = n_rows
        self.n_cols = n_cols
        pygame.display.set_caption('DCCP Snake Game')
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.p1 = []
        self.p2 = []
        self.foods = []
        self.direction1 = ''
        self.direction2 = ''
        self.reset = 0
        self.grow_number1 = 0
        self.grow_number2 = 0
        self.font = pygame.font.Font(None, 20)
        self.font2 = pygame.font.Font(None, 30)
        self.p1_lose = False
        self.p2_lose = False
        self.color_dict = {GREEN: 1, PINK: 2, YELLOW: 3}
        self.blank2 = self.blank*self.block_size
        self.cols = self.n_cols*self.block_size
        self.rows = self.n_rows*self.block_size
        self.end_status=False

    #https://jbmpa.com/pygame/9
    def write(self):
        text1 = self.font.render("1                      2                     3", True, WHITE)
        text4 = self.font.render("P1(RED):  "+str(len(self.p1))+" vs P2(BLUE):  "+str(len(self.p2)), True, WHITE)
        text_rect = text4.get_rect(center=((self.n_cols+self.blank*2)*self.block_size/2, (self.n_rows+self.blank*2)/2))
        self.display.blit(text1, [self.display_x/2-80, self.display_y-30])
        pygame.draw.rect(self.display, GREEN, [self.display_x/2-100, self.display_y-30, self.block_size, self.block_size])
        pygame.draw.rect(self.display, PINK, [self.display_x/2-10, self.display_y-30, self.block_size, self.block_size])
        pygame.draw.rect(self.display, YELLOW, [self.display_x/2+80, self.display_y-30, self.block_size, self.block_size])
        self.display.blit(text4, text_rect)

    def add_food1(self):
        new_food = Food(self)
        for obj in self.p1+self.foods:
            if obj.x == new_food.x and obj.y == new_food.y:
                break
        else:
            self.foods.append(new_food)

    def add_food2(self):
        new_food = Food(self)
        for obj in self.p2+self.foods:
            if obj.x == new_food.x and obj.y == new_food.y:
                break
        else:
            self.foods.append(new_food)

    
    def grow1(self, grow_number1):
        obj = self.p1[-1]
        for i in range(grow_number1):
            self.p1.append(Player1(obj.x-self.dx1, obj.y-self.dy1, self, RED_TAIL))
            self.p1[-1].direction = self.p1[0].direction
            self.p1[-1].dx = self.p1[0].dx
            self.p1[-1].dy = self.p1[0].dy


    def grow2(self, grow_number2):
        obj = self.p2[-1]
        for i in range(grow_number2):
            self.p2.append(Player2(obj.x-self.dx2, obj.y-self.dy2, self, BLUE_TAIL))
            self.p2[-1].direction = self.p2[0].direction
            self.p2[-1].dx = self.p2[0].dx
            self.p2[-1].dy = self.p2[0].dy
            self.grow_number2-=1


    
    
    def tick1(self, obj1):
        if len(self.p1) == 1:
            if (self.dx1 == self.dy1 == 0):
                if (obj1.direction == 'W'):
                    self.dx1 = -1
                elif (obj1.direction == 'E'):
                    self.dx1 = 1
                elif (obj1.direction == 'N'):
                    self.dy1 = -1
                elif (obj1.direction == 'S'):
                    self.dy1 = 1
            obj1.x += self.dx1
            obj1.y += self.dy1
        else:
            obj1.color = RED_TAIL
            if (self.dx1 == self.dy1 == 0):
                if (obj1.direction == 'W'):
                    self.dx1 = -1
                elif (obj1.direction == 'E'):
                    self.dx1 = 1
                elif (obj1.direction == 'N'):
                    self.dy1 = -1
                elif (obj1.direction == 'S'):
                    self.dy1 = 1
            self.p1[0].color = RED_TAIL
            self.p1 = [Player1(obj1.x+self.dx1, obj1.y+self.dy1, self, RED)]+self.p1[:-1]
            self.p1[0].direction = obj1.direction
            self.p1[0].dx = obj1.dx
            self.p1[0].dy = obj1.dy

    def tick2(self, obj2):
        if len(self.p2) == 1:
            if (self.dx2 == self.dy2 == 0):
                if (obj2.direction == 'W'):
                    self.dx2 = -1
                elif (obj2.direction == 'E'):
                    self.dx2 = 1
                elif (obj2.direction == 'N'):
                    self.dy2 = -1
                elif (obj2.direction == 'S'):
                    self.dy2 = 1
            obj2.x += self.dx2
            obj2.y += self.dy2
        else:
            self.p2[0].color = BLUE_TAIL
            self.p2 = [Player2(obj2.x+self.dx2, obj2.y + self.dy2, self, BLUE)]+self.p2[:-1]
            self.p2[0].direction = obj2.direction
            self.p2[0].dx = obj2.dx
            self.p2[0].dy = obj2.dy

    #reduce per 7 seconds
    def reduce(self, playtime):
        if playtime > 7:
            self.reset += 1
            if len(self.p1) > 1:
                del self.p1[-1]
            if len(self.p2) > 1:
                del self.p2[-1]

    def draw_line(self, x1, y1, x2, y2):
        pygame.draw.line(self.display, WHITE, (x1, y1), (x2, y2), 1)

    def play(self, n_foods=20):
        self.p1 = [Player1((self.n_cols/4+self.blank), (self.n_rows/2+self.blank), self, RED)]
        self.p2 = [Player2((self.n_cols/4*3+self.blank), (self.n_rows/2+self.blank), self, BLUE)]

        while (len(self.foods) < n_foods):
            new = Food(self)
            if self.foods == False:
                self.foods.append(new)
                continue
            for food in self.foods:
                if food.x == new.x and food.y == new.y:
                    break
                elif self.p1[0].x == new.x and self.p1[0].y == new.y:
                    break
                elif self.p2[0].x == new.x and self.p2[0].y == new.y:
                    break
            else:
                self.foods.append(new)

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                #handle event
                for obj in self.p1:
                    obj.handle_event(event)
                    self.direction1 = obj.direction
                    self.dx1 = obj.dx
                    self.dy1 = obj.dy
                for obj in self.p2:
                    obj.handle_event(event)
                    self.direction2 = obj.direction
                    self.dx2 = obj.dx
                    self.dy2 = obj.dy

            #tick
            self.tick1(self.p1[0])
            self.tick2(self.p2[0])
            playtime = (pygame.time.get_ticks() - self.start_time)/700-7*self.reset
            self.reduce(playtime)

            #interact
            head1 = self.p1[0]
            for idx, obj1 in enumerate(self.foods):
                if head1.active and obj1.active:
                    if head1.x == obj1.x and head1.y == obj1.y:
                        self.grow_number1 = self.color_dict[obj1.color]
                        del self.foods[idx]
                        self.add_food1()
                        self.grow1(self.grow_number1)
            

            head2 = self.p2[0]
            for idx, obj2 in enumerate(self.foods):
                if head2.active and obj2.active:
                    if head2.x == obj2.x and head2.y == obj2.y:
                        self.grow_number2 = self.color_dict[obj2.color]
                        del self.foods[idx]
                        self.add_food2()
                        self.grow2(self.grow_number2) 
                        
            
                       

            #draw
            self.display.fill(BLACK)
            self.draw_line(self.blank2, self.blank2, self.cols+self.blank2, self.blank2)
            self.draw_line(self.cols+self.blank2, self.blank2, self.cols+self.blank2, self.rows+self.blank2)
            self.draw_line(self.cols+self.blank2, self.rows + self.blank2, self.blank2, self.rows+self.blank2)
            self.draw_line(self.blank2, self.rows+self.blank2, self.blank2, self.blank2)
            self.write()

            for obj in self.p1:
                if obj.active:
                    obj.draw()

            for obj in self.p2:
                if obj.active:
                    obj.draw()

            for obj in self.foods:
                if obj.active:
                    obj.draw()

            #gameover
            for i in self.p1:
                #p2 win
                if i.x <= self.blank or i.x >= self.n_cols+self.blank-1:
                    self.p1_lose = True
                elif i.y <= self.blank or i.y >= self.n_rows+self.blank-1:
                    self.p1_lose = True

            for i in self.p2:
                #p1 win
                if i.x <= self.blank or i.x >= self.n_cols+self.blank-1:
                    self.p2_lose = True
                elif i.y <= self.blank or i.y >= self.n_rows+self.blank-1:
                    self.p2_lose = True

            if len(self.p1) >= 24:
                self.p2_lose = True
            if len(self.p2) >= 24:
                self.p1_lose = True

            #몸 충돌
            for i in self.p1[1:]:
                if self.p2[0].x == i.x and self.p2[0].y == i.y:
                    self.p2_lose = True
                    break
            for i in self.p2[1:]:
                if self.p1[0].x == i.x and self.p1[0].y == i.y:
                    self.p1_lose = True
                    break

            #head 충돌
            if self.p1[0].x == self.p2[0].x and self.p1[0].y == self.p2[0].y:
                if len(self.p1) > len(self.p2):
                    self.p1_lose = True

                elif len(self.p1) < len(self.p2):
                    self.p2_lose = True

                elif len(self.p1) == len(self.p2):
                    self.p1_lose = True
                    self.p2_lose = True

            #head 교차
            case=[]
            if self.p1[0].x==self.p2[0].x and int(self.p1[0].y-self.p2[0].y)==-1 and self.p1[0].direction=='S' and self.p2[0].direction=='N':
                case.append('1')
                print(case)
            if self.p1[0].x==self.p2[0].x and int(self.p1[0].y-self.p2[0].y)==1 and self.p1[0].direction=='N' and self.p2[0].direction=='S':
                case.append('1')    
            if int(self.p1[0].x-self.p2[0].x)==-1 and self.p1[0].y==self.p2[0].y and self.p1[0].direction=='E' and self.p2[0].direction=='W':
                case.append('1')   
            if int(self.p1[0].x-self.p2[0].x)==1 and self.p1[0].y==self.p2[0].y and self.p1[0].direction=='W' and self.p2[0].direction=='E':
                case.append('1')


            


            self.clock.tick(5)
            pygame.display.update()
            
        
            
            if self.p1_lose and self.p2_lose:
                end = 'Tie'
                self.game_over = True
                self.end_status=True
            elif self.p1_lose:
                end = 'P2(BLUE) win'
                self.game_over = True
                self.end_status=True
            elif self.p2_lose:
                end = 'P1(RED) win'
                self.game_over = True
                self.end_status=True
                
            for i in range(len(case)):
                if case[i]=='1':
                    if len(self.p1)>len(self.p2):
                        self.p1_lose=True
                    elif len(self.p1)<len(self.p2):
                        self.p2_lose=True
                    elif len(self.p1)==len(self.p2):
                        self.p1_lose=True
                        self.p2_lose=True   
            
            
            
            

        while self.end_status:
            end_message = self.font2.render(end, True, WHITE)
            text_rect = end_message.get_rect(center=((self.n_cols+self.blank*2)*self.block_size/2, (self.n_rows+self.blank*2)*self.block_size/2))
            self.display.blit(end_message, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_status= False
                    break

        

if __name__ == "__main__":
    Game(n_cols=80, n_rows=40, blank=5).play(n_foods=20)
