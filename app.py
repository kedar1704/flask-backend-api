from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import logging
import os

# Initialize Flask app
app = Flask(__name__)

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  
                        logging.FileHandler('/var/logs/app.log')  
                    ])


db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'mysql')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(50), nullable=False)
    message_id = db.Column(db.String(50), nullable=False, unique=True)
    sender_number = db.Column(db.String(15), nullable=False)
    receiver_number = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "message_id": self.message_id,
            "sender_number": self.sender_number,
            "receiver_number": self.receiver_number
        }


@app.route('/create', methods=['POST'])
def create_message():
    try:
        data = request.get_json()
        new_message = Message(
            account_id=data['account_id'],
            message_id=str(uuid.uuid4()),
            sender_number=data['sender_number'],
            receiver_number=data['receiver_number']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify({"message": "Message created successfully"}), 201
    except Exception as e:
        logging.error(f"Error creating message: {str(e)}")
        return jsonify({"error": "Failed to create message"}), 500

@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    try:
        messages = Message.query.filter_by(account_id=account_id).all()
        return jsonify([message.to_dict() for message in messages]), 200
    except Exception as e:
        logging.error(f"Error retrieving messages for account {account_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve messages"}), 500

@app.route('/search', methods=['GET'])
def search_messages():
    try:
        message_ids = request.args.get('message_id', '').split(',')
        sender_numbers = request.args.get('sender_number', '').split(',')
        receiver_numbers = request.args.get('receiver_number', '').split(',')
        
        query = Message.query
        
        if message_ids and message_ids[0]:
            query = query.filter(Message.message_id.in_(message_ids))
        
        if sender_numbers and sender_numbers[0]:
            query = query.filter(Message.sender_number.in_(sender_numbers))
        
        if receiver_numbers and receiver_numbers[0]:
            query = query.filter(Message.receiver_number.in_(receiver_numbers))
        
        messages = query.all()
        return jsonify([message.to_dict() for message in messages]), 200
    except Exception as e:
        logging.error(f"Error searching messages: {str(e)}")
        return jsonify({"error": "Failed to search messages"}), 500

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()  
    app.run(host='0.0.0.0', port=5000)

