import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
#from google.appengine.ext.webapp import template

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Student_record(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    name = db.StringProperty()
    age = db.StringProperty()
    sex = db.StringProperty()
    mark = db.StringProperty()

def record_key(name=None):
    """Constructs a Datastore key for a Student_record entity with record_name."""
    return db.Key.from_path('Student_record', name or 'default_record')


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())
#        self.response.out.write(template.render('index.html',{}))

class add_student(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('add.html')
        self.response.out.write(template.render())
    def post(self):
        student_record =Student_record(key_name =self.request.get("name"))
        student_record.name = self.request.get("name")
        student_record.sex = self.request.get('sex')
        student_record.mark = self.request.get('mark')
        student_record.age = self.request.get('age')
        student_record.put()
        self.redirect('/') 
class serch(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('serch.html')
        self.response.out.write(template.render())
class delete(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('delete.html')
        self.response.out.write(template.render())
    def post(self):
        name=self.request.get('detail')
        delete = db.Key.from_path('Student_record',name)
        db.delete(delete)     

class students(webapp2.RequestHandler):
    def get(self):
        value = self.request.get("detail")

        if value =="sorted by age":
            students = db.GqlQuery("SELECT * "
                                "FROM Student_record "
                                 "ORDER BY age ")
        elif value =="sorted by mark":
            students = db.GqlQuery("SELECT * "
                                "FROM Student_record "
                                 "ORDER BY mark ")
        else :
           students = db.GqlQuery("SELECT * "
                                "FROM Student_record WHERE name IN:1", [value]
                                 )
        for student in students:
            self.response.headers['Content-Type']='text/plain'
            self.response.out.write(student.name + ' ' + student.sex + ' ' + student.age + ' ' + student.mark + "\n" )

app = webapp2.WSGIApplication([('/', MainPage),
('/sign', add_student), ('/detail',students),('/serch',serch),('/delete',delete)],
                              debug=False)
