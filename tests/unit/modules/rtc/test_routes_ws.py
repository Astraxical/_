"""
Unit tests for modules/rtc/routes/ws.py
Tests for RTC WebSocket and info routes
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestWebSocketEndpoint:
    """Tests for websocket_endpoint"""
    
    @pytest.mark.asyncio
    async def test_websocket_accepts_connection(self):
        """Test that websocket accepts incoming connections"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = Exception("Stop loop")
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        mock_websocket.accept.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_echoes_messages(self):
        """Test that websocket echoes received messages"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        messages = ["Hello", "World"]
        mock_websocket.receive_text.side_effect = messages + [Exception("Stop")]
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Should have sent echo messages
        assert mock_websocket.send_text.call_count >= 1
    
    @pytest.mark.asyncio
    async def test_websocket_handles_exceptions(self):
        """Test that websocket handles exceptions gracefully"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = Exception("Connection error")
        
        # Should not raise exception
        await websocket_endpoint(mock_websocket)
        
        mock_websocket.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_closes_on_completion(self):
        """Test that websocket is closed after communication ends"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = Exception("End")
        
        await websocket_endpoint(mock_websocket)
        
        mock_websocket.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_echo_format(self):
        """Test that echo messages have correct format"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = ["test message", Exception("Stop")]
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Check that sent message contains "Echo:"
        if mock_websocket.send_text.called:
            call_args = mock_websocket.send_text.call_args[0][0]
            assert "Echo:" in call_args


class TestGetRTCInfo:
    """Tests for get_rtc_info route"""
    
    def test_get_rtc_info_returns_dict(self):
        """Test that get_rtc_info returns dictionary"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert isinstance(result, dict)
    
    def test_get_rtc_info_has_message(self):
        """Test that response includes message"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "message" in result
    
    def test_get_rtc_info_has_features(self):
        """Test that response includes features list"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "features" in result
        assert isinstance(result["features"], list)
    
    def test_get_rtc_info_includes_websockets(self):
        """Test that features include websockets"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "websockets" in result["features"]
    
    def test_get_rtc_info_includes_messaging(self):
        """Test that features include real-time messaging"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "real-time messaging" in result["features"]


class TestRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is defined"""
        from modules.rtc.routes.ws import router
        
        assert router is not None
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        from modules.rtc.routes.ws import router
        
        assert isinstance(router, APIRouter)


class TestRTCRouteIntegration:
    """Integration tests for RTC routes"""
    
    def test_get_rtc_info_with_test_client(self):
        """Test RTC info endpoint with FastAPI TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.rtc.routes.ws import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "features" in data
    
    @pytest.mark.asyncio
    async def test_websocket_with_test_client(self):
        """Test WebSocket endpoint with TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.rtc.routes.ws import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        # WebSocket testing with TestClient
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("test")
            data = websocket.receive_text()
            assert "Echo:" in data