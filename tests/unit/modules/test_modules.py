"""
Unit tests for module __init__ files
Tests for admin, forums, and rtc module initialization
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestAdminModule:
    """Tests for modules/admin/__init__.py"""
    
    def test_admin_router_exists(self):
        """Test that admin module exports a router"""
        from modules.admin import router
        
        assert router is not None
        from fastapi import APIRouter
        assert isinstance(router, APIRouter)
    
    def test_admin_router_prefix(self):
        """Test that admin router has correct prefix"""
        from modules.admin import router
        
        assert router.prefix == "/admin"
    
    def test_admin_get_module_info(self):
        """Test get_module_info returns correct structure"""
        from modules.admin import get_module_info
        
        info = get_module_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "admin"
        assert info["routes"] == ["/admin/*"]
        assert info["local_data_path"] == "modules/admin/data"
    
    def test_admin_module_info_keys(self):
        """Test that module info has all required keys"""
        from modules.admin import get_module_info
        
        info = get_module_info()
        
        assert "name" in info
        assert "routes" in info
        assert "local_data_path" in info


class TestForumsModule:
    """Tests for modules/forums/__init__.py"""
    
    def test_forums_router_exists(self):
        """Test that forums module exports a router"""
        from modules.forums import router
        
        assert router is not None
        from fastapi import APIRouter
        assert isinstance(router, APIRouter)
    
    def test_forums_router_prefix(self):
        """Test that forums router has correct prefix"""
        from modules.forums import router
        
        assert router.prefix == "/forums"
    
    def test_forums_get_module_info(self):
        """Test get_module_info returns correct structure"""
        from modules.forums import get_module_info
        
        info = get_module_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "forums"
        assert info["routes"] == ["/forums/*"]
        assert info["local_data_path"] == "modules/forums/data"
    
    def test_forums_module_info_keys(self):
        """Test that module info has all required keys"""
        from modules.forums import get_module_info
        
        info = get_module_info()
        
        assert "name" in info
        assert "routes" in info
        assert "local_data_path" in info


class TestRTCModule:
    """Tests for modules/rtc/__init__.py"""
    
    def test_rtc_router_exists(self):
        """Test that rtc module exports a router"""
        from modules.rtc import router
        
        assert router is not None
        from fastapi import APIRouter
        assert isinstance(router, APIRouter)
    
    def test_rtc_router_prefix(self):
        """Test that rtc router has correct prefix"""
        from modules.rtc import router
        
        assert router.prefix == "/rtc"
    
    def test_rtc_get_module_info(self):
        """Test get_module_info returns correct structure"""
        from modules.rtc import get_module_info
        
        info = get_module_info()
        
        assert isinstance(info, dict)
        assert info["name"] == "rtc"
        assert info["routes"] == ["/rtc/*"]
        assert info["local_data_path"] == "modules/rtc/data"
    
    def test_rtc_module_info_keys(self):
        """Test that module info has all required keys"""
        from modules.rtc import get_module_info
        
        info = get_module_info()
        
        assert "name" in info
        assert "routes" in info
        assert "local_data_path" in info


class TestForumsModels:
    """Tests for modules/forums/models/__init__.py"""
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_category_model_exists(self, mock_sessionmaker, mock_engine):
        """Test that ForumCategory model is defined"""
        from modules.forums.models import ForumCategory
        
        assert ForumCategory is not None
        assert ForumCategory.__tablename__ == "forum_categories"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_thread_model_exists(self, mock_sessionmaker, mock_engine):
        """Test that ForumThread model is defined"""
        from modules.forums.models import ForumThread
        
        assert ForumThread is not None
        assert ForumThread.__tablename__ == "forum_threads"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_post_model_exists(self, mock_sessionmaker, mock_engine):
        """Test that ForumPost model is defined"""
        from modules.forums.models import ForumPost
        
        assert ForumPost is not None
        assert ForumPost.__tablename__ == "forum_posts"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_category_creation(self, mock_sessionmaker, mock_engine):
        """Test creating a ForumCategory instance"""
        from modules.forums.models import ForumCategory
        
        category = ForumCategory(
            name="General Discussion",
            description="General topics"
        )
        
        assert category.name == "General Discussion"
        assert category.description == "General topics"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_thread_creation(self, mock_sessionmaker, mock_engine):
        """Test creating a ForumThread instance"""
        from modules.forums.models import ForumThread
        
        thread = ForumThread(
            title="Test Thread",
            content="Thread content",
            category_id=1,
            author="testuser"
        )
        
        assert thread.title == "Test Thread"
        assert thread.content == "Thread content"
        assert thread.category_id == 1
        assert thread.author == "testuser"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_post_creation(self, mock_sessionmaker, mock_engine):
        """Test creating a ForumPost instance"""
        from modules.forums.models import ForumPost
        
        post = ForumPost(
            content="Post content",
            thread_id=1,
            author="testuser"
        )
        
        assert post.content == "Post content"
        assert post.thread_id == 1
        assert post.author == "testuser"
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_thread_has_category_relationship(self, mock_sessionmaker, mock_engine):
        """Test that ForumThread has category relationship"""
        from modules.forums.models import ForumThread
        
        assert hasattr(ForumThread, 'category')
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_post_has_thread_relationship(self, mock_sessionmaker, mock_engine):
        """Test that ForumPost has thread relationship"""
        from modules.forums.models import ForumPost
        
        assert hasattr(ForumPost, 'thread')
    
    @patch('utils.db.create_engine')
    @patch('utils.db.sessionmaker')
    def test_forum_models_have_timestamps(self, mock_sessionmaker, mock_engine):
        """Test that forum models have timestamp fields"""
        from modules.forums.models import ForumCategory, ForumThread, ForumPost
        
        category = ForumCategory(name="Test", description="Test")
        thread = ForumThread(title="Test", content="Test", category_id=1, author="test")
        post = ForumPost(content="Test", thread_id=1, author="test")
        
        assert hasattr(category, 'created_at')
        assert hasattr(thread, 'created_at')
        assert hasattr(thread, 'updated_at')
        assert hasattr(post, 'created_at')
        assert hasattr(post, 'updated_at')


class TestModuleConsistency:
    """Tests for consistency across modules"""
    
    def test_all_modules_have_router(self):
        """Test that all modules export a router"""
        from modules.admin import router as admin_router
        from modules.forums import router as forums_router
        from modules.rtc import router as rtc_router
        
        from fastapi import APIRouter
        assert isinstance(admin_router, APIRouter)
        assert isinstance(forums_router, APIRouter)
        assert isinstance(rtc_router, APIRouter)
    
    def test_all_modules_have_get_module_info(self):
        """Test that all modules have get_module_info function"""
        from modules.admin import get_module_info as admin_info
        from modules.forums import get_module_info as forums_info
        from modules.rtc import get_module_info as rtc_info
        
        assert callable(admin_info)
        assert callable(forums_info)
        assert callable(rtc_info)
    
    def test_all_module_info_consistent_structure(self):
        """Test that all module info has consistent structure"""
        from modules.admin import get_module_info as admin_info
        from modules.forums import get_module_info as forums_info
        from modules.rtc import get_module_info as rtc_info
        
        for info_func in [admin_info, forums_info, rtc_info]:
            info = info_func()
            assert "name" in info
            assert "routes" in info
            assert "local_data_path" in info
            assert isinstance(info["routes"], list)
    
    def test_module_prefixes_unique(self):
        """Test that all module router prefixes are unique"""
        from modules.admin import router as admin_router
        from modules.forums import router as forums_router
        from modules.rtc import router as rtc_router
        
        prefixes = [admin_router.prefix, forums_router.prefix, rtc_router.prefix]
        assert len(prefixes) == len(set(prefixes))
    
    def test_module_names_match_prefixes(self):
        """Test that module names match their route prefixes"""
        from modules.admin import get_module_info as admin_info, router as admin_router
        from modules.forums import get_module_info as forums_info, router as forums_router
        from modules.rtc import get_module_info as rtc_info, router as rtc_router
        
        assert admin_info()["name"] in admin_router.prefix
        assert forums_info()["name"] in forums_router.prefix
        assert rtc_info()["name"] in rtc_router.prefix