from wtforms import Form, StringField, TextAreaField, DateField, TimeField

class ListaForm(Form):
    titulo = StringField('Título')

class TarefaForm(Form):
    titulo = StringField('Título')
    data = DateField('Data')
    hora = TimeField('Hora')
    descricao = TextAreaField('Descrição')