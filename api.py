from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '727272'

db = SQLAlchemy(app)
ma = Marshmallow(app)
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


users_schema = UserSchema()
user_schema = UserSchema()
UserSchema(many=True)


@app.route('/get')
def get(self):
    users = User.query.all()
    return jsonify(users_schema.dump(users))


@app.route('/get_user/<int:id>')
def get_user(self, id):
    user = User.query.all(id)
    return jsonify(users_schema.dump(user))


@app.route('/add_user', method=['POST'])
def add_user():
    user = User(first_name=request.json['first_name'],
                last_name=request.json['last_name'],
                user_name=request.json['user_name'],
                email=request.json['email'],
                password=request.json['password'])
    db.session.add(user)
    db.session.commit()
    return {201: 'Successfully added to database'}


@app.route('/update/<int:id>', method=["PUT"])
def update_user(id):
    user = User.query.get(id)
    user.first_name = request.json['first_name']
    user.last_name = request.json['last_name']
    user.user_name = request.json['user_name']
    user.email = request.json['email']
    user.password = request.json['password']
    db.session.commit()
    return {201: 'Data successfully updated'}


@app.route('/delete_user/<int:id>', method=["DELETE"])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return {200: 'User successfully deleted'}


if __name__ == '__main__':
    app.run(debug=True)
