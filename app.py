from flask import Flask, render_template, request
from pymongo import MongoClient
import time

#from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://jjames71396:qUFaF5pYhmjxAxPD@cluster0.ldooqi5.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

client.db.command("dropDatabase")

db = client['game_db']
collection = db['game_states']

players = {}


#document = {'name': 'game_state','started': False,'p1': '','p2': '','question': '', 'p1s': 0, 'p2s': 0}
#inserted_document = collection.update_one({'name':'game_state'},{'$set': document})

@app.route('/')
def index():
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    # Retrieve the game state from the database
    turn = None
    cur_player = None
    p = players
    start = False
    if game_state["question"] == '':
        question = None
    else:
        question = game_state['question']
  
            
        
    # Render the template with the game state and player names
    return render_template('index.html', question=question, time=str(time.time()), game_state=game_state)

@app.route('/answer', methods=['POST'])
def answer():
    query = {"name": "game_state"} 
    document = {'name': 'game_state','started': False,'p1': '','p2': '','question': '', 'p1s': 0, 'p2s': 0}
    answer = request.form['name']
    pl = int(request.form['pile1'])
    if pl == 1:
        collection.update_one(query, {'$set': {'p1': answer, 'p1t': str(time.time())}})
    elif pl == 2:
        collection.update_one(query, {'$set': {'p2': answer, 'p2t': str(time.time())}})

    return index()

@app.route('/start', methods=['POST'])
def start():
    global players
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    # Retrieve the game parameters from the form
    question = request.form['name']
    p1 = int(request.form['pile1'])
    p2 = int(request.form['pile2'])
    players = {
        1: p1,
        2: p2
    }

    # Save the initial game state to the database
    collection.update_one(query, {'$set': {'question': question, 'p1s': p1, 'p2s': p2, 'started': True}})
    # Redirect back to the index page
    return index()


if __name__ == '__main__':
    app.run(debug=True)