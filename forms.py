from wtforms import Form, StringField, TextAreaField, DateField, TimeField, EnumField

class ListaForm(Form):
    titulo = StringField('Título')

class TarefaForm(Form):
    titulo = StringField('Título')
    data = DateField('Data')
    hora = TimeField('Hora')
    prioridade = EnumField('Prioridade', choices=[('Sem prioridade', 'Sem prioridade'), ('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')])
    descricao = TextAreaField('Descrição')
