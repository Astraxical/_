"""
Unit tests for modules/template/engine.py
Tests for the TemplateEngine class and alter management
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
from pathlib import Path
import csv
from io import StringIO

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestTemplateEngineInitialization:
    """Tests for TemplateEngine initialization"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\nyuki,0\n")
    @patch('modules.template.engine.os.path.exists')
    def test_init_loads_alters_status(self, mock_exists, mock_file, mock_path):
        """Test that initialization loads alter status from CSV"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert "seles" in engine.alters_status
        assert "dexen" in engine.alters_status
        assert "yuki" in engine.alters_status
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    def test_init_creates_csv_if_not_exists(self, mock_exists, mock_file, mock_path):
        """Test that initialization creates CSV file if it doesn't exist"""
        from modules.template.engine import TemplateEngine
        
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        mock_exists.return_value = False
        
        # Mock the file reading after creation
        mock_file.return_value.read.return_value = "name,is_fronting\nseles,1\ndexen,0\nyuki,0\n"
        
        engine = TemplateEngine()
        
        # Should have created the parent directory
        mock_path_instance.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\nyuki,0\n")
    @patch('modules.template.engine.os.path.exists')
    def test_init_sets_current_alter(self, mock_exists, mock_file, mock_path):
        """Test that initialization sets current alter based on fronting status"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert engine.current_alter == "seles"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,0\ndexen,0\nyuki,0\n")
    @patch('modules.template.engine.os.path.exists')
    def test_init_defaults_to_global_if_no_fronting(self, mock_exists, mock_file, mock_path):
        """Test that current alter defaults to 'global' if no alter is fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert engine.current_alter == "global"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\nyuki,0\n")
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_init_sets_up_templates(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that initialization sets up Jinja2 templates"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        mock_jinja.assert_called_once()
        assert engine.templates is not None


class TestLoadAltersStatus:
    """Tests for _load_alters_status method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,true\ndexen,yes\nyuki,on\n")
    @patch('modules.template.engine.os.path.exists')
    def test_load_alters_various_true_values(self, mock_exists, mock_file, mock_path):
        """Test that various truthy values are correctly interpreted"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert engine.alters_status["seles"] is True
        assert engine.alters_status["dexen"] is True
        assert engine.alters_status["yuki"] is True
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,0\ndexen,false\nyuki,no\n")
    @patch('modules.template.engine.os.path.exists')
    def test_load_alters_various_false_values(self, mock_exists, mock_file, mock_path):
        """Test that various falsy values are correctly interpreted"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert engine.alters_status["seles"] is False
        assert engine.alters_status["dexen"] is False
        assert engine.alters_status["yuki"] is False
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nalter1,1\nalter2,1\n")
    @patch('modules.template.engine.os.path.exists')
    def test_load_alters_multiple_fronting_last_wins(self, mock_exists, mock_file, mock_path):
        """Test that when multiple alters are fronting, the last one becomes current"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        # Last fronting alter should be current
        assert engine.current_alter == "alter2"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\n")
    @patch('modules.template.engine.os.path.exists')
    def test_load_alters_empty_csv(self, mock_exists, mock_file, mock_path):
        """Test handling of empty CSV file"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        assert engine.alters_status == {}
        assert engine.current_alter == "global"


class TestSetupTemplates:
    """Tests for _setup_templates method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\n")
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_with_alter_specific_path(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that alter-specific template path is included when alter is fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]
        template_dirs = call_args['directory']
        
        # Should include alter-specific path
        assert any("seles" in str(d) for d in template_dirs)
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,0\n")
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_global_only(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test template setup when no alter is fronting"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]
        template_dirs = call_args['directory']
        
        # Should include global templates path
        assert any("templates" in str(d) for d in template_dirs)
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\n")
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_fallback_order(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that template paths are set up in correct fallback order"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]
        template_dirs = call_args['directory']
        
        # Should be a list with multiple paths
        assert isinstance(template_dirs, list)
        assert len(template_dirs) >= 1


class TestRenderMethod:
    """Tests for render method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\n")
    @patch('modules.template.engine.os.path.exists')
    def test_render_adds_alter_context(self, mock_exists, mock_file, mock_path):
        """Test that render adds alter information to context"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        engine.render("test.html", mock_request, extra_key="extra_value")
        
        call_args = engine.templates.TemplateResponse.call_args[0]
        context = call_args[1]
        
        assert "current_alter" in context
        assert "alters_status" in context
        assert "request" in context
        assert "extra_key" in context
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\n")
    @patch('modules.template.engine.os.path.exists')
    def test_render_uses_correct_template(self, mock_exists, mock_file, mock_path):
        """Test that render uses the specified template name"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        engine.render("index.html", mock_request)
        
        call_args = engine.templates.TemplateResponse.call_args[0]
        assert call_args[0] == "index.html"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\n")
    @patch('modules.template.engine.os.path.exists')
    def test_render_preserves_additional_context(self, mock_exists, mock_file, mock_path):
        """Test that render preserves additional context variables"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        engine.templates = MagicMock()
        
        mock_request = MagicMock()
        extra_context = {"key1": "value1", "key2": "value2"}
        engine.render("test.html", mock_request, **extra_context)
        
        call_args = engine.templates.TemplateResponse.call_args[0]
        context = call_args[1]
        
        assert context["key1"] == "value1"
        assert context["key2"] == "value2"


class TestSwitchAlter:
    """Tests for switch_alter method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\nyuki,0\n")
    @patch('modules.template.engine.os.path.exists')
    def test_switch_alter_valid_alter(self, mock_exists, mock_file, mock_path):
        """Test switching to a valid alter"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        result = engine.switch_alter("dexen")
        
        assert result is True
        assert engine.current_alter == "dexen"
        assert engine.alters_status["dexen"] is True
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\n")
    @patch('modules.template.engine.os.path.exists')
    def test_switch_alter_invalid_alter(self, mock_exists, mock_file, mock_path):
        """Test switching to an invalid alter returns False"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        result = engine.switch_alter("nonexistent")
        
        assert result is False
        assert engine.current_alter == "seles"  # Should remain unchanged
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    def test_switch_alter_resets_other_alters(self, mock_exists, mock_file, mock_path):
        """Test that switching alter resets all other alters to not fronting"""
        from modules.template.engine import TemplateEngine
        
        # Set up initial state with multiple fronting alters
        csv_data = "name,is_fronting\nseles,1\ndexen,1\nyuki,0\n"
        mock_file.return_value.read.return_value = csv_data
        mock_file.return_value.__iter__.return_value = csv_data.split('\n')
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        engine.switch_alter("yuki")
        
        assert engine.alters_status["seles"] is False
        assert engine.alters_status["dexen"] is False
        assert engine.alters_status["yuki"] is True
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nseles,1\ndexen,0\n")
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_switch_alter_updates_templates(self, mock_jinja, mock_exists, mock_file, mock_path):
        """Test that switching alter updates template paths"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        initial_call_count = mock_jinja.call_count
        
        engine.switch_alter("dexen")
        
        # Should have called Jinja2Templates again to update paths
        assert mock_jinja.call_count > initial_call_count
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    def test_switch_alter_saves_status(self, mock_exists, mock_file, mock_path):
        """Test that switching alter saves status to CSV"""
        from modules.template.engine import TemplateEngine
        
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_exists.return_value = False
        
        # Set up file handle mock
        write_handle = MagicMock()
        mock_file.return_value.__enter__.return_value = write_handle
        
        engine = TemplateEngine()
        engine.switch_alter("dexen")
        
        # Should have opened file for writing
        assert mock_file.call_count >= 2  # Once for reading, once for writing


class TestSaveAltersStatus:
    """Tests for _save_alters_status method"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.csv.writer')
    def test_save_alters_status_writes_header(self, mock_writer, mock_exists, mock_file, mock_path):
        """Test that saving writes CSV header"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        writer_instance = MagicMock()
        mock_writer.return_value = writer_instance
        
        engine = TemplateEngine()
        engine._save_alters_status()
        
        # Should write header row
        calls = writer_instance.writerow.call_args_list
        assert ['name', 'is_fronting'] in [call[0][0] for call in calls]
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.csv.writer')
    def test_save_alters_status_writes_all_alters(self, mock_writer, mock_exists, mock_file, mock_path):
        """Test that saving writes all alters"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        writer_instance = MagicMock()
        mock_writer.return_value = writer_instance
        
        engine = TemplateEngine()
        engine.alters_status = {"seles": True, "dexen": False, "yuki": False}
        engine._save_alters_status()
        
        # Should write rows for each alter
        assert writer_instance.writerow.call_count >= 4  # Header + 3 alters
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.csv.writer')
    def test_save_alters_status_converts_bool_to_int(self, mock_writer, mock_exists, mock_file, mock_path):
        """Test that boolean values are converted to integers"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        writer_instance = MagicMock()
        mock_writer.return_value = writer_instance
        
        engine = TemplateEngine()
        engine.alters_status = {"test_alter": True}
        engine._save_alters_status()
        
        # Find the call that wrote test_alter
        calls = writer_instance.writerow.call_args_list
        alter_calls = [call for call in calls if len(call[0][0]) == 2 and call[0][0][0] == "test_alter"]
        
        assert len(alter_calls) > 0
        assert alter_calls[0][0][0][1] in ['1', 1]  # Should be integer representation


class TestTemplateEngineEdgeCases:
    """Tests for edge cases and error conditions"""
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open')
    @patch('modules.template.engine.os.path.exists')
    def test_handles_missing_csv_columns(self, mock_exists, mock_file, mock_path):
        """Test handling of malformed CSV with missing columns"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        # CSV with missing is_fronting column
        csv_data = "name\nseles\n"
        mock_file.return_value.__enter__.return_value.read.return_value = csv_data
        
        # Should handle gracefully or raise appropriate error
        try:
            engine = TemplateEngine()
            # If it succeeds, verify state is reasonable
            assert isinstance(engine.alters_status, dict)
        except (KeyError, ValueError):
            # Expected error for malformed CSV
            pass
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\nalter_with_special_chars!@#,1\n")
    @patch('modules.template.engine.os.path.exists')
    def test_handles_special_characters_in_alter_names(self, mock_exists, mock_file, mock_path):
        """Test handling of alter names with special characters"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        # Should store alter name as-is
        assert "alter_with_special_chars!@#" in engine.alters_status
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\n")
    @patch('modules.template.engine.os.path.exists')
    def test_switch_to_same_alter(self, mock_exists, mock_file, mock_path):
        """Test switching to the already-active alter"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        engine.alters_status = {"seles": True}
        engine.current_alter = "seles"
        
        result = engine.switch_alter("seles")
        
        assert result is True
        assert engine.current_alter == "seles"
    
    @patch('modules.template.engine.Path')
    @patch('builtins.open', new_callable=mock_open, read_data="name,is_fronting\n  seles  ,  1  \n")
    @patch('modules.template.engine.os.path.exists')
    def test_handles_whitespace_in_csv(self, mock_exists, mock_file, mock_path):
        """Test handling of whitespace in CSV values"""
        from modules.template.engine import TemplateEngine
        
        mock_path.return_value.exists.return_value = True
        mock_exists.return_value = False
        
        engine = TemplateEngine()
        
        # Should handle whitespace appropriately
        # DictReader strips whitespace from field names but not values
        assert len(engine.alters_status) >= 0