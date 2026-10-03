# 可选浏览器流程检查

正常演示只需要 Python 依赖，不需要 Node.js。若要自动复现录制流程：先按主 README 安装 Python 工程，再在 examples 目录执行：

```bash
npm install
npx playwright install chromium
node ui_browser_validation.mjs
```

需要系统支持 WebGL / 软件渲染。程序启动本地 Panda 仿真，实际操作滑块与按钮，检查跟随、夹爪、保持、复位和保存，在 runs/ui-check-时间戳 下保留视频、截图、日志与 episode。首次安装浏览器需要联网。可使用 TELEOP_CHROME 指定已有 Chrome 可执行文件。它不是机器人厂家控制程序，也不生成任务成功标签。
