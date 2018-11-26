import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """外星人类"""
    def __init__(self, game_setting, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.game_setting = game_setting

        # 加载外星人图像，并设置rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个尾箱人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True
        return False

    def update(self):
        """移动外星人"""
        self.x += self.game_setting.fleet_direction * self.game_setting.alien_speed_factor
        self.rect.x = self.x