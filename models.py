from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Time, Enum
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
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)  
    prioridade = Column(Enum('Sem prioridade', 'Baixa', 'Média', 'Alta'), nullable=True, default='Sem prioridade')
    descricao = Column(Text)

    concluida = Column(Integer, default=False)

    lista_id = Column(Integer, ForeignKey('listas.id'))
    lista = relationship('Lista', back_populates='tarefas')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data': self.data.strftime('%Y-%m-%d'),
            'hora': self.hora.strftime('%H:%M'),
            'prioridade': self.prioridade,
            'descricao': self.descricao,
            'concluida': self.concluida
        }
