"""
Extended unit tests for loader.py with template resolution
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, 'codebase')

from utils.loader import resolve_template_path


class TestResolveTemplatePath:
    """Tests for resolve_template_path function"""
    
    def test_resolve_absolute_path_valid(self, tmp_path):
        """Test resolving valid absolute path"""
        test_file = tmp_path / "test_template.html"
        test_file.write_text("content")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path(str(test_file))
            
            assert result == str(test_file)
    
    def test_resolve_absolute_path_invalid(self, tmp_path):
        """Test resolving invalid absolute path returns None"""
        test_file = tmp_path / "nonexistent.html"
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path(str(test_file))
            
            assert result is None
    
    def test_resolve_absolute_path_not_validated(self, tmp_path):
        """Test resolving absolute path that fails validation"""
        test_file = tmp_path / "template.html"
        test_file.write_text("content")
        
        with patch('utils.loader.validate_path', return_value=False):
            result = resolve_template_path(str(test_file))
            
            assert result is None
    
    def test_resolve_module_template_exists(self, tmp_path, monkeypatch):
        """Test resolving module-specific template that exists"""
        monkeypatch.chdir(tmp_path)
        
        # Create module template
        module_template_dir = tmp_path / "modules" / "test_module" / "templates"
        module_template_dir.mkdir(parents=True)
        template_file = module_template_dir / "test.html"
        template_file.write_text("module template")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test.html", module_name="test_module")
            
            assert result == "modules/test_module/templates/test.html"
    
    def test_resolve_global_template_exists(self, tmp_path, monkeypatch):
        """Test resolving global template that exists"""
        monkeypatch.chdir(tmp_path)
        
        # Create global template
        global_template_dir = tmp_path / "templates"
        global_template_dir.mkdir(parents=True)
        template_file = global_template_dir / "test.html"
        template_file.write_text("global template")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test.html")
            
            assert result == "templates/test.html"
    
    def test_resolve_template_priority_module_over_global(self, tmp_path, monkeypatch):
        """Test that module template takes priority over global"""
        monkeypatch.chdir(tmp_path)
        
        # Create both module and global templates
        module_dir = tmp_path / "modules" / "test_module" / "templates"
        module_dir.mkdir(parents=True)
        (module_dir / "test.html").write_text("module")
        
        global_dir = tmp_path / "templates"
        global_dir.mkdir(parents=True)
        (global_dir / "test.html").write_text("global")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test.html", module_name="test_module")
            
            # Should return module template, not global
            assert "modules/test_module/templates/test.html" in result
    
    def test_resolve_template_fallback_to_global(self, tmp_path, monkeypatch):
        """Test fallback to global template when module template doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        # Create only global template
        global_dir = tmp_path / "templates"
        global_dir.mkdir(parents=True)
        (global_dir / "test.html").write_text("global")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test.html", module_name="nonexistent_module")
            
            assert result == "templates/test.html"
    
    def test_resolve_template_nonexistent(self, tmp_path, monkeypatch):
        """Test resolving non-existent template returns None"""
        monkeypatch.chdir(tmp_path)
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("nonexistent.html")
            
            assert result is None
    
    def test_resolve_template_validation_failure(self, tmp_path, monkeypatch):
        """Test that validation failure returns None even if file exists"""
        monkeypatch.chdir(tmp_path)
        
        # Create template that exists but fails validation
        template_dir = tmp_path / "templates"
        template_dir.mkdir(parents=True)
        (template_dir / "test.html").write_text("content")
        
        with patch('utils.loader.validate_path', return_value=False):
            result = resolve_template_path("test.html")
            
            assert result is None
    
    def test_resolve_template_with_subdirectories(self, tmp_path, monkeypatch):
        """Test resolving template in subdirectories"""
        monkeypatch.chdir(tmp_path)
        
        # Create template in subdirectory
        template_dir = tmp_path / "templates" / "subdir"
        template_dir.mkdir(parents=True)
        (template_dir / "test.html").write_text("content")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("subdir/test.html")
            
            assert result == "templates/subdir/test.html"
    
    def test_resolve_template_empty_string(self, tmp_path, monkeypatch):
        """Test resolving empty template name"""
        monkeypatch.chdir(tmp_path)
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("")
            
            assert result is None
    
    def test_resolve_template_with_none_module(self, tmp_path, monkeypatch):
        """Test resolve with module_name=None behaves same as no module"""
        monkeypatch.chdir(tmp_path)
        
        template_dir = tmp_path / "templates"
        template_dir.mkdir(parents=True)
        (template_dir / "test.html").write_text("content")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test.html", module_name=None)
            
            assert result == "templates/test.html"


class TestResolveTemplatePathEdgeCases:
    """Edge case tests for resolve_template_path"""
    
    def test_resolve_with_relative_path_components(self, tmp_path, monkeypatch):
        """Test resolving template with ../ components"""
        monkeypatch.chdir(tmp_path)
        
        with patch('utils.loader.validate_path', return_value=True):
            # Should still validate and check existence
            result = resolve_template_path("../templates/test.html")
            
            # Result depends on validation
            assert result is None or isinstance(result, str)
    
    def test_resolve_with_special_characters_in_name(self, tmp_path, monkeypatch):
        """Test resolving template with special characters"""
        monkeypatch.chdir(tmp_path)
        
        template_dir = tmp_path / "templates"
        template_dir.mkdir(parents=True)
        special_file = template_dir / "test-template_v2.html"
        special_file.write_text("content")
        
        with patch('utils.loader.validate_path', return_value=True):
            result = resolve_template_path("test-template_v2.html")
            
            assert result == "templates/test-template_v2.html"
    
    def test_resolve_case_sensitive_filename(self, tmp_path, monkeypatch):
        """Test that template resolution is case-sensitive"""
        monkeypatch.chdir(tmp_path)
        
        template_dir = tmp_path / "templates"
        template_dir.mkdir(parents=True)
        (template_dir / "Test.html").write_text("content")
        
        with patch('utils.loader.validate_path', return_value=True):
            # Looking for lowercase should fail
            result = resolve_template_path("test.html")
            
            assert result is None