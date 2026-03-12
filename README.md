# 三国霸业 (Three Kingdoms)

经典的三国策略游戏，使用 Python 和 Pygame 开发。

![License](https://img.shields.io/github/license/ganecheng-ai/three-kingdoms)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## 游戏特色

- **经典玩法**: 重现经典三国霸业游戏的核心玩法
- **精美画面**: 精心设计的游戏界面和动画效果（浮动标题、脉动菜单、粒子效果等）
- **简体中文**: 完整支持简体中文界面
- **跨平台**: 支持 Windows、Linux、macOS 三大主流操作系统
- **丰富音效**: 包含背景音乐和多种游戏音效（点击、战斗、胜利、失败等）
- **智能 AI**: 多难度 AI 对手，支持外交和战争策略
- **完整游戏系统**:
  - 武将系统：历史著名武将，各具特色属性
  - 城市系统：招兵买马、建设发展、税收征收
  - 军队系统：步兵、骑兵、弓兵、战车多种兵种
  - 战斗系统：回合制战斗，策略制胜
  - 外交系统：改善关系、结盟、宣战

## 游戏截图

### 主菜单界面
```
┌──────────────────────────────────────────────────────┐
│                                                      │
│                    ★  ★    ★   ★                     │
│                                                      │
│               三 国 霸 业                            │
│               v0.6.3                                 │
│                                                      │
│           ✨ [开始游戏] ✨                           │
│           ✨ [载入游戏] ✨                           │
│           ✨ [游戏设置] ✨                           │
│           ✨ [退出游戏] ✨                           │
│                                                      │
│                    ★  ★    ★   ★                     │
└──────────────────────────────────────────────────────┘
```

### 世界地图界面
```
┌──────────────────────────────────────────────────────┐
│  第 1 回合                                           │
│                                                      │
│    [洛阳]────[许昌]                                  │
│      │          │                                    │
│    [长安]────[成都]────[建业]                        │
│                                                      │
│  势力：蜀国  🟩 魏国  🟦 吴国  🟥                      │
└──────────────────────────────────────────────────────┘
```

### 城市管理界面
```
┌──────────────────────────────────────────────────────┐
│  成都                        第 1 回合               │
│  ┌─────────────────────────────────────────────┐     │
│  │ 人口：50000    金钱：10000    粮食：20000   │     │
│  │ 城墙：3        市场：2        农田：3       │     │
│  │                                             │     │
│  │ 武将：关羽 张飞 赵云 诸葛亮               │     │
│  │ 士兵：步兵 5000  骑兵 2000  弓兵 3000       │     │
│  └─────────────────────────────────────────────┘     │
│  [招兵]  [建设]  [武将]  [撤退]                       │
└──────────────────────────────────────────────────────┘
```

### 战斗界面
```
┌──────────────────────────────────────────────────────┐
│  战斗：成都 vs 长安                                  │
│  ┌─────────────────┐     ┌─────────────────┐        │
│  │   我军 (蜀国)   │  VS │   敌军 (魏国)   │        │
│  │  ⚔️ 关羽 5000   │     │  ⚔️ 曹操 8000   │        │
│  │  ⚔️ 张飞 4000   │     │  ⚔️ 司马懿 6000 │        │
│  └─────────────────┘     └─────────────────┘        │
│                                                     │
│  [攻击]  [防御]  [计谋]  [撤退]                      │
└──────────────────────────────────────────────────────┘
```

## 安装说明

### 系统要求

- Python 3.10 或更高版本
- 操作系统：Windows 10+ / Ubuntu 20.04+ / macOS 11+
- 内存：至少 512MB RAM
- 存储：至少 100MB 可用空间

### 从源码运行

```bash
# 克隆仓库
git clone git@github.com:ganecheng-ai/three-kingdoms.git
cd three-kingdoms

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python -m src.main
```

### 下载安装包

从 [Releases](https://github.com/ganecheng-ai/three-kingdoms/releases) 页面下载对应操作系统的安装包。

## 游戏操作

### 主菜单
- **开始游戏**: 开始新的游戏
- **载入游戏**: 读取已保存的游戏进度
- **游戏设置**: 调整游戏选项
- **退出游戏**: 退出游戏

### 世界地图
- 点击城市查看城市信息
- 右键取消选择
- ESC 返回主菜单

### 城市管理
- **概况**: 查看城市基本信息
- **招兵**: 招募士兵扩充军队
- **建设**: 建造城市建筑
- **武将**: 管理麾下武将

### 战斗系统
- **攻击**: 对敌军发动攻击
- **撤退**: 尝试撤离战场
- 空格键继续回合

## 游戏版本

当前最新版本：**v0.6.3**

更新日志详见 [plan.md](plan.md) 中的发布记录。

## 日志文件

游戏运行日志保存在以下位置：
- **Windows**: `%APPDATA%\ThreeKingdoms\game.log`
- **Linux/macOS**: `~/.three_kingdoms/game.log`

如果遇到问题，请提供日志文件以便分析定位。

## 游戏开发

### 技术栈

- **游戏引擎**: Pygame 2.5+
- **编程语言**: Python 3.10+
- **构建工具**: PyInstaller
- **测试框架**: pytest
- **版本控制**: Git + GitHub Actions

### 架构设计

```
src/
├── main.py              # 游戏入口
├── game.py              # 游戏核心逻辑（主循环、场景管理）
├── config.py            # 游戏配置
├── resource_loader.py   # 资源加载器（单例模式）
├── resource_generator.py # 程序化资源生成器
├── animations.py        # 动画系统（淡入淡出、脉动、浮动、粒子）
├── ai.py                # AI 逻辑（战略 AI、战斗 AI、外交 AI）
├── entities/            # 游戏实体
│   ├── general.py       # 武将类
│   ├── city.py          # 城市类
│   └── army.py          # 军队类
├── scenes/              # 游戏场景
│   ├── base_scene.py    # 场景基类
│   ├── menu_scene.py    # 主菜单
│   ├── world_scene.py   # 世界地图
│   ├── city_scene.py    # 城市界面
│   └── battle_scene.py  # 战斗场景
├── ui/                  # UI 组件
│   ├── button.py        # 按钮组件
│   └── panel.py         # 面板组件
└── resources/           # 游戏资源
    ├── images/          # 图片资源
    ├── sounds/          # 音效资源
    └── fonts/           # 字体资源
```

## 开发计划

详见 [plan.md](plan.md)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone git@github.com:ganecheng-ai/three-kingdoms.git
cd three-kingdoms

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 .\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/ -v

# 运行游戏
python -m src.main
```

### 代码规范

- 遵循 PEP 8 代码风格
- 使用类型注解
- 编写单元测试
- 保持代码可读性和可维护性

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢所有为开源社区做出贡献的开发者！

## 联系方式

- GitHub Issues: [问题反馈](https://github.com/ganecheng-ai/three-kingdoms/issues)
- Repository: [ganecheng-ai/three-kingdoms](https://github.com/ganecheng-ai/three-kingdoms)
