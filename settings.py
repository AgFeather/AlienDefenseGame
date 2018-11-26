
class Setting():
    '''存储关于游戏所有设置的类'''

    def __init__(self):
        '''游戏初始化设置'''
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船移动速度
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10  # 限制子弹的最大数量

        # 外星人设置
        self.fleet_drop_speed = 40
        self.score_scale = 1.5  # 击杀外星人得分的提高速度

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 2
        self.fleet_direction = 1  # 1表示向右移动，-1表示向左移动
        self.alien_points = 50  # 消灭一个外星人的计分

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points *= int(self.score_scale)