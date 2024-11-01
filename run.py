from saldozen import app, db, ExpenseType

def create_initial_expense_types():
    expense_types = ['Alimentação', 'Transporte', 'Lazer', 'Saúde', 'Moradia', 'Água', 'Enegia']
    for type_name in expense_types:
        if not ExpenseType.query.filter_by(name=type_name).first():
            expense_type = ExpenseType(name=type_name)
            db.session.add(expense_type)
    db.session.commit()

with app.app_context():
    db.create_all()
    create_initial_expense_types() 
# checks if the run.py file has executed directly and not imported
if __name__ == "__main__":
    app.run(debug=True)
