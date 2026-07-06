from flask import Flask


def create_app() -> Flask:

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def hello():
        return {"message": "Welcome to the PlaceHub API!"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
