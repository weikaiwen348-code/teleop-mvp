# 制作与验证来源

PPT 通过 Artifact Tool 的 JavaScript API 制作，原生表格与图表可编辑。生成脚本依赖作者环境的 Artifact Tool 与 presentation skill，不是运行遥操作工程的依赖。脚本和原录制脚本保留当次工作路径用于追溯；可选的跨目录浏览器检查脚本位于 examples/ui_browser_validation.mjs。

PPT 已通过包结构、页面几何和字体检查，并从最终文件重新导入、渲染并逐页检查。原生图表包含由本次实际日志抽样、保留六位小数的嵌入工作簿。未声称在原生 PowerPoint 应用中完成打开/编辑验收。演示视频为自动操作真实界面录制，非实体机器人实验。
