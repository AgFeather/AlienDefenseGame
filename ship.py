import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, game_setting, screen):
        '''初始化飞船并设置'''
        super(Ship, self).__init__()
        self.screen = screen
        self.game_setting = game_setting

        # 加载飞船图像并获得其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect =  self.image.get_rect() # 获取图片的矩形框
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx # 飞船中心坐标等于屏幕中心坐标
        self.rect.bottom = self.screen_rect.bottom # 飞船下边缘坐标等于屏幕下边缘
        self.center = float(self.rect.centerx) # 将centerx转换为float

        # 移动标志
        self.moving_right = False
        self.moving_left = False


    def update(self):
        '''根据移动标识调整飞船的位置'''
        if self.moving_right and self.rect.right < self.screen_rect.right: # 控制不出屏幕的右边
            self.center += self.game_setting.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.game_setting.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center


    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx