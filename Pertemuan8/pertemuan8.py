from flask import Flask, request

app = Flask(__name__)

@app.route("/hello")
def index():
    return "Hello IBDA"

@app.route("/say-hello/<string:name>")
def sayHello(name):
    # name = request.args.get("name")
    age = request.args.get("age")
    res = {"message": f"tes Hello, {name} || usia: {age}"}
    return res

@app.route("/message", methods=['POST'])
def createMessage():
    data = request.get_json()

    #validation logic
    if data["id"] == 0:
        return {
            "status" : "ERROR",
            "message": "Invalid ID Message"
        }
    
    result = {
        "status": "OK",
        "data" : data
    }

    """
    masukan ini di postman
    {
    "id" : 2,
    "message" : "apa itu"
    }
    """

    return result

if __name__ == "__main__":
    app.run()