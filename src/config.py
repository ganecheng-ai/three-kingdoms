"""
三国霸业 - 游戏配置
Three Kingdoms Game Configuration
"""

# 屏幕设置
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# 颜色定义 (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (220, 50, 50)
COLOR_GREEN = (50, 180, 50)
COLOR_BLUE = (50, 100, 200)
COLOR_GOLD = (255, 215, 0)
COLOR_BROWN = (139, 90, 43)
COLOR_DARK_GREEN = (34, 139, 34)
COLOR_SAND = (238, 214, 167)
COLOR_WATER = (65, 105, 225)

# 游戏标题
GAME_TITLE = "三国霸业"
GAME_VERSION = "0.6.1"

# 字体设置
FONT_SIZE_TITLE = 48
FONT_SIZE_LARGE = 36
FONT_SIZE_NORMAL = 24
FONT_SIZE_SMALL = 18

# 场景类型
SCENE_MENU = "menu"
SCENE_WORLD = "world"
SCENE_CITY = "city"
SCENE_BATTLE = "battle"

# 游戏状态
STATE_RUNNING = "running"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

# 势力颜色
FACTION_COLORS = {
    "shu": (50, 200, 50),      # 蜀 - 绿色
    "wei": (50, 50, 200),      # 魏 - 蓝色
    "wu": (200, 50, 50),       # 吴 - 红色
    "neutral": (150, 150, 50), # 中立 - 黄色
}

# 势力名称
FACTION_NAMES = {
    "shu": "蜀",
    "wei": "魏",
    "wu": "吴",
    "neutral": "中立",
}
