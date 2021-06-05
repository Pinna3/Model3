from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.Text(30), nullable=False)

    def __repr__(self):
        return f'{self.id} {self.name}'


@app.route('/<int:id>', methods=['GET', 'POST'])
def index(id):
    contact = Contact.query.get_or_404(id)
    all_contacts = Contact.query.order_by(Contact.id).all()
    contacts_len = len(Contact.query.all())
    contacts_index = [i+1 for i in range(contacts_len)]
    contacts_zipped = zip(all_contacts, contacts_index)
    return render_template(
        'index.html',
        contact=contact,
        contacts=all_contacts,
        contacts_len=contacts_len,
        contacts_zipped=contacts_zipped
    )


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(f'/{contact.id}')
    else:
        return render_template('edit.html', contact=contact)


@app.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/1')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        contact_name = request.form['name']
        contact_email = request.form['email']
        new_contact = Contact(name=contact_name, email=contact_email)
        db.session.add(new_contact)
        db.session.commit()
        return redirect(f'/{new_contact.id}')
    else:
        return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)
