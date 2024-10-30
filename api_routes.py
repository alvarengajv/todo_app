from flask import Blueprint, jsonify, request
from models import Lista, Tarefa
from database import db_session
from datetime import datetime
from sqlalchemy.exc import IntegrityError

api_bp = Blueprint('api', __name__)


#---------------------------------------------- Rotas da API para Listas ------------------------------------------
@api_bp.route('/listas', methods=['GET'])
def get_listas():
    listas = db_session.query(Lista).all()
    return jsonify([lista.to_dict() for lista in listas])

@api_bp.route('/listas', methods=['POST'])
def add_lista():
    data = request.get_json()
    titulo = data.get('titulo')
    
    if not titulo or titulo.strip() == "":
        return jsonify({'error': 'O título da lista é obrigatório!'}), 400
    
    lista = Lista(titulo=titulo.strip())

    try:
        db_session.add(lista)
        db_session.commit()
        return jsonify(lista.to_dict()), 201
    
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Erro ao adicionar a lista ao banco de dados.'}), 500

@api_bp.route('/listas/<int:id>', methods=['PUT'])
def update_lista(id):
    lista = db_session.query(Lista).get(id)
    if not lista:
        return jsonify({'error': 'Lista não encontrada'}), 404

    data = request.get_json()
    titulo = data.get('titulo')

    if not titulo or titulo.strip() == "":
        return jsonify({'error': 'O título da lista é obrigatório!'}), 400
    
    lista = Lista(titulo=titulo.strip())
    
    try:
        db_session.commit()
        return jsonify(lista.to_dict())
    
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Erro ao atualizar a lista no banco de dados.'}), 500

@api_bp.route('/listas/<int:id>', methods=['DELETE'])
def delete_lista(id):
    lista = db_session.query(Lista).get(id)
    if lista:
        db_session.delete(lista)
        db_session.commit()
        return jsonify({'message': 'Lista removida com sucesso'})
    return jsonify({'error': 'Lista não encontrada'}), 404


#---------------------------------------------- Rotas API para Tarefas ------------------------------------------
@api_bp.route('/listas/<int:id_lista>/tarefas', methods=['GET'])
def get_tarefas(id_lista):
    lista = db_session.query(Lista).get(id_lista)

    if lista:
        return jsonify([tarefa.to_dict() for tarefa in lista.tarefas])
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/listas/<int:id_lista>/tarefas', methods=['POST'])
def add_tarefa(id_lista):
    lista = db_session.query(Lista).get(id_lista)

    if not lista:
        return jsonify({'error': 'Lista não encontrada'}), 404

    data = request.get_json()

    titulo = data.get('titulo')
    data_str = data.get('data')
    hora_str = data.get('hora')
    prioridade = data.get('prioridade', 'Sem prioridade')
    descricao = data.get('descricao', '')

    if not titulo or titulo.strip() == "":
        return jsonify({'error': 'O título da lista é obrigatório!'}), 400
    
    if not data_str or not hora_str:
        return jsonify({'error': 'Data e hora são obrigatórias.'}), 400

    try:
        data_formatada = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora_formatada = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Formato de data ou hora inválido.'}), 400

    if prioridade not in ['Sem prioridade', 'Baixa', 'Média', 'Alta']:
        return jsonify({'error': 'Prioridade inválida. Escolha entre: Sem prioridade, Baixa, Média, Alta.'}), 400

    tarefa = Tarefa(
        titulo=titulo,
        data=data_formatada,
        hora=hora_formatada,
        prioridade=prioridade,
        descricao=descricao,
        lista=lista
    )

    try:
        db_session.add(tarefa)
        db_session.commit()
        return jsonify(tarefa.to_dict()), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Erro ao criar a tarefa.'}), 500

@api_bp.route('/listas/<int:id_lista>/tarefas/<int:id_tarefa>', methods=['PUT'])
def edit_tarefa(id_lista, id_tarefa):
    tarefa = db_session.query(Tarefa).filter_by(id=id_tarefa, lista_id=id_lista).first()

    if not tarefa:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    lista = db_session.query(Lista).get(id_lista)
    if not lista:
        return jsonify({'error': 'Lista não encontrada'}), 404

    data = request.get_json()

    titulo = data.get('titulo', tarefa.titulo)
    data_str = data.get('data')
    hora_str = data.get('hora')
    prioridade = data.get('prioridade', tarefa.prioridade)
    descricao = data.get('descricao', tarefa.descricao)
    nova_lista_id = data.get('lista_id', id_lista)

    if not titulo or titulo.strip() == "":
        return jsonify({'error': 'O título da lista é obrigatório!'}), 400
    
    if not data_str or not hora_str:
        return jsonify({'error': 'Data e hora são obrigatórias.'}), 400

    try:
        data_formatada = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora_formatada = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Formato de data ou hora inválido.'}), 400

    if prioridade not in ['Sem prioridade', 'Baixa', 'Média', 'Alta']:
        return jsonify({'error': 'Prioridade inválida. Escolha entre: Sem prioridade, Baixa, Média, Alta.'}), 400

    tarefa.titulo = titulo
    tarefa.data = data_formatada
    tarefa.hora = hora_formatada
    tarefa.prioridade = prioridade
    tarefa.descricao = descricao

    if nova_lista_id != id_lista:
        nova_lista = db_session.query(Lista).get(nova_lista_id)
        if not nova_lista:
            return jsonify({'error': 'Nova lista não encontrada.'}), 404
        tarefa.lista = nova_lista

    try:
        db_session.commit()
        return jsonify({'success': True, 'tarefa': tarefa.to_dict()}), 200
    except IntegrityError:
        db_session.rollback()
        return jsonify({'error': 'Erro ao atualizar a tarefa.'}), 500

@api_bp.route('/listas/<int:id_lista>/tarefas/<int:id_tarefa>/concluir', methods=['PUT'])
def concluir_tarefa(id_lista, id_tarefa):
    tarefa = db_session.query(Tarefa).get(id_tarefa)
    if tarefa:
        data = request.get_json()
        tarefa.concluida = 1 if data['concluida'] else 0  
        db_session.commit()  
        return jsonify(tarefa.to_dict())  
    return jsonify({'error': 'Tarefa não encontrada'}), 404

@api_bp.route('/listas/<int:id_lista>/tarefas/<int:id_tarefa>', methods=['DELETE'])
def delete_tarefa(id_lista, id_tarefa):
    tarefa = db_session.query(Tarefa).filter_by(id=id_tarefa, lista_id=id_lista).first()
    if tarefa:
        db_session.delete(tarefa)
        db_session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Tarefa não encontrada'}), 404
