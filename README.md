# 三国霸业 (Three Kingdoms)

经典的三国策略游戏，使用 Python 和 Pygame 开发。

![License](https://img.shields.io/github/license/ganecheng-ai/three-kingdoms)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## 游戏特色

- **经典玩法**: 重现经典三国霸业游戏的核心玩法
- **精美画面**: 精心设计的游戏界面和动画效果
- **简体中文**: 完整支持简体中文界面
- **跨平台**: 支持 Windows、Linux、macOS 三大主流操作系统

## 游戏截图

（待添加）

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

## 游戏界面

```
┌─────────────────────────────────────────┐
│           三 国 霸 业                    │
│           v0.1.0                        │
│                                         │
│          [开始游戏]                     │
│          [载入游戏]                     │
│          [游戏设置]                     │
│          [退出游戏]                     │
└─────────────────────────────────────────┘
```

## 开发计划

详见 [plan.md](plan.md)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢所有为开源社区做出贡献的开发者！

## 联系方式

- GitHub Issues: [问题反馈](https://github.com/ganecheng-ai/three-kingdoms/issues)
- Repository: [ganecheng-ai/three-kingdoms](https://github.com/ganecheng-ai/three-kingdoms)
