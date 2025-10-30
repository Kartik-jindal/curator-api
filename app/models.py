from sqlalchemy import Boolean , Column , ForeignKey , Integer, String , Table , Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Table that links content and tags (many-to-many relationship)
content_tags_association = Table(
    'content_tags', Base.metadata,
    Column('content_id', Integer , ForeignKey('content.id') , primary_key = True ),
    Column('tag_id' , Integer , ForeignKey('tags.id'), primary_key = True )
)

# Table that links Users and Tags they follow (many-to-many relationship)
user_followed_tags_association = Table(
    'user_followed_tags', Base.metadata,
    Column('user_id' , Integer , ForeignKey('users.id') , primary_key = True ),
    Column('tag_id' , Integer , ForeignKey('tags.id') , primary_key = True )
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key = True , index = True)
    email = Column(String , unique = True , index = True , nullable = False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String , nullable = False)
    created_at = Column(DateTime(timezone = True) , server_default = func.now())

    # creating relationship with Content (one-to-many i.e a user can have multiple content)
    content = relationship("Content", back_populates = "owner")

    # creating relationship with Tags (many-to-many i.e a user can follow multiple tags)
    followed_tags = relationship("Tag" , secondary = user_followed_tags_association, back_populates = "followers")
    
class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key = True , index = True)
    title = Column(String , index = True , nullable= False)
    url = Column(String , nullable = False)
    description = Column(Text , nullable = True)
    owner_id = Column(Integer, ForeignKey("users.id") , nullable = False)
    created_at = Column(DateTime(timezone= True) , server_default = func.now())

    owner = relationship("User" , back_populates = "content")
    tags = relationship("Tag" , secondary = content_tags_association , back_populates = "content_items")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer , primary_key = True , index= True)
    name = Column(String , unique = True , index = True , nullable = False)

    content_items = relationship("Content" , secondary = content_tags_association , back_populates = "tags")

    followers = relationship("User" , secondary = user_followed_tags_association , back_populates = "followed_tags")
