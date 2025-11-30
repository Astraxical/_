"""
Unit tests for the Template Engine module
"""
import pytest
import csv
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
from fastapi import Request
from fastapi.templating import Jinja2Templates

# Add codebase to path
import sys
sys.path.insert(0, 'codebase')

from modules.template.engine import TemplateEngine


class TestTemplateEngineInit:
    """Tests for TemplateEngine initialization"""
    
    def test_init_creates_default_csv_if_not_exists(self, tmp_path, monkeypatch):
        """Test that __init__ creates default alters.csv if it doesn't exist"""
        # Change to tmp directory
        monkeypatch.chdir(tmp_path)
        
        engine = TemplateEngine()
        
        # Check that CSV was created
        csv_path = Path("modules/template/data/alters.csv")
        assert csv_path.exists()
        
        # Verify content
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3
            assert rows[0]['name'] == 'seles'
            assert rows[0]['is_fronting'] == '1'
    
    def test_init_loads_existing_csv(self, tmp_path, monkeypatch):
        """Test that __init__ correctly loads existing alters.csv"""
        monkeypatch.chdir(tmp_path)
        
        # Create CSV with custom data
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['custom_alter', '1'])
            writer.writerow(['another_alter', '0'])
        
        engine = TemplateEngine()
        
        assert engine.current_alter == 'custom_alter'
        assert engine.alters_status == {'custom_alter': True, 'another_alter': False}
    
    def test_init_handles_various_truthy_values(self, tmp_path, monkeypatch):
        """Test that _load_alters_status handles different truthy string values"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', 'true'])
            writer.writerow(['alter2', 'TRUE'])
            writer.writerow(['alter3', 'yes'])
            writer.writerow(['alter4', 'YES'])
            writer.writerow(['alter5', 'on'])
            writer.writerow(['alter6', 'ON'])
            writer.writerow(['alter7', '0'])
            writer.writerow(['alter8', 'false'])
        
        engine = TemplateEngine()
        
        # All should be evaluated correctly
        assert engine.alters_status['alter1'] is True
        assert engine.alters_status['alter2'] is True
        assert engine.alters_status['alter3'] is True
        assert engine.alters_status['alter4'] is True
        assert engine.alters_status['alter5'] is True
        assert engine.alters_status['alter6'] is True
        assert engine.alters_status['alter7'] is False
        assert engine.alters_status['alter8'] is False
    
    def test_init_sets_current_alter_to_first_fronting(self, tmp_path, monkeypatch):
        """Test that current_alter is set to the first fronting alter"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', '0'])
            writer.writerow(['alter2', '1'])
            writer.writerow(['alter3', '1'])  # Second fronting should be ignored
        
        engine = TemplateEngine()
        
        assert engine.current_alter == 'alter2'
    
    def test_init_defaults_to_global_if_no_fronting_alter(self, tmp_path, monkeypatch):
        """Test that current_alter defaults to 'global' if no alter is fronting"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', '0'])
            writer.writerow(['alter2', '0'])
        
        engine = TemplateEngine()
        
        assert engine.current_alter == 'global'


class TestTemplateEngineSetupTemplates:
    """Tests for _setup_templates method"""
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_with_alter_specific_path(self, mock_jinja, mock_exists, tmp_path, monkeypatch):
        """Test that _setup_templates includes alter-specific path when it exists"""
        monkeypatch.chdir(tmp_path)
        
        # Create CSV
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
        
        # Mock path existence
        def mock_exists_fn(path):
            return path in ['modules/template/templates/seles', 'modules/template/templates/global']
        mock_exists.side_effect = mock_exists_fn
        
        engine = TemplateEngine()
        
        # Verify Jinja2Templates was called with correct paths
        call_args = mock_jinja.call_args[1]['directory']
        assert 'modules/template/templates/seles' in call_args
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_skips_nonexistent_alter_path(self, mock_jinja, mock_exists, tmp_path, monkeypatch):
        """Test that _setup_templates skips alter-specific path if it doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
        
        # Mock path existence - alter path doesn't exist
        def mock_exists_fn(path):
            return path == 'modules/template/templates/global'
        mock_exists.side_effect = mock_exists_fn
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]['directory']
        assert 'modules/template/templates/seles' not in call_args
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_setup_templates_for_global_alter(self, mock_jinja, mock_exists, tmp_path, monkeypatch):
        """Test that _setup_templates doesn't include alter path for 'global' alter"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', '0'])
        
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        
        call_args = mock_jinja.call_args[1]['directory']
        # Should not have alter-specific path since current_alter is 'global'
        assert 'modules/template/templates/global' in call_args
        assert 'templates' in call_args


class TestTemplateEngineRender:
    """Tests for render method"""
    
    def test_render_adds_alter_context(self, tmp_path, monkeypatch):
        """Test that render method adds alter information to context"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
            writer.writerow(['dexen', '0'])
        
        engine = TemplateEngine()
        
        # Mock the templates object
        mock_request = Mock(spec=Request)
        engine.templates = Mock()
        engine.templates.TemplateResponse = Mock(return_value="response")
        
        result = engine.render("test.html", mock_request, custom_key="custom_value")
        
        # Verify TemplateResponse was called with correct context
        call_args = engine.templates.TemplateResponse.call_args[0]
        context = call_args[1]
        
        assert context['request'] == mock_request
        assert context['current_alter'] == 'seles'
        assert context['alters_status'] == {'seles': True, 'dexen': False}
        assert context['custom_key'] == "custom_value"
    
    def test_render_preserves_additional_context(self, tmp_path, monkeypatch):
        """Test that render preserves additional context variables"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['test', '1'])
        
        engine = TemplateEngine()
        mock_request = Mock(spec=Request)
        engine.templates = Mock()
        engine.templates.TemplateResponse = Mock(return_value="response")
        
        engine.render("test.html", mock_request, key1="value1", key2="value2", key3=123)
        
        context = engine.templates.TemplateResponse.call_args[0][1]
        assert context['key1'] == "value1"
        assert context['key2'] == "value2"
        assert context['key3'] == 123


class TestTemplateEngineSwitchAlter:
    """Tests for switch_alter method"""
    
    def test_switch_alter_success(self, tmp_path, monkeypatch):
        """Test successful alter switching"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
            writer.writerow(['dexen', '0'])
            writer.writerow(['yuki', '0'])
        
        engine = TemplateEngine()
        
        assert engine.current_alter == 'seles'
        
        result = engine.switch_alter('dexen')
        
        assert result is True
        assert engine.current_alter == 'dexen'
        assert engine.alters_status['seles'] is False
        assert engine.alters_status['dexen'] is True
        assert engine.alters_status['yuki'] is False
    
    def test_switch_alter_resets_all_alters(self, tmp_path, monkeypatch):
        """Test that switch_alter resets all other alters to not fronting"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', '1'])
            writer.writerow(['alter2', '1'])  # Start with multiple fronting
            writer.writerow(['alter3', '0'])
        
        engine = TemplateEngine()
        engine.switch_alter('alter3')
        
        assert engine.alters_status['alter1'] is False
        assert engine.alters_status['alter2'] is False
        assert engine.alters_status['alter3'] is True
    
    def test_switch_alter_invalid_name(self, tmp_path, monkeypatch):
        """Test switching to non-existent alter returns False"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
        
        engine = TemplateEngine()
        original_alter = engine.current_alter
        
        result = engine.switch_alter('nonexistent')
        
        assert result is False
        assert engine.current_alter == original_alter
    
    def test_switch_alter_saves_to_csv(self, tmp_path, monkeypatch):
        """Test that switch_alter persists changes to CSV"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
            writer.writerow(['dexen', '0'])
        
        engine = TemplateEngine()
        engine.switch_alter('dexen')
        
        # Verify CSV was updated
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = {row['name']: row['is_fronting'] for row in reader}
            assert rows['seles'] == '0'
            assert rows['dexen'] == '1'
    
    @patch('modules.template.engine.os.path.exists')
    @patch('modules.template.engine.Jinja2Templates')
    def test_switch_alter_calls_setup_templates(self, mock_jinja, mock_exists, tmp_path, monkeypatch):
        """Test that switch_alter calls _setup_templates to update template paths"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
            writer.writerow(['dexen', '0'])
        
        mock_exists.return_value = True
        
        engine = TemplateEngine()
        initial_call_count = mock_jinja.call_count
        
        engine.switch_alter('dexen')
        
        # _setup_templates should have been called again
        assert mock_jinja.call_count > initial_call_count


class TestTemplateEngineSaveAltersStatus:
    """Tests for _save_alters_status method"""
    
    def test_save_alters_status_writes_correct_format(self, tmp_path, monkeypatch):
        """Test that _save_alters_status writes CSV in correct format"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['alter1', '1'])
        
        engine = TemplateEngine()
        engine.alters_status = {'alter1': False, 'alter2': True, 'alter3': False}
        engine._save_alters_status()
        
        # Verify CSV structure
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 3
            assert all('name' in row and 'is_fronting' in row for row in rows)
    
    def test_save_alters_status_converts_bool_to_int_string(self, tmp_path, monkeypatch):
        """Test that boolean values are converted to '0' or '1' strings"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['test', '0'])
        
        engine = TemplateEngine()
        engine.alters_status = {'true_alter': True, 'false_alter': False}
        engine._save_alters_status()
        
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = {row['name']: row['is_fronting'] for row in reader}
            assert rows['true_alter'] == '1'
            assert rows['false_alter'] == '0'


class TestTemplateEngineEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_empty_csv_file(self, tmp_path, monkeypatch):
        """Test handling of empty CSV file"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            pass  # Create empty file
        
        # Should handle gracefully or create default
        engine = TemplateEngine()
        assert isinstance(engine.alters_status, dict)
    
    def test_csv_with_only_header(self, tmp_path, monkeypatch):
        """Test CSV with only header row"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
        
        engine = TemplateEngine()
        assert engine.alters_status == {}
        assert engine.current_alter == 'global'
    
    def test_switch_to_same_alter(self, tmp_path, monkeypatch):
        """Test switching to currently active alter"""
        monkeypatch.chdir(tmp_path)
        
        csv_path = Path("modules/template/data/alters.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'is_fronting'])
            writer.writerow(['seles', '1'])
        
        engine = TemplateEngine()
        result = engine.switch_alter('seles')
        
        assert result is True
        assert engine.current_alter == 'seles'
        assert engine.alters_status['seles'] is True