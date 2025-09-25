
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mvp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'change-this-secret'  # change in prod
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    # add other fields as needed

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

    _table_args_ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment.id'), nullable=False)
    value = db.Column(db.String(20), nullable=False)  # could be letter or numeric
    note = db.Column(db.String(255), nullable=True)
    enrollment = db.relationship('Enrollment', backref='grades')

# Auth endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'user exists'}), 400
    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'registered'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'invalid credentials'}), 401
    access = create_access_token(identity=user.id)
    return jsonify({'access_token': access}), 200

# Student CRUD
@app.route('/api/students', methods=['GET'])
@jwt_required()
def list_students():
    students = Student.query.all()
    out = []
    for s in students:
        out.append({'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name, 'email': s.email})
    return jsonify(out)

@app.route('/api/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.json
    s = Student(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id}), 201

@app.route('/api/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    s = Student.query.get_or_404(student_id)
    return jsonify({'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name, 'email': s.email})

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@jwt_required()
def update_student(student_id):
    s = Student.query.get_or_404(student_id)
    data = request.json
    s.first_name = data.get('first_name', s.first_name)
    s.last_name = data.get('last_name', s.last_name)
    s.email = data.get('email', s.email)
    db.session.commit()
    return jsonify({'msg': 'updated'})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'msg': 'deleted'})

# Courses
@app.route('/api/courses', methods=['GET'])
@jwt_required()
def list_courses():
    cs = Course.query.all()
    return jsonify([{'id': c.id, 'code': c.code, 'title': c.title} for c in cs])

@app.route('/api/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.json
    c = Course(code=data.get('code'), title=data.get('title'))
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id}), 201

@app.route('/api/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    c = Course.query.get_or_404(course_id)
    return jsonify({'id': c.id, 'code': c.code, 'title': c.title})

# Enrollments (assign student to course)
@app.route('/api/enrollments', methods=['POST'])
@jwt_required()
def enroll_student():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    if not Student.query.get(student_id) or not Course.query.get(course_id):
        return jsonify({'msg': 'invalid student or course id'}), 400
    # Unique constraint will prevent duplicates
    e = Enrollment(student_id=student_id, course_id=course_id)
    try:
        db.session.add(e)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return jsonify({'msg': 'already enrolled or error', 'error': str(exc)}), 400
    return jsonify({'id': e.id}), 201

@app.route('/api/enrollments/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_enrollments(student_id):
    ens = Enrollment.query.filter_by(student_id=student_id).all()
    return jsonify([{'id': e.id, 'course': {'id': e.course.id, 'code': e.course.code, 'title': e.course.title}} for e in ens])

# Grades
@app.route('/api/grades', methods=['POST'])
@jwt_required()
def add_grade():
    data = request.json
    enrollment_id = data.get('enrollment_id')
    value = data.get('value')
    note = data.get('note')
    if not Enrollment.query.get(enrollment_id):
        return jsonify({'msg': 'invalid enrollment'}), 400
    g = Grade(enrollment_id=enrollment_id, value=value, note=note)
    db.session.add(g)
    db.session.commit()
    return jsonify({'id': g.id}), 201

@app.route('/api/grades/enrollment/<int:enrollment_id>', methods=['GET'])
@jwt_required()
def get_grades_for_enrollment(enrollment_id):
    grades = Grade.query.filter_by(enrollment_id=enrollment_id).all()
    return jsonify([{'id': g.id, 'value': g.value, 'note': g.note} for g in grades])

@app.route('/api/grades/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_grades_for_student(student_id):
    ens = Enrollment.query.filter_by(student_id=student_id).all()
    out = []
    for e in ens:
        for g in e.grades:
            out.append({
                'grade_id': g.id,
                'value': g.value,
                'note': g.note,
                'course': {'id': e.course.id, 'code': e.course.code, 'title': e.course.title},
                'enrollment_id': e.id
            })
    return jsonify(out)

if __name__ == '_main_':
    app.run(debug=True)