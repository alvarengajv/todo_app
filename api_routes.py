from flask import Blueprint, jsonify, request
from models import Lista, Tarefa
from database import db_session
from datetime import datetime

api_bp = Blueprint('api', __name__)

#---------------------------------------------- Rotas da API para Listas ------------------------------------------
@api_bp.route('/listas', methods=['GET'])
def get_listas():
    listas = db_session.query(Lista).all()
    return jsonify([lista.to_dict() for lista in listas])

@api_bp.route('/listas', methods=['POST'])
def api_add_lista():
    data = request.get_json()
    titulo = data.get('titulo')
    
    if not titulo:
        return jsonify({'error': 'O título da lista é obrigatório!'}), 400

    lista = Lista(titulo=titulo)
    db_session.add(lista)
    db_session.commit()

    return jsonify(lista.to_dict()), 201

@api_bp.route('/listas/<int:id>', methods=['PUT'])
def update_lista(id):
    lista = db_session.query(Lista).get(id)
    if lista:
        data = request.get_json()
        lista.titulo = data['titulo']
        db_session.commit()
        return jsonify(lista.to_dict())
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/listas/<int:id>', methods=['DELETE'])
def delete_lista(id):
    lista = db_session.query(Lista).get(id)
    if lista:
        db_session.delete(lista)
        db_session.commit()
        return jsonify({'message': 'Lista removida com sucesso'})
    return jsonify({'error': 'Lista não encontrada'}), 404




#---------------------------------------------- Rotas da API para Tarefas ------------------------------------------
@api_bp.route('/listas/<int:id_lista>/tarefas', methods=['GET'])
def get_tarefas(id_lista):
    lista = db_session.query(Lista).get(id_lista)
    if lista:
        return jsonify([tarefa.to_dict() for tarefa in lista.tarefas])
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/listas/<int:id_lista>/tarefas', methods=['POST'])
def add_tarefa(id_lista):
    lista = db_session.query(Lista).get(id_lista)
    if lista:
        data = request.get_json()

        data_formatada = datetime.strptime(data['data'], '%Y-%m-%d').date()

        hora_formatada = datetime.strptime(data['hora'], '%H:%M').time()

        tarefa = Tarefa(
            titulo=data['titulo'],
            data=data_formatada,  
            hora=hora_formatada,  
            descricao=data['descricao'],
            lista=lista
        )

        db_session.add(tarefa)
        db_session.commit()
        return jsonify(tarefa.to_dict()), 201

    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/listas/<int:id_lista>/tarefas/<int:id_tarefa>', methods=['PUT'])
def edit_tarefa(id_lista, id_tarefa):
    tarefa = db_session.query(Tarefa).filter_by(id=id_tarefa, lista_id=id_lista).first()
    if not tarefa:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    data = request.get_json()
    tarefa.titulo = data.get('titulo', tarefa.titulo)
    tarefa.data = datetime.strptime(data.get('data'), '%Y-%m-%d').date()
    tarefa.hora = datetime.strptime(data.get('hora'), '%H:%M').time()
    tarefa.descricao = data.get('descricao', tarefa.descricao)
    db_session.commit()

    return jsonify({'success': True, 'tarefa': tarefa.to_dict()}), 200

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
