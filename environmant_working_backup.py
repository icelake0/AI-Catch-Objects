import pygame, sys, random

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, score_time, score_color
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.left <= 0 or ball.right >= screen_width:
		ball_speed_x *= -1

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1

	if ball.bottom >= screen_height:
		score_time = pygame.time.get_ticks()
		player_score -= 10
		score_color = pygame.Color('red')
		ball_speed_y *= -1
	
	if ball.colliderect(player):
		score_time = pygame.time.get_ticks()
		player_score += 10
		score_color = pygame.Color('green')
		ball_speed_y *= -1
		

def player_animation():
	player.x += player_speed

	if player.left <= 0:
		player.left = 0
	if player.right >= screen_width:
		player.right = screen_width

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time, score_color

	ball.center = (random.choice(range(20, screen_width - 20)), 20)
	current_time = pygame.time.get_ticks()

	if current_time - score_time < 700:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7
		score_color = pygame.Color('gray')
		score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Storage')

# Colors
light_grey = (200,200,200)
package_color = (176, 145, 110)
bg_color = pygame.Color('grey12')
score_color = pygame.Color('gray')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width /2- 70, screen_height - 20 , 140,10)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7
player_speed = 0
ball_moving = False
score_time = True

# Score Text
player_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 16)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player_speed -= 6
			if event.key == pygame.K_RIGHT:
				player_speed += 6
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player_speed += 6
			if event.key == pygame.K_RIGHT:
				player_speed -= 6
	
	#Game Logic
	ball_animation()
	player_animation()

	# Visuals 
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, package_color, ball)

	if score_time:
		ball_start()

	player_text = basic_font.render(f'{player_score}',False,score_color)
	screen.blit(player_text,(screen_width/2 -20, screen_height/2))

	pygame.display.flip()
	clock.tick(60)
