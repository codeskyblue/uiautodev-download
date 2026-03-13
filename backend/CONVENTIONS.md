# 开发偏好与规范

## 包管理工具
- **前端**: 使用 `bun` 作为包管理工具
- **后端**: 使用 `uv` 作为包管理工具，Python 版本 3.10

## 设计原则
- 使用测试驱动开发 (TDD)
- 函数不应该过长
- 使用合适的设计模式来组织代码

## 前端设计
- 界面设计要简约现代

## 代码风格偏好

### 优先使用现成的库
与其自己实现，优先选择成熟的现成库。

**示例**: 缓存功能
- ❌ 自己实现 `Cache` 类
- ✅ 使用 [cashews](https://github.com/Krukov/cashews) 库

### 代码简洁性
优先选择更简洁的 API 和写法。

**示例**: 异步线程执行
```python
# ❌ 冗长
loop = asyncio.get_event_loop()
detail = await loop.run_in_executor(None, self._get_version_detail_sync, version)
return detail

# ✅ 简洁
return await asyncio.to_thread(self._get_version_detail_sync, version)
```

### 配置集中管理
使用配置对象而不是直接读取环境变量。

**示例**:
```python
# ❌ 直接读取环境变量
self.access_key = os.getenv("R2_AK")

# ✅ 从 settings 读取
self.access_key = settings.r2_access_key_id
```

### 装饰器风格
偏好使用装饰器来实现横切关注点（如缓存）。

```python
@cache(ttl="10m", key="versions:list")
async def list_versions(self) -> list[str]:
    ...
```

## 项目特定规范
- 后端使用 Python 3.10
- 遵循 TDD 开发流程
