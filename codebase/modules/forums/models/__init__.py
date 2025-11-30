"""
Forums Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

# Use relative import from the codebase directory
from ...utils.db import Base

# Association table for many-to-many relationship between threads and tags
thread_tags = Table('thread_tags', Base.metadata,
    Column('thread_id', Integer, ForeignKey('forum_threads.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('forum_tags.id'), primary_key=True)
)


class ForumTag(Base):
    __tablename__ = "forum_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    threads = relationship("ForumThread", secondary="thread_tags", back_populates="tags")


class ForumCategory(Base):
    __tablename__ = "forum_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    parent = relationship("ForumCategory", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("ForumCategory", back_populates="parent")
    threads = relationship("ForumThread", back_populates="category")


class ForumThread(Base):
    __tablename__ = "forum_threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category_id = Column(Integer, ForeignKey("forum_categories.id"))
    author = Column(String, index=True)
    is_pinned = Column(Boolean, default=False)  # For sticky/pinned threads
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("ForumCategory", back_populates="threads")
    posts = relationship("ForumPost", back_populates="thread")
    tags = relationship("ForumTag", secondary="thread_tags", back_populates="threads")


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    thread_id = Column(Integer, ForeignKey("forum_threads.id"))
    author = Column(String, index=True)
    parent_post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    thread = relationship("ForumThread", back_populates="posts")
    parent_post = relationship("ForumPost", remote_side=[id], back_populates="replies")
    replies = relationship("ForumPost", back_populates="parent_post")


class ForumThread(Base):
    __tablename__ = "forum_threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    category_id = Column(Integer, ForeignKey("forum_categories.id"))
    author = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("ForumCategory", back_populates="threads")
    posts = relationship("ForumPost", back_populates="thread")


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    thread_id = Column(Integer, ForeignKey("forum_threads.id"))
    author = Column(String, index=True)
    parent_post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    thread = relationship("ForumThread", back_populates="posts")
    parent_post = relationship("ForumPost", remote_side=[id], back_populates="replies")
    replies = relationship("ForumPost", back_populates="parent_post")