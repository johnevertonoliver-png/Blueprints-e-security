Para executar o exemplo de blueprint:
1. Git clone : repositório
2. cd repositório 
3. criar e ativar uma venv
4. criar uma .env a partir da .env.example, e colocar uma senha local (arquivos que o .gitignore ignorou)


MEDIDAS DE SEGURANÇA DA ATIVIDADE:

1. Isolamento da secret key, em vez de escrever senhas direto no código do Flask (como app.config['SECRET_KEY'] = 'senha123'), usar o arquivo .env.
2. Vazamento de senhas, não salvar as senhas dos usuarios em textos puro, utilizando a extenção werkzeug.security, para guardar as senhas como hashs
3. Anti-CSRF, quando a requisição for POST, validar o token único da sessão, para garantir que a requisição veio do próprio site e não de um hacker.
4. O uso do cookie HttpOnly, onde cookies de sessão são protegidos contra leitura via JavaScript e configurados para trafegar apenas em conexões seguras.
5. session.clear() no login, evita que um invasor "sequestre" a sessão de um usuário limpando completamente o identificador antigo da sessão no momento em que o login é efetuado.
6. @login_required (autenticação) e @role_required (autorização), Decorators que bloqueiam o acesso a páginas restritas (como criar ou deletar posts). A aplicação valida se o usuário está logado e se possui o nível de permissão correto.
