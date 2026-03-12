"""
军队类 - 三国军队实体
Army Class - Three Kingdoms army entity
"""

import pygame
from typing import Optional, Dict, List, Tuple, Any
from src.resource_loader import resource_loader
from src.config import COLOR_WHITE, COLOR_GOLD, FONT_SIZE_NORMAL, FONT_SIZE_SMALL


class Army:
    """军队类"""

    # 士兵类型
    SOLDIER_TYPES = {
        "infantry": {
            "name": "步兵",
            "cost": 10,
            "attack": 10,
            "defense": 15,
            "speed": 5,
            "icon": (100, 100, 100),
        },
        "cavalry": {
            "name": "骑兵",
            "cost": 20,
            "attack": 20,
            "defense": 10,
            "speed": 15,
            "icon": (150, 100, 50),
        },
        "archer": {
            "name": "弓兵",
            "cost": 15,
            "attack": 18,
            "defense": 8,
            "speed": 8,
            "icon": (100, 150, 50),
        },
        "siege": {
            "name": "战车",
            "cost": 50,
            "attack": 35,
            "defense": 25,
            "speed": 3,
            "icon": (150, 50, 50),
        },
    }

    FORMATION_BONUS = {
        "goose": {"attack": 1.1, "defense": 0.9, "speed": 1.0},      # 雁行阵
        "square": {"attack": 1.0, "defense": 1.2, "speed": 0.8},     # 方阵
        "wedge": {"attack": 1.2, "defense": 0.8, "speed": 1.1},      # 锋矢阵
        "circle": {"attack": 0.9, "defense": 1.3, "speed": 0.7},     # 圆阵
        "mobile": {"attack": 1.0, "defense": 1.0, "speed": 1.3},     # 机动阵
    }

    def __init__(
        self,
        owner: str,
        general=None,
        soldiers: Optional[Dict[str, int]] = None,
        formation: str = "square",
    ):
        """初始化军队

        Args:
            owner: 所有者势力
            general: 率领武将
            soldiers: 各兵种数量字典
            formation: 阵型
        """
        self.owner = owner
        self.general = general
        self.soldiers = soldiers or {
            "infantry": 0,
            "cavalry": 0,
            "archer": 0,
            "siege": 0,
        }
        self.formation = formation
        self.morale = 100  # 士气 0-100
        self.stamina = 100  # 体力 0-100
        self.position: Optional[Tuple[int, int]] = None
        self._had_soldiers = self.total_soldiers > 0  # 标记是否曾经有士兵

        # 战斗相关
        self.is_moving = False
        self.move_progress = 0
        self.target_position: Optional[Tuple[int, int]] = None

    @property
    def total_soldiers(self) -> int:
        """总兵力"""
        return sum(self.soldiers.values())

    @property
    def attack_power(self) -> float:
        """总攻击力"""
        base_attack = 0
        for soldier_type, count in self.soldiers.items():
            if soldier_type in self.SOLDIER_TYPES:
                base_attack += count * self.SOLDIER_TYPES[soldier_type]["attack"] / 100

        # 武将加成
        if self.general:
            base_attack *= 1 + self.general.wu_li / 200

        # 阵型加成
        formation_mult = self.FORMATION_BONUS.get(self.formation, {}).get("attack", 1.0)
        base_attack *= formation_mult

        # 士气影响
        base_attack *= (50 + self.morale) / 100

        return int(base_attack)

    @property
    def defense_power(self) -> float:
        """总防御力"""
        base_defense = 0
        for soldier_type, count in self.soldiers.items():
            if soldier_type in self.SOLDIER_TYPES:
                base_defense += count * self.SOLDIER_TYPES[soldier_type]["defense"] / 100

        # 武将加成
        if self.general:
            base_defense *= 1 + self.general.tong_shuai / 200

        # 阵型加成
        formation_mult = self.FORMATION_BONUS.get(self.formation, {}).get("defense", 1.0)
        base_defense *= formation_mult

        return int(base_defense)

    @property
    def speed(self) -> float:
        """行军速度"""
        if self.total_soldiers == 0:
            return 0

        total_speed = 0
        total_count = 0
        for soldier_type, count in self.soldiers.items():
            if soldier_type in self.SOLDIER_TYPES:
                total_speed += self.SOLDIER_TYPES[soldier_type]["speed"] * count
                total_count += count

        if total_count == 0:
            return 0

        base_speed = total_speed / total_count

        # 阵型加成
        formation_mult = self.FORMATION_BONUS.get(self.formation, {}).get("speed", 1.0)
        base_speed *= formation_mult

        # 体力影响
        base_speed *= (50 + self.stamina) / 100

        return base_speed

    def add_soldiers(self, soldier_type: str, count: int) -> int:
        """添加士兵

        Args:
            soldier_type: 兵种类型
            count: 数量

        Returns:
            实际添加的数量
        """
        if soldier_type not in self.soldiers:
            return 0

        actual_count = max(0, count)
        self.soldiers[soldier_type] += actual_count
        if actual_count > 0:
            self._had_soldiers = True
        return actual_count

    def remove_soldiers(self, soldier_type: str, count: int) -> int:
        """移除士兵（损失）

        Args:
            soldier_type: 兵种类型
            count: 数量

        Returns:
            实际移除的数量
        """
        if soldier_type not in self.soldiers:
            return 0

        current = self.soldiers[soldier_type]
        removed = min(current, count)
        self.soldiers[soldier_type] -= removed
        return removed

    def take_casualties(self, casualty_rate: float):
        """承受伤亡

        Args:
            casualty_rate: 伤亡比例 0-1
        """
        for soldier_type in self.soldiers:
            losses = int(self.soldiers[soldier_type] * casualty_rate)
            self.soldiers[soldier_type] -= losses

        # 士气下降
        self.morale = max(0, self.morale - int(casualty_rate * 30))

    def set_formation(self, formation: str) -> bool:
        """设置阵型

        Args:
            formation: 阵型名称

        Returns:
            是否设置成功
        """
        if formation in self.FORMATION_BONUS:
            self.formation = formation
            return True
        return False

    def get_formations(self) -> List[str]:
        """获取所有可用阵型"""
        return list(self.FORMATION_BONUS.keys())

    def get_formation_bonus(self) -> Dict[str, float]:
        """获取当前阵型加成"""
        return self.FORMATION_BONUS.get(self.formation, {}).copy()

    def recover_stamina(self, amount: int):
        """恢复体力

        Args:
            amount: 恢复量
        """
        self.stamina = min(100, self.stamina + amount)

    def recover_morale(self, amount: int):
        """恢复士气

        Args:
            amount: 恢复量
        """
        self.morale = min(100, self.morale + amount)

    def is_defeated(self) -> bool:
        """是否被击败"""
        # 士气为 0 表示溃逃
        if self.morale <= 0:
            return True
        # 有士兵但全部阵亡才算被击败
        if self.total_soldiers <= 0 and hasattr(self, '_had_soldiers') and self._had_soldiers:
            return True
        return False

    def get_soldier_breakdown(self) -> Dict[str, Dict]:
        """获取兵种详细信息"""
        breakdown = {}
        for soldier_type, count in self.soldiers.items():
            if soldier_type in self.SOLDIER_TYPES:
                info = self.SOLDIER_TYPES[soldier_type].copy()
                info["count"] = count
                breakdown[soldier_type] = info
        return breakdown

    def get_info_dict(self) -> Dict[str, Any]:
        """获取军队信息字典"""
        info = {
            "势力": self.owner,
            "总兵力": self.total_soldiers,
            "士气": self.morale,
            "体力": self.stamina,
            "阵型": self.formation,
            "攻击力": self.attack_power,
            "防御力": self.defense_power,
            "速度": self.speed,
        }

        if self.general:
            info["主将"] = self.general.name
        else:
            info["主将"] = "无"

        # 添加各兵种数量
        for soldier_type, count in self.soldiers.items():
            if count > 0:
                type_name = self.SOLDIER_TYPES.get(soldier_type, {}).get("name", soldier_type)
                info[type_name] = count

        return info

    def draw(self, screen: pygame.Surface, x: int, y: int, show_details: bool = True):
        """绘制军队

        Args:
            screen: 屏幕 Surface
            x: X 坐标
            y: Y 坐标
            show_details: 是否显示详细信息
        """
        font = resource_loader.get_font(FONT_SIZE_NORMAL)
        small_font = resource_loader.get_font(FONT_SIZE_SMALL)

        # 势力颜色
        faction_colors_map = {
            "shu": (50, 200, 50),
            "wei": (50, 50, 200),
            "wu": (200, 50, 50),
            "neutral": (150, 150, 50),
        }
        color = faction_colors_map.get(self.owner, (128, 128, 128))

        # 绘制背景框
        if show_details:
            rect_width = 220
            rect_height = 180
        else:
            rect_width = 150
            rect_height = 40

        rect = pygame.Rect(x, y, rect_width, rect_height)
        pygame.draw.rect(screen, (40, 40, 60), rect)
        pygame.draw.rect(screen, color, rect, 2)

        # 绘制主将名字（如果有）
        if self.general:
            name_text = font.render(f"{self.general.name}", True, COLOR_GOLD)
        else:
            name_text = font.render("军队", True, COLOR_GOLD)
        screen.blit(name_text, (x + 10, y + 5))

        if not show_details:
            return

        # 绘制总兵力
        soldier_text = small_font.render(f"兵力：{self.total_soldiers}", True, COLOR_WHITE)
        screen.blit(soldier_text, (x + 10, y + 30))

        # 绘制士气条
        self._draw_bar(screen, x + 10, y + 50, "士气", self.morale, 100, (200, 200, 50))

        # 绘制体力条
        self._draw_bar(screen, x + 10, y + 68, "体力", self.stamina, 100, (50, 200, 50))

        # 绘制阵型
        formation_text = small_font.render(f"阵型：{self.formation}", True, COLOR_WHITE)
        screen.blit(formation_text, (x + 10, y + 86))

        # 绘制各兵种数量
        y_offset = y + 105
        for soldier_type, count in self.soldiers.items():
            if count > 0:
                type_info = self.SOLDIER_TYPES.get(soldier_type, {})
                type_name = type_info.get("name", soldier_type)
                type_color = type_info.get("icon", (255, 255, 255))
                soldier_count_text = small_font.render(
                    f"{type_name}: {count}", True, type_color
                )
                screen.blit(soldier_count_text, (x + 10, y_offset))
                y_offset += 16

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
        bar_width = 100
        bar_height = 10
        bar_x = x + 35
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, y + 2, bar_width, bar_height))

        # 实际条
        if maximum > 0:
            fill_width = int(bar_width * current / maximum)
            pygame.draw.rect(screen, color, (bar_x, y + 2, fill_width, bar_height))

        # 数值
        value_text = small_font.render(f"{current}/{maximum}", True, COLOR_WHITE)
        screen.blit(value_text, (bar_x + bar_width + 5, y))

    def clone(self) -> 'Army':
        """克隆军队"""
        new_army = Army(
            owner=self.owner,
            general=self.general,
            soldiers=self.soldiers.copy(),
            formation=self.formation,
        )
        new_army.morale = self.morale
        new_army.stamina = self.stamina
        return new_army


class ArmyManager:
    """军队管理器"""

    def __init__(self):
        self.armies: List[Army] = []

    def create_army(
        self,
        owner: str,
        general=None,
        soldiers: Optional[Dict[str, int]] = None,
        formation: str = "square",
    ) -> Army:
        """创建军队"""
        army = Army(owner, general, soldiers, formation)
        self.armies.append(army)
        return army

    def remove_army(self, army: Army):
        """移除军队"""
        if army in self.armies:
            self.armies.remove(army)

    def get_armies_by_owner(self, owner: str) -> List[Army]:
        """获取某势力的所有军队"""
        return [army for army in self.armies if army.owner == owner]

    def get_all_armies(self) -> List[Army]:
        """获取所有军队"""
        return self.armies.copy()

    def clear_defeated_armies(self):
        """清除被击败的军队"""
        self.armies = [army for army in self.armies if not army.is_defeated()]
