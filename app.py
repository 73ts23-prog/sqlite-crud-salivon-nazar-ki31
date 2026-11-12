from flask import Flask,render_template,request,redirect,url_for,abort
import database_connector as db
app=Flask(__name__)
db.create_db_table()
@app.get('/')
def index():
    return render_template('index.html',books=db.get_all_items())
def form_data():
    values=tuple(request.form.get(k,'').strip() for k in ('title','author','year','genre','status'))
    if any(not x for x in values):
        abort(400,'Заповніть усі поля')
    try:
        year=int(values[2])
    except ValueError:
        abort(400,'Рік має бути числом')
    if not 1450<=year<=2100:
        abort(400,'Рік має бути від 1450 до 2100')
    return values[:2]+(year,)+values[3:]
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        db.insert_item(form_data())
        return redirect(url_for('index'))
    return render_template('form.html',book=None)
@app.route('/edit/<int:item_id>',methods=['GET','POST'])
def edit(item_id):
    book=db.get_item_by_id(item_id)
    if book is None:abort(404)
    if request.method=='POST':
        db.update_item(item_id,form_data())
        return redirect(url_for('index'))
    return render_template('form.html',book=book)
@app.post('/delete/<int:item_id>')
def delete(item_id):
    if not db.delete_item(item_id):abort(404)
    return redirect(url_for('index'))
if __name__=='__main__':app.run(host='127.0.0.1',port=5087,debug=False)
