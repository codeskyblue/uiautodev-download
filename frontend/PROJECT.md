# UIAuto.dev Download Site

项目简介：为 https://uiauto.dev 提供下载页面。

## 技术栈

- **包管理器**: bun
- **框架**: SvelteKit (Svelte 5)
- **UI组件**: shadcn-svelte
- **样式**: tailwindcss v4

## 项目结构

```
src/
├── lib/
│   ├── api.ts              # API 服务层
│   ├── components/
│   │   └── ui/             # shadcn-svelte 组件
│   └── utils.ts            # 工具函数
├── routes/
│   ├── +page.svelte        # 首页（最新版本下载）
│   ├── +layout.svelte      # 全局布局
│   ├── +layout.ts          # 预渲染配置
│   └── history/
│       └── +page.svelte    # 历史版本页面
└── routes/layout.css       # 全局样式和 Tailwind 配置
```

## API 接口

后端地址通过 vite.config.ts 代理到 `http://localhost:7001`

- `GET /api/versions` - 获取所有版本列表（按降序排列）
- `GET /api/versions/{version}` - 获取指定版本的文件详情

## 页面说明

### 首页 (/)

显示最新版本的下载链接，包含：
- 版本徽章显示
- 平台检测（macOS/Windows/Linux）
- 文件大小格式化
- 下载按钮

### 历史版本页面 (/history)

可折叠的版本列表，文件浏览器风格：
- 展开显示版本文件
- 最新版本高亮
- 响应式展开/收起

## 代码规范

### Svelte 5 注意事项

1. **链接处理**: 内部链接必须使用 `resolve()` 函数
   ```ts
   import { resolve } from '$app/paths';
   // ✅ 正确
   <a href={resolve('/history')}>History</a>
   // ❌ 错误
   <a href="/history">History</a>
   ```
   - 外部链接（如 `https://...`）和下载链接使用标准 `href`

2. **响应式集合**: 使用 `SvelteSet` 代替原生 `Set`
   ```ts
   import { SvelteSet } from 'svelte/reactivity';
   let expandedVersions = new SvelteSet<string>();
   ```

3. **状态管理**: 使用 `$state` runes
   ```ts
   let data = $state<string>('');
   ```

### shadcn-svelte 组件使用

```ts
import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
import { Badge } from '$lib/components/ui/badge';
import * as Table from '$lib/components/ui/table';
```

### 添加新组件

```bash
bunx shadcn-svelte@latest add <component-name> -y
```

## 开发命令

```bash
bun run dev      # 启动开发服务器
bun run build    # 构建生产版本
bun run preview  # 预览构建结果
```

## 测试检查

修改代码后，使用 svelte-autofixer 检查：
- 运行 MCP svelte-autofixer 工具
- 修复所有 issues 和 suggestions

## 部署配置

- 静态站点预渲染：`export const prerender = true;`
- Vite 代理：开发环境 `/api` 请求代理到后端
