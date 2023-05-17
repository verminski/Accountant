from flask import Flask, render_template, request, redirect, url_for
from models import db, Products, Account, History, add_event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db.init_app(app)

@app.route('/')
def index():
    account = Account.query.first()
    if account is None:
        account = Account(balance=0)
        db.session.add(account)
        db.session.commit()
    products = Products.query.all()
    return render_template('index.html', saldo=account.balance, magazyn=products)

@app.route('/historia')
@app.route('/historia/<int:od>/<int:do>/')
def historia(od = None, do = None):
    history = History.query.all()
    if od is None and do is None:
        return render_template('historia.html', historia=History.query.all())
    elif od > do or od < 0 or do < 0 or do > len(history):
        return render_template('historia.html', historia=[], error=f'Nieprawidłowy zakres, dozwolone wartości: od 0 do {str(len(history) -1)}')
    else:
        return render_template('historia.html', historia=history[od:do])

@app.route('/saldo', methods=['GET', 'POST'])
def saldo():
    if request.method == 'POST':
        opcja_saldo = request.form['opcja_saldo']
        if opcja_saldo == 'dodaj':
            kwota = float(request.form['kwota'])
            account = Account.query.first()
            account.balance += kwota
            new_event = add_event('Saldo', f'Dodano {kwota} do salda. Stan po operacji: {account.balance}')
            db.session.add(account)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('index'))
        elif opcja_saldo == "odejmij":
            kwota = float(request.form['kwota'])
            account = Account.query.first()
            account.balance -= kwota
            new_event = add_event('Saldo', f'Odjęto {kwota} od salda. Stan po operacji: {account.balance}')
            db.session.add(account)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print("Błędna komenda. Wpisz 'dodaj' lub 'odejmij'.")

    account = Account.query.first()
    return render_template('saldo.html', saldo=account.balance)

@app.route('/zakup', methods=['GET', 'POST'])
def zakup():
    if request.method == 'POST':
        produkt = request.form['produkt']
        cena = float(request.form['cena'])
        ilosc = int(request.form['ilosc'])

        product = Products.query.filter_by(name=produkt).first()
        if product:
            return render_template('zakup.html', error="Produkt już istnieje w magazynie.")
        else:
            account = Account.query.first()
            if account.balance < cena * ilosc:
                return render_template('zakup.html', error="Niewystarczające środki na koncie.")
            new_product = Products(name=produkt, quantity=ilosc, price=cena)
            account.balance -= cena * ilosc
            new_event = add_event('Zakup', f'Kupiono {ilosc} sztuk {produkt} za {cena} PLN')
            db.session.add(new_product)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('zakup.html')

@app.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if request.method == 'POST':
        produkt = request.form['produkt']
        ilosc = int(request.form['ilosc'])

        product = Products.query.filter_by(name=produkt).first()
        if product:
            if product.quantity >= ilosc:
                cena = product.price
                product.quantity -= ilosc
                if product.quantity == 0:
                    db.session.delete(product)

                account = Account.query.first()
                account.balance += cena * ilosc

                new_event = add_event('Sprzedaż', f'Sprzedano {ilosc} sztuk {produkt} za {cena} PLN')
                db.session.add(account)
                db.session.add(new_event)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                return render_template('sprzedaz.html', error="Nie ma wystarczającej ilości produktu w magazynie.")
        else:
            return render_template('sprzedaz.html', error="Produkt nie istnieje w magazynie.")

    return render_template('sprzedaz.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)