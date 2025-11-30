"""
Tests for modules/forums/models/__init__.py
"""
import pytest
from datetime import datetime


def test_forum_category_creation(test_db_session):
    """Test creating a ForumCategory"""
    from modules.forums.models import ForumCategory
    
    category = ForumCategory(
        name="General Discussion",
        description="A place for general topics"
    )
    
    test_db_session.add(category)
    test_db_session.commit()
    
    retrieved = test_db_session.query(ForumCategory).filter_by(name="General Discussion").first()
    
    assert retrieved is not None
    assert retrieved.name == "General Discussion"
    assert retrieved.description == "A place for general topics"
    assert isinstance(retrieved.created_at, datetime)


def test_forum_thread_creation(test_db_session):
    """Test creating a ForumThread"""
    from modules.forums.models import ForumCategory, ForumThread
    
    # Create category first
    category = ForumCategory(name="Tech", description="Technology discussions")
    test_db_session.add(category)
    test_db_session.commit()
    
    # Create thread
    thread = ForumThread(
        title="Test Thread",
        content="This is a test thread content",
        category_id=category.id,
        author="testuser"
    )
    
    test_db_session.add(thread)
    test_db_session.commit()
    
    retrieved = test_db_session.query(ForumThread).filter_by(title="Test Thread").first()
    
    assert retrieved is not None
    assert retrieved.title == "Test Thread"
    assert retrieved.content == "This is a test thread content"
    assert retrieved.author == "testuser"
    assert retrieved.category_id == category.id
    assert isinstance(retrieved.created_at, datetime)
    assert isinstance(retrieved.updated_at, datetime)


def test_forum_thread_category_relationship(test_db_session):
    """Test relationship between ForumThread and ForumCategory"""
    from modules.forums.models import ForumCategory, ForumThread
    
    category = ForumCategory(name="Gaming", description="Gaming topics")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Best Games 2025",
        content="What are your favorite games?",
        category_id=category.id,
        author="gamer123"
    )
    
    test_db_session.add(thread)
    test_db_session.commit()
    
    # Test relationship
    assert thread.category is not None
    assert thread.category.name == "Gaming"
    assert thread.category.id == category.id


def test_forum_post_creation(test_db_session):
    """Test creating a ForumPost"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    
    # Create category and thread
    category = ForumCategory(name="Help", description="Help forum")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Need Help",
        content="I need assistance",
        category_id=category.id,
        author="needhelp"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    # Create post
    post = ForumPost(
        content="Here is my reply",
        thread_id=thread.id,
        author="helper"
    )
    
    test_db_session.add(post)
    test_db_session.commit()
    
    retrieved = test_db_session.query(ForumPost).first()
    
    assert retrieved is not None
    assert retrieved.content == "Here is my reply"
    assert retrieved.author == "helper"
    assert retrieved.thread_id == thread.id
    assert isinstance(retrieved.created_at, datetime)
    assert isinstance(retrieved.updated_at, datetime)


def test_forum_post_thread_relationship(test_db_session):
    """Test relationship between ForumPost and ForumThread"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    
    category = ForumCategory(name="News", description="News forum")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Breaking News",
        content="Latest updates",
        category_id=category.id,
        author="newsreporter"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    post = ForumPost(
        content="Thanks for the update!",
        thread_id=thread.id,
        author="reader"
    )
    test_db_session.add(post)
    test_db_session.commit()
    
    # Test relationship
    assert post.thread is not None
    assert post.thread.title == "Breaking News"
    assert post.thread.id == thread.id


def test_multiple_threads_per_category(test_db_session):
    """Test that a category can have multiple threads"""
    from modules.forums.models import ForumCategory, ForumThread
    
    category = ForumCategory(name="Programming", description="Programming discussions")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread1 = ForumThread(
        title="Python Tips",
        content="Share your Python tips",
        category_id=category.id,
        author="pythonista"
    )
    
    thread2 = ForumThread(
        title="JavaScript Tricks",
        content="JavaScript best practices",
        category_id=category.id,
        author="jsdev"
    )
    
    test_db_session.add_all([thread1, thread2])
    test_db_session.commit()
    
    threads = test_db_session.query(ForumThread).filter_by(category_id=category.id).all()
    
    assert len(threads) == 2


def test_multiple_posts_per_thread(test_db_session):
    """Test that a thread can have multiple posts"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    
    category = ForumCategory(name="Discussion", description="General discussions")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Popular Thread",
        content="This will have many replies",
        category_id=category.id,
        author="starter"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    post1 = ForumPost(content="First reply", thread_id=thread.id, author="user1")
    post2 = ForumPost(content="Second reply", thread_id=thread.id, author="user2")
    post3 = ForumPost(content="Third reply", thread_id=thread.id, author="user3")
    
    test_db_session.add_all([post1, post2, post3])
    test_db_session.commit()
    
    posts = test_db_session.query(ForumPost).filter_by(thread_id=thread.id).all()
    
    assert len(posts) == 3


def test_forum_category_without_threads(test_db_session):
    """Test creating a category without threads"""
    from modules.forums.models import ForumCategory, ForumThread
    
    category = ForumCategory(name="Empty Category", description="No threads yet")
    test_db_session.add(category)
    test_db_session.commit()
    
    threads = test_db_session.query(ForumThread).filter_by(category_id=category.id).all()
    
    assert len(threads) == 0


def test_forum_thread_without_posts(test_db_session):
    """Test creating a thread without posts"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    
    category = ForumCategory(name="Test", description="Test category")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="No Replies",
        content="This thread has no replies",
        category_id=category.id,
        author="lonely"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    posts = test_db_session.query(ForumPost).filter_by(thread_id=thread.id).all()
    
    assert len(posts) == 0


def test_forum_thread_update_timestamp(test_db_session):
    """Test that updated_at changes on update"""
    from modules.forums.models import ForumCategory, ForumThread
    import time
    
    category = ForumCategory(name="Update Test", description="Testing updates")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Original Title",
        content="Original content",
        category_id=category.id,
        author="author"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    original_updated = thread.updated_at
    
    time.sleep(0.1)
    
    thread.title = "Updated Title"
    test_db_session.commit()
    
    assert thread.updated_at >= original_updated


def test_forum_post_update_timestamp(test_db_session):
    """Test that post updated_at changes on update"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    import time
    
    category = ForumCategory(name="Post Update", description="Test post updates")
    test_db_session.add(category)
    test_db_session.commit()
    
    thread = ForumThread(
        title="Thread",
        content="Content",
        category_id=category.id,
        author="author"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    post = ForumPost(
        content="Original post",
        thread_id=thread.id,
        author="poster"
    )
    test_db_session.add(post)
    test_db_session.commit()
    
    original_updated = post.updated_at
    
    time.sleep(0.1)
    
    post.content = "Edited post"
    test_db_session.commit()
    
    assert post.updated_at >= original_updated


def test_forum_category_empty_description(test_db_session):
    """Test creating category with empty description"""
    from modules.forums.models import ForumCategory
    
    category = ForumCategory(name="No Description", description="")
    test_db_session.add(category)
    test_db_session.commit()
    
    retrieved = test_db_session.query(ForumCategory).filter_by(name="No Description").first()
    assert retrieved.description == ""


def test_forum_thread_long_content(test_db_session):
    """Test thread with very long content"""
    from modules.forums.models import ForumCategory, ForumThread
    
    category = ForumCategory(name="Long Content", description="Test long content")
    test_db_session.add(category)
    test_db_session.commit()
    
    long_content = "A" * 10000  # 10k characters
    
    thread = ForumThread(
        title="Long Thread",
        content=long_content,
        category_id=category.id,
        author="verbose"
    )
    test_db_session.add(thread)
    test_db_session.commit()
    
    retrieved = test_db_session.query(ForumThread).filter_by(title="Long Thread").first()
    assert len(retrieved.content) == 10000


def test_forum_models_table_names():
    """Test that all models have correct table names"""
    from modules.forums.models import ForumCategory, ForumThread, ForumPost
    
    assert ForumCategory.__tablename__ == "forum_categories"
    assert ForumThread.__tablename__ == "forum_threads"
    assert ForumPost.__tablename__ == "forum_posts"