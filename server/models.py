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

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError ("Name is required")
        
    
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError("An Author with the same name already exist.")
        
        return name

    @validates('phone_number')
    def validate_number(self, key, phone_number):
        # Remove any non-digit characters (e.g., spaces, dashes)
        cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Check if phone_number has exactly 10 digits
        if len(cleaned_phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        
        return cleaned_phone_number

            

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

    @validates('title')
    def validate_title(self, key, title):
        # Check if the title is not empty and contains a clickbait keyword
        if not title or title.strip() == "":
            raise ValueError("Posts must have titles.")
        
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title is not sufficiently clickbait-y. It must contain one of the following: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        
        return title
    

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be atleast 250 characters.")
        

        return content
    

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Content must be no more than 250 characters.")
        return summary
    

    @validates('category')
    def validate_category(self, key, category):
    # Ensure category is either 'Fiction' or 'Non-Fiction'
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        return category




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
