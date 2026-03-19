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

### 异步（推荐）

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

---

## API 参考

### `DiscoveryClient(gateway_addr, *, app_secret, ...)`

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

---

### 心跳 / 保活

心跳可选，用于向网关上报服务健康状态，维持 ETCD 租约。
`instance_id` 由管理员配置服务端点时设置，可通过 `get_instances()` 查询。

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
await client.start_keepalive(
    service_name="stew.api.v1.OrderService",
    instance_id="order-service-prod-1",
    interval=30,              # 每 30 秒发送一次，应小于 TTL（默认 60 s）
    on_error=lambda e: logging.warning("keepalive error: %s", e),
)

# ... 服务运行中 ...

# 停止单个实例的心跳循环
client.stop_keepalive(
    service_name="stew.api.v1.OrderService",
    instance_id="order-service-prod-1",
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

适合作为 Docker `ENTRYPOINT` 脚本或 Kubernetes init-container：

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
    # 查询当前激活版本用于乐观锁
    versions = c.list_descriptor_versions(SVC_NAME)
    active = next((v.version for v in versions if v.is_active), None)

    try:
        result = c.upload_descriptor_from_file(
            service_name=SVC_NAME,
            pb_path=PB_PATH,
            version=VERSION,
            description="auto-submitted at startup",
            previous_version=active or "",
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
    ├── discovery_client.py    # 主 SDK 实现
    └── api/v1/                # protoc 生成的 pb2 文件
```
