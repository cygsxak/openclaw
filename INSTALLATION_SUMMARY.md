# Clawdbot 配置安装总结

> 安装日期: 2026年1月27日

## ✅ 安装完成状态

已按照 README 和 AGENTS.md 说明成功配置和安装 Clawdbot 项目。

以下是一些常用命令：

配置和设置：

飞书说明
https://github.com/AlexAnys/feishu-moltbot-bridge 

/workspaces/feishu/feishu-moltbot-bridge-main
运行 
FEISHU_APP_ID=cli_a9f09d8f6c38dbc2 node bridge.mjs

/home/codespace/.clawdbot/secrets

程序 
/home/codespace/clawd/docs/stock


~/.clawdbot/clawdbot.json 【配置文件】


pnpm openclaw onboard - 交互式向导配置
pnpm openclaw config - 配置管理
pnpm openclaw doctor - 健康检查
网关控制：

pnpm openclaw gateway run --port 18789 - 启动网关
pnpm openclaw gateway status - 查看网关状态
pnpm openclaw:watch - 开发模式（自动重载）
与 AI 交互：

pnpm openclaw agent --message "你好" - 直接与 AI 对话
pnpm openclaw message send --to <号码> --message "消息" - 发送消息
通道管理：

pnpm openclaw channels login - 登录 WhatsApp 等通道
pnpm openclaw channels status - 查看通道状态


---

## 📋 完成的步骤

### 1. 系统环境检查

| 组件 | 版本 | 状态 | 要求 |
|------|------|------|------|
| Node.js | v24.11.1 | ✅ 通过 | ≥ 22.x |
| npm | v11.6.2 | ✅ 通过 | - |
| pnpm | v10.23.0 | ✅ 通过 | - |

### 2. 依赖安装

```bash
$ pnpm install
```

**执行的修复：**
- ✅ 修复了 `pnpm-workspace.yaml`，添加 `packages/*` 路径以支持 clawdbot 兼容垫片
- ✅ 配置了 `pnpm.peerDependencyRules` 以允许工作区中的 clawdbot 包
- ✅ 重新生成了 `pnpm-lock.yaml`

**结果：** 31 个工作区项目全部安装成功

### 3. UI 构建

```bash
$ pnpm ui:build
```

**输出：**
- ✅ Vite 构建成功
- ✅ 生成了控制面板资源到 `dist/control-ui/`
- 📦 构建大小：74.84 kB CSS + 351.48 kB JS

### 4. 项目编译

```bash
$ pnpm build
```

**编译步骤：**
1. ✅ Canvas A2UI bundling (537.48 kB)
2. ✅ TypeScript 编译 (`tsc -p tsconfig.json`)
3. ✅ Canvas A2UI 文件复制
4. ✅ Hook metadata 复制（4个钩子）
5. ✅ Build info 生成

**生成的目录结构：**
```
dist/
├── acp/
├── agents/
├── auto-reply/
├── browser/
├── canvas-host/
├── channels/
├── cli/
├── commands/
├── config/
├── control-ui/
├── entry.js          # CLI 入口点
├── build-info.json   # 构建信息
└── [更多模块...]
```

### 5. 代码质量检查

```bash
$ pnpm lint
```

**结果：**
- ✅ **0 warnings**
- ✅ **0 errors**
- 📊 检查了 **2509 个文件**，使用 104 条规则
- ⏱️ 完成时间：13.2 秒（2 线程）

---

## 🎯 项目当前状态

| 项目指标 | 值 |
|---------|-----|
| **版本** | 2026.1.26 |
| **工作区包数量** | 31 个项目 |
| **核心包** | openclaw + clawdbot |
| **扩展数量** | 28 个 |
| **构建输出** | dist/ (完整) |
| **CLI 可用性** | ✅ 可运行 |

### 验证 CLI

```bash
$ pnpm clawdbot --version
2026.1.26
```

---

## 📝 修改的配置文件

### 1. `pnpm-workspace.yaml`

```diff
packages:
  - .
  - ui
+ - packages/*
  - extensions/*
```

**原因：** 添加 `packages/clawdbot` 兼容垫片到工作区，解决扩展依赖问题

### 2. `package.json`

```diff
  "pnpm": {
    "minimumReleaseAge": 2880,
    "overrides": {
      "@sinclair/typebox": "0.34.47",
      "hono": "4.11.4",
      "tar": "7.5.4"
-   }
+   },
+   "peerDependencyRules": {
+     "ignoreMissing": ["clawdbot"],
+     "allowAny": ["clawdbot"]
+   }
  },
```

**原因：** 允许工作区使用开发版本的 clawdbot (2026.1.26)，而不要求 npm 上已发布的版本

### 3. `pnpm-lock.yaml`

**状态：** 已重新生成以反映新的工作区配置

---

## 🚀 可用的开发命令

### 开发模式

```bash
# 启动网关（监控模式）
pnpm gateway:watch

# 启动网关（开发模式，跳过通道）
pnpm gateway:dev

# 启动网关（开发模式 + 重置）
pnpm gateway:dev:reset

# 运行配置向导
pnpm clawdbot onboard

# 直接与 AI 交互
pnpm clawdbot agent --message "你好"
```

### 构建命令

```bash
# 完整构建（TypeScript + UI）
pnpm build

# 仅构建 UI
pnpm ui:build

# Canvas A2UI bundling
pnpm canvas:a2ui:bundle
```

### 测试命令

```bash
# 运行所有测试
pnpm test

# 生成测试覆盖率
pnpm test:coverage

# 实时测试（需要真实密钥）
CLAWDBOT_LIVE_TEST=1 pnpm test:live
```

### 代码质量

```bash
# 运行 linter
pnpm lint

# 格式化代码
pnpm format

# 检查 TypeScript 最大行数
pnpm check:ts-max-loc
```

### 文档

```bash
# 启动文档开发服务器
pnpm docs:dev

# 检查文档链接
pnpm docs:build
```

---

## 📚 重要文档链接

### 入门指南
- [Getting Started](https://docs.clawd.bot/start/getting-started) - 新手入门完整指南
- [Onboarding Wizard](https://docs.clawd.bot/start/wizard) - 向导式配置
- [Showcase](https://docs.clawd.bot/start/showcase) - 功能展示
- [FAQ](https://docs.clawd.bot/start/faq) - 常见问题

### 配置文档
- [Configuration Reference](https://docs.clawd.bot/gateway/configuration) - 完整配置参考
- [Gateway Runbook](https://docs.clawd.bot/gateway) - 网关运维手册
- [Security Guide](https://docs.clawd.bot/gateway/security) - 安全配置指南
- [Doctor Tool](https://docs.clawd.bot/gateway/doctor) - 诊断和迁移工具

### 通道配置
- [Channels Overview](https://docs.clawd.bot/channels) - 通道总览
- [WhatsApp](https://docs.clawd.bot/channels/whatsapp) - WhatsApp 配置
- [Telegram](https://docs.clawd.bot/channels/telegram) - Telegram 配置
- [Discord](https://docs.clawd.bot/channels/discord) - Discord 配置
- [Slack](https://docs.clawd.bot/channels/slack) - Slack 配置
- [更多通道...](https://docs.clawd.bot/channels)

### 高级功能
- [Browser Control](https://docs.clawd.bot/tools/browser) - 浏览器控制
- [Canvas & A2UI](https://docs.clawd.bot/platforms/mac/canvas) - 可视化工作区
- [Voice Wake](https://docs.clawd.bot/nodes/voicewake) - 语音唤醒
- [Skills Platform](https://docs.clawd.bot/tools/skills) - 技能平台
- [Remote Gateway](https://docs.clawd.bot/gateway/remote) - 远程网关

### 平台指南
- [macOS](https://docs.clawd.bot/platforms/macos) - Mac 应用配置
- [iOS](https://docs.clawd.bot/platforms/ios) - iOS 节点
- [Android](https://docs.clawd.bot/platforms/android) - Android 节点
- [Linux](https://docs.clawd.bot/platforms/linux) - Linux 部署
- [Windows (WSL2)](https://docs.clawd.bot/platforms/windows) - Windows 支持

---

## 🔧 下一步操作

### 1. 基础配置

```bash
# 运行向导式配置
pnpm clawdbot onboard --install-daemon
```

这将引导您完成：
- ✅ 网关配置
- ✅ 工作区设置
- ✅ 通道连接
- ✅ 技能安装
- ✅ 守护进程设置

### 2. 最小配置文件

创建 `~/.clawdbot/clawdbot.json`：

```json5
{
  agent: {
    // 选择您的模型
    model: "anthropic/claude-opus-4-5"
  },
  gateway: {
    // 网关配置
    mode: "local",
    bind: "loopback",
    port: 18789
  }
}
```

### 3. 配置消息通道

**WhatsApp 示例：**
```bash
# 登录 WhatsApp
pnpm clawdbot channels login

# 配置允许列表
pnpm clawdbot config set channels.whatsapp.allowFrom "+1234567890"
```

**Telegram 示例：**
```bash
# 设置 Bot Token
pnpm clawdbot config set channels.telegram.botToken "YOUR_BOT_TOKEN"
```

### 4. 启动网关

```bash
# 启动网关
pnpm clawdbot gateway run --port 18789

# 或使用监控模式（自动重载）
pnpm gateway:watch
```

### 5. 测试 AI 助手

```bash
# 发送消息
pnpm clawdbot message send --to "+1234567890" --message "测试消息"

# 直接与 AI 交互
pnpm clawdbot agent --message "你好，请介绍一下自己"
```

---

## ⚠️ 注意事项

### 安全提示

1. **DM 配置策略**
   - 默认启用配对模式 (`dmPolicy="pairing"`)
   - 需要批准配对码才能与陌生人交互
   - 公开 DM 需要显式设置 `dmPolicy="open"` 和 `allowFrom: ["*"]`

2. **凭证管理**
   - 凭证存储在 `~/.clawdbot/credentials/`
   - 会话数据在 `~/.clawdbot/sessions/`
   - 不要提交敏感配置到版本控制

3. **运行 doctor 工具**
   ```bash
   pnpm clawdbot doctor
   ```
   检测配置问题和安全风险

### 开发注意事项

1. **版本管理**
   - 当前版本 (2026.1.26) 尚未发布到 npm
   - 使用了工作区引用来解决依赖问题
   - 发布前需要同步所有包版本

2. **构建流程**
   - 修改 TypeScript 代码后运行 `pnpm build`
   - UI 变更需要 `pnpm ui:build`
   - 使用 `pnpm gateway:watch` 获得自动重载

3. **测试覆盖率**
   - 最低覆盖率要求：70%（行/分支/函数/语句）
   - 运行 `pnpm test:coverage` 查看报告

---

## 🐛 故障排除

### 常见问题

**1. pnpm install 失败**
```bash
# 清除缓存并重新安装
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**2. 构建错误**
```bash
# 清理并重新构建
rm -rf dist
pnpm build
```

**3. CLI 命令找不到**
```bash
# 确保使用 pnpm 运行
pnpm clawdbot --version

# 或使用完整路径
node dist/entry.js --version
```

**4. 网关无法启动**
```bash
# 检查端口占用
lsof -i :18789

# 使用不同端口
pnpm clawdbot gateway --port 18790
```

### 获取帮助

- 📖 [文档中心](https://docs.clawd.bot)
- 💬 [Discord 社区](https://discord.gg/clawd)
- 🐛 [GitHub Issues](https://github.com/clawdbot/clawdbot/issues)
- 📧 [故障排除指南](https://docs.clawd.bot/channels/troubleshooting)

---

## 📊 项目统计

| 指标 | 值 |
|------|-----|
| 总文件数 | 2509+ |
| 代码行数 | ~700 LOC/file 平均 |
| 测试覆盖率 | 目标 ≥70% |
| 支持的通道 | 13+ (核心 + 扩展) |
| 支持的平台 | macOS, iOS, Android, Linux, Windows (WSL2) |
| 开发语言 | TypeScript (ESM) |
| 运行时 | Node.js ≥22 |

---

## 🎉 安装成功！

项目已完全配置并准备就绪。您可以：

1. ✅ 运行开发命令
2. ✅ 启动网关服务
3. ✅ 连接消息通道
4. ✅ 与 AI 助手交互
5. ✅ 开始开发和测试

祝您使用愉快！🦞

---

*最后更新: 2026年1月27日*
