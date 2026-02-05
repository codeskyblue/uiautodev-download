# uiautodev工具下载界面

这个项目提供uiautodev工具的下载功能，以及统计下载量，支持按月，年维度统计，保存到json中就行了。

项目基于Cloudflare的r2提供下载支持。点击下载会自动重定向到对应的下载地址，从而实现下载计数。
访问用的key，secret，endpoint都需要从.env文件中获取。

r2下的目录结构为

```
0.2.1
 - uiautodev-desktop.dmg
 - uiautodev-windows.exe

0.2.0
 - uiautodev-desktop.dmg
 - uiautodev-windows.exe
```

默认使用最新的版本号作为下载地址。通过点击查看历史可以看到所有的版本文件。

# 后端设计

下载地址的格式为

https://dl.uiauto.dev/0.2.1/uiautodev-desktop.dmg

# 前端设计

- 使用sveltekit作为前端框架
- 使用tailwindcss定义样式
- 使用命令行来初始化前端

    ```
    npx sv create frontend --template minimal --types ts --install bun --add prettier --add tailwindcss="plugins:typography"
    cd frontend && bun add lucide
    ```

- 图标使用https://lucide.dev/guide/
- 语言要支持国际化(中英）


- 使用fastapi作为后端
- 支持使用命令行的--port或env PORT传递端口，监听0.0.0.0