from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "best-one-secret"

orders = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form.get('name')
    upi = request.form.get('upi')
    total = request.form.get('total')
    orders.append({'name': name, 'upi': upi, 'total': total, 'status': 'Pending', 'items': []})
    return render_template('order.html', name=name)

# --- ADMIN PART ---

@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == 'admin123':
            session['is_admin'] = True
            return redirect('/admin')
        else:
            return "Galat Password! <a href='/admin-login'>Wapas Jao</a>"
    return '''
    <h2>Admin Login</h2>
    <form method="POST">
        Password: <input type="password" name="password">
        <button>Login</button>
    </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect('/admin-login')
    return render_template('admin.html', orders=orders)

@app.route('/approve/<int:i>')
def approve(i):
    if not session.get('is_admin'):
        return redirect('/admin-login')
    orders[i]['status'] = 'Approved'
    return redirect('/admin')

@app.route('/delete/<int:i>')
def delete(i):
    if not session.get('is_admin'):
        return redirect('/admin-login')
    orders.pop(i)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
