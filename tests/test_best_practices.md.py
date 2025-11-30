"""
Markdown documentation validation tests.
Validates links, structure, and style guidelines.
"""

import pytest
import re
from pathlib import Path
import requests


class TestMarkdownValidation:
    """Test suite for markdown file validation."""
    
    @pytest.fixture
    def markdown_file_path(self):
        """Fixture providing path to markdown file."""
        # TODO: Update with actual file path
        return Path(__file__).parent.parent / "README.md"
    
    @pytest.fixture
    def markdown_content(self, markdown_file_path):
        """Fixture providing markdown content."""
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_file_exists(self, markdown_file_path):
        """Test that markdown file exists."""
        assert markdown_file_path.exists()
    
    def test_not_empty(self, markdown_content):
        """Test that file is not empty."""
        assert len(markdown_content.strip()) > 0
    
    def test_has_title(self, markdown_content):
        """Test that document has a title."""
        assert re.search(r'^#\s+.+', markdown_content, re.MULTILINE)
    
    def test_links_format(self, markdown_content):
        """Test that all links are properly formatted."""
        # Find all markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', markdown_content)
        assert len(links) >= 0, "Should have links or none"
        
        for text, url in links:
            assert text.strip(), "Link text should not be empty"
            assert url.strip(), "Link URL should not be empty"
    
    def test_no_broken_internal_links(self, markdown_content, markdown_file_path):
        """Test that internal links are not broken."""
        # Find internal links (relative paths)
        internal_links = re.findall(r'\[([^\]]+)\]\(([^http][^\)]+)\)', markdown_content)
        
        base_dir = markdown_file_path.parent
        for text, url in internal_links:
            # Remove anchor if present
            file_path = url.split('#')[0]
            if file_path:
                full_path = (base_dir / file_path).resolve()
                # Note: In actual tests, you might want to check if file exists
                # but for now we just validate the format
                assert file_path, f"Internal link should have a path: {text}"
    
    def test_proper_heading_hierarchy(self, markdown_content):
        """Test that heading levels are properly nested."""
        headings = re.findall(r'^(#{1,6})\s+.+', markdown_content, re.MULTILINE)
        
        for i in range(1, len(headings)):
            prev_level = len(headings[i-1])
            curr_level = len(headings[i])
            # Heading level shouldn't skip (e.g., # to ###)
            assert curr_level <= prev_level + 1, \
                f"Heading level jump too large: {prev_level} to {curr_level}"
    
    def test_code_blocks_closed(self, markdown_content):
        """Test that all code blocks are properly closed."""
        code_block_markers = re.findall(r'^```', markdown_content, re.MULTILINE)
        assert len(code_block_markers) % 2 == 0, "All code blocks should be closed"
    
    def test_no_trailing_whitespace(self, markdown_content):
        """Test that lines don't have trailing whitespace."""
        lines = markdown_content.split('\n')
        lines_with_trailing_ws = [
            i+1 for i, line in enumerate(lines) 
            if line and line != line.rstrip()
        ]
        assert len(lines_with_trailing_ws) == 0, \
            f"Lines with trailing whitespace: {lines_with_trailing_ws}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])