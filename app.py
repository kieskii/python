from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, EditForm, DeleteForm # Assumindo que você já tem um formulário de login configurado

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'  # Use SQLite para simplicidade
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

@app.route('/results')
def results():
    users = User.query.all()
    return render_template('results.html', users=users)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.password = form.password.data
        db.session.commit()
        return redirect(url_for('results'))
    return render_template('edit_user.html', form=form, user=user)


@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('results'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados dentro do contexto da aplicação
    app.run(debug=True)
