# 游戏资源说明

## 资源目录结构

```
src/resources/
├── images/          # 图片资源
│   ├── city_*.png   # 城市图标 (按势力)
│   ├── terrain_*.png # 地形瓦片
│   ├── soldier_*.png # 士兵图标 (按兵种)
│   └── flag_*.png    # 势力旗帜
├── sounds/          # 音效资源
│   └── (待添加)
└── fonts/           # 字体资源
    └── (待添加)
```

## 已生成资源

### 城市图标 (city_*.png)
- `city_wei.png` - 魏国城市 (蓝色)
- `city_shu.png` - 蜀国城市 (绿色)
- `city_wu.png` - 吴国城市 (红色)
- `city_neutral.png` - 中立城市 (棕色)

### 地形瓦片 (terrain_*.png)
- `terrain_plain.png` - 平原
- `terrain_mountain.png` - 山脉
- `terrain_water.png` - 水域
- `terrain_forest.png` - 森林
- `terrain_city.png` - 城市

### 士兵图标 (soldier_*.png)
- `soldier_infantry.png` - 步兵
- `soldier_cavalry.png` - 骑兵
- `soldier_archer.png` - 弓兵
- `soldier_siege.png` - 战车

### 势力旗帜 (flag_*.png)
- `flag_wei.png` - 魏国旗帜
- `flag_shu.png` - 蜀国旗帜
- `flag_wu.png` - 吴国旗帜

## 程序化生成资源

游戏使用 `resource_generator.py` 模块程序化生成所有图形资源。
这样可以：
1. 减小仓库体积
2. 避免版权问题
3. 支持自定义修改

### 生成资源
```bash
python src/resource_generator.py
```

## 待添加资源

### 音效资源
- 背景音乐 (BGM)
- 战斗音效
- UI 点击音效
- 马匹音效
- 武器碰撞音效

### 字体资源
- 中文字体 (如需特殊字体)
- 英文字体

## 资源生成器 API

```python
from src.resource_generator import ResourceGenerator

generator = ResourceGenerator('path/to/resources')

# 生成城市图标
city_img = generator.generate_city_image('shu', size=60)

# 生成武将头像
portrait = generator.generate_general_portrait('guan_yu', 'shu', size=80)

# 生成士兵图标
soldier = generator.generate_soldier_icon('cavalry', size=40)

# 生成地形瓦片
terrain = generator.generate_terrain_tile('mountain', size=64)

# 生成旗帜
flag = generator.generate_flag('wei', width=40, height=60)

# 生成所有资源
generator.generate_all_resources()
```
