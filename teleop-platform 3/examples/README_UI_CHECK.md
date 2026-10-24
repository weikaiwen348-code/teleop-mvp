# 可选浏览器流程检查 · v0.3

普通演示只需 Python，不需要 Node.js。开发者可先安装 Python 演示依赖，再在 examples 中运行：

```bash
npm install
npx playwright install chromium
node ui_browser_validation.mjs
```

Python 解释器可通过 `TELEOP_PYTHON` 指定，默认 `python`；在项目虚拟环境已激活的终端运行即可。`TELEOP_CHROME` 可指定已有 Chrome，`TELEOP_UI_OUTPUT` 可指定新的检查目录。默认输出 `runs/ui-check-时间戳`。

程序使用空闲端口，真实操作网页按钮和滑块键盘输入，验证模型、运动/夹爪、保持/恢复、急停/复位、完成保存；第二段预放一个同名 NPZ，核实拒绝覆盖且页面明确显示导出失败。保留检查 JSON、截图、服务器日志与两个 episode；第二段故意产生失败，不能作为成功示教。

v0.3 此脚本不录制视频，以降低浏览器负载。已交付视频和对应录制来源在 defense 中，属于 v0.2 历史演示。自动化不是人类示教或实体实验。Python 自检菜单不依赖这一可选工具。
