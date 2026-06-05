from werkzeug.security import generate_password_hash

# "Banco de dados" de usuários em memória
# A senha NUNCA é guardada em texto puro — apenas o hash.
usuarios = {
    'admin': {
        'senha_hash': generate_password_hash('admin123'),
        'papel': 'admin'      # pode tudo
    },
    'editor': {
        'senha_hash': generate_password_hash('editor123'),
        'papel': 'editor'     # pode criar/editar, mas não deletar
    }
}







posts = [
    {'id': 1, 'titulo': 'Primeiro Post', 'conteudo': 'Conteúdo do primeiro post.', 'autor': 'admin'},
    {'id': 2, 'titulo': 'Segundo Post', 'conteudo': 'Conteúdo do segundo post.', 'autor': 'editor'},
    {'id': 3, 'titulo': 'Terceiro Post', 'conteudo': 'Conteúdo do terceiro post.', 'autor': 'admin'}
]