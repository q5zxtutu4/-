"""粒子爱心动画。运行：python particle_heart.py

仅使用 Python 标准库；需要安装带 Tk 支持的 Python。
空格暂停/继续，鼠标点击释放粒子，Esc 退出。
"""

import math
import random
import time
import tkinter as tk


WIDTH, HEIGHT = 900, 720
BACKGROUND = "#090510"
COLORS = ("#ff4388", "#ff65a0", "#ff91bc", "#ffc0d8", "#ff2e72")


def heart_point(angle):
    """经典参数方程，返回以原点为中心的爱心坐标。"""
    x = 16 * math.sin(angle) ** 3
    y = (13 * math.cos(angle) - 5 * math.cos(2 * angle)
         - 2 * math.cos(3 * angle) - math.cos(4 * angle))
    return x, -y


def fade(color, brightness):
    brightness = max(0.0, min(1.0, brightness))
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    bg = [int(BACKGROUND[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(b + (c - b) * brightness):02x}"
                         for c, b in zip(rgb, bg))


class ParticleHeart:
    def __init__(self, root):
        self.root = root
        root.title("心动粒子 · Particle Heart")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.rng = random.Random()
        self.particles = []
        self.sparks = []
        self.elapsed = 0.0
        self.last_time = time.perf_counter()
        self.paused = False
        self.emission = 0.0

        # 暗色星尘背景。
        for _ in range(100):
            x, y = self.rng.uniform(0, WIDTH), self.rng.uniform(0, HEIGHT)
            r = self.rng.choice((0.6, 0.8, 1.1))
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                    fill="#35213e", outline="")

        # 外缘密集，内部疏松，每个粒子都有独立的闪烁相位。
        for i in range(950):
            angle = self.rng.uniform(0, math.tau)
            x, y = heart_point(angle)
            scale = (self.rng.uniform(0.93, 1.06) if i < 620
                     else math.sqrt(self.rng.random()) * 0.94)
            x = x * scale + self.rng.gauss(0, 0.12)
            y = y * scale + self.rng.gauss(0, 0.12)
            color = self.rng.choice(COLORS)
            radius = self.rng.uniform(0.8, 2.0)
            halo = self.canvas.create_oval(0, 0, 0, 0, outline="",
                                           fill=fade(color, 0.12))
            dot = self.canvas.create_oval(0, 0, 0, 0, outline="", fill=color)
            self.particles.append((x, y, radius, self.rng.uniform(0, math.tau),
                                   color, halo, dot))

        self.canvas.create_text(WIDTH/2, 600, text="FOR YOU",
                                fill="#ff9fc7", font=("Arial", 23, "bold"))
        self.canvas.create_text(WIDTH/2, 647,
                                text="SPACE  pause / resume     CLICK  sparkle     ESC  exit",
                                fill="#806780", font=("Arial", 10))
        root.bind("<space>", self.toggle_pause)
        root.bind("<Escape>", lambda event: root.destroy())
        self.canvas.bind("<Button-1>", self.burst)
        self.animate()

    def toggle_pause(self, event=None):
        self.paused = not self.paused

    def add_spark(self, x, y, burst=False):
        # 限制粒子总数，连续点击也不会无限增加画布对象。
        if len(self.sparks) >= 350:
            return
        angle = self.rng.uniform(0, math.tau)
        speed = self.rng.uniform(45, 155) if burst else self.rng.uniform(12, 45)
        color = self.rng.choice(COLORS)
        item = self.canvas.create_oval(0, 0, 0, 0, fill=color, outline="")
        lifetime = self.rng.uniform(0.7, 1.6)
        self.sparks.append([item, x, y, math.cos(angle)*speed,
                            math.sin(angle)*speed - 25, lifetime,
                            lifetime, color, self.rng.uniform(1.2, 3)])

    def burst(self, event):
        if not self.paused:
            for _ in range(65):
                self.add_spark(event.x, event.y, burst=True)

    def place(self, item, x, y, radius):
        self.canvas.coords(item, x-radius, y-radius, x+radius, y+radius)

    def animate(self):
        now = time.perf_counter()
        dt = min(now - self.last_time, 0.05)
        self.last_time = now
        if not self.paused:
            self.elapsed += dt
            t = self.elapsed
            pulse = 1 + 0.045 * math.sin(t * 3.2) + 0.018 * math.sin(t * 6.4)
            for x, y, radius, phase, color, halo, dot in self.particles:
                px = WIDTH/2 + x * 15 * pulse + math.sin(t*1.7 + phase)*1.5
                py = 315 + y * 15 * pulse + math.cos(t*1.4 + phase)*1.5
                flicker = 0.65 + 0.35 * math.sin(t*2.6 + phase)**2
                r = radius * (0.8 + flicker*0.3)
                self.place(halo, px, py, r*2.6)
                self.place(dot, px, py, r)
                self.canvas.itemconfigure(dot, fill=fade(color, flicker))

            self.emission += dt * 45
            while self.emission >= 1:
                self.emission -= 1
                x, y = heart_point(self.rng.uniform(0, math.tau))
                self.add_spark(WIDTH/2 + x*15*pulse, 315 + y*15*pulse)

            alive = []
            for spark in self.sparks:
                item, x, y, vx, vy, life, total, color, radius = spark
                life -= dt
                if life <= 0:
                    self.canvas.delete(item)
                    continue
                x += vx * dt
                y += vy * dt
                vy += 18 * dt
                self.place(item, x, y, radius * (0.3 + 0.7 * life/total))
                self.canvas.itemconfigure(item, fill=fade(color, life/total))
                alive.append([item, x, y, vx, vy, life, total, color, radius])
            self.sparks = alive

        self.root.after(16, self.animate)


if __name__ == "__main__":
    window = tk.Tk()
    ParticleHeart(window)
    window.mainloop()
