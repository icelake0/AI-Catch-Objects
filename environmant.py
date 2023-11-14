import pygame, sys, random


class FragilePackagesStore:
    def __init__(self):
        self.setup_store()

        # Packages that falls randomly
        self.package = pygame.Rect(
            self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30
        )
        
        # Net for catching package
        self.net = pygame.Rect(
            self.screen_width / 2 - 70, self.screen_height - 20, 140, 10
        )

        # Environment Variables
        self.package_speed_x = 7 * random.choice((1, -1))
        self.package_speed_y = 7
        self.net_speed = 0
        self.package_moving = False
        self.score_time = True

        # Score Text
        self.net_score = 0
        self.basic_font = pygame.font.Font("freesansbold.ttf", 50)
    
    def setup_store(self):
        # General setup
        pygame.mixer.pre_init(44100, -16, 1, 1024)
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # Main Window
        self.screen_width = 900
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Storage")
        
        # Colors
        self.light_grey = (200, 200, 200)
        self.package_color = (176, 145, 110)
        self.bg_color = pygame.Color("grey12")
        self.score_color = pygame.Color("gray")
        
        
    def setup_package(self):
        self.package.x += self.package_speed_x
        self.package.y += self.package_speed_y

        if self.package.left <= 0 or self.package.right >= self.screen_width:
            self.package_speed_x *= -1

        if self.package.top <= 0 or self.package.bottom >= self.screen_height:
            self.package_speed_y *= -1

        if self.package.bottom >= self.screen_height:
            self.score_time = pygame.time.get_ticks()
            self.net_score -= 10
            self.score_color = pygame.Color("red")
            self.package_speed_y *= -1

        if self.package.colliderect(self.net):
            self.score_time = pygame.time.get_ticks()
            self.net_score += 10
            self.score_color = pygame.Color("green")
            self.package_speed_y *= -1

    def move_net(self):
        self.net.x += self.net_speed

        if self.net.left <= 0:
            self.net.left = 0
        if self.net.right >= self.screen_width:
            self.net.right = self.screen_width

    def drop_package(self):
        self.package.center = (random.choice(range(20, self.screen_width - 20)), 20)
        current_time = pygame.time.get_ticks()

        if current_time - self.score_time < 700:
            self.package_speed_y, self.package_speed_x = 0, 0
        else:
            self.package_speed_x = 7 * random.choice((1, -1))
            self.package_speed_y = 7
            self.score_color = pygame.Color("gray")
            self.score_time = None

    def monitor_store(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.net_speed -= 6
                    if event.key == pygame.K_RIGHT:
                        self.net_speed += 6
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.net_speed += 6
                    if event.key == pygame.K_RIGHT:
                        self.net_speed -= 6

            self.setup_package()
            self.move_net()

            # Visuals
            #self.screen.fill(self.bg_color)
            bg = pygame.image.load("package_store.jpg")
            self.screen.blit(bg, (0, 0))
            pygame.draw.rect(self.screen, self.light_grey, self.net)
            pygame.draw.rect(self.screen, self.package_color, self.package)

            if self.score_time:
                self.drop_package()

            net_text = self.basic_font.render(
                f"{self.net_score}", False, self.score_color
            )
            self.screen.blit(
                net_text, (self.screen_width / 2 - 20, self.screen_height / 2)
            )

            pygame.display.flip()
            self.clock.tick(60)


store = FragilePackagesStore().monitor_store()