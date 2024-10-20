from wtforms import Form, StringField, TextAreaField

class ListaForm(Form):
    titulo = StringField('Título')

class TarefaForm(Form):
    titulo = StringField('Título')
    data = StringField('Data')
    hora = StringField('Hora')
    descricao = TextAreaField('Descrição')