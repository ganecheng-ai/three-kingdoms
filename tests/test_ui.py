"""
UI 组件测试
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestButton:
    """按钮组件测试"""

    def test_create_button(self):
        """测试创建按钮"""
        from src.ui import Button
        button = Button(100, 100, 120, 40, "测试按钮")
        assert button.text == "测试按钮"
        assert button.rect.x == 100
        assert button.rect.y == 100

    def test_button_set_position(self):
        """测试设置按钮位置"""
        from src.ui import Button
        button = Button(0, 0, 100, 30, "移动")
        button.set_position(50, 50)
        assert button.rect.x == 50
        assert button.rect.y == 50

    def test_button_set_enabled(self):
        """测试设置启用状态"""
        from src.ui import Button
        button = Button(0, 0, 100, 30, "禁用")
        button.set_enabled(False)
        assert button.enabled is False


class TestPanel:
    """面板组件测试"""

    def test_create_panel(self):
        """测试创建面板"""
        from src.ui import Panel
        panel = Panel(50, 50, 200, 150, "测试面板")
        assert panel.title == "测试面板"
        assert panel.rect.width == 200
        assert panel.rect.height == 150

    def test_panel_add_content(self):
        """测试添加内容"""
        from src.ui import Panel
        panel = Panel(0, 0, 100, 100)
        panel.add_content("第一行")
        panel.add_content("第二行")
        assert len(panel.content) == 2

    def test_panel_clear_content(self):
        """测试清空内容"""
        from src.ui import Panel
        panel = Panel(0, 0, 100, 100)
        panel.add_content("内容")
        panel.clear_content()
        assert len(panel.content) == 0


class TestInfoPanel:
    """信息面板测试"""

    def test_create_info_panel(self):
        """测试创建信息面板"""
        from src.ui import InfoPanel
        panel = InfoPanel(0, 0, 150, 100, "信息")
        assert panel.title == "信息"

    def test_set_info(self):
        """测试设置信息"""
        from src.ui import InfoPanel
        panel = InfoPanel(0, 0, 150, 100)
        panel.set_info({"人口": 10000, "兵力": 5000})
        assert len(panel.content) == 2


class TestSelectionPanel:
    """选择面板测试"""

    def test_create_selection_panel(self):
        """测试创建选择面板"""
        from src.ui import SelectionPanel
        panel = SelectionPanel(0, 0, 150, 100, "选择")
        assert panel.title == "选择"

    def test_set_options(self):
        """测试设置选项"""
        from src.ui import SelectionPanel
        panel = SelectionPanel(0, 0, 150, 100)
        panel.set_options(["选项 1", "选项 2", "选项 3"])
        assert len(panel.options) == 3
        assert panel.selected_index == -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
