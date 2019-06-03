from flask import Flask
import optical

app = Flask(__name__)

## Registrar los controladores en la instancia de Flask
app.register_blueprint(optical.mod)

if __name__ == "__main__":

    app.run()