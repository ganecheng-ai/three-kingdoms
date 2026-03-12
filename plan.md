# 三国霸业游戏开发计划

## 项目概述
使用 Python 开发一个经典的三国霸业策略游戏，支持简体中文，画面精美，操作流畅。

## 技术选型
- **游戏引擎**: Pygame (跨平台 2D 游戏开发)
- **构建工具**: PyInstaller (打包成可执行文件)
- **编程语言**: Python 3.10+
- **版本控制**: Git + GitHub Actions

## 目录结构
```
three-kingdoms/
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── main.py             # 游戏入口
│   ├── game.py             # 游戏核心逻辑
│   ├── config.py           # 游戏配置
│   ├── resources/          # 游戏资源
│   │   ├── images/         # 图片资源
│   │   ├── sounds/         # 音效资源
│   │   └── fonts/          # 字体资源
│   ├── scenes/             # 游戏场景
│   │   ├── __init__.py
│   │   ├── base_scene.py   # 场景基类
│   │   ├── menu_scene.py   # 主菜单
│   │   ├── world_scene.py  # 世界地图
│   │   ├── city_scene.py   # 城市界面
│   │   └── battle_scene.py # 战斗场景
│   ├── entities/           # 游戏实体
│   │   ├── __init__.py
│   │   ├── general.py      # 武将类
│   │   ├── city.py         # 城市类
│   │   └── army.py         # 军队类
│   └── ui/                 # UI 组件
│       ├── __init__.py
│       ├── button.py       # 按钮组件
│       └── panel.py        # 面板组件
├── tests/                  # 测试目录
├── build/                  # 构建输出
├── .github/
│   └── workflows/          # GitHub Actions
├── requirements.txt        # 依赖列表
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 开发阶段

### 第一阶段：项目基础搭建
- [x] 创建目录结构
- [x] 配置 Python 环境和依赖
- [x] 设置 Git 仓库
- [x] 创建基础的游戏循环

### 第二阶段：核心引擎开发
- [x] 实现游戏主循环
- [x] 实现场景管理器
- [x] 实现资源加载器
- [x] 实现事件处理系统

### 第三阶段：游戏界面开发
- [x] 实现主菜单界面
- [x] 实现世界地图界面
- [x] 实现城市界面
- [x] 实现战斗界面
- [x] 实现 UI 组件系统

### 第四阶段：游戏逻辑开发
- [x] 实现武将系统
- [x] 实现城市管理系统
- [x] 实现军队系统
- [x] 实现战斗系统
- [x] 实现 AI 逻辑

### 第五阶段：资源和美化
- [x] 添加游戏背景音乐
- [x] 添加游戏音效
- [x] 优化游戏画面 (程序化生成资源)
- [x] 添加动画效果

### 第六阶段：打包发布
- [x] 配置 PyInstaller 打包
- [x] 创建 GitHub Actions workflow
- [x] 修复构建配置问题
- [x] 测试各平台构建
- [x] 发布第一个版本 v0.1.0

## 发布记录

### v0.2.1 (2026-03-12)
- 更新 GitHub Actions 配置，使用最新版本的 actions 以修复 Node.js 20 废弃警告
- 更新游戏版本号显示

### v0.2.0 (2026-03-12)
- 添加游戏背景音乐（程序化生成的古典风格 BGM）
- 添加游戏音效（点击、战斗、胜利、失败、行军、建造等音效）
- 添加动画效果系统（淡入淡出、缩放、浮动、震动、粒子效果等）
- 改进主菜单界面（浮动标题、脉动菜单项、星星背景、淡入淡出）
- 改进世界地图界面（城市缩放动画、浮动效果、点击粒子效果）

### v0.1.0 (2026-03-12)
- 首个 alpha 版本发布
- 支持 Windows (.exe)、Linux (.tar.gz)、macOS (.tar.gz) 三个平台
- 包含完整的游戏功能：主菜单、世界地图、城市管理、战斗系统
- 自动生成 SHA256 checksums.txt 文件

## 发布流程
- 使用 Git Tag 触发自动构建
- 构建 Windows/Linux/macOS 三个平台
- 生成 SHA256 checksums.txt

## 开发原则
1. 代码质量优先
2. 及时提交和测试
3. 遵循 Python 最佳实践
4. 保持代码可读性和可维护性
