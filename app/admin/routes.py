from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from . import admin_bp
from app.security import login_required, role_required
from data import posts, usuarios


# ========== AUTENTICAÇÃO ==========

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('usuario', '')
        senha = request.form.get('senha', '')
        user = usuarios.get(nome)

        # Compara o hash; mensagem genérica para não revelar o que errou
        if user and check_password_hash(user['senha_hash'], senha):
            session.clear()                      # evita session fixation
            session['usuario'] = nome
            session['papel'] = user['papel']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Usuário ou senha inválidos.', 'error')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Sessão encerrada.', 'success')
    return redirect(url_for('blog.index'))

# ========== CRUD PROTEGIDO ==========

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html', posts=posts)

@admin_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        conteudo = request.form.get('conteudo', '').strip()

        # Validação de entrada no servidor (nunca confie só no HTML)
        if not titulo or not conteudo:
            flash('Título e conteúdo são obrigatórios.', 'error')
            return render_template('admin/new_post.html')

        novo_id = max([p['id'] for p in posts], default=0) + 1
        posts.append({
            'id': novo_id,
            'titulo': titulo,
            'conteudo': conteudo,
            'autor': session['usuario']
        })
        flash('Postagem criada com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/new_post.html')

@admin_bp.route('/editar/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        flash('Postagem não encontrada.', 'error')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        post['titulo'] = request.form.get('titulo', '').strip()
        post['conteudo'] = request.form.get('conteudo', '').strip()
        flash('Postagem atualizada!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_post.html', post=post)

@admin_bp.route('/deletar/<int:post_id>', methods=['POST'])
@role_required('admin')      # Apenas administradores podem deletar
def deletar_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    flash('Postagem deletada.', 'success')
    return redirect(url_for('admin.dashboard'))