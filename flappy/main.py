import random
import pygame
import sys

class Bird(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__()
        self.frame1 = pygame.image.load('images/bird1.png')
        self.frame2 = pygame.image.load('images/bird2.png')
        self.frame1 = pygame.transform.scale(self.frame1, (50, 50))
        self.frame2 = pygame.transform.scale(self.frame2, (50, 50))
        self.frames = [self.frame1, self.frame2]
        self.frame_index = 0
        self.gravity = 0
        self.is_jumping = False
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (40, 230))

    def animate_bird(self): 
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): 
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
  
    def do_gravity(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            self.gravity = -7
        self.gravity += 1
        self.rect.y += self.gravity
          
    def update(self): 
        self.animate_bird()
        self.do_gravity()

class Tree_Top(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__()

        self.top1 = pygame.image.load('images/top1.png')
        self.top2 = pygame.image.load('images/top2.png')


        self.tree_top = [self.top1, self.top2]
        self.index = random.randint(0,1)
        
        self.image = self.tree_top[self.index]
        self.rect = self.image.get_rect(midtop = (500,0))

    def move_tree(self): 
        self.rect.x -= 5
        if self.rect.x <= -100: 
            self.kill()

    def update(self): 
        self.move_tree()

class Tree_Bottom(pygame.sprite.Sprite): 
    def __init__(self): 
        super().__init__()

        self.counted = False

        self.bottom1 = pygame.image.load('images/bottom1.png')
        self.bottom2 = pygame.image.load('images/bottom2.png')

        self.tree_bottom = [self.bottom1, self.bottom2]
        self.index = random.randint(0,1)

        self.image = self.tree_bottom[self.index]
        self.rect = self.image.get_rect(midbottom = (500,300))

    def move_tree(self): 
        self.rect.x -= 5
        if self.rect.x <= -100: 
            self.kill()

    def update(self): 
        self.move_tree()

def collision():
    if pygame.sprite.spritecollide(bird.sprite, treetop, False):
        treetop.empty()
        treebottom.empty()
        return False
    if pygame.sprite.spritecollide(bird.sprite, treebottom, False):
        treetop.empty()
        treebottom.empty()
        return False
    if bird.sprite.rect.y >= 280:
        return False
    return True

def reset_game():
    global bird, treetop, treebottom, game_active, score, start_time, passed
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())
    treetop.empty()
    treebottom.empty()
    score = 0
    passed = 0  
    game_active = False

def score_count(): 
    global passed
    for tree in treebottom:
        if tree.rect.x < -50 and not tree.counted:  
            passed += 1
            tree.counted = True  
    scorescreen = test_font.render(f'score: {passed}', False, (255,255,255))
    score_rect = scorescreen.get_rect(center = (150,340))
    screen.blit(scorescreen, score_rect)
    return passed


pygame.init()
screen = pygame.display.set_mode((300,400))
clock = pygame.time.Clock()

game_active = False
passed = 0
score = 0


# fonts
test_font = pygame.font.Font(None, 30)

ground = pygame.image.load('images/ground.png')
sky = pygame.image.load('images/sky.png')
sky_scaled = pygame.transform.scale(sky, (300, 300))

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

treetop = pygame.sprite.Group()
treebottom = pygame.sprite.Group()

# timer
tree_top_timer = pygame.USEREVENT + 1
pygame.time.set_timer(tree_top_timer, 1500)

tree_bottom_timer = pygame.USEREVENT + 2
pygame.time.set_timer(tree_bottom_timer, 1500)

while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                reset_game()
                game_active = True

        if event.type == tree_top_timer: 
            treetop.add(Tree_Top())

        if event.type == tree_bottom_timer: 
            treebottom.add(Tree_Bottom())
    
    if game_active:   
        bird.update()
        treetop.update()
        treebottom.update()
        screen.fill((0, 0, 0)) 
        
        screen.blit(ground, (0,300))
        screen.blit(sky_scaled, (0,0))
        bird.draw(screen)
        treetop.draw(screen)
        treebottom.draw(screen)

        if bird.sprite.rect.y >= 300: 
            game_active = False

        game_active = collision()
        score = score_count()
    else: 
        screen.fill((255,255,255))
        bird_image = pygame.image.load('images/bird1.png')
        bird_image = pygame.transform.scale(bird_image, (200, 200))
        bird_rect = bird_image.get_rect(center = (150,200))
        screen.blit(bird_image, bird_rect)
        
        if score == 0: 
            message = test_font.render('space bar for play', False, (0,0,0))
            mesrect = message.get_rect(center = (150,340))
            screen.blit(message, mesrect)
        else: 
            score_message = test_font.render(f'score: {score}', False, (0,0,0))
            score_message_rect = score_message.get_rect(center = (150,340))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
