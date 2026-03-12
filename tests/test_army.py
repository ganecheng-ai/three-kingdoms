"""
军队系统测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestArmy:
    """军队类测试"""

    def test_create_army(self):
        """测试创建军队"""
        from src.entities import Army
        army = Army(owner="shu")
        assert army.owner == "shu"
        assert army.total_soldiers == 0
        assert army.morale == 100
        assert army.stamina == 100

    def test_army_with_general(self):
        """测试带武将的军队"""
        from src.entities import Army, General
        general = General("guan_yu")
        army = Army(owner="shu", general=general)
        assert army.general == general
        assert army.general.name == "关羽"

    def test_add_soldiers(self):
        """测试添加士兵"""
        from src.entities import Army
        army = Army(owner="shu")
        army.add_soldiers("infantry", 100)
        army.add_soldiers("cavalry", 50)
        assert army.soldiers["infantry"] == 100
        assert army.soldiers["cavalry"] == 50
        assert army.total_soldiers == 150

    def test_remove_soldiers(self):
        """测试移除士兵"""
        from src.entities import Army
        army = Army(owner="shu")
        army.add_soldiers("infantry", 100)
        removed = army.remove_soldiers("infantry", 30)
        assert removed == 30
        assert army.soldiers["infantry"] == 70

    def test_attack_power(self):
        """测试攻击力计算"""
        from src.entities import Army, General
        army = Army(owner="shu")
        army.add_soldiers("infantry", 1000)
        # 基础攻击力 = 1000 * 10 / 100 = 100
        assert army.attack_power >= 100

    def test_attack_power_with_general(self):
        """测试带武将的军队攻击力"""
        from src.entities import Army, General
        general = General("guan_yu")  # 武力 97
        army = Army(owner="shu", general=general)
        army.add_soldiers("infantry", 1000)
        # 有武将加成，攻击力应该更高
        assert army.attack_power > 100

    def test_defense_power(self):
        """测试防御力计算"""
        from src.entities import Army
        army = Army(owner="shu")
        army.add_soldiers("infantry", 1000)
        # 基础防御力 = 1000 * 15 / 100 = 150
        assert army.defense_power >= 150

    def test_speed(self):
        """测试速度计算"""
        from src.entities import Army
        army = Army(owner="shu")
        army.add_soldiers("infantry", 1000)
        # 步兵速度为 5
        assert army.speed >= 5

    def test_formation(self):
        """测试阵型系统"""
        from src.entities import Army
        army = Army(owner="shu", formation="wedge")
        assert army.formation == "wedge"
        assert army.set_formation("square")
        assert army.formation == "square"
        assert not army.set_formation("invalid")

    def test_formation_bonus(self):
        """测试阵型加成"""
        from src.entities import Army
        army = Army(owner="shu", formation="wedge")
        bonus = army.get_formation_bonus()
        assert "attack" in bonus
        assert "defense" in bonus
        assert "speed" in bonus

    def test_take_casualties(self):
        """测试承受伤亡"""
        from src.entities import Army
        army = Army(owner="shu")
        army.add_soldiers("infantry", 1000)
        army.take_casualties(0.3)  # 30% 伤亡
        assert army.soldiers["infantry"] == 700
        assert army.morale < 100

    def test_recover(self):
        """测试恢复"""
        from src.entities import Army
        army = Army(owner="shu")
        army.morale = 50
        army.stamina = 50
        army.recover_morale(30)
        army.recover_stamina(30)
        assert army.morale == 80
        assert army.stamina == 80

    def test_is_defeated(self):
        """测试是否被击败"""
        from src.entities import Army
        army = Army(owner="shu")
        assert not army.is_defeated()
        army.morale = 0
        assert army.is_defeated()

    def test_get_info_dict(self):
        """测试获取信息字典"""
        from src.entities import Army, General
        general = General("guan_yu")
        army = Army(owner="shu", general=general)
        army.add_soldiers("infantry", 500)
        info = army.get_info_dict()
        assert "总兵力" in info
        assert "士气" in info
        assert "主将" in info
        assert info["主将"] == "关羽"

    def test_soldier_types(self):
        """测试兵种类型"""
        from src.entities import Army
        army = Army(owner="shu")
        # 测试所有兵种
        for soldier_type in ["infantry", "cavalry", "archer", "siege"]:
            army.add_soldiers(soldier_type, 100)
        assert army.total_soldiers == 400

    def test_clone(self):
        """测试克隆军队"""
        from src.entities import Army
        army = Army(owner="shu", formation="wedge")
        army.add_soldiers("infantry", 500)
        army.morale = 80
        cloned = army.clone()
        assert cloned.owner == army.owner
        assert cloned.formation == army.formation
        assert cloned.total_soldiers == army.total_soldiers
        assert cloned.morale == army.morale


class TestArmyManager:
    """军队管理器测试"""

    def test_create_army(self):
        """测试创建军队"""
        from src.entities import ArmyManager
        manager = ArmyManager()
        army = manager.create_army("shu")
        assert army in manager.armies
        assert army.owner == "shu"

    def test_remove_army(self):
        """测试移除军队"""
        from src.entities import ArmyManager
        manager = ArmyManager()
        army = manager.create_army("shu")
        manager.remove_army(army)
        assert army not in manager.armies

    def test_get_armies_by_owner(self):
        """测试按势力获取军队"""
        from src.entities import ArmyManager
        manager = ArmyManager()
        manager.create_army("shu")
        manager.create_army("shu")
        manager.create_army("wei")
        shu_armies = manager.get_armies_by_owner("shu")
        wei_armies = manager.get_armies_by_owner("wei")
        assert len(shu_armies) == 2
        assert len(wei_armies) == 1

    def test_clear_defeated_armies(self):
        """测试清除被击败的军队"""
        from src.entities import ArmyManager
        manager = ArmyManager()
        army1 = manager.create_army("shu")
        army2 = manager.create_army("wei")
        army2.morale = 0  # 击败
        manager.clear_defeated_armies()
        assert army1 in manager.armies
        assert army2 not in manager.armies


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
