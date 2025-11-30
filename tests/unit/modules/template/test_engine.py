"""
Unit tests for modules/template/engine.py
Tests for template engine and alter management
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path
import csv
import os

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestTemplateEngineInit:
    """Tests for TemplateEngine initialization"""
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_template_engine_initialization(self, mock_file, mock_exists):
        """Test basic template engine initialization"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine is not None
        assert hasattr(engine, 'alters_status')
        assert hasattr(engine, 'current_alter')
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_template_engine_loads_alters(self, mock_file, mock_exists):
        """Test that template engine loads alters from CSV"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert 'seles' in engine.alters_status
        assert 'dexen' in engine.alters_status
        assert 'yuki' in engine.alters_status
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_template_engine_sets_current_alter(self, mock_file, mock_exists):
        """Test that current alter is set based on fronting status"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.current_alter == 'seles'
        assert engine.alters_status['seles'] is True
    
    @patch('modules.template.engine.Path.exists')
    @patch('modules.template.engine.Path.mkdir')
    @patch('builtins.open', new_callable=mock_open)
    def test_template_engine_creates_default_csv(self, mock_file, mock_mkdir, mock_exists):
        """Test that template engine creates default CSV if not exists"""
        mock_exists.return_value = False
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        # Should create directories and write default CSV
        mock_mkdir.assert_called()
        assert mock_file.call_count >= 2  # Write then read
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\ndexen,0\nyuki,0\n')
    def test_template_engine_no_fronting_defaults_to_global(self, mock_file, mock_exists):
        """Test that engine defaults to global when no alter is fronting"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.current_alter == 'global'
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,true\ndexen,false\n')
    def test_template_engine_parses_boolean_strings(self, mock_file, mock_exists):
        """Test that engine correctly parses various boolean string formats"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.alters_status['seles'] is True
        assert engine.alters_status['dexen'] is False
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,yes\ndexen,no\n')
    def test_template_engine_parses_yes_no(self, mock_file, mock_exists):
        """Test that engine correctly parses yes/no values"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.alters_status['seles'] is True
        assert engine.alters_status['dexen'] is False
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,on\ndexen,off\n')
    def test_template_engine_parses_on_off(self, mock_file, mock_exists):
        """Test that engine correctly parses on/off values"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.alters_status['seles'] is True
        assert engine.alters_status['dexen'] is False


class TestTemplateEngineSetup:
    """Tests for template setup methods"""
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\n')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_with_alter(self, mock_jinja, mock_file, mock_path_exists, mock_os_exists):
        """Test template setup with a specific alter"""
        mock_path_exists.return_value = True
        mock_os_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        # Should set up Jinja2Templates with multiple paths
        mock_jinja.assert_called()
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\n')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_global_only(self, mock_jinja, mock_file, mock_path_exists, mock_os_exists):
        """Test template setup with global alter only"""
        mock_path_exists.return_value = True
        mock_os_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.current_alter == 'global'
        mock_jinja.assert_called()


class TestTemplateEngineRender:
    """Tests for template rendering"""
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\n')
    def test_render_adds_alter_context(self, mock_file, mock_exists):
        """Test that render adds alter information to context"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        mock_request = MagicMock()
        mock_templates = MagicMock()
        engine.templates = mock_templates
        
        engine.render("test.html", mock_request, extra_key="extra_value")
        
        # Verify TemplateResponse was called with context including alter info
        call_args = mock_templates.TemplateResponse.call_args
        assert call_args is not None
        context = call_args[0][1]
        assert 'current_alter' in context
        assert 'alters_status' in context
        assert 'request' in context
        assert 'extra_key' in context
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\n')
    def test_render_preserves_custom_context(self, mock_file, mock_exists):
        """Test that render preserves custom context variables"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        mock_request = MagicMock()
        mock_templates = MagicMock()
        engine.templates = mock_templates
        
        custom_context = {"user": "test_user", "page": "home"}
        engine.render("test.html", mock_request, **custom_context)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        assert context['user'] == 'test_user'
        assert context['page'] == 'home'
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\n')
    def test_render_includes_request(self, mock_file, mock_exists):
        """Test that render includes request in context"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        mock_request = MagicMock()
        mock_templates = MagicMock()
        engine.templates = mock_templates
        
        engine.render("test.html", mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        assert context['request'] == mock_request


class TestTemplateEngineSwitchAlter:
    """Tests for alter switching functionality"""
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_to_valid_alter(self, mock_file, mock_exists):
        """Test switching to a valid alter"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        result = engine.switch_alter('dexen')
        
        assert result is True
        assert engine.current_alter == 'dexen'
        assert engine.alters_status['dexen'] is True
        assert engine.alters_status['seles'] is False
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\n')
    def test_switch_alter_to_invalid_alter(self, mock_file, mock_exists):
        """Test switching to an invalid alter returns False"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        result = engine.switch_alter('nonexistent')
        
        assert result is False
        assert engine.current_alter == 'seles'  # Should remain unchanged
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_switch_alter_resets_all_alters(self, mock_file, mock_exists):
        """Test that switching resets all other alters to not fronting"""
        mock_exists.return_value = True
        
        # Setup mock to return different data on subsequent reads
        mock_file.return_value.read.side_effect = [
            'name,is_fronting\nseles,1\ndexen,0\nyuki,0\n',
            'name,is_fronting\nseles,1\ndexen,0\nyuki,0\n'
        ]
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        engine.switch_alter('yuki')
        
        assert engine.alters_status['yuki'] is True
        assert engine.alters_status['seles'] is False
        assert engine.alters_status['dexen'] is False
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\n')
    @patch('modules.template.engine.Jinja2Templates')
    def test_switch_alter_updates_templates(self, mock_jinja, mock_file, mock_exists):
        """Test that switching alter updates template paths"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        initial_call_count = mock_jinja.call_count
        engine.switch_alter('dexen')
        
        # Should call Jinja2Templates again to update paths
        assert mock_jinja.call_count > initial_call_count
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\n')
    def test_switch_alter_saves_to_csv(self, mock_file, mock_exists):
        """Test that switching alter saves state to CSV"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        engine.switch_alter('dexen')
        
        # Verify file was opened for writing
        write_calls = [call for call in mock_file.call_args_list if 'w' in str(call)]
        assert len(write_calls) > 0
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\n')
    def test_switch_alter_same_alter(self, mock_file, mock_exists):
        """Test switching to the same alter that's already fronting"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        result = engine.switch_alter('seles')
        
        assert result is True
        assert engine.current_alter == 'seles'
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_multiple_times(self, mock_file, mock_exists):
        """Test switching alters multiple times"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        engine.switch_alter('dexen')
        assert engine.current_alter == 'dexen'
        
        engine.switch_alter('yuki')
        assert engine.current_alter == 'yuki'
        
        engine.switch_alter('seles')
        assert engine.current_alter == 'seles'


class TestTemplateEngineSaveAltersStatus:
    """Tests for saving alter status"""
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_alters_status_writes_csv(self, mock_file, mock_exists):
        """Test that _save_alters_status writes to CSV file"""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = 'name,is_fronting\nseles,1\n'
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        engine._save_alters_status()
        
        # Verify file was opened for writing
        write_calls = [call for call in mock_file.call_args_list if 'w' in str(call)]
        assert len(write_calls) > 0
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\n')
    def test_save_alters_status_format(self, mock_file, mock_exists):
        """Test that saved status has correct format"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        engine._save_alters_status()
        
        # Get the write calls
        write_calls = mock_file.return_value.write.call_args_list
        assert len(write_calls) > 0


class TestTemplateEngineEdgeCases:
    """Tests for edge cases and error handling"""
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\n')
    def test_empty_csv_file(self, mock_file, mock_exists):
        """Test handling of empty CSV file"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        assert engine.alters_status == {}
        assert engine.current_alter == 'global'
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\nseles,0\n')
    def test_duplicate_alter_names(self, mock_file, mock_exists):
        """Test handling of duplicate alter names in CSV"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        # Last entry should win
        assert 'seles' in engine.alters_status
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,invalid_value\n')
    def test_invalid_boolean_values(self, mock_file, mock_exists):
        """Test handling of invalid boolean values"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        # Should default to False for invalid values
        assert engine.alters_status.get('seles') is False
    
    @patch('modules.template.engine.Path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,1\n')
    def test_multiple_fronting_alters(self, mock_file, mock_exists):
        """Test handling of multiple alters marked as fronting"""
        mock_exists.return_value = True
        
        from modules.template.engine import TemplateEngine
        engine = TemplateEngine()
        
        # Should handle gracefully - last one wins
        assert engine.current_alter in ['seles', 'dexen']