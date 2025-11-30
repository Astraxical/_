"""
Unit tests for modules/forums/models/__init__.py
"""
import pytest
from datetime import datetime
from modules.forums.models import ForumCategory, ForumThread, ForumPost


class TestForumCategoryModel:
    """Test ForumCategory database model"""
    
    def test_forum_category_creation(self, test_db_session):
        """Test creating a ForumCategory instance"""
        category = ForumCategory(
            name="General Discussion",
            description="General topics and discussions"
        )
        test_db_session.add(category)
        test_db_session.commit()
        
        assert category.id is not None
        assert category.name == "General Discussion"
        assert category.description == "General topics and discussions"
        assert isinstance(category.created_at, datetime)
    
    def test_forum_category_default_created_at(self, test_db_session):
        """Test that created_at is set automatically"""
        category = ForumCategory(name="Test Category")
        test_db_session.add(category)
        test_db_session.commit()
        
        assert category.created_at is not None
        assert isinstance(category.created_at, datetime)
    
    def test_forum_category_query_by_name(self, test_db_session):
        """Test querying category by name"""
        category = ForumCategory(
            name="Tech Talk",
            description="Technology discussions"
        )
        test_db_session.add(category)
        test_db_session.commit()
        
        found = test_db_session.query(ForumCategory).filter(
            ForumCategory.name == "Tech Talk"
        ).first()
        
        assert found is not None
        assert found.name == "Tech Talk"
    
    def test_forum_category_without_description(self, test_db_session):
        """Test creating category without description"""
        category = ForumCategory(name="Minimal Category")
        test_db_session.add(category)
        test_db_session.commit()
        
        assert category.id is not None
        assert category.description is None
    
    def test_forum_category_tablename(self):
        """Test that tablename is correctly set"""
        assert ForumCategory.__tablename__ == "forum_categories"
    
    def test_forum_category_multiple_categories(self, test_db_session):
        """Test creating multiple categories"""
        categories = [
            ForumCategory(name="Category 1", description="First"),
            ForumCategory(name="Category 2", description="Second"),
            ForumCategory(name="Category 3", description="Third")
        ]
        test_db_session.add_all(categories)
        test_db_session.commit()
        
        all_categories = test_db_session.query(ForumCategory).all()
        assert len(all_categories) >= 3


class TestForumThreadModel:
    """Test ForumThread database model"""
    
    def test_forum_thread_creation(self, test_db_session):
        """Test creating a ForumThread instance"""
        category = ForumCategory(name="Test Category")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Test Thread",
            content="This is a test thread",
            category_id=category.id,
            author="testuser"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        assert thread.id is not None
        assert thread.title == "Test Thread"
        assert thread.content == "This is a test thread"
        assert thread.author == "testuser"
        assert thread.category_id == category.id
    
    def test_forum_thread_timestamps(self, test_db_session):
        """Test that timestamps are set automatically"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Test",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        assert isinstance(thread.created_at, datetime)
        assert isinstance(thread.updated_at, datetime)
    
    def test_forum_thread_category_relationship(self, test_db_session):
        """Test relationship between thread and category"""
        category = ForumCategory(name="Test Category")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Test Thread",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        assert thread.category is not None
        assert thread.category.name == "Test Category"
    
    def test_forum_thread_query_by_author(self, test_db_session):
        """Test querying threads by author"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread1 = ForumThread(
            title="Thread 1",
            content="Content 1",
            category_id=category.id,
            author="author1"
        )
        thread2 = ForumThread(
            title="Thread 2",
            content="Content 2",
            category_id=category.id,
            author="author1"
        )
        test_db_session.add_all([thread1, thread2])
        test_db_session.commit()
        
        threads = test_db_session.query(ForumThread).filter(
            ForumThread.author == "author1"
        ).all()
        
        assert len(threads) == 2
    
    def test_forum_thread_query_by_category(self, test_db_session):
        """Test querying threads by category"""
        category1 = ForumCategory(name="Category 1")
        category2 = ForumCategory(name="Category 2")
        test_db_session.add_all([category1, category2])
        test_db_session.commit()
        
        thread1 = ForumThread(
            title="Thread 1",
            content="Content",
            category_id=category1.id,
            author="user"
        )
        thread2 = ForumThread(
            title="Thread 2",
            content="Content",
            category_id=category1.id,
            author="user"
        )
        test_db_session.add_all([thread1, thread2])
        test_db_session.commit()
        
        threads = test_db_session.query(ForumThread).filter(
            ForumThread.category_id == category1.id
        ).all()
        
        assert len(threads) == 2
    
    def test_forum_thread_tablename(self):
        """Test that tablename is correctly set"""
        assert ForumThread.__tablename__ == "forum_threads"


class TestForumPostModel:
    """Test ForumPost database model"""
    
    def test_forum_post_creation(self, test_db_session):
        """Test creating a ForumPost instance"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Test Thread",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        post = ForumPost(
            content="This is a reply",
            thread_id=thread.id,
            author="replier"
        )
        test_db_session.add(post)
        test_db_session.commit()
        
        assert post.id is not None
        assert post.content == "This is a reply"
        assert post.thread_id == thread.id
        assert post.author == "replier"
    
    def test_forum_post_timestamps(self, test_db_session):
        """Test that timestamps are set automatically"""
        category = ForumCategory(name="Test")
        thread = ForumThread(
            title="Test",
            content="Content",
            category_id=1,
            author="user"
        )
        test_db_session.add_all([category, thread])
        test_db_session.commit()
        
        post = ForumPost(
            content="Reply",
            thread_id=thread.id,
            author="user"
        )
        test_db_session.add(post)
        test_db_session.commit()
        
        assert isinstance(post.created_at, datetime)
        assert isinstance(post.updated_at, datetime)
    
    def test_forum_post_thread_relationship(self, test_db_session):
        """Test relationship between post and thread"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Test Thread",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        post = ForumPost(
            content="Reply",
            thread_id=thread.id,
            author="replier"
        )
        test_db_session.add(post)
        test_db_session.commit()
        
        assert post.thread is not None
        assert post.thread.title == "Test Thread"
    
    def test_forum_post_query_by_thread(self, test_db_session):
        """Test querying posts by thread"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Thread",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        posts = [
            ForumPost(content="Reply 1", thread_id=thread.id, author="user1"),
            ForumPost(content="Reply 2", thread_id=thread.id, author="user2"),
            ForumPost(content="Reply 3", thread_id=thread.id, author="user3")
        ]
        test_db_session.add_all(posts)
        test_db_session.commit()
        
        found_posts = test_db_session.query(ForumPost).filter(
            ForumPost.thread_id == thread.id
        ).all()
        
        assert len(found_posts) == 3
    
    def test_forum_post_query_by_author(self, test_db_session):
        """Test querying posts by author"""
        category = ForumCategory(name="Test")
        thread = ForumThread(
            title="Thread",
            content="Content",
            category_id=1,
            author="user"
        )
        test_db_session.add_all([category, thread])
        test_db_session.commit()
        
        post1 = ForumPost(content="Post 1", thread_id=thread.id, author="author1")
        post2 = ForumPost(content="Post 2", thread_id=thread.id, author="author1")
        test_db_session.add_all([post1, post2])
        test_db_session.commit()
        
        posts = test_db_session.query(ForumPost).filter(
            ForumPost.author == "author1"
        ).all()
        
        assert len(posts) == 2
    
    def test_forum_post_tablename(self):
        """Test that tablename is correctly set"""
        assert ForumPost.__tablename__ == "forum_posts"
    
    def test_forum_post_multiple_replies_same_thread(self, test_db_session):
        """Test multiple posts in the same thread"""
        category = ForumCategory(name="Test")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Popular Thread",
            content="Content",
            category_id=category.id,
            author="user"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        posts = [
            ForumPost(content=f"Reply {i}", thread_id=thread.id, author=f"user{i}")
            for i in range(10)
        ]
        test_db_session.add_all(posts)
        test_db_session.commit()
        
        found_posts = test_db_session.query(ForumPost).filter(
            ForumPost.thread_id == thread.id
        ).all()
        
        assert len(found_posts) == 10


class TestForumModelsRelationships:
    """Test relationships between forum models"""
    
    def test_full_forum_hierarchy(self, test_db_session):
        """Test complete hierarchy: category -> thread -> posts"""
        category = ForumCategory(name="Tech", description="Technology")
        test_db_session.add(category)
        test_db_session.commit()
        
        thread = ForumThread(
            title="Python Tips",
            content="Share your Python tips",
            category_id=category.id,
            author="pythonista"
        )
        test_db_session.add(thread)
        test_db_session.commit()
        
        posts = [
            ForumPost(content="Use list comprehensions", thread_id=thread.id, author="user1"),
            ForumPost(content="Try type hints", thread_id=thread.id, author="user2")
        ]
        test_db_session.add_all(posts)
        test_db_session.commit()
        
        # Verify the hierarchy
        assert thread.category.name == "Tech"
        assert len(test_db_session.query(ForumPost).filter(
            ForumPost.thread_id == thread.id
        ).all()) == 2