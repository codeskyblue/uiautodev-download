# 介绍
这是一个下载站的项目。其官方主页是https://uiauto.dev 一个用于移动端UI自动化的工具。

首页显示所有的版本，默认只显示最新版的下载地址，其他的可以通过链接点击进进入到历史版本界面。历史版本界面就像普通的文件浏览器一样。

后端接口地址 http://localhost:7001/openapi.json

# 技术栈

- bun 作为nodejs的包管理工具
- sveltekit ref:mcp svelte
- shadcn-svelte ref:mcp shadcn-svelte
- tailwindcss 用于前端的样式

# 工具使用

- 获取json结尾的内容，可以直接用curl来获取。加上--max-time 10 防止接收超时

# 修改后的检查

- svelte-autofixer的警告不能忽略
- 相关的测试也必须全部通过

这步是一定要做的，关于怎么做，自己想想。想出来后，补充到该文档中。