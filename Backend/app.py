from flask import Flask
from flask_cors import CORS
import optical
import procesado

app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "Hello!!"

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
## Registrar los controladores en la instancia de Flask
app.register_blueprint(optical.mod)
app.register_blueprint(procesado.mod)

if __name__ == "__main__":
    app.run(host="0.0.0.0")    
