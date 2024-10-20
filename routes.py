from flask import jsonify, Blueprint, request
from models import Lista, Tarefa
from database import init_db

api_bp = Blueprint('api', __name__)

session = None

def init_api(app):
    global session
    session = init_db(app)

# ----------------------------------------------------- Listas ---------------------------------------------------------------------

@api_bp.route('/api/listas', methods=['GET'])
def get_listas():
    listas = session.query(Lista).all()
    return jsonify([lista.to_dict() for lista in listas])

@api_bp.route('/api/listas', methods=['POST'])
def add_lista():
    data = request.get_json()
    lista = Lista(titulo=data['titulo'])
    session.add(lista)
    session.commit()
    return jsonify(lista.to_dict()), 201

@api_bp.route('/api/listas/<int:id>', methods=['PUT'])
def update_lista(id):
    lista = session.query(Lista).get(id)
    if lista:
        data = request.get_json()
        lista.titulo = data['titulo']
        session.commit()
        return jsonify(lista.to_dict())
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/api/listas/<int:id>', methods=['DELETE'])
def delete_lista(id):
    lista = session.query(Lista).get(id)
    if lista:
        session.delete(lista)
        session.commit()
        return jsonify({'message': 'Lista removida com sucesso'})
    return jsonify({'error': 'Lista não encontrada'}), 404


# ----------------------------------------------------- Tarefas -----------------------------------------------------

@api_bp.route('/api/listas/<int:id>/tarefas', methods=['GET'])
def get_tarefas(id):
    lista = session.query(Lista).get(id)
    if lista:
        return jsonify([tarefa.to_dict() for tarefa in lista.tarefas])
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/api/listas/<int:id>/tarefas', methods=['POST'])
def add_tarefa(id):
    lista = session.query(Lista).get(id)
    if lista:
        data = request.get_json()
        tarefa = Tarefa (
        titulo=data['titulo'], 
        data=data['data'], 
        hora=data['hora'], 
        descricao=data['descricao'], 
        lista=lista)
        session.add(tarefa)
        session.commit()
        return jsonify(tarefa.to_dict()), 201
    return jsonify({'error': 'Lista não encontrada'}), 404

@api_bp.route('/api/listas/<int:id_lista>/tarefas/<int:id_tarefa>', methods=['PUT'])
def update_tarefa(id_lista, id_tarefa):
    tarefa = session.query(Tarefa).get(id_tarefa)
    if tarefa:
        data = request.get_json()
        tarefa.titulo = data['titulo']
        tarefa.data = data['data']
        tarefa.hora = data['hora']
        tarefa.descricao = data['descricao']
        session.commit()
        return jsonify(tarefa.to_dict())
    return jsonify({'error': 'Tarefa não encontrada'}), 404

@api_bp.route('/api/listas/<int:id_lista>/tarefas/<int:id_tarefa>', methods=['DELETE'])
def delete_tarefa(id_lista, id_tarefa):
    tarefa = session.query(Tarefa).get(id_tarefa)
    if tarefa:
        session.delete(tarefa)
        session.commit()
        return jsonify({'message': 'Tarefa removida com sucesso'})
    return jsonify({'error': 'Tarefa não encontrada'}), 404

