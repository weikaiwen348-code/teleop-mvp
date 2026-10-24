# GitHub 更新与新手协作

## 当前状态

2026-10-04 重新核对：目标 `https://github.com/weikaiwen348-code/teleop-mvp` 返回 404。连接能识别账号 `weikaiwen348-code`，但可访问仓库和安装账号列表为空。GitHub 插件已安装；命令行也未建立可用连接。

本次审查基于此前交付的 172 文件工程，没有读取远端最新 commit。

**本次已准备 v0.3 更新后的完整工程与文档，尚未向 GitHub 写入，没有远端 commit、分支或 PR。** 404 可能是地址、改名、不存在或授权范围问题，现有信息不能确定具体原因。

仓库负责人先在自己登录的 GitHub 中确认正确链接，再让当前 GitHub 连接获得该仓库访问权。不要把密码、密钥或访问令牌发到聊天。若仓库改名，请使用新链接。

## 恢复访问后的合并顺序

1. 先读旧仓库 README、目录和 AGENTS.md 等协作约定，确认默认分支及未提交工作。
2. 从最新默认分支建独立分支，例如 `review/teleop-v03`。这是建议名称，本次没有创建。
3. 把工程先放进独立的 `reference-platform/` 子目录，保留旧代码；若目录已存在，先比较再合并。
4. 保留原根 README 内容，新增指向 `reference-platform/docs/TEAM_GUIDE.md` 的入口。
5. 一起放入运行代码、模型、网页资源、配置、报告、样例和 defense 材料，并保留许可来源。
6. 排除密钥、个人环境、缓存、个人 runs 数据和重复压缩包。
7. 提交并上传；保护分支需要 PR 时按规则提交审阅，不强制覆盖。
8. 核对远端 commit/PR、指南链接、PPT/视频下载，再由另一组员独立获取运行。

真实适配器尚未完成，不用本仿真工程替换旧项目真机占位或删除旧停止控制逻辑。建议提交说明：`fix: harden teleop controls and add beginner workflow`。

## 第一次使用 Git 的同学

Git 是本地版本工具，GitHub 是协作平台。clone 下载仓库与历史；pull 获取更新；commit 在本地保存一个版本；push 上传版本；PR 是请求审核并合并修改。

只读材料时，直接在 GitHub 点开 Markdown；PPT、MP4 下载打开即可。ZIP 下载不会自动更新。

### 合并后的首次获取

下面命令在仓库访问恢复后使用。地址以确认后的地址为准；目录假设负责人采用 reference-platform，最终以仓库 README 为准。

```bash
git clone https://github.com/weikaiwen348-code/teleop-mvp.git
cd teleop-mvp/reference-platform
```

然后按 [新手指南](TEAM_GUIDE.md) 安装和运行。

### 已 clone 的同学获取更新

在仓库根目录先运行 `git status`。工作区干净且处于团队约定的主分支时，再运行：

```bash
git pull --ff-only
```

有自己改过的文件，先保存并让负责人协助合并；不要用 reset --hard 或强制推送。快进更新失败时先排查历史分歧。

### 修改材料

在干净、更新过的主分支上创建自己的分支：

```bash
git switch -c docs/update-defense-notes
```

修改后看 `git status`，只添加确定要分享的文件。以下示例在仓库根目录执行，并假设该文件路径存在：

```bash
git add reference-platform/docs/TEAM_TASKS.md
git commit -m "docs: update team task ownership"
git push -u origin docs/update-defense-notes
```

Git 要求配置身份时使用自己的姓名和邮箱。PPT/视频不便逐行合并，主副本每次由一人负责编辑。

## 推荐根 README 入口

只有工程已经加入该路径后，下面链接才有效：

```markdown
## 全组从这里开始

[新手总指南：版本区别、材料、操作与分工](reference-platform/docs/TEAM_GUIDE.md)

当前交付为 Panda 遥操作软件框架与仿真验证，实体硬件与跨地域实验仍待完成。
```

上传前核对：旧工程保留，新目录可独立安装，材料版本一致，许可齐全，无密钥或个人数据。上传后核对：有远端提交链接，组员能访问，首页能进入指南，材料能下载，另一人能独立复现。
