"""
Tests for GitHub workflow configuration files
These tests validate the structure and content of workflow YAML files
"""
import pytest
import os
import yaml


def test_lint_workflow_exists():
    """Test that lint workflow file exists"""
    workflow_path = ".github/workflows/lint.yml"
    assert os.path.exists(workflow_path), "lint.yml workflow file should exist"


def test_test_workflow_exists():
    """Test that test workflow file exists"""
    workflow_path = ".github/workflows/test.yml"
    assert os.path.exists(workflow_path), "test.yml workflow file should exist"


def test_lint_workflow_valid_yaml():
    """Test that lint workflow is valid YAML"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            assert config is not None
        except yaml.YAMLError as e:
            pytest.fail(f"lint.yml is not valid YAML: {e}")


def test_test_workflow_valid_yaml():
    """Test that test workflow is valid YAML"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            assert config is not None
        except yaml.YAMLError as e:
            pytest.fail(f"test.yml is not valid YAML: {e}")


def test_lint_workflow_has_name():
    """Test that lint workflow has a name"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'name' in config
        assert config['name'] == 'Lint'


def test_test_workflow_has_name():
    """Test that test workflow has a name"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'name' in config
        assert config['name'] == 'Test'


def test_lint_workflow_triggers():
    """Test that lint workflow has correct triggers"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'on' in config
        assert 'push' in config['on']
        assert 'pull_request' in config['on']


def test_test_workflow_triggers():
    """Test that test workflow has correct triggers"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'on' in config
        assert 'push' in config['on']
        assert 'pull_request' in config['on']


def test_lint_workflow_runs_on_ubuntu():
    """Test that lint workflow runs on ubuntu"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'jobs' in config
        job = list(config['jobs'].values())[0]
        assert job['runs-on'] == 'ubuntu-latest'


def test_test_workflow_runs_on_ubuntu():
    """Test that test workflow runs on ubuntu"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        assert 'jobs' in config
        job = list(config['jobs'].values())[0]
        assert job['runs-on'] == 'ubuntu-latest'


def test_lint_workflow_uses_python():
    """Test that lint workflow sets up Python"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        python_setup = any('setup-python' in str(step.get('uses', '')) for step in steps)
        assert python_setup, "Workflow should set up Python"


def test_test_workflow_uses_python():
    """Test that test workflow sets up Python"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        python_setup = any('setup-python' in str(step.get('uses', '')) for step in steps)
        assert python_setup, "Workflow should set up Python"


def test_lint_workflow_installs_ruff():
    """Test that lint workflow installs ruff"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        # Check for ruff installation
        install_steps = [step.get('run', '') for step in steps if 'run' in step]
        ruff_installed = any('ruff' in step for step in install_steps)
        assert ruff_installed, "Workflow should install ruff"


def test_lint_workflow_runs_ruff():
    """Test that lint workflow runs ruff check"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        run_steps = [step.get('run', '') for step in steps if 'run' in step]
        ruff_check = any('ruff check' in step for step in run_steps)
        assert ruff_check, "Workflow should run ruff check"


def test_test_workflow_installs_requirements():
    """Test that test workflow installs requirements"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        install_steps = [step.get('run', '') for step in steps if 'run' in step]
        requirements_installed = any('requirements.txt' in step for step in install_steps)
        assert requirements_installed, "Workflow should install requirements"


def test_test_workflow_runs_pytest():
    """Test that test workflow runs pytest"""
    workflow_path = ".github/workflows/test.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        job = list(config['jobs'].values())[0]
        steps = job['steps']
        
        run_steps = [step.get('run', '') for step in steps if 'run' in step]
        pytest_run = any('pytest' in step for step in run_steps)
        assert pytest_run, "Workflow should run pytest"


def test_workflows_use_python_310():
    """Test that both workflows use Python 3.10"""
    for workflow_file in ['lint.yml', 'test.yml']:
        workflow_path = f".github/workflows/{workflow_file}"
        
        with open(workflow_path, 'r') as f:
            config = yaml.safe_load(f)
            job = list(config['jobs'].values())[0]
            steps = job['steps']
            
            for step in steps:
                if 'setup-python' in str(step.get('uses', '')):
                    assert step.get('with', {}).get('python-version') == '3.10'


def test_workflows_checkout_code():
    """Test that both workflows checkout the code"""
    for workflow_file in ['lint.yml', 'test.yml']:
        workflow_path = f".github/workflows/{workflow_file}"
        
        with open(workflow_path, 'r') as f:
            config = yaml.safe_load(f)
            job = list(config['jobs'].values())[0]
            steps = job['steps']
            
            checkout = any('checkout' in str(step.get('uses', '')) for step in steps)
            assert checkout, f"{workflow_file} should checkout code"


def test_workflows_trigger_on_main_branch():
    """Test that workflows trigger on main branch"""
    for workflow_file in ['lint.yml', 'test.yml']:
        workflow_path = f".github/workflows/{workflow_file}"
        
        with open(workflow_path, 'r') as f:
            config = yaml.safe_load(f)
            push_config = config['on']['push']
            
            assert 'branches' in push_config
            assert 'main' in push_config['branches']


def test_lint_workflow_triggers_on_dev_branches():
    """Test that lint workflow triggers on dev branches"""
    workflow_path = ".github/workflows/lint.yml"
    
    with open(workflow_path, 'r') as f:
        config = yaml.safe_load(f)
        push_config = config['on']['push']
        
        assert 'd-0' in push_config['branches']
        assert 'd-1' in push_config['branches']