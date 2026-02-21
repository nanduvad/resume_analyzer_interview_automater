from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../dist')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

def error_response(message, status_code):
    return jsonify({'success': False, 'message': message, 'timestamp': datetime.utcnow().isoformat()}), status_code

# JWT error handlers - return clean JSON instead of 422/401 defaults
@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return error_response('Invalid token: ' + error_string, 401)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return error_response('Token has expired', 401)

@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return error_response('Authorization required: ' + error_string, 401)

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return error_response('Token has been revoked', 401)

# Import and register blueprints
try:
    from backend.routes.auth import auth_bp
    from backend.routes.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    print("✅ Auth and API routes registered")
except ImportError as e:
    print(f"⚠️  Could not import some routes: {e}")

# Try to import other routes if they exist
try:
    from backend.routes.candidates import candidates_bp
    app.register_blueprint(candidates_bp, url_prefix='/api/candidates')
except ImportError:
    pass

try:
    from backend.routes.jobs import jobs_bp
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
except ImportError:
    pass

try:
    from backend.routes.questions import questions_bp
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
except ImportError:
    pass

# Serve frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'TalentMatch API'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
