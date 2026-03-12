"""
动画系统 - 管理游戏动画效果
Animation System - Manage game animation effects
"""

import pygame
import math
from typing import List, Tuple, Optional, Callable
from enum import Enum


class AnimationType(Enum):
    """动画类型"""
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    SLIDE_IN = "slide_in"
    SLIDE_OUT = "slide_out"
    PULSE = "pulse"
    BOUNCE = "bounce"
    SHAKE = "shake"
    FLOAT = "float"
    SCALE_IN = "scale_in"
    SCALE_OUT = "scale_out"
    ROTATE = "rotate"
    FLASH = "flash"


class EasingType(Enum):
    """缓动类型"""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class Animation:
    """动画基类"""

    def __init__(
        self,
        animation_type: AnimationType,
        duration: float,
        easing: EasingType = EasingType.EASE_IN_OUT,
        on_complete: Optional[Callable] = None,
    ):
        self.animation_type = animation_type
        self.duration = duration
        self.easing = easing
        self.on_complete = on_complete

        self.elapsed = 0.0
        self.is_complete = False
        self.is_paused = False

    def _ease(self, t: float) -> float:
        """缓动函数"""
        if self.easing == EasingType.LINEAR:
            return t
        elif self.easing == EasingType.EASE_IN:
            return t * t * t
        elif self.easing == EasingType.EASE_OUT:
            t = 1 - t
            return 1 - t * t * t
        elif self.easing == EasingType.EASE_IN_OUT:
            if t < 0.5:
                return 4 * t * t * t
            else:
                t = 1 - t
                return 1 - 4 * t * t * t
        elif self.easing == EasingType.BOUNCE:
            if t < 0.5:
                return self._bounce(t * 2) * 0.5
            else:
                return self._bounce((1 - t) * 2) * 0.5 + 0.5
        elif self.easing == EasingType.ELASTIC:
            if t == 0 or t == 1:
                return t
            return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1
        return t

    def _bounce(self, t: float) -> float:
        """弹跳缓动"""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375

    def update(self, delta_time: float):
        """更新动画"""
        if self.is_paused or self.is_complete:
            return

        self.elapsed += delta_time
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.is_complete = True
            if self.on_complete:
                self.on_complete()

    def get_progress(self) -> float:
        """获取动画进度 (0-1)"""
        if self.duration == 0:
            return 1.0
        t = self.elapsed / self.duration
        return self._ease(t)


class FadeAnimation(Animation):
    """淡入淡出动画"""

    def __init__(
        self,
        fade_in: bool,
        duration: float = 0.5,
        easing: EasingType = EasingType.EASE_IN_OUT,
        on_complete: Optional[Callable] = None,
    ):
        animation_type = AnimationType.FADE_IN if fade_in else AnimationType.FADE_OUT
        super().__init__(animation_type, duration, easing, on_complete)
        self.fade_in = fade_in

    def get_alpha(self) -> int:
        """获取当前透明度 (0-255)"""
        progress = self.get_progress()
        if self.fade_in:
            return int(255 * (1 - progress))
        else:
            return int(255 * progress)


class SlideAnimation(Animation):
    """滑动动画"""

    def __init__(
        self,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        duration: float = 0.5,
        easing: EasingType = EasingType.EASE_OUT,
        on_complete: Optional[Callable] = None,
    ):
        super().__init__(AnimationType.SLIDE_IN, duration, easing, on_complete)
        self.start_pos = start_pos
        self.end_pos = end_pos

    def get_position(self) -> Tuple[int, int]:
        """获取当前位置"""
        progress = self.get_progress()
        x = int(self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress)
        y = int(self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress)
        return (x, y)


class PulseAnimation(Animation):
    """脉动动画"""

    def __init__(
        self,
        start_scale: float = 1.0,
        end_scale: float = 1.2,
        duration: float = 0.8,
        easing: EasingType = EasingType.EASE_IN_OUT,
        on_complete: Optional[Callable] = None,
    ):
        super().__init__(AnimationType.PULSE, duration, easing, on_complete)
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.initial_duration = duration

    def get_scale(self) -> float:
        """获取当前缩放比例"""
        # 使用正弦波实现脉动效果
        cycles = self.elapsed / self.initial_duration
        progress = cycles % 1.0
        eased = self._ease(progress)
        # 在 start_scale 和 end_scale 之间插值
        return self.start_scale + (self.end_scale - self.start_scale) * abs(math.sin(progress * math.pi))

    def update(self, delta_time: float):
        """脉动动画是循环的"""
        if self.is_paused:
            return
        self.elapsed += delta_time


class ShakeAnimation(Animation):
    """震动动画"""

    def __init__(
        self,
        intensity: int = 10,
        duration: float = 0.5,
        on_complete: Optional[Callable] = None,
    ):
        super().__init__(AnimationType.SHAKE, duration, EasingType.EASE_OUT, on_complete)
        self.intensity = intensity
        self.original_offset = 0

    def get_offset(self) -> Tuple[int, int]:
        """获取当前震动偏移"""
        if self.is_complete:
            return (0, 0)

        progress = self.get_progress()
        # 震动幅度随时间衰减
        decay = 1 - progress
        offset_x = int(self.intensity * decay * (math.sin(self.elapsed * 50) if self.elapsed > 0 else 0))
        offset_y = int(self.intensity * decay * (math.cos(self.elapsed * 50) if self.elapsed > 0 else 0))
        return (offset_x, offset_y)


class FloatAnimation(Animation):
    """浮动动画"""

    def __init__(
        self,
        amplitude: int = 10,
        frequency: float = 2.0,
        duration: float = 0,  # 0 表示无限循环
        start_phase: float = 0,
        on_complete: Optional[Callable] = None,
    ):
        super().__init__(AnimationType.FLOAT, duration, EasingType.LINEAR, on_complete)
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_phase = start_phase

    def get_offset(self) -> int:
        """获取当前浮动偏移"""
        t = self.elapsed * self.frequency * 2 * math.pi + self.start_phase
        return int(self.amplitude * math.sin(t))


class ScaleAnimation(Animation):
    """缩放动画"""

    def __init__(
        self,
        start_scale: float = 0.0,
        end_scale: float = 1.0,
        duration: float = 0.5,
        easing: EasingType = EasingType.EASE_OUT,
        on_complete: Optional[Callable] = None,
    ):
        animation_type = AnimationType.SCALE_IN if end_scale > start_scale else AnimationType.SCALE_OUT
        super().__init__(animation_type, duration, easing, on_complete)
        self.start_scale = start_scale
        self.end_scale = end_scale

    def get_scale(self) -> float:
        """获取当前缩放比例"""
        progress = self.get_progress()
        return self.start_scale + (self.end_scale - self.start_scale) * progress


class FlashAnimation(Animation):
    """闪烁动画"""

    def __init__(
        self,
        color: Tuple[int, int, int] = (255, 255, 255),
        flashes: int = 3,
        duration: float = 0.6,
        on_complete: Optional[Callable] = None,
    ):
        super().__init__(AnimationType.FLASH, duration, EasingType.LINEAR, on_complete)
        self.color = color
        self.flashes = flashes
        self.flash_duration = duration / flashes

    def get_alpha(self) -> int:
        """获取当前闪烁透明度"""
        if self.is_complete:
            return 0

        flash_index = int(self.elapsed / self.flash_duration)
        flash_progress = (self.elapsed % self.flash_duration) / self.flash_duration

        # 交替显示和隐藏
        if flash_index % 2 == 0:
            return int(255 * (1 - flash_progress))
        else:
            return 0


class AnimationManager:
    """动画管理器"""

    def __init__(self):
        self.animations: List[Animation] = []
        self.active_animations: dict = {}

    def add_animation(self, key: str, animation: Animation):
        """添加动画"""
        self.animations.append(animation)
        self.active_animations[key] = animation

    def remove_animation(self, key: str):
        """移除动画"""
        if key in self.active_animations:
            self.animations.remove(self.active_animations[key])
            del self.active_animations[key]

    def get_animation(self, key: str) -> Optional[Animation]:
        """获取动画"""
        return self.active_animations.get(key)

    def update(self, delta_time: float):
        """更新所有动画"""
        completed = []
        for anim in self.animations:
            anim.update(delta_time)
            if anim.is_complete:
                completed.append(anim)

        # 移除已完成的动画
        for anim in completed:
            if anim in self.animations:
                self.animations.remove(anim)
            for key, value in list(self.active_animations.items()):
                if value == anim:
                    del self.active_animations[key]

    def is_playing(self, key: str) -> bool:
        """检查动画是否正在播放"""
        return key in self.active_animations and not self.active_animations[key].is_complete

    def clear(self):
        """清空所有动画"""
        self.animations.clear()
        self.active_animations.clear()


# 粒子系统
class Particle:
    """粒子"""

    def __init__(
        self,
        x: int,
        y: int,
        vx: float,
        vy: float,
        color: Tuple[int, int, int],
        lifetime: float,
        size: int = 4,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.size = size
        self.is_alive = True

    def update(self, delta_time: float):
        """更新粒子"""
        self.age += delta_time
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # 重力
        self.vy += 50 * delta_time

        if self.age >= self.lifetime:
            self.is_alive = False

    def draw(self, screen: pygame.Surface):
        """绘制粒子"""
        alpha = 1 - (self.age / self.lifetime)
        size = int(self.size * alpha)
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)


class ParticleSystem:
    """粒子系统"""

    def __init__(self):
        self.particles: List[Particle] = []

    def emit(
        self,
        x: int,
        y: int,
        color: Tuple[int, int, int],
        count: int = 10,
        speed_range: Tuple[float, float] = (50, 150),
        angle_range: Tuple[float, float] = (0, math.pi),
        lifetime_range: Tuple[float, float] = (0.5, 1.0),
        size_range: Tuple[int, int] = (3, 6),
    ):
        """发射粒子"""
        import random

        for _ in range(count):
            speed = random.uniform(*speed_range)
            angle = random.uniform(*angle_range)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            lifetime = random.uniform(*lifetime_range)
            size = random.randint(*size_range)

            particle = Particle(x, y, vx, vy, color, lifetime, size)
            self.particles.append(particle)

    def emit_explosion(
        self,
        x: int,
        y: int,
        color: Tuple[int, int, int],
        count: int = 20,
    ):
        """发射爆炸粒子"""
        import random

        for _ in range(count):
            speed = random.uniform(100, 300)
            angle = random.uniform(0, 2 * math.pi)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            lifetime = random.uniform(0.5, 1.0)
            size = random.randint(2, 5)

            particle = Particle(x, y, vx, vy, color, lifetime, size)
            self.particles.append(particle)

    def update(self, delta_time: float):
        """更新粒子系统"""
        for particle in self.particles:
            particle.update(delta_time)

        # 移除已死亡的粒子
        self.particles = [p for p in self.particles if p.is_alive]

    def draw(self, screen: pygame.Surface):
        """绘制所有粒子"""
        for particle in self.particles:
            particle.draw(screen)


# 全局动画管理器
animation_manager = AnimationManager()
particle_system = ParticleSystem()
