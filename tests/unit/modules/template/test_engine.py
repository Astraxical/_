"""
Unit tests for modules/template/engine.py
Tests for the TemplateEngine class and alter-based template rendering
"""
import pytest
import csv
import os
from unittest.mock import patch, MagicMock, mock_open, call
from pathlib import Path
import sys

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestTemplateEngineInit:
    """Tests for TemplateEngine initialization"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    @patch('os.path.exists')
    def test_init_loads_existing_csv(self, mock_exists, mock_file, mock_path):
        """Test that initialization loads existing CSV file"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        assert engine.alters_status == {"seles": True, "dexen": False, "yuki": False}
        assert engine.current_alter == "seles"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_init_creates_default_csv_if_not_exists(self, mock_exists, mock_file, mock_path):
        """Test that initialization creates default CSV if it doesn't exist"""
        from modules.template.engine import TemplateEngine
        
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path_instance.parent.mkdir = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_exists.return_value = True
        
        # Mock the CSV reading after creation
        with patch('csv.DictReader') as mock_reader:
            mock_reader.return_value = iter([
                {'name': 'seles', 'is_fronting': '1'},
                {'name': 'dexen', 'is_fronting': '0'},
                {'name': 'yuki', 'is_fronting': '0'}
            ])
            engine = TemplateEngine()
        
        mock_path_instance.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\ndexen,true\nseles,false\nyuki,yes\n')
    @patch('os.path.exists')
    def test_init_handles_various_truthy_values(self, mock_exists, mock_file, mock_path):
        """Test that initialization handles various truthy string values"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        assert engine.alters_status["dexen"] is True
        assert engine.alters_status["seles"] is False
        assert engine.alters_status["yuki"] is True
        assert engine.current_alter == "dexen"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\ndexen,0\nyuki,0\n')
    @patch('os.path.exists')
    def test_init_defaults_to_global_when_no_alter_fronting(self, mock_exists, mock_file, mock_path):
        """Test that current_alter remains 'global' when no alter is fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        assert engine.current_alter == "global"
        assert all(not status for status in engine.alters_status.values())


class TestTemplateEngineSetupTemplates:
    """Tests for _setup_templates method"""
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_setup_templates_with_active_alter(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test template setup with an active alter"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.side_effect = [True, True, True]  # alter path, global path, templates path
        
        engine = TemplateEngine()
        
        # Should have called Jinja2Templates with alter-specific, global, and standard paths
        assert mock_jinja.called
        call_args = mock_jinja.call_args[1]['directory']
        assert 'modules/template/templates/seles' in call_args
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,0\ndexen,0\nyuki,0\n')
    def test_setup_templates_with_global_alter(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test template setup when current alter is global"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.side_effect = [True, True]  # global path, templates path
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]['directory']
        assert 'modules/template/templates/seles' not in call_args
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\ndexen,1\nseles,0\nyuki,0\n')
    def test_setup_templates_skips_nonexistent_paths(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test template setup skips paths that don't exist"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.side_effect = [False, False, True]  # alter path doesn't exist, global doesn't exist
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]['directory']
        assert len([p for p in call_args if 'dexen' in p]) == 0
        assert 'templates' in call_args


class TestTemplateEngineRender:
    """Tests for render method"""
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_render_includes_alter_context(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test that render includes alter information in context"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        mock_templates_instance = MagicMock()
        mock_jinja.return_value = mock_templates_instance
        
        engine = TemplateEngine()
        mock_request = MagicMock()
        
        engine.render("test.html", mock_request, extra_key="extra_value")
        
        # Verify TemplateResponse was called with correct context
        mock_templates_instance.TemplateResponse.assert_called_once()
        call_args = mock_templates_instance.TemplateResponse.call_args
        
        assert call_args[0][0] == "test.html"
        context = call_args[0][1]
        assert context["request"] == mock_request
        assert context["current_alter"] == "seles"
        assert context["alters_status"] == {"seles": True, "dexen": False, "yuki": False}
        assert context["extra_key"] == "extra_value"
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_render_merges_additional_context(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test that render merges additional context correctly"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        mock_templates_instance = MagicMock()
        mock_jinja.return_value = mock_templates_instance
        
        engine = TemplateEngine()
        mock_request = MagicMock()
        
        engine.render("test.html", mock_request, user="john", page=1)
        
        context = mock_templates_instance.TemplateResponse.call_args[0][1]
        assert context["user"] == "john"
        assert context["page"] == 1


class TestTemplateEngineSwitchAlter:
    """Tests for switch_alter method"""
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_to_existing_alter(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test switching to an existing alter"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        # Mock the _save_alters_status method
        with patch.object(engine, '_save_alters_status') as mock_save:
            result = engine.switch_alter("dexen")
        
        assert result is True
        assert engine.current_alter == "dexen"
        assert engine.alters_status["dexen"] is True
        assert engine.alters_status["seles"] is False
        assert engine.alters_status["yuki"] is False
        mock_save.assert_called_once()
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_to_nonexistent_alter(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test switching to a non-existent alter returns False"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        original_alter = engine.current_alter
        
        result = engine.switch_alter("nonexistent")
        
        assert result is False
        assert engine.current_alter == original_alter
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_resets_all_other_alters(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test that switching resets all other alters to not fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        with patch.object(engine, '_save_alters_status'):
            engine.switch_alter("yuki")
        
        assert engine.alters_status["yuki"] is True
        assert engine.alters_status["seles"] is False
        assert engine.alters_status["dexen"] is False
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_alter_calls_setup_templates(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test that switching an alter triggers template setup"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        with patch.object(engine, '_setup_templates') as mock_setup, \
             patch.object(engine, '_save_alters_status'):
            engine.switch_alter("dexen")
            mock_setup.assert_called_once()


class TestTemplateEngineSaveAltersStatus:
    """Tests for _save_alters_status method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    @patch('os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_save_alters_status_writes_csv(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that _save_alters_status writes correct CSV format"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        engine.alters_status = {"seles": False, "dexen": True, "yuki": False}
        
        # Create a new mock for writing
        write_mock = mock_open()
        with patch('builtins.open', write_mock):
            engine._save_alters_status()
        
        # Verify write was called
        write_mock.assert_called_once()
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    @patch('os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_save_alters_status_preserves_all_alters(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that _save_alters_status preserves all alters"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        original_count = len(engine.alters_status)
        
        with patch('csv.writer') as mock_writer:
            mock_writer_instance = MagicMock()
            mock_writer.return_value = mock_writer_instance
            engine._save_alters_status()
            
            # Should write header + all alters
            assert mock_writer_instance.writerow.call_count == original_count + 1


class TestTemplateEngineEdgeCases:
    """Tests for edge cases and error handling"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\n')
    @patch('os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_handles_empty_csv(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test handling of empty CSV file (header only)"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        assert engine.alters_status == {}
        assert engine.current_alter == "global"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,ON\ndexen,off\nyuki,1\n')
    @patch('os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_handles_case_insensitive_boolean_values(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test case-insensitive boolean parsing"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        assert engine.alters_status["seles"] is True  # 'ON' -> True
        assert engine.alters_status["dexen"] is False  # 'off' -> False
        assert engine.alters_status["yuki"] is True  # '1' -> True
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,0\nyuki,0\n')
    def test_switch_to_same_alter(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test switching to the same alter that's already active"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        with patch.object(engine, '_save_alters_status') as mock_save:
            result = engine.switch_alter("seles")
        
        assert result is True
        assert engine.current_alter == "seles"
        mock_save.assert_called_once()
    
    @patch('modules.template.engine.Jinja2Templates')
    @patch('os.path.exists')
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='name,is_fronting\nseles,1\ndexen,1\nyuki,0\n')
    def test_multiple_alters_fronting_last_one_wins(self, mock_file, mock_path, mock_exists, mock_jinja):
        """Test behavior when multiple alters are marked as fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        # The last one read should be the current alter
        assert engine.current_alter in ["seles", "dexen"]
        # Both should be marked as fronting initially
        assert engine.alters_status["seles"] is True
        assert engine.alters_status["dexen"] is True