from flask import Flask, render_template, request, redirect
from database import DatabaseAPI

app = Flask(__name__)

@app.route('/')
def produtos():
    db = DatabaseAPI()
    produtos = db.get_produtos()
    return render_template('produtos.html', produtos=produtos)

@app.route('/cadastrar', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        validade = request.form['validade']
        db = DatabaseAPI()
        db.create_produto(nome, quantidade, preco, validade)
        return redirect('/')
    
@app.route('/deletar/<int:id>')
def deletar(id):
    db = DatabaseAPI()
    db.delete_produto(id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)