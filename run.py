import os

from app import create_app
from app.extensions import db
from app.models import Usuario, Transacao

app = create_app(os.environ.get("FLASK_CONFIG", "default"))

'''
@app.shell_context_processor
def make_shell_context():
    """Permite usar `flask shell` já com db, Usuario e Transacao importados."""
    return {"db": db, "Usuario": Usuario, "Transacao": Transacao}
'''

if __name__ == "__main__":
    app.run()
