# 答辩当天操作卡

提前确认 PPT 和 MP4 都能在答辩电脑打开；视频为无配音、有中文字幕，可边播放边讲解。现场演示需要 Python 3.10+ 和支持 WebGL 的浏览器。首次安装依赖需要联网，请提前完成。

```bash
cd teleop-platform
python -m pip install -e '.[demo]'
python -m teleop ui --output runs/defense-01 --open-browser
```

端口占用：添加 `--port 8081`。输出目录已存在：改为新名字，如 `runs/defense-02`。

## 一分钟现场演示

1. 等待模型加载，点击“开启跟随”。
2. 将关节 1 从当前值小幅调至约 0.2 rad，等待跟随；不要一次拖到范围端点。
3. 小幅调节夹爪，展示观测与记录计数。
4. 点击“暂停指令发送”，观察“保持”。
5. 点击“恢复指令发送”，再点“开启跟随”。
6. 点击“软件急停”，展示锁定；点击“本地复位”。
7. 点击“结束并保存”，等待保存完成，再在终端按 Ctrl+C。

```bash
python -m teleop inspect runs/defense-01
```

## 讲解提示

- 第一页先说明“本次是软件框架与仿真验证”。
- 第五页播放 `panda-teleop-demo.mp4`，讲关节、夹爪、断流与保存。
- 第六至九页用实际日志解释动作语义、状态恢复和频率；不要将周期当作远程单向时延。
- 如果现场运行环境不适配，直接播放录制视频，并展示 `manual_demo_episode` 中的数据。不要把录制视频说成实时运行。
- PPT 可编辑，逐页讲稿位于演讲者备注；完整问答见 `defense-script-and-qa.md`。

## 字体与自动化复现

PPT 使用 Noto Sans CJK SC。如电脑替换字体导致换行变化，可安装 `fonts/NotoSansCJKsc-Regular.otf` 后重启演示软件；目录含开源许可证。逐页 PNG 预览可作为排版参照。

可选自动界面检查在 `examples/ui_browser_validation.mjs`；需 Node.js 和 Playwright，在 examples 目录安装依赖和浏览器后执行。它通过真实滑块/按钮操作生成仿真数据，不是人工示教或实体实验。
