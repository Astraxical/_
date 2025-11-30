"""
Unit tests for RTC WebSocket routes
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch

import sys
sys.path.insert(0, 'codebase')


class TestRTCInfoRoute:
    """Tests for RTC info route"""
    
    def test_get_rtc_info_returns_dict(self):
        """Test that get_rtc_info returns a dictionary"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert isinstance(result, dict)
    
    def test_get_rtc_info_has_message(self):
        """Test that response includes message"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "message" in result
        assert "RTC" in result["message"]
    
    def test_get_rtc_info_has_features(self):
        """Test that response includes features list"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "features" in result
        assert isinstance(result["features"], list)
    
    def test_get_rtc_info_includes_websockets(self):
        """Test that websockets feature is included"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "websockets" in result["features"]
    
    def test_get_rtc_info_includes_messaging(self):
        """Test that real-time messaging feature is included"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "real-time messaging" in result["features"]


class TestWebSocketEndpoint:
    """Tests for WebSocket endpoint"""
    
    @pytest.mark.asyncio
    async def test_websocket_accepts_connection(self):
        """Test that websocket accepts connections"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text = AsyncMock(side_effect=Exception("Stop loop"))
        
        with pytest.raises(Exception):
            await websocket_endpoint(mock_websocket)
        
        mock_websocket.accept.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_echoes_messages(self):
        """Test that websocket echoes received messages"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        messages = ["Hello", "World"]
        mock_websocket.receive_text = AsyncMock(side_effect=messages + [Exception("Stop")])
        
        with pytest.raises(Exception):
            await websocket_endpoint(mock_websocket)
        
        # Check that messages were echoed
        calls = mock_websocket.send_text.call_args_list
        assert any("Echo: Hello" in str(call) for call in calls)
    
    @pytest.mark.asyncio
    async def test_websocket_closes_on_exception(self):
        """Test that websocket closes properly on exception"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text = AsyncMock(side_effect=Exception("Connection error"))
        
        await websocket_endpoint(mock_websocket)
        
        mock_websocket.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_handles_multiple_messages(self):
        """Test that websocket handles multiple messages in sequence"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        messages = ["msg1", "msg2", "msg3"]
        mock_websocket.receive_text = AsyncMock(side_effect=messages + [Exception("Stop")])
        
        with pytest.raises(Exception):
            await websocket_endpoint(mock_websocket)
        
        # Verify multiple sends
        assert mock_websocket.send_text.call_count >= len(messages)


class TestRTCRouterConfiguration:
    """Tests for RTC router configuration"""
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from modules.rtc.routes.ws import router
        from fastapi import APIRouter
        
        assert isinstance(router, APIRouter)


class TestRTCIntegration:
    """Integration tests for RTC routes"""
    
    def test_rtc_info_endpoint_accessible(self):
        """Test that RTC info endpoint is accessible"""
        from modules.rtc.routes.ws import router
        
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "features" in data
    
    def test_websocket_endpoint_exists(self):
        """Test that websocket endpoint is registered"""
        from modules.rtc.routes.ws import router
        
        # Check that websocket route exists
        routes = [route.path for route in router.routes]
        assert "/ws" in routes