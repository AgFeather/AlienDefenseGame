import sys
import pygame
import time


from bullet import Bullet
from alien import Alien


'''保存管理事件的代码，简化run_game()并隔离事件管理循环'''
def check_events(game_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    """相应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 退出游戏
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_setting, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:  # 检测到有按键被按下
            check_keydown_events(event, game_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:  # 检测到按键被松开
            check_keyup_events(event, ship)


def check_keydown_events(event, game_setting, screen, ship, bullets):
    """相应按键被按下"""
    if event.key == pygame.K_q:  # 按下q键退出游戏
        sys.exit()
    if event.key == pygame.K_RIGHT:
        # 将飞船的向右移动标识置为True
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_setting, screen, ship, bullets)


def check_keyup_events(event, ship):
    """相应按键被松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


# 屏幕更新相关代码
def update_screen(game_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重新绘制屏幕
    screen.fill(game_settings.bg_color)
    # 绘制飞船
    ship.blitme()
    # 绘制编组中外星人，外星人的位置由rect决定
    aliens.draw(screen)
    # 在飞船和外星人后面重新绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 显示计分板
    sb.show_score()
    # 如果游戏处于非进行状态，就绘制play按钮
    if stats.game_active is False:
        play_button.draw_button()

    # 更新屏幕上的内容，显示新的元素，删除原来的元素
    pygame.display.flip()


# 外星人相关函数
def create_fleet(game_setting, screen, ship, aliens):
    """创建外星人群"""
    # 外星人间距为外星人的宽度
    alien = Alien(game_setting, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(game_setting, alien_width)
    number_rows = get_number_rows(game_setting, ship.rect.height, alien.rect.height)

    # 创建多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_setting, screen, aliens, alien_number, row_number)


def get_number_aliens_x(game_setting, alien_width):
    """计算一行可容纳多少个外星人"""
    available_space_x = game_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(game_setting, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其加入当前行
    alien = Alien(game_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x  # 新创建的alien的x值
    alien.rect.y = alien.rect.height + 2 * row_number * alien.rect.height  # y值
    aliens.add(alien)


def get_number_rows(game_setting, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (game_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(game_setting, screen, stats, sb,  ship, aliens, bullets):
    check_fleet_edges(game_setting, aliens)  # 检查战队中是否有外星人位于屏幕边缘并更新外星人位置
    aliens.update()  # 对编组中的每个alien都调用update方法（自动）

    # 检查外星人和飞船之间是否碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_setting, screen, stats, sb,  ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(game_setting, screen, stats, sb,  ship, aliens, bullets)



def check_aliens_bottom(game_setting, screen, stats, sb,  ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞倒一样进行处理
            ship_hit(game_setting, screen, stats, sb,  ship, aliens, bullets)
            break


def ship_hit(game_setting, screen, stats, sb,  ship, aliens, bullets):
    """响应被外星人撞到飞船的操作"""
    if stats.ships_left > 0:
        # 将ships_left 减一
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(game_setting, screen, ship, aliens)
        ship.center_ship()
        # 暂停一下
        time.sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # 游戏结束时重新显示光标



def check_fleet_edges(game_setting, aliens):
    """对所有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_setting, aliens)
            break


def change_fleet_direction(game_setting, aliens):
    """改变战队中所有外星人的运动方向"""
    for alien in aliens.sprites():
        alien.rect.y +=  game_setting.fleet_drop_speed
    game_setting.fleet_direction *= -1


# 子弹相关函数
def update_bullets(game_setting, stats, sb, screen, ship, bullets, aliens):
    bullets.update()  # group会自动调用每个Sprite的update()方法
    # 删除已经消失的子弹
    for bullet in bullets:
        if bullet.rect.y <= 0:
            bullets.remove(bullet)
    # 检查子弹和外星人是否碰撞
    check_bullet_alien_collisions(game_setting, stats, sb, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(game_setting, stats, sb, screen, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人，如果有，删除，对应的的外星人和子弹
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for alien in collisions.values():
            stats.score += game_setting.alien_points
            sb.prep_score()
        check_high_score(stats, sb)  # 检查是否诞生了新的最高分
    # 当检测到所有外星人都被杀死后，重新生成新一群外星人
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        game_setting.increase_speed()  # 提高速度
        stats.level += 1  # 提高游戏等级
        sb.prep_level()

        create_fleet(game_setting, screen, ship, aliens)


def fire_bullet(game_setting, screen, ship, bullets):
    # 如果子弹的数量没有达到最大限制，就发射一枚子弹
    if len(bullets) < game_setting.bullets_allowed:
        new_bullet = Bullet(game_setting, screen, ship)
        bullets.add(new_bullet)


# 按钮相关函数
def check_play_button(game_setting, screen, stats, sb, play_botton, ship, aliens, bullets, mouse_x, mouse_y):
    """玩家单机play按钮时开始新游戏"""
    button_clicked =  play_botton.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置统计信息
        stats.game_active = True
        stats.reset_stats()
        game_setting.initialize_dynamic_settings()

        # 重置计分板图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(game_setting, screen, ship, aliens)
        ship.center_ship()


# 计分板相关函数
def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()