# Stew Gateway — Python SDK

Python 客户端 SDK，用于向 Stew 网关提交 Protobuf 描述符、管理版本及维持服务健康心跳。

---

## 安装

```bash
# 使用 uv（推荐）
cd /path/to/stew/proto/sdk/python
uv sync

# 或直接 pip
pip install grpcio protobuf
```

---

## 前置条件：admin-first 模型

SDK **不负责**服务注册/注销，这些操作需要管理员通过前端完成：

```
1. [管理员] 在管理页面 "服务管理" -> "初始化服务"
   填写服务名、描述、协议 -> 提交

2. [管理员] 系统返回：
   - app_id     — 凭证 ID
   - app_secret — 凭证密钥（仅显示一次，必须妥善保存）

3. [管理员] 在管理页面配置服务端点、负载均衡策略、中间件

4. [管理员] 将 app_secret 通过安全渠道下发给业务团队

5. [业务侧] 使用 SDK 上传 .pb 描述符，触发路由热加载
```

> `app_secret` 是一个格式为 `ak_xxx` 的 API Key，绑定了服务名和操作权限，
> 网关通过它识别调用方有权操作哪个服务。

---

## 快速上手

### 一键接入（推荐）

`GatewayClient` 是最简单的接入方式：连接网关、追加本机 endpoint、上传描述符、启动心跳保活一步完成。
当网关启动时不可达（`UNAVAILABLE`），后台会以指数退避自动轮询重试，直到注册成功，
业务服务无需处理网关宕机场景。首次 keepalive 会立即发送；运行中如果心跳因异常或网络
问题失败，客户端会持续重试，并在恢复阶段只重传本地 `.pb` 描述符，然后再恢复心跳；
前端管理的服务配置不会被本地 SDK 回写覆盖。

当提供 `local_endpoint` 时，SDK 会把该地址注册成一个独立的业务侧 endpoint 实例，并把
`endpoint_id` 持久化到本地绑定文件。默认只把地址、端口、协议、TLS 配置视为 endpoint
身份；`weight` 默认不由业务侧管理，因此不会参与 endpoint 绑定复用判断。前端后续如果调整
该 endpoint 的权重，SDK 不会因此生成新的 `endpoint_id` 或覆盖前端配置。如果地址、端口、
协议或 TLS 配置变化，SDK 才会生成新的 `endpoint_id`，避免覆盖前端已配置的 endpoint。
如果本地还没有保存过 `endpoint_id`，SDK 会先调用 `get_instances()` 拉取当前服务实例，按
地址/端口优先匹配已有 endpoint，并复用远端实例的 `endpoint_id`、`protocol`、`tls_enabled`
等配置后再执行注册，避免把管理端已经配置的实例字段冲掉。

```python
import asyncio
from stew import Endpoint, GatewayClient

async def main():
    async with GatewayClient(
        "127.0.0.1:3012",
        app_secret="ak_xxx",
        service_name="stew.api.v1.OrderService",
        pb_path="./order_service.pb",
        local_endpoint=Endpoint(address="127.0.0.1", port=50051),
    ) as gw:
        # 可选：等待首次注册成功后再提供服务流量
        await gw.registered.wait()
        await asyncio.Event().wait()  # 持续运行

asyncio.run(main())
```

### 异步（低层 API）

需要精细控制描述符版本或手动管理心跳时使用 `DiscoveryClient`：

```python
import asyncio
from stew import DiscoveryClient

async def main():
    async with DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
        result = await client.upload_descriptor_from_file(
            service_name="stew.api.v1.OrderService",
            pb_path="./order_service.pb",
        )
        print("applied version:", result["applied_version"])

asyncio.run(main())
```

### 同步（启动脚本 / 非 async 场景）

```python
from stew import SyncDiscoveryClient

with SyncDiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as c:
    result = c.upload_descriptor_from_file(
        service_name="stew.api.v1.OrderService",
        pb_path="./order_service.pb",
    )
    print("applied version:", result["applied_version"])
```

`local_endpoint` / `register_endpoint()` 的权重约定：

- `Endpoint.weight > 0`：业务侧显式指定权重
- `Endpoint.weight = 0` 或留空：视为“未指定权重”，由前端管理
- 对已有 endpoint：服务端保留当前已有权重
- 对新注册 endpoint：服务端先使用默认权重 `1`
- 前端后续修改权重后，SDK 不会因为权重变化而重建 `endpoint_id`

### 通过环境变量传入凭证

```bash
export APP_SECRET="ak_xxx"
export GATEWAY_ADDR="127.0.0.1:3012"
```

```python
import os
from stew import DiscoveryClient

# app_secret 自动从 APP_SECRET 环境变量读取
async with DiscoveryClient(os.environ["GATEWAY_ADDR"]) as client:
    ...
```

优先级：构造函数 `app_secret` > `api_key` > 环境变量 `APP_SECRET` > `SERVICE_API_KEY`

### 自动透传当前 gRPC Context

如果业务服务本身是通过 Stew 网关接入的，并且在 gRPC handler 内还会再次使用 SDK 调回网关
（例如调用 `FileStorageClient` 下载用户上传的文件），推荐启用 SDK 提供的 gRPC context 自动透传能力。

透传后，SDK 会自动把当前请求里的以下 metadata 一并转发给网关：

- `authorization`
- `x-user-*`
- `x-token-*`
- `x-client-context`
- `x-request-id`
- `traceparent` / `tracestate` / `baggage` / `x-b3-*`

入站请求里的 `x-api-key` 不会被继续转发；SDK 始终使用当前客户端自身的 `app_secret`
作为下游网关调用凭证，避免把上游服务凭证错误透传出去。

#### 同步 gRPC 服务：使用拦截器

```python
from concurrent import futures

import grpc

from stew import FileStorageClient, GrpcContextPassthroughInterceptor


class FileServiceServicer:
    def IngestGatewayFile(self, request, context):
        with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
            info = client.get_file_info(file_id=request.file_id)
            return info


server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=10),
    interceptors=[GrpcContextPassthroughInterceptor()],
)
```

#### `grpc.aio` 服务：使用异步拦截器

```python
import grpc

from stew import AioGrpcContextPassthroughInterceptor, FileStorageClient


class FileServiceServicer:
    async def IngestGatewayFile(self, request, context):
        async with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
            info = await client.get_file_info(file_id=request.file_id)
            return info


server = grpc.aio.server(
    interceptors=[AioGrpcContextPassthroughInterceptor()],
)
```

#### 无法统一挂拦截器时：使用装饰器

```python
from stew import FileStorageClient, grpc_context_passthrough_handler


class FileServiceServicer:
    @grpc_context_passthrough_handler
    async def IngestGatewayFile(self, request, context):
        async with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
            return await client.get_file_info(file_id=request.file_id)
```

只有在业务框架不方便统一注册 gRPC interceptor 时，才建议使用装饰器；能挂拦截器时，优先挂拦截器。

### 文件存储客户端

`FileStorageService` 现在已经接入 SDK，可直接通过 `FileStorageClient` 或 `SyncFileStorageClient` 调用。

```python
import asyncio
from stew import FileStorageClient

async def main():
    async with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
        result = await client.upload_file(
            filename="avatar.png",
            content_type="image/png",
            folder="/profiles",
            data=b"binary-image-data",
        )
        print(result.file_info.id)

asyncio.run(main())
```

如需使用 gRPC 分片下载，SDK 会通过同一个 `DownloadFile` unary RPC 循环发送 `range: bytes=start-end` metadata，而不是退回 HTTP：

```python
import asyncio
from stew import FileStorageClient

async def main():
    async with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
        downloaded = await client.download_file_in_chunks(
            file_id="550e8400-e29b-41d4-a716-446655440000",
            chunk_size=1024 * 1024,
            verify_integrity=True,
            on_progress=lambda p: print(
                f"chunk {p.chunk_index}/{p.total_chunks} "
                f"{p.downloaded_bytes}/{p.total_bytes} bytes"
            ),
        )
        print(downloaded.filename, len(downloaded.data), downloaded.etag)

asyncio.run(main())
```

其中：

- `on_progress` 会在每个分片下载完成后触发一次，参数为 `DownloadProgress`
- `verify_integrity=True` 会在本地拼装完成后计算 SHA-256，再通过 gRPC `DownloadFile(verify_only=true)` 让服务端确认一致性

如果文件较大，优先使用直接写盘接口，避免先把所有分片拼到内存里：

```python
import asyncio
from stew import FileStorageClient

async def main():
    async with FileStorageClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
        saved = await client.download_file_to_path(
            file_id="550e8400-e29b-41d4-a716-446655440000",
            output_path="./downloads/report.pdf",
            chunk_size=1024 * 1024,
            verify_integrity=True,
            replace_existing=True,
        )
        print(saved.path, saved.bytes_written, saved.etag)

asyncio.run(main())
```

`download_file_to_path()` 默认支持断点续下：如果目标路径旁边已经存在同名 `.part` 文件，SDK 会检测已下载字节数，并从对应偏移继续通过 gRPC `Range` metadata 拉取剩余内容。

如果最终目标文件已经存在，SDK 默认会抛出 `FileExistsError`，避免无意覆盖既有业务文件；只有显式传入 `replace_existing=True` 时，下载完成后才会替换目标文件。

更贴近业务接入的完整流程示例见：

- `examples/file_storage_download.py`：通用写盘下载
- `examples/file_storage_business_download.py`：先 `get_file_info()`，再按业务目录落盘并启用续传与完整性校验

---

## API 参考

### `GatewayClient(gateway_addr, *, app_secret, service_name, pb_path, ...)` — 推荐

一键接入封装：追加本机 endpoint + 上传描述符 + 启动心跳，网关不可达时后台自动轮询重试。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `gateway_addr` | `str` | 必填 | 网关地址，如 `127.0.0.1:3012` |
| `app_secret` | `str` | `""` | 管理员下发的服务凭证 |
| `api_key` | `str` | `""` | `app_secret` 的别名（兼容旧代码） |
| `service_name` | `str` | 必填 | 完全限定服务名，如 `stew.api.v1.OrderService` |
| `pb_path` | `str` | 必填 | `.pb` 描述符文件路径 |
| `local_endpoint` | `Endpoint \\| None` | `None` | 业务服务自己的 IP/端口；`weight` 留空或 `0` 表示由前端管理 |
| `endpoint_state_path` | `str` | `""` | endpoint_id 本地绑定文件路径；默认使用 `{pb_path}.endpoint.json` |
| `endpoint_protocol` | `str` | `"grpc"` | 该 endpoint 的后端协议 |
| `endpoint_tls_enabled` | `bool` | `False` | 该 endpoint 是否要求 TLS |
| `version` | `str` | `""` | 版本号，留空自动生成 |
| `description` | `str` | `""` | 版本描述 |
| `keepalive_interval` | `int` | `30` | 心跳间隔（秒），须小于网关 TTL |
| `descriptor_refresh_interval` | `int` | `30` | 本地 `.pb` 文件轮询间隔（秒），`0` 表示关闭动态刷新 |
| `retry_base_delay` | `float` | `5.0` | 网关不可达时首次重试等待（秒） |
| `retry_max_delay` | `float` | `300.0` | 重试间隔上限（秒） |
| `use_tls` | `bool` | `False` | 是否启用 TLS |
| `timeout` | `float` | `10.0` | 单次 RPC 超时（秒） |
| `on_registered` | `Callable[[], None] \| None` | `None` | 首次注册成功后的回调 |

**属性与方法：**

| 成员 | 说明 |
|------|------|
| `registered` | `asyncio.Event`，首次注册成功后置位 |
| `await start()` | 连接并执行注册；网关不可达时启动后台重试任务 |
| `await stop()` | 取消重试任务并关闭连接 |

`endpoint_state_path` 保存的是 endpoint 配置与 `endpoint_id` 的绑定关系。默认文件名是 `{pb_path}.endpoint.json`。

运行中恢复行为：

- keepalive 启动后立即发送第一次心跳，不等待一个完整间隔。
- 心跳遇到异常、网络问题或网关重启后的运行时状态丢失时，会按指数退避持续恢复。
- 恢复时只会重传本地 `.pb` 描述符，再补发心跳；不会覆盖前端管理的实例配置。
- 当提供 `local_endpoint` 时，SDK 会为该 endpoint 生成或复用本地保存的 `endpoint_id`，并以追加实例的方式注册到网关，不会覆盖已有 endpoint。
- `weight` 不参与 endpoint 绑定复用判断。业务侧通常只传地址和端口，权重由前端统一调整。
- `GatewayClient` 默认每 30 秒检查一次本地 `.pb` 文件，文件变化后自动上传新描述符，实现动态更新服务。

**错误处理行为：**

| 情形 | 行为 |
|------|------|
| 网关 `UNAVAILABLE` | 后台指数退避重试（5 s → 10 s → … → 300 s） |
| `ConflictError`（乐观锁冲突） | 视为幂等成功，注册完成 |
| `PERMISSION_DENIED` / `INVALID_ARGUMENT` | 记录警告，停止重试（非瞬时错误） |

---

### `DiscoveryClient(gateway_addr, *, app_secret, ...)` — 低层 API

需要精细控制版本或手动管理心跳时使用。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `gateway_addr` | `str` | 必填 | 网关地址，如 `127.0.0.1:3012` |
| `app_secret` | `str` | `""` | 管理员下发的服务凭证 |
| `api_key` | `str` | `""` | `app_secret` 的别名（兼容旧代码） |
| `use_tls` | `bool` | `False` | 是否启用 TLS |
| `timeout` | `float` | `10.0` | 单次 RPC 超时（秒） |
| `retry_max` | `int` | `10` | 网关不可达时最大重试次数 |
| `retry_base_delay` | `float` | `2.0` | 初始重试间隔（秒），指数增长 |
| `retry_max_delay` | `float` | `60.0` | 重试间隔上限（秒） |

### gRPC Context 透传辅助 API

| API | 说明 |
|------|------|
| `GrpcContextPassthroughInterceptor()` | 用于 `grpc.server(...)` 的同步服务端拦截器 |
| `AioGrpcContextPassthroughInterceptor()` | 用于 `grpc.aio.server(...)` 的异步服务端拦截器 |
| `@grpc_context_passthrough_handler` | 无法统一挂拦截器时，可直接包单个业务方法 |
| `grpc_context_passthrough(context)` | 低层 context manager，适合特殊场景手工包裹 |
| `collect_grpc_context_metadata(context)` | 提取当前请求中允许透传的 metadata 白名单 |

---

### 描述符管理

#### `upload_descriptor_from_file()`

从文件读取并上传 `.pb` 描述符，是最常用的方法。

```python
result = await client.upload_descriptor_from_file(
    service_name="stew.api.v1.OrderService",  # 必须与 app_secret 绑定的服务名一致
    pb_path="./order_service.pb",
    version="v2.1.0",           # 留空则自动生成 {timestamp}-{hash}
    description="v2.1.0 新增退款接口",
    previous_version="v2.0.0", # 乐观锁：当前激活版本，留空则跳过检查
    force=False,                # True 则忽略兼容性警告
)
# 返回值
# {
#   "applied_version":        "v2.1.0",
#   "discovered_services":    ["stew.api.v1.OrderService"],
#   "compatibility_warnings": [],
#   "descriptor_hash":        "sha256:a1b2c3...",
# }
```

#### `upload_descriptor()`

直接传入二进制数据（适合从内存或网络获取描述符的场景）：

```python
with open("order_service.pb", "rb") as f:
    data = f.read()

result = await client.upload_descriptor(
    service_name="stew.api.v1.OrderService",
    descriptor_data=data,
    version="v2.1.0",
)
```

#### `rollback_descriptor()`

回滚到之前的版本：

```python
active = await client.rollback_descriptor(
    service_name="stew.api.v1.OrderService",
    target_version="v2.0.0",
)
print("当前激活版本:", active)
```

#### `list_descriptor_versions()`

查看版本历史：

```python
versions = await client.list_descriptor_versions("stew.api.v1.OrderService")
for v in versions:
    flag = "[active]" if v.is_active else "        "
    print(f"{flag} {v.version}  hash={v.descriptor_hash[:12]}  {v.description}")
```

#### `get_active_version()`

获取当前激活版本号（用于乐观锁）：

```python
active = await client.get_active_version("stew.api.v1.OrderService")
# 如果没有任何版本，返回 None
```

#### `refresh_descriptor_from_file()`

重新读取本地 `.pb` 文件并执行一次描述符刷新，只更新描述符本身：

```python
result = await client.refresh_descriptor_from_file(
    service_name="stew.api.v1.OrderService",
    pb_path="./order_service.pb",
    description="manual descriptor refresh",
)
print(result["applied_version"])
```

#### `register_endpoint()`

追加一个业务侧自管理的 endpoint，不影响前端已配置的其他 endpoint。推荐做法是业务侧只注册 `address` 和 `port`，不要主动设置 `weight`；权重由前端统一配置。

```python
registration = await client.register_endpoint(
    service_name="stew.api.v1.OrderService",
    endpoint=Endpoint(address="127.0.0.1", port=50051),
    endpoint_id="existing-or-empty",
)
print(registration["endpoint_id"])
```

返回结果里的 `endpoint_id` 可直接用于后续 `heartbeat()` 或 `start_keepalive()` 的 `instance_id`。当 `weight`
留空或为 `0` 时：

- SDK 在未显式传入 `endpoint_id` 时，会先查询现有实例；如果发现同地址/端口的 endpoint，优先复用远端 `endpoint_id`，并沿用已有 `protocol`、`tls_enabled`、`version`
- 如果该地址/端口对应的 endpoint 已存在，服务端会保留已有权重
- 如果这是一个新 endpoint，服务端先使用默认权重 `1`
- 前端后续改权重时，不会导致 SDK 重新生成新的 `endpoint_id`

#### `deregister_endpoint()`

按 `endpoint_id` 注销一个业务侧 endpoint：

```python
await client.deregister_endpoint(
    service_name="stew.api.v1.OrderService",
    endpoint_id="endpoint-123",
)
```

#### `start_descriptor_refresh()`

周期轮询本地 `.pb` 文件，发现变化后自动上传新描述符：

```python
await client.start_descriptor_refresh(
    service_name="stew.api.v1.OrderService",
    pb_path="./order_service.pb",
    interval=30,
)

# ... 服务运行中 ...

client.stop_descriptor_refresh(
    service_name="stew.api.v1.OrderService",
    pb_path="./order_service.pb",
)
```

---

### 心跳 / 保活

心跳可选，用于向网关上报服务健康状态，维持 ETCD 租约。
如果你是通过 `register_endpoint()` 追加业务侧 endpoint，后续 keepalive 应使用返回的 `endpoint_id` 作为 `instance_id`；如果是对已有实例发心跳，可通过 `get_instances()` 查询。

#### 单次心跳

```python
from stew.api.v1 import service_discovery_pb2 as _pb

await client.heartbeat(
    service_name="stew.api.v1.OrderService",
    instance_id="order-service-prod-1",
    status=_pb.SERVICE_STATUS_HEALTHY,   # 默认值
    message="all systems nominal",
)
```

状态常量：

| 常量 | 含义 |
|------|------|
| `_pb.SERVICE_STATUS_HEALTHY` | 健康 |
| `_pb.SERVICE_STATUS_UNHEALTHY` | 不健康 |
| `_pb.SERVICE_STATUS_MAINTENANCE` | 维护中 |
| `_pb.SERVICE_STATUS_DRAINING` | 排水中（下线前） |

#### 后台心跳循环

```python
from stew import Endpoint, RegistrationConfig

registration = await client.register_endpoint(
    service_name="stew.api.v1.OrderService",
    endpoint=Endpoint(address="127.0.0.1", port=50051),
)

await client.start_keepalive(
    service_name="stew.api.v1.OrderService",
    instance_id=registration["endpoint_id"],
    interval=30,              # 每 30 秒发送一次，应小于 TTL（默认 60 s）
    registration=RegistrationConfig(
        descriptor_path="./order_service.pb",
    ),
    on_error=lambda e: logging.warning("keepalive error: %s", e),
)

await client.start_descriptor_refresh(
    service_name="stew.api.v1.OrderService",
    pb_path="./order_service.pb",
    interval=30,
)

# ... 服务运行中 ...

# 停止单个实例的心跳循环
client.stop_keepalive(
    service_name="stew.api.v1.OrderService",
    instance_id=registration["endpoint_id"],
)

client.stop_descriptor_refresh(
    service_name="stew.api.v1.OrderService",
    pb_path="./order_service.pb",
)

# 关闭 client 时自动取消所有心跳循环
await client.close()
```

---

### 查询接口（只读）

#### `list_services()`

列出网关上所有已注册的服务：

```python
services = await client.list_services(
    name_prefix="stew.api.v1.",  # 可选，按前缀过滤
    tag_filters={"env": "prod"}, # 可选，按标签过滤
)
for s in services:
    print(s["service_name"], s["instance_id"], s["status"])
```

#### `get_instances()`

查询某个服务的所有实例：

```python
instances = await client.get_instances(
    "stew.api.v1.OrderService",
    healthy_only=True,
)
for inst in instances:
    print(inst["instance_id"], inst["version"], inst["status"])
```

---

## 错误处理

```python
from stew import DiscoveryClient, DiscoveryError, ConflictError, NotFoundError

async with DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx") as client:
    try:
        await client.upload_descriptor_from_file(
            service_name="stew.api.v1.OrderService",
            pb_path="./order_service.pb",
            previous_version="v2.0.0",
        )
    except ConflictError:
        # previous_version 与网关当前激活版本不一致（乐观锁冲突）
        active = await client.get_active_version("stew.api.v1.OrderService")
        print("版本冲突，当前激活版本:", active)
    except NotFoundError as e:
        # 回滚时目标版本不存在
        print("版本不存在:", e)
    except DiscoveryError as e:
        # 其他 gRPC 错误（PERMISSION_DENIED、UNAVAILABLE 等）
        print(f"gRPC 错误 [{e.code}]: {e}")
    except PermissionError as e:
        # 调用了 register() / deregister()（admin-only）
        print("权限错误:", e)
```

| 异常 | 触发条件 |
|------|----------|
| `ConflictError` | `previous_version` 乐观锁不匹配（gRPC FAILED_PRECONDITION） |
| `NotFoundError` | 回滚时目标版本不存在（gRPC NOT_FOUND） |
| `DiscoveryError` | 其他 gRPC 错误，`.code` 属性为 `grpc.StatusCode` |
| `PermissionError` | 调用了 `register()` / `deregister()`（admin-only，直接抛出，不发 RPC） |

---

## 完整示例：服务启动时提交描述符

### 方式一：GatewayClient（asyncio 服务，推荐）

网关不可达时自动后台重试，适合长时间运行的 async 服务：

```python
#!/usr/bin/env python3
"""main.py — asyncio 服务入口"""
import asyncio
import logging
import os

from stew import Endpoint, GatewayClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

GATEWAY    = os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012")
APP_SECRET = os.environ["APP_SECRET"]
SVC_NAME   = os.environ["SERVICE_NAME"]
PB_PATH    = os.environ.get("DESCRIPTOR_FILE", "service.pb")
VERSION    = os.environ.get("SERVICE_VERSION", "")

async def main():
    async with GatewayClient(
        GATEWAY,
        app_secret=APP_SECRET,
        service_name=SVC_NAME,
        pb_path=PB_PATH,
        local_endpoint=Endpoint(address="127.0.0.1", port=50051),
        version=VERSION,
        descriptor_refresh_interval=30,
    ) as gw:
        # 等待首次注册成功（会同时追加本机 endpoint 并上传描述符）
        await gw.registered.wait()
        # 启动业务 gRPC server ...
        await asyncio.Event().wait()

asyncio.run(main())
```

### 方式二：SyncDiscoveryClient（启动脚本 / init-container）

适合一次性提交描述符并退出的场景。**注意**：此方式不含自动重试；若网关不可达将直接失败退出。

```python
#!/usr/bin/env python3
"""submit_descriptor.py — 服务启动时向网关提交描述符"""
import logging
import os
import sys

from stew import SyncDiscoveryClient, ConflictError, DiscoveryError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("submit_descriptor")

GATEWAY    = os.environ.get("GATEWAY_ADDR", "127.0.0.1:3012")
APP_SECRET = os.environ["APP_SECRET"]          # 管理员下发的凭证
SVC_NAME   = os.environ["SERVICE_NAME"]        # 如 stew.api.v1.OrderService
PB_PATH    = os.environ.get("DESCRIPTOR_FILE", "service.pb")
VERSION    = os.environ.get("SERVICE_VERSION", "")

with SyncDiscoveryClient(GATEWAY, app_secret=APP_SECRET) as c:
    try:
        result = c.refresh_descriptor_from_file(
            service_name=SVC_NAME,
            pb_path=PB_PATH,
            version=VERSION,
            description="auto-submitted at startup",
        )
        log.info("descriptor applied: %s", result["applied_version"])
        for w in result["compatibility_warnings"]:
            log.warning("compat warning: %s", w)
    except ConflictError as e:
        # 并发启动时另一个实例已先提交，幂等忽略
        log.info("descriptor already updated by peer: %s", e)
    except DiscoveryError as e:
        log.error("descriptor submit failed: %s", e)
        sys.exit(1)
```

---

## 乐观锁并发更新

多实例并发发布时，使用 `previous_version` 保证安全：

```python
from stew import DiscoveryClient, ConflictError
import asyncio

async def safe_upload(client: DiscoveryClient, pb_path: str, version: str):
    svc = "stew.api.v1.OrderService"
    for attempt in range(3):
        active = await client.get_active_version(svc)
        try:
            await client.upload_descriptor_from_file(
                service_name=svc,
                pb_path=pb_path,
                version=version,
                previous_version=active or "",
            )
            return
        except ConflictError:
            if attempt == 2:
                raise
            await asyncio.sleep(0.5 * (attempt + 1))
```

---

## TLS 连接

```python
client = DiscoveryClient(
    "gateway.example.com:443",
    app_secret="ak_xxx",
    use_tls=True,
)
```

---

## 目录结构

```
proto/sdk/python/
├── pyproject.toml
├── README.md                  # 本文件
├── examples/
│   ├── descriptor_submit.py   # 启动时提交描述符（命令行工具）
│   └── keepalive_demo.py      # 心跳保活示例
└── stew/
    ├── __init__.py            # 公开导出
    ├── discovery_client.py    # discovery 兼容入口
    ├── file_storage_client.py # FileStorageService SDK 封装
    ├── _discovery/            # discovery 内部拆分实现
    └── api/v1/                # protoc 生成的 pb2 文件
```
