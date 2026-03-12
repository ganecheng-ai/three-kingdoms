"""
武将类 - 三国武将实体
General Class - Three Kingdoms general entity
"""

import pygame
from typing import Optional, Dict, List, Tuple
from src.resource_loader import resource_loader
from src.config import COLOR_WHITE, COLOR_GOLD, FONT_SIZE_NORMAL, FONT_SIZE_SMALL


class General:
    """武将类"""

    # 武将数据
    GENERAL_DATA = {
        # 蜀国武将
        "liu_bei": {
            "name": "刘备", "faction": "shu",
            "武力": 75, "智力": 85, "统率": 90, "政治": 88,
            "hp": 100, "mp": 80,
        },
        "guan_yu": {
            "name": "关羽", "faction": "shu",
            "武力": 97, "智力": 80, "统率": 92, "政治": 70,
            "hp": 100, "mp": 60,
        },
        "zhang_fei": {
            "name": "张飞", "faction": "shu",
            "武力": 98, "智力": 60, "统率": 85, "政治": 50,
            "hp": 100, "mp": 50,
        },
        "zhuge_liang": {
            "name": "诸葛亮", "faction": "shu",
            "武力": 40, "智力": 100, "统率": 90, "政治": 95,
            "hp": 70, "mp": 100,
        },
        "zhao_yun": {
            "name": "赵云", "faction": "shu",
            "武力": 96, "智力": 75, "统率": 88, "政治": 65,
            "hp": 100, "mp": 70,
        },
        # 魏国武将
        "cao_cao": {
            "name": "曹操", "faction": "wei",
            "武力": 80, "智力": 95, "统率": 95, "政治": 90,
            "hp": 100, "mp": 90,
        },
        "xiahou_dun": {
            "name": "夏侯惇", "faction": "wei",
            "武力": 90, "智力": 70, "统率": 85, "政治": 60,
            "hp": 100, "mp": 60,
        },
        "dian_wei": {
            "name": "典韦", "faction": "wei",
            "武力": 95, "智力": 50, "统率": 75, "政治": 40,
            "hp": 100, "mp": 50,
        },
        "simayi": {
            "name": "司马懿", "faction": "wei",
            "武力": 50, "智力": 98, "统率": 92, "政治": 88,
            "hp": 75, "mp": 100,
        },
        # 吴国武将
        "sun_quan": {
            "name": "孙权", "faction": "wu",
            "武力": 70, "智力": 85, "统率": 88, "政治": 85,
            "hp": 95, "mp": 80,
        },
        "zhou_yu": {
            "name": "周瑜", "faction": "wu",
            "武力": 75, "智力": 96, "统率": 90, "政治": 80,
            "hp": 85, "mp": 95,
        },
        "lu_xun": {
            "name": "陆逊", "faction": "wu",
            "武力": 65, "智力": 95, "统率": 92, "政治": 85,
            "hp": 80, "mp": 95,
        },
        "gan_ning": {
            "name": "甘宁", "faction": "wu",
            "武力": 92, "智力": 65, "统率": 80, "政治": 50,
            "hp": 100, "mp": 60,
        },
    }

    FACTION_NAMES = {
        "shu": "蜀",
        "wei": "魏",
        "wu": "吴",
        "neutral": "中立",
    }

    FACTION_COLORS = {
        "shu": (50, 200, 50),    # 绿色
        "wei": (50, 50, 200),    # 蓝色
        "wu": (200, 50, 50),     # 红色
        "neutral": (150, 150, 50),  # 黄色
    }

    def __init__(self, general_id: str):
        """初始化武将

        Args:
            general_id: 武将 ID，如 "liu_bei"
        """
        if general_id not in self.GENERAL_DATA:
            raise ValueError(f"未知的武将 ID: {general_id}")

        data = self.GENERAL_DATA[general_id]
        self.id = general_id
        self.name = data["name"]
        self.faction = data["faction"]

        # 属性
        self.wu_li = data["武力"]      # 武力
        self.zhi_li = data["智力"]     # 智力
        self.tong_shuai = data["统率"]  # 统率
        self.zheng_zhi = data["政治"]  # 政治

        # 状态
        self.hp = data["hp"]
        self.max_hp = data["hp"]
        self.mp = data["mp"]
        self.max_mp = data["mp"]

        # 等级和经验
        self.level = 1
        self.exp = 0
        self.max_exp = 100

        # 状态
        self.is_alive = True
        self.status_effects: List[str] = []  # 状态效果

    @classmethod
    def create_by_name(cls, name: str) -> Optional['General']:
        """根据中文名称创建武将

        Args:
            name: 武将中文名称，如 "刘备"

        Returns:
            General 实例或 None
        """
        for general_id, data in cls.GENERAL_DATA.items():
            if data["name"] == name:
                return cls(general_id)
        return None

    @classmethod
    def get_all_generals(cls, faction: Optional[str] = None) -> List[str]:
        """获取所有武将 ID 列表

        Args:
            faction: 势力过滤，如 "shu"、"wei"、"wu"

        Returns:
            武将 ID 列表
        """
        if faction:
            return [gid for gid, data in cls.GENERAL_DATA.items() if data["faction"] == faction]
        return list(cls.GENERAL_DATA.keys())

    def get_attack_power(self) -> int:
        """获取攻击力"""
        return self.wu_li + self.level * 2

    def get_defense_power(self) -> int:
        """获取防御力"""
        return self.tong_shuai + self.level * 2

    def get_strategy_power(self) -> int:
        """获取策略力"""
        return self.zhi_li + self.level * 2

    def take_damage(self, damage: int) -> int:
        """受到伤害

        Args:
            damage: 原始伤害值

        Returns:
            实际受到的伤害值
        """
        actual_damage = max(1, damage - self.get_defense_power() // 4)
        self.hp = max(0, self.hp - actual_damage)

        if self.hp <= 0:
            self.is_alive = False

        return actual_damage

    def heal(self, amount: int) -> int:
        """治疗

        Args:
            amount: 治疗量

        Returns:
            实际治疗量
        """
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def gain_exp(self, exp: int) -> bool:
        """获得经验

        Args:
            exp: 经验值

        Returns:
            是否升级
        """
        self.exp += exp
        if self.exp >= self.max_exp:
            self.level_up()
            return True
        return False

    def level_up(self):
        """升级"""
        self.level += 1
        self.exp = 0
        self.max_exp = int(self.max_exp * 1.5)

        # 属性提升
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.wu_li += 1
        self.zhi_li += 1
        self.tong_shuai += 1
        self.zheng_zhi += 1

    def add_status_effect(self, effect: str):
        """添加状态效果"""
        if effect not in self.status_effects:
            self.status_effects.append(effect)

    def remove_status_effect(self, effect: str):
        """移除状态效果"""
        if effect in self.status_effects:
            self.status_effects.remove(effect)

    def get_info_dict(self) -> Dict[str, any]:
        """获取武将信息字典"""
        return {
            "姓名": self.name,
            "势力": self.FACTION_NAMES.get(self.faction, "未知"),
            "等级": self.level,
            "武力": self.wu_li,
            "智力": self.zhi_li,
            "统率": self.tong_shuai,
            "政治": self.zheng_zhi,
            "HP": f"{self.hp}/{self.max_hp}",
            "MP": f"{self.mp}/{self.max_mp}",
        }

    def draw(self, screen: pygame.Surface, x: int, y: int, show_details: bool = True):
        """绘制武将信息

        Args:
            screen: 屏幕 Surface
            x: X 坐标
            y: Y 坐标
            show_details: 是否显示详细信息
        """
        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        # 势力颜色
        faction_color = self.FACTION_COLORS.get(self.faction, COLOR_WHITE)

        # 绘制背景框
        if show_details:
            rect_width = 200
            rect_height = 150
        else:
            rect_width = 150
            rect_height = 40

        rect = pygame.Rect(x, y, rect_width, rect_height)
        pygame.draw.rect(screen, (40, 40, 60), rect)
        pygame.draw.rect(screen, faction_color, rect, 2)

        # 绘制名字
        name_text = font.render(self.name, True, COLOR_GOLD)
        screen.blit(name_text, (x + 10, y + 5))

        if not show_details:
            return

        # 绘制属性
        y_offset = y + 35
        attributes = [
            ("等级", self.level),
            ("势力", self.FACTION_NAMES.get(self.faction, "未知")),
            ("武力", self.wu_li),
            ("智力", self.zhi_li),
            ("统率", self.tong_shuai),
            ("政治", self.zheng_zhi),
        ]

        for attr_name, attr_value in attributes:
            attr_text = small_font.render(f"{attr_name}: {attr_value}", True, COLOR_WHITE)
            screen.blit(attr_text, (x + 10, y_offset))
            y_offset += 18

        # 绘制 HP/MP 条
        self._draw_bar(screen, x + 10, y_offset, "HP", self.hp, self.max_hp, (200, 50, 50))
        y_offset += 15
        self._draw_bar(screen, x + 10, y_offset, "MP", self.mp, self.max_mp, (50, 50, 200))

    def _draw_bar(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        label: str,
        current: int,
        maximum: int,
        color: Tuple[int, int, int],
    ):
        """绘制状态条"""
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        # 标签
        label_text = small_font.render(f"{label}:", True, COLOR_WHITE)
        screen.blit(label_text, (x, y))

        # 背景条
        bar_width = 80
        bar_height = 10
        bar_x = x + 35
        pygame.draw.rect(screen, (80, 0, 0), (bar_x, y + 2, bar_width, bar_height))

        # 实际条
        if maximum > 0:
            fill_width = int(bar_width * current / maximum)
            pygame.draw.rect(screen, color, (bar_x, y + 2, fill_width, bar_height))

        # 数值
        value_text = small_font.render(f"{current}/{maximum}", True, COLOR_WHITE)
        screen.blit(value_text, (bar_x + bar_width + 5, y))
