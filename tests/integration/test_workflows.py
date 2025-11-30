"""
Integration tests for GitHub workflow files
"""
import pytest
import yaml
from pathlib import Path


class TestWorkflowFiles:
    """Test GitHub workflow configuration files"""
    
    def test_lint_workflow_exists(self):
        """Test that lint.yml workflow file exists"""
        workflow_path = Path(".github/workflows/lint.yml")
        assert workflow_path.exists()
    
    def test_test_workflow_exists(self):
        """Test that test.yml workflow file exists"""
        workflow_path = Path(".github/workflows/test.yml")
        assert workflow_path.exists()
    
    def test_lint_workflow_valid_yaml(self):
        """Test that lint.yml is valid YAML"""
        workflow_path = Path(".github/workflows/lint.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        assert content is not None
        assert isinstance(content, dict)
    
    def test_test_workflow_valid_yaml(self):
        """Test that test.yml is valid YAML"""
        workflow_path = Path(".github/workflows/test.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        assert content is not None
        assert isinstance(content, dict)
    
    def test_lint_workflow_structure(self):
        """Test that lint.yml has correct structure"""
        workflow_path = Path(".github/workflows/lint.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        assert 'name' in content
        assert content['name'] == 'Lint'
        assert 'on' in content
        assert 'jobs' in content
    
    def test_test_workflow_structure(self):
        """Test that test.yml has correct structure"""
        workflow_path = Path(".github/workflows/test.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        assert 'name' in content
        assert content['name'] == 'Test'
        assert 'on' in content
        assert 'jobs' in content
    
    def test_lint_workflow_runs_ruff(self):
        """Test that lint workflow runs ruff"""
        workflow_path = Path(".github/workflows/lint.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        steps = content['jobs']['lint']['steps']
        
        # Check that ruff is installed and run
        step_commands = []
        for step in steps:
            if 'run' in step:
                step_commands.append(step['run'])
        
        commands_str = ' '.join(step_commands)
        assert 'ruff' in commands_str.lower()
    
    def test_test_workflow_runs_pytest(self):
        """Test that test workflow runs pytest"""
        workflow_path = Path(".github/workflows/test.yml")
        
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)
        
        steps = content['jobs']['build']['steps']
        
        # Check that pytest is run
        step_commands = []
        for step in steps:
            if 'run' in step:
                step_commands.append(step['run'])
        
        commands_str = ' '.join(step_commands)
        assert 'pytest' in commands_str.lower()
    
    def test_workflows_use_python_3_10(self):
        """Test that workflows use Python 3.10"""
        for workflow_file in ['lint.yml', 'test.yml']:
            workflow_path = Path(f".github/workflows/{workflow_file}")
            
            with open(workflow_path, 'r') as f:
                content = yaml.safe_load(f)
            
            # Find python-version in steps
            jobs = content['jobs']
            for job_name, job_data in jobs.items():
                for step in job_data['steps']:
                    if 'with' in step and 'python-version' in step['with']:
                        assert step['with']['python-version'] == '3.10'
    
    def test_workflows_trigger_on_correct_branches(self):
        """Test that workflows trigger on correct branches"""
        for workflow_file in ['lint.yml', 'test.yml']:
            workflow_path = Path(f".github/workflows/{workflow_file}")
            
            with open(workflow_path, 'r') as f:
                content = yaml.safe_load(f)
            
            # Check push branches
            if 'push' in content['on']:
                branches = content['on']['push']['branches']
                assert 'main' in branches
    
    def test_workflows_use_ubuntu_latest(self):
        """Test that workflows use ubuntu-latest runner"""
        for workflow_file in ['lint.yml', 'test.yml']:
            workflow_path = Path(f".github/workflows/{workflow_file}")
            
            with open(workflow_path, 'r') as f:
                content = yaml.safe_load(f)
            
            jobs = content['jobs']
            for job_name, job_data in jobs.items():
                assert job_data['runs-on'] == 'ubuntu-latest'


class TestRequirementsFile:
    """Test requirements files"""
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists"""
        req_path = Path("codebase/requirements.txt")
        assert req_path.exists()
    
    def test_requirements_txt_not_empty(self):
        """Test that requirements.txt is not empty"""
        req_path = Path("codebase/requirements.txt")
        
        with open(req_path, 'r') as f:
            content = f.read()
        
        assert len(content.strip()) > 0
    
    def test_requirements_txt_has_fastapi(self):
        """Test that requirements.txt includes fastapi"""
        req_path = Path("codebase/requirements.txt")
        
        with open(req_path, 'r') as f:
            content = f.read().lower()
        
        assert 'fastapi' in content
    
    def test_requirements_txt_has_uvicorn(self):
        """Test that requirements.txt includes uvicorn"""
        req_path = Path("codebase/requirements.txt")
        
        with open(req_path, 'r') as f:
            content = f.read().lower()
        
        assert 'uvicorn' in content
    
    def test_requirements_txt_has_sqlalchemy(self):
        """Test that requirements.txt includes sqlalchemy"""
        req_path = Path("codebase/requirements.txt")
        
        with open(req_path, 'r') as f:
            content = f.read().lower()
        
        assert 'sqlalchemy' in content
    
    def test_requirements_dev_exists(self):
        """Test that requirements-dev.txt exists"""
        req_path = Path("requirements-dev.txt")
        assert req_path.exists()
    
    def test_requirements_dev_has_pytest(self):
        """Test that requirements-dev.txt includes pytest"""
        req_path = Path("requirements-dev.txt")
        
        with open(req_path, 'r') as f:
            content = f.read().lower()
        
        assert 'pytest' in content