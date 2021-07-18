from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging


application=Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db' #three /// for relative path to your python file and 4 //// for giving it the path when accessing from root.

db=SQLAlchemy(application)
#Comment this once database is created.
db.create_all()
#We need to add the model of database along with creating the table witht he respective class

#######STEPS FOR CREATING THE DATABASE AND ADDING VALUES TO THE COLUMNS:
""" Enter the python command to the terminal from the directory that has your .py file.
-- Then import the db from your python file by : from app import db
-- After your db is imported write the command db.create_all to create the database file
-- then iport the class that helps you in accessing your database fields
-- if you want to check if you already have any data in your database or not, type ClassName.query.all() in our case classNAme is BlogPost.
"""

#If you want to add instances of your data to the table use
# db.session.add(title="",author="")
# _---- TO access value sof any specific field of any instance use
# 1. BlogPost.query[0].author   OR
# 2.BlogPost.query.all()[0].author




class BlogPost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default='N/A')
    dateposted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)

post_details=[
    {
        "title":"Post 1",
        "content":"KASLDLKASMDPKMAS",
        "Author":"RANDOM"
    },

    {
        "title":"Post 2",
        "content":"KASLDLKASMDPKMAS"
    }

]

#This might contain the domain name like www.tensai.com/page name but we are using local host right now and the website is not live so just 
#routing it to the page name
#This means that this is just your domain. the index page

# YPu can set multiple pages to route to the same method byt wrting those routes before that particular method
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/posts',methods=['GET',"POST"])
def posts():
        if request.method =='POST':
            post_title=request.form['title']
            post_content=request.form['content']
            post_author=request.form['author']
            new_post =BlogPost(title=post_title,content=post_content,author=post_author)
            db.session.add(new_post)
            #TO commit it to the database otherwise it will be there for only that particular session
            db.session.commit()
            return redirect('/posts')
        else:

            post_details=BlogPost.query.order_by(BlogPost.dateposted).all()

            return render_template('posts.html',postii=post_details)


@application.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@application.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    
    post=BlogPost.query.get_or_404(id)

    #so if we are on edit page then only post method will be called and fields can be updated, otherwise else condition will be called
    #which will lead us to edit page.
    
    if request.method =='POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',postii=post)


@application.route('/posts/new',methods=['GET','POST'])
def new_post():

    #so if we are on edit page then only post method will be called and fields can be updated, otherwise else condition will be called
    #which will lead us to edit page.
    
    if request.method =='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post =BlogPost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        #TO commit it to the database otherwise it will be there for only that particular session
        db.session.commit()
        return redirect('/posts') # we will direct it to the same page for now where we are displaying our posts
    # So if we are not adding anything, we will read every blogpost in the database and displaying them on the basis of date posted.p

    else:
        return render_template('new_post.html')


@application.route('/home/user/<string:name>/posts/<int:id>')
#here both home and the / will point to the same method
def hello(name,id):
    return "Hello, "+ name +"your post id is"+ str(id)

@application.route('/onlyget',methods=['GET'])
def get_only():
    return " You will only get infromTion from this page!!!"


if __name__=="__main__":
    application.run(debug=True)




# To filter instances from database use
    #------- BlogPost.query.filter_by(title='').all()
# To delete instances from database use 
    #------- db.session.delelte(BlogPost.query.get(id))
    #------- db.session.commit()
# To update any field of an instance use
    #------- Blogpsot.query.get(id).fieldname=''
    #------- db.session.commit()
