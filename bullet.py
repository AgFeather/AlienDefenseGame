import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''一个队飞船发射的子弹进行管理的类，子弹类继承自Sprite，Sprite可以将游戏中相关的元素编组，进而同时操作编组中的所有元素'''

    def __init__(self, game_setting, screen, ship):
        '''在飞船所在位置的创建一个子弹对象'''
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再移动到正确的位置
        self.rect = pygame.Rect(0, 0, game_setting.bullet_width, game_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹的位置
        self.y = float(self.rect.y)
        self.color = game_setting.bullet_color
        self.speed_factor = game_setting.bullet_speed_factor

    def update(self):
        """更新子弹状态，相当于向上移动子弹"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
