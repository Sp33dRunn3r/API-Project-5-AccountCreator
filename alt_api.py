# This is an alternative way to create the API for the given front-end.
# These are the primary routes used for the project. Different from regular "app.routes",
# these routes utilize the "flask-restx" library, which creates a more simplistic form of accessing
# and modifying data through visually represented HTTP requests. They are represented through port:5000.


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource, fields
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '727272'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'user_name', 'email', 'password')

    model = api.model('model', {
        'first_name': fields.String('Enter first name'),
        'last_name': fields.String('Enter last name'),
        'user_name': fields.String('Enter user name'),
        'email': fields.String('Enter email'),
        'password': fields.String('Enter password')
    })


users_schema = UserSchema()
user_schema = UserSchema()


@api.route('/get')
class GET(Resource):
    def get(self):
        users = User.query.all()
        return jsonify(users_schema.dump(users))


@api.route('/get/<int:id>')
class GET(Resource):
    def get(self, id):
        user = User.query.all(id)
        return jsonify(users_schema.dump(user))


@api.route('/post')
class POST(Resource):
    def post(self):
        user = User(first_name=request.json['first_name'],
                    last_name=request.json['last_name'],
                    user_name=request.json['user_name'],
                    email=request.json['email'],
                    password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return {201: 'Successfully added to database'}


@api.route('/put/<int:id>')
class PUT(Resource):
    def put(self, id):
        user = User.query.get(id)
        user.first_name = request.json['first_name']
        user.last_name = request.json['last_name']
        user.user_name = request.json['user_name']
        user.email = request.json['email']
        user.password = request.json['password']
        db.session.commit()
        return {201: 'Data successfully updated'}


@api.route('/delete/<int:id>')
class DELETE(Resource):
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {200: 'User successfully deleted'}


if __name__ == '__main__':
    app.run(debug=True)
