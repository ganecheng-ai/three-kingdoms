"""
武将系统测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGeneral:
    """武将类测试"""

    def test_create_general(self):
        """测试创建武将"""
        from src.entities import General
        guan_yu = General("guan_yu")
        assert guan_yu.name == "关羽"
        assert guan_yu.faction == "shu"
        assert guan_yu.wu_li == 97

    def test_create_general_by_name(self):
        """测试通过中文名称创建武将"""
        from src.entities import General
        liu_bei = General.create_by_name("刘备")
        assert liu_bei is not None
        assert liu_bei.faction == "shu"

        invalid = General.create_by_name("无效武将")
        assert invalid is None

    def test_get_all_generals(self):
        """测试获取所有武将"""
        from src.entities import General
        all_generals = General.get_all_generals()
        assert len(all_generals) > 0

        shu_generals = General.get_all_generals("shu")
        assert len(shu_generals) > 0
        assert "guan_yu" in shu_generals

        wei_generals = General.get_all_generals("wei")
        assert len(wei_generals) > 0

    def test_general_stats(self):
        """测试武将属性"""
        from src.entities import General
        zhao_yun = General("zhao_yun")
        assert zhao_yun.get_attack_power() > 0
        assert zhao_yun.get_defense_power() > 0
        assert zhao_yun.get_strategy_power() > 0

    def test_take_damage(self):
        """测试受到伤害"""
        from src.entities import General
        zhang_fei = General("zhang_fei")
        initial_hp = zhang_fei.hp
        damage = zhang_fei.take_damage(100)
        assert damage > 0
        assert zhang_fei.hp < initial_hp

    def test_heal(self):
        """测试治疗"""
        from src.entities import General
        liu_bei = General("liu_bei")
        liu_bei.take_damage(50)
        healed = liu_bei.heal(30)
        assert healed > 0
        assert liu_bei.hp > 0

    def test_gain_exp_and_level_up(self):
        """测试获得经验和升级"""
        from src.entities import General
        cao_cao = General("cao_cao")
        initial_level = cao_cao.level
        cao_cao.gain_exp(200)
        assert cao_cao.level > initial_level

    def test_faction_colors(self):
        """测试势力颜色"""
        from src.entities import General
        assert "shu" in General.FACTION_COLORS
        assert "wei" in General.FACTION_COLORS
        assert "wu" in General.FACTION_COLORS

    def test_get_info_dict(self):
        """测试获取信息字典"""
        from src.entities import General
        zhou_yu = General("zhou_yu")
        info = zhou_yu.get_info_dict()
        assert "姓名" in info
        assert info["姓名"] == "周瑜"
        assert "势力" in info
        assert "等级" in info


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
