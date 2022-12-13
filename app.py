
import os
from flask import Flask, request, url_for, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

cd = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(cd, 'railway.sqlite3')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.../railway.sqlite3'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()


class Train(db.Model):
    train_id = db.Column(db.Integer, primary_key=True)
    train_name = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.Integer)  # foreign key
    dest = db.Column(db.Integer)  # foreign key
    seats_no = db.Column(db.Integer)


class Seats(db.Model):
    seat_no = db.Column(db.Integer, primary_key=True)
    availTA = db.Column(db.Integer)  # boolean
    availTB = db.Column(db.Integer)  # boolean
    availTC = db.Column(db.Integer)  # boolean


class Station(db.Model):
    station_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String, unique=True, nullable=False)
    TAarr = db.Column(db.Integer)  # boolean
    TBarr = db.Column(db.Integer)  # boolean
    TCarr = db.Column(db.Integer)  # boolean


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    mob_no = db.Column(db.Integer)

    def get_id(self):
        return (self.user_id)


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)  # foreign key
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    b_point = db.Column(db.String)
    d_point = db.Column(db.String)
    seat_no = db.Column(db.Integer)  # foreign key
    fare = db.Column(db.Integer)


class FoodOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)  # foreign key
    item = db.Column(db.String)
    category = db.Column(db.String)
    qty = db.Column(db.String)
    price = db.Column(db.Integer)
    train_id = db.Column(db.Integer)  # foreign key
    station_name = db.Column(db.String)  # foreign key


# db.create_all()  # need to call initially only once to create tables


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def dashboard():
    if not current_user:
        return render_template('landing.html')

    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email_id']
        password = request.form.get('pass')
        # print(password)
        user = db.session.query(User).filter(
            User.email == email, User.password == password).first()
        if user:
            login_user(user, remember=False)
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong password or email id')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email_id']
        password = request.form.get('pass')
        user = db.session.query(User).filter(
            User.email == email).first()
        if user:
            flash('email id already exists. Try again')
            return render_template('register.html')
        else:
            new_user = User(user_name=user_name,
                            email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route('/book', methods=['POST', 'GET'])
def book_tickets():
    if request.method == 'POST':
        trains = ['TA', 'TB', 'TC']
        avail_trains = []
        start = request.form['start']
        end = request.form['end']

        for train in trains:
            Tavail = db.session.query(Station).all()
            if train == 'TA':
                if Tavail[int(start)-1].TAarr and Tavail[int(end)-1].TAarr:
                    avail_trains.append('TA')
            elif train == 'TB':
                if Tavail[int(start)-1].TAarr and Tavail[int(end)-1].TBarr:
                    avail_trains.append('TB')
            else:
                if Tavail[int(start)-1].TAarr and Tavail[int(end)-1].TCarr:
                    avail_trains.append('TC')

        # print(avail_trains)
        avail = []
        for train in avail_trains:
            savail = db.session.query(Train).filter(
                Train.train_name == train).first()
            # list of available seats in the required trains
            avail.append(savail)
        return render_template('train_list.html', trains=avail_trains, avail=avail)
    else:
        stations = db.session.query(Station).all()
        return render_template('book_tickets.html', stations=stations)


@app.route('/book/<string:train_name>', methods=['POST', 'GET'])
def view_train(train_name):
    if request.method == 'POST':
        pass_no = request.form['passengers']
        # print(pass_no)
        seats = db.session.query(Seats).all()
        avail_seats = []
        if train_name == 'TA':
            for seat in seats:
                avail_seats.append(seat.availTA)
        elif train_name == 'TB':
            for seat in seats:
                avail_seats.append(seat.availTB)
        else:
            for seat in seats:
                avail_seats.append(seat.availTC)
        return render_template('view_train.html', seats=avail_seats, train_name=train_name, pass_no=int(pass_no))
    return 'view get'


@app.route('/book/<string:train_name>/booking', methods=['POST'])
def book_train(train_name):
    if request.method == 'POST':
        need = request.form.getlist('seat_book')
        names = request.form.getlist('Name')
        # print(names)
        tot_avail_seats = db.session.query(Train).filter(
            Train.train_name == train_name).first()
        tot_avail_seats.seats_no = tot_avail_seats.seats_no - \
            len(need)  # train booking
        # print(tot_avail_seats.seats_no)

        for name in names:
            ticket = Ticket(user_id=current_user.user_id,
                            name=name)  # ticket booking
            db.session.add(ticket)
            # print(ticket)
        seats = db.session.query(Seats).all()
        if train_name == 'TA':
            for seat in seats:
                if str(seat.seat_no) in need:
                    seat.availTA = 0
        elif train_name == 'TB':
            for seat in seats:
                if str(seat.seat_no) in need:
                    seat.availTB = 0
        else:
            for seat in seats:
                if str(seat.seat_no) in need:
                    seat.availTC = 0
        db.session.commit()
        return redirect(url_for('order_food'))


@app.route('/food', methods=['POST', 'GET'])
def order_food():
    # if request.method == 'POST':
    # return render_template('food_booking.html')

    return render_template('food_booking.html')


@app.route('/cancel', methods=['POST', 'GET'])
def cancel_tickets():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    else:
        return render_template('cancel_tickets.html')


@app.route('/profile', methods=['GET'])
def profile():
    # print(cur_user)
    return render_template('profile.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, port=8080)
