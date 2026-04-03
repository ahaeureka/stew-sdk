from pathlib import Path

from stew.discovery_client import Endpoint, EndpointBinding, GatewayClient


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
        endpoint=Endpoint(address="127.0.0.1", port=50051, weight=10),
    )
    binding = EndpointBinding(
        endpoint_id="endpoint-123",
        service_name="stew.api.v1.TestService",
        address="127.0.0.1",
        port=50051,
        weight=10,
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
        endpoint=Endpoint(address="127.0.0.1", port=50052, weight=10),
    )
    stale_binding = EndpointBinding(
        endpoint_id="endpoint-123",
        service_name="stew.api.v1.TestService",
        address="127.0.0.1",
        port=50051,
        weight=10,
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
    assert desired.weight == 10
    assert desired.protocol == "grpc"
    assert desired.tls_enabled is False