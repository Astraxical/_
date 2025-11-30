"""
Comprehensive unit tests for the Template Engine module.
Tests alter management, template rendering, and CSV persistence.
"""
import pytest
import csv
import os
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys

# Add codebase to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..', 'codebase'))

from modules.template.engine import TemplateEngine


class TestTemplateEngineInitialization:
    """Test template engine initialization and setup."""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_init_loads_alters_from_csv(self, mock_file, mock_path):
        """Test that initialization correctly loads alter status from CSV."""
        mock_path.return_value.exists.return_value = True
        
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        assert engine.alters_status == {'seles': True, 'dexen': False, 'yuki': False}
        assert engine.current_alter == 'seles'
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_creates_csv_if_not_exists(self, mock_file, mock_path):
        """Test that initialization creates default CSV if it doesn't exist."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        with patch('modules.template.engine.TemplateEngine._load_alters_status'), \
             patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        # Verify directory creation was attempted
        mock_path_instance.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\ndexen,1\nyuki,0\n')
    def test_init_sets_current_alter_to_fronting(self, mock_file, mock_path):
        """Test that current_alter is set to the fronting alter."""
        mock_path.return_value.exists.return_value = True
        
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        assert engine.current_alter == 'dexen'
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\ndexen,0\nyuki,0\n')
    def test_init_defaults_to_global_when_no_fronting(self, mock_file, mock_path):
        """Test that current_alter defaults to 'global' when no alter is fronting."""
        mock_path.return_value.exists.return_value = True
        
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        assert engine.current_alter == 'global'


class TestTemplateSetup:
    """Test template path resolution and setup."""
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_with_alter_specific_path(self, mock_jinja, mock_exists):
        """Test that alter-specific template paths are added when they exist."""
        mock_exists.side_effect = lambda path: path in [
            'modules/template/templates/seles',
            'modules/template/templates/global'
        ]
        
        with patch('modules.template.engine.TemplateEngine._load_alters_status'):
            engine = TemplateEngine()
            engine.current_alter = 'seles'
            engine._setup_templates()
        
        # Verify Jinja2Templates was called with correct paths
        call_args = mock_jinja.call_args[1]['directory']
        assert 'modules/template/templates/seles' in call_args
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_skips_nonexistent_paths(self, mock_jinja, mock_exists):
        """Test that nonexistent paths are not added to template search."""
        mock_exists.return_value = False
        
        with patch('modules.template.engine.TemplateEngine._load_alters_status'):
            engine = TemplateEngine()
            engine.current_alter = 'nonexistent'
            engine._setup_templates()
        
        call_args = mock_jinja.call_args[1]['directory']
        assert 'templates' in call_args  # Global fallback always included
        assert 'modules/template/templates/nonexistent' not in call_args


class TestAlterSwitching:
    """Test alter switching functionality."""
    
    @patch('modules.template.engine.TemplateEngine._save_alters_status')
    @patch('modules.template.engine.TemplateEngine._setup_templates')
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    def test_switch_alter_success(self, mock_load, mock_setup, mock_save):
        """Test successful alter switching."""
        engine = TemplateEngine()
        engine.alters_status = {'seles': True, 'dexen': False, 'yuki': False}
        engine.current_alter = 'seles'
        
        result = engine.switch_alter('dexen')
        
        assert result is True
        assert engine.current_alter == 'dexen'
        assert engine.alters_status == {'seles': False, 'dexen': True, 'yuki': False}
        mock_setup.assert_called()
        mock_save.assert_called_once()
    
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    def test_switch_alter_invalid_alter(self, mock_load):
        """Test switching to a nonexistent alter fails gracefully."""
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
            engine.alters_status = {'seles': True, 'dexen': False}
            
            result = engine.switch_alter('invalid')
        
        assert result is False
        assert engine.current_alter != 'invalid'
    
    @patch('modules.template.engine.TemplateEngine._save_alters_status')
    @patch('modules.template.engine.TemplateEngine._setup_templates')
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    def test_switch_alter_resets_all_others(self, mock_load, mock_setup, mock_save):
        """Test that switching an alter sets all others to False."""
        engine = TemplateEngine()
        engine.alters_status = {'seles': True, 'dexen': True, 'yuki': True}
        
        engine.switch_alter('seles')
        
        assert engine.alters_status == {'seles': True, 'dexen': False, 'yuki': False}


class TestTemplateRendering:
    """Test template rendering with alter context."""
    
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    @patch('modules.template.engine.TemplateEngine._setup_templates')
    def test_render_includes_alter_context(self, mock_setup, mock_load):
        """Test that render method includes alter status in context."""
        engine = TemplateEngine()
        engine.current_alter = 'seles'
        engine.alters_status = {'seles': True, 'dexen': False, 'yuki': False}
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        engine.render('index.html', mock_request, custom_var='value')
        
        # Verify TemplateResponse was called with correct context
        call_args = engine.templates.TemplateResponse.call_args
        context = call_args[0][1]
        
        assert context['request'] == mock_request
        assert context['current_alter'] == 'seles'
        assert context['alters_status'] == {'seles': True, 'dexen': False, 'yuki': False}
        assert context['custom_var'] == 'value'
    
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    @patch('modules.template.engine.TemplateEngine._setup_templates')
    def test_render_custom_context_doesnt_override_defaults(self, mock_setup, mock_load):
        """Test that custom context variables don't override required context."""
        engine = TemplateEngine()
        engine.current_alter = 'dexen'
        engine.alters_status = {'dexen': True}
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        # Try to override required context keys
        engine.render('test.html', mock_request, 
                     current_alter='fake', 
                     alters_status={'fake': True})
        
        call_args = engine.templates.TemplateResponse.call_args
        context = call_args[0][1]
        
        # Custom values should be overridden by engine values
        assert context['current_alter'] == 'dexen'
        assert context['alters_status'] == {'dexen': True}


class TestCSVPersistence:
    """Test CSV file saving and loading."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.Path')
    def test_save_alters_status_writes_correct_format(self, mock_path, mock_file):
        """Test that alter status is saved in correct CSV format."""
        with patch('modules.template.engine.TemplateEngine._load_alters_status'), \
             patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
            engine.alters_status = {'seles': True, 'dexen': False, 'yuki': True}
            
            engine._save_alters_status()
        
        # Verify CSV was written with header and data
        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        
        assert 'name,is_fronting' in written_data
        assert 'seles,1' in written_data
        assert 'dexen,0' in written_data
        assert 'yuki,1' in written_data
    
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,true\ndexen,yes\nyuki,1\n')
    @patch('modules.template.engine.Path')
    def test_load_handles_various_boolean_formats(self, mock_path, mock_file):
        """Test that loading handles various boolean string formats."""
        mock_path.return_value.exists.return_value = True
        
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        # All should be interpreted as True
        assert engine.alters_status['seles'] is True
        assert engine.alters_status['dexen'] is True
        assert engine.alters_status['yuki'] is True


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\n')
    @patch('modules.template.engine.Path')
    def test_empty_csv_handled_gracefully(self, mock_path, mock_file):
        """Test that empty CSV (only headers) is handled gracefully."""
        mock_path.return_value.exists.return_value = True
        
        with patch('modules.template.engine.TemplateEngine._setup_templates'):
            engine = TemplateEngine()
        
        assert engine.alters_status == {}
        assert engine.current_alter == 'global'
    
    @patch('modules.template.engine.TemplateEngine._load_alters_status')
    @patch('modules.template.engine.TemplateEngine._setup_templates')
    def test_render_with_no_custom_context(self, mock_setup, mock_load):
        """Test rendering without additional context variables."""
        engine = TemplateEngine()
        engine.current_alter = 'seles'
        engine.alters_status = {'seles': True}
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        engine.render('test.html', mock_request)
        
        # Should still work with just required context
        assert engine.templates.TemplateResponse.called