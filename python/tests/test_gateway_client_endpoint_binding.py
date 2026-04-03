import asyncio
from pathlib import Path

from stew.api.v1 import service_discovery_pb2 as discovery_pb2
from stew.discovery_client import Endpoint, EndpointBinding, GatewayClient
from stew.discovery_client import DiscoveryClient


def make_gateway_client(tmp_path: Path, *, endpoint: Endpoint) -> GatewayClient:
    pb_path = tmp_path / "service.pb"
    pb_path.write_bytes(b"descriptor")
    return GatewayClient(
        "127.0.0.1:3012",
        app_secret="test-secret",
        service_name="stew.api.v1.TestService",
        pb_path=str(pb_path),
        local_endpoint=endpoint,
        endpoint_state_path=str(tmp_path / "endpoint-binding.json"),
    )


def test_resolve_endpoint_binding_reuses_matching_binding(tmp_path: Path) -> None:
    client = make_gateway_client(
        tmp_path,
        endpoint=Endpoint(address="127.0.0.1", port=50051),
    )
    binding = EndpointBinding(
        endpoint_id="endpoint-123",
        service_name="stew.api.v1.TestService",
        address="127.0.0.1",
        port=50051,
        weight=25,
        protocol="grpc",
        tls_enabled=False,
    )

    client._save_endpoint_binding(binding)

    stale, desired = client._resolve_endpoint_binding()

    assert stale is None
    assert desired == binding


def test_resolve_endpoint_binding_rotates_when_config_changes(tmp_path: Path) -> None:
    client = make_gateway_client(
        tmp_path,
        endpoint=Endpoint(address="127.0.0.1", port=50052),
    )
    stale_binding = EndpointBinding(
        endpoint_id="endpoint-123",
        service_name="stew.api.v1.TestService",
        address="127.0.0.1",
        port=50051,
        weight=25,
        protocol="grpc",
        tls_enabled=False,
    )

    client._save_endpoint_binding(stale_binding)

    stale, desired = client._resolve_endpoint_binding()

    assert stale == stale_binding
    assert desired.endpoint_id != stale_binding.endpoint_id
    assert desired.service_name == stale_binding.service_name
    assert desired.address == "127.0.0.1"
    assert desired.port == 50052
    assert desired.weight == 0
    assert desired.protocol == "grpc"
    assert desired.tls_enabled is False


def test_register_endpoint_reuses_existing_remote_endpoint_config() -> None:
    captured: dict[str, object] = {}

    existing_instance = discovery_pb2.ServiceInstance(
        service_name="stew.api.v1.TestService",
        instance_id="endpoint-123",
        version="admin-v1",
        status=discovery_pb2.SERVICE_STATUS_HEALTHY,
        protocol="http",
        tls_enabled=True,
        lb=discovery_pb2.LoadBalancer(
            endpoints=[
                discovery_pb2.Endpoint(
                    address="127.0.0.1",
                    port=50051,
                    weight=25,
                )
            ]
        ),
    )
    registered_instance = discovery_pb2.ServiceInstance(
        service_name="stew.api.v1.TestService",
        instance_id="endpoint-123",
        version="admin-v1",
        status=discovery_pb2.SERVICE_STATUS_HEALTHY,
        protocol="http",
        tls_enabled=True,
        lb=discovery_pb2.LoadBalancer(
            endpoints=[
                discovery_pb2.Endpoint(
                    address="127.0.0.1",
                    port=50051,
                    weight=25,
                )
            ]
        ),
    )

    class Stub:
        async def GetServiceInstances(self, request, metadata, timeout):
            captured["get_instances_request"] = request
            captured["get_instances_metadata"] = metadata
            captured["get_instances_timeout"] = timeout
            return discovery_pb2.GetServiceInstancesResponse(instances=[existing_instance])

        async def RegisterServiceEndpoint(self, request, metadata, timeout):
            captured["register_request"] = request
            captured["register_metadata"] = metadata
            captured["register_timeout"] = timeout
            return discovery_pb2.RegisterServiceEndpointResponse(
                success=True,
                endpoint_id="endpoint-123",
                registered_service=registered_instance,
            )

    client = DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    result = asyncio.run(
        client.register_endpoint(
            service_name="stew.api.v1.TestService",
            endpoint=Endpoint(address="127.0.0.1", port=50051),
        )
    )

    get_instances_request = captured["get_instances_request"]
    register_request = captured["register_request"]
    assert get_instances_request.service_name == "stew.api.v1.TestService"
    assert get_instances_request.healthy_only is False
    assert register_request.endpoint_id == "endpoint-123"
    assert register_request.version == "admin-v1"
    assert register_request.protocol == "http"
    assert register_request.tls_enabled is True
    assert register_request.endpoint.address == "127.0.0.1"
    assert register_request.endpoint.port == 50051
    assert result["endpoint_id"] == "endpoint-123"
    assert result["protocol"] == "http"
    assert result["tls_enabled"] is True


def test_register_endpoint_keeps_default_request_when_no_remote_match() -> None:
    captured: dict[str, object] = {}

    class Stub:
        async def GetServiceInstances(self, request, metadata, timeout):
            captured["get_instances_request"] = request
            return discovery_pb2.GetServiceInstancesResponse(instances=[])

        async def RegisterServiceEndpoint(self, request, metadata, timeout):
            captured["register_request"] = request
            return discovery_pb2.RegisterServiceEndpointResponse(
                success=True,
                endpoint_id="generated-endpoint",
                registered_service=discovery_pb2.ServiceInstance(
                    service_name="stew.api.v1.TestService",
                    instance_id="generated-endpoint",
                    version="",
                    status=discovery_pb2.SERVICE_STATUS_HEALTHY,
                    protocol="grpc",
                    tls_enabled=False,
                    lb=discovery_pb2.LoadBalancer(
                        endpoints=[
                            discovery_pb2.Endpoint(
                                address="127.0.0.1",
                                port=50051,
                                weight=1,
                            )
                        ]
                    ),
                ),
            )

    client = DiscoveryClient("127.0.0.1:3012", app_secret="ak_xxx")
    client._stub = Stub()  # type: ignore[assignment]

    asyncio.run(
        client.register_endpoint(
            service_name="stew.api.v1.TestService",
            endpoint=Endpoint(address="127.0.0.1", port=50051),
        )
    )

    register_request = captured["register_request"]
    assert register_request.endpoint_id == ""
    assert register_request.version == ""
    assert register_request.protocol == "grpc"
    assert register_request.tls_enabled is False