# Clawdbot 网关启动和认证问题修复总结

## 问题描述

启动 clawdbot 网关时遇到以下错误：
```
Disconnected from gateway.
disconnected (1008): device identity required
```

## 根本原因

1. **Signal 频道配置无效**：账户号码 "164" 不完整（缺少国家代码）
2. **网关认证令牌问题**：网关配置中认证模式设置为 `token`，但客户端连接时未提供正确的令牌

## 解决步骤

### 1. 启动网关
```bash
cd /workspaces/clawdbot
nohup pnpm clawdbot gateway run > /tmp/clawdbot-gateway.log 2>&1 &
sleep 3
ss -ltnp | grep 18789  # 验证网关在监听 18789 端口
```

### 2. 诊断配置问题
```bash
pnpm clawdbot doctor
```
输出显示：
- Signal DM 策略为 "pairing"（需要配对码）
- 网关认证模式为 "token"

### 3. 禁用 Signal 频道
Signal 账户配置无效，需要禁用该频道以避免启动失败：
```bash
pnpm clawdbot config set channels.signal.enabled false
```

### 4. 修复网关认证
```bash
pnpm clawdbot doctor --fix
```
此命令自动修复了几个配置问题：
- 调整了文件权限（`~/.clawdbot/clawdbot.json` 设为 600）

### 5. 重启网关应用配置
```bash
pkill -9 -f "clawdbot-gateway|gateway run" || true
sleep 2
nohup pnpm clawdbot gateway run > /tmp/clawdbot-gateway.log 2>&1 &
sleep 3
ss -ltnp | grep 18789
```

### 6. 验证状态
```bash
pnpm clawdbot channels status
```

## 最终状态

✅ **网关正常运行**
- 监听地址：`ws://127.0.0.1:18789`
- 进程 PID：13523
- **无认证错误** —— 连接不再出现 "device identity required" 错误

## 关键配置文件位置
- 配置文件：`~/.clawdbot/clawdbot.json`
- 网关日志：`/tmp/clawdbot-gateway.log`
- 会话存储：`~/.clawdbot/agents/main/sessions/`

## 后续建议

如需使用 Signal 频道，需要配置有效的 Signal 账户（包含完整的国家代码）。
