"""Tests for generated RPC method behavior."""

from unittest.mock import AsyncMock

import pytest

from copilot.generated.rpc import (
    CommandsApi,
    CommandsInvokeRequest,
    ServerModelsApi,
    ServerToolsApi,
    SlashCommandInvocationResultKind,
)


@pytest.mark.asyncio
async def test_commands_invoke_deserializes_slash_command_result():
    client = AsyncMock()
    client.request = AsyncMock(return_value={"kind": "text", "text": "hello", "markdown": True})
    api = CommandsApi(client, "sess-1")

    result = await api.invoke(CommandsInvokeRequest(name="help"))

    assert result.kind is SlashCommandInvocationResultKind.TEXT
    assert result.text == "hello"
    assert result.markdown is True


@pytest.mark.asyncio
async def test_generated_rpc_rejects_missing_required_params():
    client = AsyncMock()
    api = CommandsApi(client, "sess-1")

    with pytest.raises(TypeError, match="params is required"):
        await api.invoke(None)  # type: ignore[arg-type]

    client.request.assert_not_called()


@pytest.mark.asyncio
async def test_generated_rpc_allows_missing_optional_only_params():
    client = AsyncMock()
    client.request = AsyncMock(side_effect=[{"models": []}, {"tools": []}])

    await ServerModelsApi(client).list()
    await ServerToolsApi(client).list()

    assert client.request.call_args_list[0].args[:2] == ("models.list", {})
    assert client.request.call_args_list[1].args[:2] == ("tools.list", {})


@pytest.mark.asyncio
async def test_generated_session_rpc_checks_active_callback_before_request():
    client = AsyncMock()
    api = CommandsApi(
        client,
        "sess-1",
        lambda: (_ for _ in ()).throw(RuntimeError("session inactive")),
    )

    with pytest.raises(RuntimeError, match="session inactive"):
        await api.invoke(CommandsInvokeRequest(name="help"))

    client.request.assert_not_called()
