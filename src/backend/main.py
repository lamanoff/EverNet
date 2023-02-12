from services.hidden_service import HiddenService
from services.tor_bundle import TorBundle
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello, world!</h1>'


if __name__ == '__main__':
    tor_bundle = TorBundle()
    tor_bundle.start('tor', 9011, 9050)
    hidden_service = HiddenService()
    hidden_service.start('Test', '127.0.0.1', 9011, {80: 5001})
    print(hidden_service.get_address())
    app.run(host='0.0.0.0', port=5001)
    
