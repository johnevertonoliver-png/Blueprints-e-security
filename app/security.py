import secrets
from functools import wraps
from flask import session, flash, redirect, url_for, abort, request

# ========== AUTENTICAÇÃO / AUTORIZAÇÃO ==========

def login_required(f):
    """Garante que há um usuário autenticado na sessão."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs) 
    return wrapper

def role_required(*papeis):
    """Garante que o usuário logado possui um dos papéis exigidos."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('admin.login'))
            if session.get('papel') not in papeis:
                abort(403)   # Acesso negado
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ========== PROTEÇÃO CSRF (token próprio) ==========

def gerar_csrf_token():
    """Cria (uma vez por sessão) um token aleatório e o devolve.
    Será exposto aos templates como a função csrf_token()."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

def validar_csrf():
    """Compara o token enviado no formulário com o guardado na sessão.
    Em caso de falha, aborta com 403."""
    enviado = request.form.get('csrf_token')
    esperado = session.get('_csrf_token')
    if not esperado or not enviado or not secrets.compare_digest(enviado, esperado):
        abort(403)