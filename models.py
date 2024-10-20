from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Lista(Base):
    __tablename__ = 'listas'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)

    tarefas = relationship('Tarefa', back_populates='lista')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tarefas': [tarefa.to_dict() for tarefa in self.tarefas]
        }

class Tarefa(Base):
    __tablename__ = 'tarefas'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    data = Column(String(10), nullable=False)  
    hora = Column(String(5), nullable=False)   
    descricao = Column(Text)

    lista_id = Column(Integer, ForeignKey('listas.id'))
    lista = relationship('Lista', back_populates='tarefas')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data': self.data,
            'hora': self.hora,
            'descricao': self.descricao
        }
