import os

class Config:
    # Lê o segredo do ambiente; nunca deixe um valor fixo em produção
    SECRET_KEY = os.environ.get('SECRET_KEY', 'apenas-para-dev')
     # --- Segurança dos cookies de sessão ---
    SESSION_COOKIE_HTTPONLY = True    # JavaScript não acessa o cookie (mitiga XSS)
    SESSION_COOKIE_SAMESITE = 'Lax'   # Mitiga CSRF em navegações de terceiros
    SESSION_COOKIE_SECURE = False     # True em produção (HTTPS)

class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True      # Exige HTTPS para enviar o cookie

class DevelopmentConfig(Config):
    DEBUG = True