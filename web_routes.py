from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Lista, Tarefa
from database import db_session
from datetime import datetime

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/home')
def home():
    listas = db_session.query(Lista).all()
    return render_template('home.html', listas=listas)

@web_bp.route('/lista/<int:id>')
def lista(id):
    lista = db_session.query(Lista).get(id)
    tarefas = lista.tarefas
    return render_template('lista.html', lista=lista, tarefas=tarefas)

@web_bp.route('/lista/add', methods=['GET', 'POST'])
def add_lista():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        if titulo:
            nova_lista = Lista(titulo=titulo)
            db_session.add(nova_lista)
            db_session.commit()
            return redirect(url_for('web.home'))
        return "Erro: Título da lista não fornecido", 400
    return render_template('add_lista.html')

@web_bp.route('/lista/<int:id>/edit', methods=['GET', 'PUT'])
def edit_lista(id):
    lista = db_session.query(Lista).get(id)
    if not lista:
        return jsonify({'error': 'Lista não encontrada'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        titulo = data.get('titulo')

        if not titulo:
            return jsonify({'error': 'Título é obrigatório!'}), 400

        lista.titulo = titulo
        db_session.commit()

        return jsonify({'success': True, 'redirect': url_for('web.lista', id=id)})
    
    return render_template('edit_lista.html', lista=lista)

@web_bp.route('/lista/<int:id>/delete', methods=['DELETE'])
def delete_lista(id):
    lista = db_session.query(Lista).get(id)
    if lista:
        db_session.delete(lista)
        db_session.commit()
        
        return jsonify({'success': True, 'redirect': url_for('web.home')}), 200
    return jsonify({'error': 'Lista não encontrada'}), 404

@web_bp.route('/lista/<int:lista_id>/tarefa/add', methods=['GET', 'POST'])
def add_tarefa(lista_id):
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        data = request.form.get('data')
        hora = request.form.get('hora')
        descricao = request.form.get('descricao')

        if not titulo or not data or not hora:
            return "Erro: Título, Data e Hora são obrigatórios!", 400
        try:
            data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
            hora_formatada = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            return "Erro: Data ou Hora inválidos!", 400

        nova_tarefa = Tarefa(
            titulo=titulo,
            data=data_formatada,
            hora=hora_formatada,
            descricao=descricao,
            lista_id=lista_id
        )

        db_session.add(nova_tarefa)
        db_session.commit()

        return redirect(url_for('web.lista', id=lista_id))
    return render_template('add_tarefa.html', lista_id=lista_id)

@web_bp.route('/lista/<int:lista_id>/tarefa/<int:tarefa_id>/edit', methods=['GET', 'PUT'])
def edit_tarefa(lista_id, tarefa_id):
    tarefa = db_session.query(Tarefa).filter_by(id=tarefa_id, lista_id=lista_id).first()
    if not tarefa:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        data_tarefa = data.get('data')
        hora_tarefa = data.get('hora')

        if not data_tarefa or not hora_tarefa:
            return jsonify({'error': 'Data e hora são obrigatórios!'}), 400

        try:
            data_formatada = datetime.strptime(data_tarefa, '%Y-%m-%d').date()
            hora_formatada = datetime.strptime(hora_tarefa, '%H:%M').time()
        except ValueError:
            return jsonify({'error': 'Data ou Hora inválidos!'}), 400

        tarefa.titulo = titulo
        tarefa.data = data_formatada
        tarefa.hora = hora_formatada
        tarefa.descricao = descricao
        db_session.commit()

        return jsonify({'success': True, 'redirect': url_for('web.lista', id=lista_id)})

    return render_template('edit_tarefa.html', tarefa=tarefa, lista_id=lista_id)

@web_bp.route('/lista/<int:lista_id>/tarefa/<int:tarefa_id>/delete', methods=['DELETE'])
def delete_tarefa(lista_id, tarefa_id):
    tarefa = db_session.query(Tarefa).filter_by(id=tarefa_id, lista_id=lista_id).first()
    if tarefa:
        db_session.delete(tarefa)
        db_session.commit()
        return jsonify({'success': True, 'message': 'Tarefa deletada com sucesso'}), 200
    return jsonify({'error': 'Tarefa não encontrada'}), 404
