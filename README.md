# 粒子爱心动画

使用 Python 和 Tkinter 绘制粉色粒子爱心，包含跳动、闪烁、光晕、飘散，以及鼠标点击释放粒子的效果。

## 运行

需要 Python 3.6 或更新版本，以及 Tkinter 图形界面支持。无需安装第三方 Python 库，程序需在有桌面图形环境的电脑上运行。

下载本仓库后，在文件所在目录打开终端：

```bash
python particle_heart.py
```

部分系统使用 `python3 particle_heart.py`。可先执行 `python -m tkinter` 检查 Tkinter 是否可用；如果提示缺少 tkinter，请通过 Python 安装程序或系统包管理器安装 Tk 支持。

## 操作

- 空格：暂停或继续。
- 鼠标左键：在点击位置释放粒子（暂停时不触发）。
- Esc：退出。

## 自定义

在 `particle_heart.py` 中可以调整 `COLORS` 修改粒子颜色、`BACKGROUND` 修改背景颜色，以及 `pulse` 表达式修改心跳幅度和速度。

程序仅使用 Python 标准库，不访问网络，不需要账号、密码或令牌。
