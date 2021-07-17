from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
from paypalhttp import HttpError
import re
import os
import json
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toton_007@127.0.0.1/missibot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email_verify = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"username:{self.username}, email:{self.email}, phone:{self.phone}," \
               f" email_verify:{self.email_verify}  "


@app.route("/")
def home():
    user = User.query.all()
    print(user)
    return render_template(template_name_or_list="home.html", session=session)


@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        password = data['password']
        phone = data['phone']
        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        email = data['email']
        if re.match(regex, email) is not None:
            print("match")
            if len(phone) == 10:
                print(len(phone))
                try:
                    hashed_pass = generate_password_hash(password)
                    user = User(username=data['username'], email=data['email'],
                                phone=phone, password=hashed_pass)
                    db.session.add(user)
                    db.session.commit()
                    found_user = User.query.filter_by(
                        email=data["email"]).first()
                    user = {
                        "username": found_user.username,
                        "email": found_user.email,
                        "phone": found_user.phone,
                        "email_verify": found_user.email_verify
                    }
                    json_data = json.dumps(user, indent=4)
                    return jsonify({"user": json_data})
                except Exception as e:
                    if "Duplicate entry" in e.args[0]:
                        print(e.args[0].split(' ')[4])
                        duplicate = e.args[0].split(' ')[4]
                        return jsonify({"duplicate": duplicate})
                    else:
                        print(e)
            else:
                err = "Please enter 10 digit phone no."
                return jsonify(err)
        else:
            print("not match")
            return jsonify("PLease enter a valid email")
    else:
        return render_template(template_name_or_list="registration.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        # print(data['email'], data['password'])
        password = data['password']
        found_user = User.query.filter_by(email=data["email"]).first()
        if found_user:
            if check_password_hash(found_user.password, password):
                print('pass matched')
                if not found_user.email_verify:
                    return jsonify({"not_email": "Email not verified"})
                else:
                    session['email'] = data['email']
                    return jsonify({"email": "Email has verified"})
            else:
                print('pass not matched')
                return jsonify({"not_pass": "Password didn't match"})
        else:
            print('not found')
            return jsonify({"not_user": "User not found"})
    else:
        return render_template(template_name_or_list="login.html")


@app.route("/verify_email", methods=["GET", "POST"])
def verify_email():
    if request.method == "POST":
        data = request.get_json()
        # print(data['email'])
        found_user = User.query.filter_by(email=data["email"]).first()
        sender_mail = 'business.toton@gmail.com'
        receivers_mail = [f"{data['email']}"]
        print(found_user)
        if found_user:
            if not found_user.email_verify:
                try:
                    msg = Message('Verify Your Email', sender=sender_mail,
                                  recipients=receivers_mail)
                    msg.html = """<h3>Thank You !</h3> <strong>Your email has been verified.</strong>
                        <a href="http://localhost:8000/">Go back</a>"""
                    mail.send(msg)
                    found_user.email_verify = True
                    db.session.commit()
                    user = {
                        "username": found_user.username,
                        "email": found_user.email,
                        "phone": found_user.phone,
                        "email_verify": found_user.email_verify
                    }
                    json_data = json.dumps(user, indent=4)
                    return jsonify({"email_sent": "mail sent", "user": json_data})
                except Exception as e:
                    print(e)
                    return jsonify({"err": "Can't sent mail"})
            else:
                return jsonify({"email": "Email has verified"})
        else:
            print('not found')
            return jsonify({"not_user": "User not found"})
    else:
        return render_template(template_name_or_list="verify_email.html")


@app.route("/forgot_pass", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        data = request.get_json()
        print(data['email'])
        found_user = User.query.filter_by(email=data["email"]).first()
        sender_mail = 'business.toton@gmail.com'
        receivers_mail = [f"{data['email']}"]

        if found_user:
            print("user match")
            try:
                msg = Message('Chang Password', sender=sender_mail,
                              recipients=receivers_mail)
                msg.html = f"<h3>Don't worry</h3>" \
                           f"<strong>We will generate a new password for you</strong>" \
                           f"<a href='http://localhost:8000/change_pass/{found_user.id}'>Click here to change " \
                           f"password</a> "
                mail.send(msg)
                return jsonify({"email_sent": "mail sent"})
            except Exception as e:
                print(e)
                return jsonify("can't sent email")
        else:
            print("user not found")
            return jsonify({"not_user": "User not found"})
    else:
        return render_template(template_name_or_list="forgot_pass.html")


@app.route("/change_pass/<user_id>", methods=["GET", "POST"])
def change_password(user_id):
    print(user_id)
    found_user = User.query.filter_by(id=user_id).first()
    print(found_user)
    if request.method == "POST":
        data = request.get_json()
        password = data['password']
        hashed_pass = generate_password_hash(password)
        found_user.password = hashed_pass
        db.session.commit()
        return jsonify({"msg": "Password has successfully changed"})
    else:
        return render_template(template_name_or_list="change_pass.html", user_id=user_id)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST" and session.get("email") is not None:
        session.pop("email", None)
        return jsonify("Successfully logged out")


class CreateOrder(PayPalClient):

    def create_order(self, debug=False):
        req = OrdersCreateRequest()
        req.prefer('return=representation')
        # 3. Call PayPal to set up a transaction
        req.request_body(self.build_request_body())
        response = self.client.execute(req)
        if debug:
            print('Order With Complete Payload:')
            print('Status Code:', response.status_code)
            print('Status:', response.result.status)
            print('Order ID:', response.result.id)
            print('Intent:', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(
                    link.rel, link.href, link.method))
                print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code,
                                                   response.result.purchase_units[0].amount.value))
                # If call returns body in response, you can get the deserialized version from the result attribute of
                # the response
            order = response.result
            print(order)
        return response

    @staticmethod
    def build_request_body():
        """Method to create body with CAPTURE intent"""
        return \
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": "100.00"
                        }
                    }
                ]
            }


class CaptureOrder(PayPalClient):

    def capture_order(self, order_id, debug=False):
        """Method to authorize order using order_id"""
        req = OrdersCaptureRequest(order_id)
        req.prefer("return=representation")
        # 3. Call PayPal to authorize an order
        req.request_body(self.build_request_body())
        response = self.client.execute(req)
        # 4. Save the authorization ID to your database. Implement logic to save authorization to your database for
        # future reference.
        if debug:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Authorization ID:',
                  response.result.purchase_units[0].payments.authorizations[0].id)
            print('Links:')
            for link in response.result.links:
                print(('\t{}: {}\tCall Type: {}'
                      .format(link.rel, link.href, link.method)))
            print('Authorization Links:')
            for link in response.result.purchase_units[0].payments.authorizations[0].links:
                print(('\t{}: {}\tCall Type: {}'
                      .format(link.rel, link.href, link.method)))
            print("Buyer:")
            print(("\tEmail Address: {}\n\tPhone Number: {}"
                   .format(response.result.payer.email_address,
                           response.result.payer.phone.phone_number.national_number)))
            # json_data = self.object_to_json(response.result)
            # print("json_data: ", json.dumps(json_data, indent=4))
        return response

    @staticmethod
    def build_request_body():
        return \
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": "100.00"
                        }
                    }
                ]
            }


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        try:
            response_data = CreateOrder().create_order(debug=True)
            # print("id", response_data.result.id)
            order_id = response_data.result.id
            return jsonify({"order_id": order_id})
        except IOError as ioe:
            print(ioe)
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)
    else:
        return render_template(template_name_or_list="payment.html")


@app.route("/execute_payment", methods=["POST"])
def capture_payment():
    data = request.get_json()
    print(data["orderID"])
    complete_order = CaptureOrder().capture_order(
        order_id=data["orderID"], debug=True)
    order_id = complete_order.result.id
    return jsonify({"id": order_id})


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000, use_reloader=False)
