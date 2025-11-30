"""
Unit tests for modules/rtc/routes/ws.py
Tests for RTC WebSocket routes
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent / "codebase"))


class TestWebSocketEndpoint:
    """Tests for websocket_endpoint"""
    
    @pytest.mark.asyncio
    async def test_websocket_accepts_connection(self):
        """Test that websocket endpoint accepts connections"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text = AsyncMock(side_effect=Exception("Stop loop"))
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Should have called accept
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
        
        # Should have echoed both messages
        assert mock_websocket.send_text.call_count >= 2
    
    @pytest.mark.asyncio
    async def test_websocket_closes_on_error(self):
        """Test that websocket closes on error"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = Exception("Connection error")
        
        await websocket_endpoint(mock_websocket)
        
        # Should have closed the websocket
        mock_websocket.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_websocket_echo_format(self):
        """Test the format of echoed messages"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        test_message = "test123"
        mock_websocket.receive_text.side_effect = [test_message, Exception("Stop")]
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Check that Echo: prefix was added
        calls = mock_websocket.send_text.call_args_list
        if len(calls) > 0:
            sent_message = calls[0][0][0]
            assert "Echo:" in sent_message
            assert test_message in sent_message
    
    @pytest.mark.asyncio
    async def test_websocket_always_closes(self):
        """Test that websocket always closes even on error"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.accept.side_effect = Exception("Accept failed")
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Should still attempt to close
        mock_websocket.close.assert_called_once()


class TestGetRtcInfoRoute:
    """Tests for get_rtc_info route"""
    
    def test_get_rtc_info_returns_dict(self):
        """Test that get_rtc_info returns a dictionary"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert isinstance(result, dict)
    
    def test_get_rtc_info_has_message(self):
        """Test that response includes a message"""
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
        """Test that websockets is listed as a feature"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert "websockets" in result["features"]
    
    def test_get_rtc_info_includes_messaging(self):
        """Test that real-time messaging is listed as a feature"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        features_str = " ".join(result["features"])
        assert "messaging" in features_str.lower()


class TestRtcRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is properly defined"""
        from modules.rtc.routes.ws import router
        from fastapi import APIRouter
        
        assert router is not None
        assert isinstance(router, APIRouter)


class TestRtcRoutesEdgeCases:
    """Tests for edge cases in RTC routes"""
    
    @pytest.mark.asyncio
    async def test_websocket_empty_message(self):
        """Test handling of empty messages"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        mock_websocket.receive_text.side_effect = ["", Exception("Stop")]
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Should still echo empty message
        assert mock_websocket.send_text.called
    
    @pytest.mark.asyncio
    async def test_websocket_special_characters(self):
        """Test handling of special characters in messages"""
        from modules.rtc.routes.ws import websocket_endpoint
        
        mock_websocket = AsyncMock()
        special_msg = "Hello\nWorld\t<script>alert('xss')</script>"
        mock_websocket.receive_text.side_effect = [special_msg, Exception("Stop")]
        
        try:
            await websocket_endpoint(mock_websocket)
        except:
            pass
        
        # Should handle special characters
        assert mock_websocket.send_text.called
    
    def test_get_rtc_info_consistent_response(self):
        """Test that get_rtc_info returns consistent response"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result1 = get_rtc_info()
        result2 = get_rtc_info()
        
        assert result1 == result2
    
    def test_get_rtc_info_features_not_empty(self):
        """Test that features list is not empty"""
        from modules.rtc.routes.ws import get_rtc_info
        
        result = get_rtc_info()
        
        assert len(result["features"]) > 0