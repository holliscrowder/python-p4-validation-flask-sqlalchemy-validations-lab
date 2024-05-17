from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, _, name):
        if not name:
            raise ValueError("Author name must be a non-empty string.")
        
        same_name = type(self).query.filter(type(self).name==name).all()
        if len(same_name) > 0 and same_name[0] is not self:
            raise ValueError("Author name must be unique.")

        return name
    
    @validates("phone_number")
    def validate_phone_number(self, _, phone_number):
        if len(str(phone_number)) != 10 or phone_number.isnumeric() == False:
            raise ValueError("Phone number must be 10 digit integer.")
        
        return phone_number
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_name(self, _, title):
        if not title or isinstance(title, str) == False:
            raise ValueError("Title must be a non-empty string.")
        if "Won't Believe" not in title and "Secret" not in title and "Top" not in title and "Guess" not in title:
            raise ValueError("Title must be sufficiently click-baity.")
        
        return title
    
    @validates("content")
    def validate_content(self, _, content):
        if not isinstance(content, str) or len(content) < 250:
            raise ValueError("Content must be string of at least 250 characters.")
        return content

    @validates("summary")
    def validate_summary(self, _, summary):
        if not isinstance(summary, str) or len(summary) > 250:
            raise ValueError("Summary must be 250 or fewer characters.")
        return summary
    
    @validates("category")
    def validate_category(self, _, category):
        if category not in ['Non-Fiction', 'Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
