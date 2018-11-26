import pygame
from pygame.sprite import Group

from settings import Setting
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    game_settings = Setting()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建Play按钮
    play_buttom = Button(game_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(game_settings)
    # 创造一个计分板
    sb = Scoreboard(game_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(game_settings, screen)
    # 子弹编组，用来存储所有有效子弹
    bullets = Group()
    # 创建外星人编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(game_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(game_settings, screen, stats, sb, play_buttom, ship, aliens, bullets)

        if stats.game_active:
            # 根据事件更新飞船的位置
            ship.update()
            # 根据事件更新子弹
            gf.update_bullets(game_settings, stats, sb, screen, ship, bullets, aliens)
            # 更新外星人位置
            gf.update_aliens(game_settings, screen, stats, sb,  ship, aliens, bullets)

        # 更新当前屏幕
        gf.update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_buttom)


if __name__ == '__main__':
    run_game()
