from ChatApp import create_app
from flask_wtf.csrf import CSRFProtect

app = create_app()
csrf = CSRFProtect(app)