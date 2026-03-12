"""
城市类 - 三国城市实体
City Class - Three Kingdoms city entity
"""

import pygame
from typing import Optional, Dict, Any, Tuple


class City:
    """城市类"""

    # 势力颜色
    FACTION_COLORS = {
        "wei": (100, 100, 200),   # 魏 - 蓝色
        "shu": (100, 200, 100),   # 蜀 - 绿色
        "wu": (200, 100, 100),    # 吴 - 红色
        "neutral": (139, 90, 43),  # 中立 - 棕色
    }

    FACTION_NAMES = {
        "wei": "魏",
        "shu": "蜀",
        "wu": "吴",
        "neutral": "中立",
    }

    def __init__(self, name: str, x: int, y: int, owner: str = "neutral"):
        """初始化城市

        Args:
            name: 城市名称
            x: 地图 X 坐标
            y: 地图 Y 坐标
            owner: 所有者势力
        """
        self.name = name
        self.x = x
        self.y = y
        self.owner = owner  # "wei", "shu", "wu", "neutral"
        self.population = 10000
        self.gold = 1000
        self.food = 1000
        self.soldiers = 1000
        self.max_soldiers = 5000
        self.defense = 100  # 城防值

        # 建筑等级
        self.buildings = {
            "farm": 1,       # 农田 - 增加粮草产量
            "market": 1,     # 市集 - 增加金钱收入
            "barracks": 1,   # 兵营 - 加快招兵速度
            "wall": 1,       # 城墙 - 提升城防
            "dojo": 0,       # 武馆 - 训练武将
        }

        # 驻守武将
        self.generals = []

        # 点击区域
        self.rect = pygame.Rect(x - 30, y - 30, 60, 60)

    @property
    def color(self) -> tuple:
        """获取势力颜色"""
        return self.FACTION_COLORS.get(self.owner, self.FACTION_COLORS["neutral"])

    @property
    def faction_name(self) -> str:
        """获取势力名称"""
        return self.FACTION_NAMES.get(self.owner, "未知")

    def draw(self, screen: pygame.Surface, scale: float = 1.0, offset_y: int = 0):
        """绘制城市

        Args:
            screen: 屏幕表面
            scale: 缩放比例
            offset_y: Y 轴偏移量
        """
        from src.resource_loader import resource_loader
        from src.config import COLOR_WHITE, FONT_SIZE_SMALL

        # 应用偏移
        draw_y = self.y + offset_y

        # 绘制城市区域 (带缩放)
        radius = int(25 * scale)
        pygame.draw.circle(screen, self.color, (self.x, draw_y), radius)
        pygame.draw.circle(screen, COLOR_WHITE, (self.x, draw_y), radius, 2)

        # 绘制城市名称
        font = resource_loader.get_font(FONT_SIZE_SMALL)
        name_text = font.render(self.name, True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(self.x, draw_y - 40 - int(10 * (scale - 1))))
        screen.blit(name_text, name_rect)

        # 绘制兵力
        soldier_text = font.render(f"{self.soldiers}", True, COLOR_WHITE)
        soldier_rect = soldier_text.get_rect(center=(self.x, draw_y + 45 + int(10 * (scale - 1))))
        screen.blit(soldier_text, soldier_rect)

    def is_clicked(self, pos: tuple) -> bool:
        """检查是否被点击"""
        return self.rect.collidepoint(pos)

    def recruit_soldiers(self, soldier_type: str, count: int) -> Tuple[bool, int, int]:
        """招募士兵

        Args:
            soldier_type: 士兵类型 (infantry, cavalry, archer, siege)
            count: 招募数量

        Returns:
            (是否成功，实际招募数量，花费金币)
        """
        costs = {
            "infantry": 10,   # 步兵
            "cavalry": 20,    # 骑兵
            "archer": 15,     # 弓兵
            "siege": 50,      # 战车
        }

        cost = costs.get(soldier_type, 10)
        total_cost = cost * count

        # 检查金钱是否足够
        if self.gold < total_cost:
            return (False, 0, 0)

        # 检查是否超过上限
        available_space = self.max_soldiers - self.soldiers
        actual_count = min(count, available_space)

        if actual_count <= 0:
            return (False, 0, 0)

        # 扣除金钱，增加士兵
        self.gold -= cost * actual_count
        self.soldiers += actual_count

        return (True, actual_count, cost * actual_count)

    def collect_tax(self) -> int:
        """征收税款

        Returns:
            征收的税款
        """
        base_tax = 100 * self.buildings["market"]
        tax = base_tax + self.population // 100
        self.gold += tax
        return tax

    def collect_food(self) -> int:
        """征收粮草

        Returns:
            征收的粮草
        """
        base_food = 100 * self.buildings["farm"]
        food = base_food + self.population // 100
        self.food += food
        return food

    def upgrade_building(self, building_type: str) -> Tuple[bool, int]:
        """升级建筑

        Args:
            building_type: 建筑类型

        Returns:
            (是否成功，升级花费)
        """
        costs = {
            "farm": 200,
            "market": 200,
            "barracks": 300,
            "wall": 500,
            "dojo": 400,
        }

        if building_type not in costs:
            return (False, 0)

        cost = costs[building_type]

        # 检查金钱是否足够
        if self.gold < cost:
            return (False, 0)

        # 检查建筑是否已满级
        if self.buildings.get(building_type, 0) >= 5:
            return (False, 0)

        # 升级建筑
        self.gold -= cost
        self.buildings[building_type] = self.buildings.get(building_type, 0) + 1

        # 升级城墙时增加城防
        if building_type == "wall":
            self.defense += 50

        return (True, cost)

    def add_general(self, general) -> bool:
        """添加武将

        Args:
            general: 武将对象

        Returns:
            是否添加成功
        """
        if len(self.generals) >= 5:  # 最多 5 名武将
            return False

        if general not in self.generals:
            self.generals.append(general)
            return True
        return False

    def remove_general(self, general) -> bool:
        """移除武将

        Args:
            general: 武将对象

        Returns:
            是否移除成功
        """
        if general in self.generals:
            self.generals.remove(general)
            return True
        return False

    def get_info_dict(self) -> Dict[str, Any]:
        """获取城市信息字典"""
        return {
            "城市": self.name,
            "势力": self.faction_name,
            "人口": self.population,
            "兵力": f"{self.soldiers}/{self.max_soldiers}",
            "金钱": self.gold,
            "粮草": self.food,
            "城防": self.defense,
        }

    def end_turn(self):
        """结束回合处理"""
        # 自然增长人口
        if self.population < 10000:
            self.population += 10

        # 自动征收粮草
        self.collect_food()
