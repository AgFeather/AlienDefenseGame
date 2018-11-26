

class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, game_settings):
        """初始化统计信息"""
        self.game_settings =  game_settings
        self.game_active = False  # 游戏进行状态
        self.reset_stats()
        self.high_score = 0  # 最高得分，任何情况下都不应重置最高得分

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.game_settings.ship_limit  # 飞船生命值
        self.score = 0  # 计分板当前得分
        self.level = 1