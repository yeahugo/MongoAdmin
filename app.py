import datetime

from flask import Flask

from flask.ext import admin
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.form import rules
from flask.ext.admin.contrib.mongoengine import ModelView
from werkzeug.contrib.fixers import ProxyFix

# Create application
app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {'DB': 'ModelDB'}

# Create models
db = MongoEngine()
db.init_app(app)

# Define mongoengine documents

class File(db.Document):
    name = db.StringField(max_length=20)
    data = db.FileField()

class Image(db.Document):
    name = db.StringField(max_length=20)
    image = db.ImageField(thumbnail_size=(100, 100, True))

    def __unicode__(self):
        return self.name

class EmImage(db.EmbeddedDocument):
#    image = db.ReferenceField(Image)
    name = db.StringField(max_length=200)
    image = db.ImageField(thumbnail_size=(100,100,True))

class EmFile(db.EmbeddedDocument):
#    gcodeFile = db.ReferenceField(File)
    name = db.StringField(max_length=200)
    data = db.FileField()

class Catalog(db.Document):
    name = db.StringField(max_length = 200)
    def __unicode__(self):
        return self.name

class Toy(db.Document):
    name = db.StringField(max_length = 200)
    print_time = db.StringField(max_length = 50)
    object_size = db.StringField(max_length = 50)
    file_size = db.StringField(max_length = 50)
    parts_num = db.IntField()
    catalog = db.ReferenceField(Catalog)
    description = db.StringField(max_length = 10000)
    images = db.ListField(db.EmbeddedDocumentField(EmImage))
    thumbnail = db.ListField(db.EmbeddedDocumentField(EmImage))
    gcode = db.ListField(db.EmbeddedDocumentField(EmFile))


class ToyView(ModelView):
    column_filters = ['name']
    column_list = ('name', 'print_time','object_size','file_size')

#    column_searchable_list = ('name')

class CatalogView(ModelView):
    column_filters = ['name']

# Customized admin views
# Flask views
@app.route('/index')
def index():
    return redirect('admin')
    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Toy Model Admin')
    # Add views
#    admin.add_view(ModelView(EmFile))
#    admin.add_view(ModelView(EmImage))
    admin.add_view(ToyView(Toy))
    admin.add_view(ModelView(Catalog))

    # Start app
    app.run('0.0.0.0')
