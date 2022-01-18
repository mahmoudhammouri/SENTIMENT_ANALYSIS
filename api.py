from flask import Flask, request
from flask_restful import Api, Resource
import text_classifier

app = Flask(__name__)
api = Api(app)


class TextClassification(Resource):
    def post(self):
        try:
            text = request.json['text']
            label, ratio = text_classifier.prediction(text=text)
            return {"LABEL": label,
                    "RATIO": ratio}
        except Exception as e:
            return {"ERROR": str(e)}


api.add_resource(TextClassification, '/api/textClassification')
if __name__ == '__main__':
    app.run()
