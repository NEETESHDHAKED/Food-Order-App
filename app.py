from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "best-one-secret"

orders = []

FOOD_PHOTOS = {
    'Pizza': '/static/pizza.jpg',
    'Burger': '/static/burger.jpg',
    'Maggie': '/static/maggie.jpg',
    'Coffee': '/static/coffee.jpg',
    'Dal Bati': '/static/dalbati.jpg',
    'DalBati': '/static/dalbati.jpg',
    'Paneer': '/static/paneer.jpg',
}

FOOD_PRICES = {
    'Pizza': 199,
    'Burger': 99,
    'Maggie': 49,
    'Coffee': 39,
    'Dal Bati': 129,
    'Paneer': 149,
}

@app.route('/')
def home():
    return render_template('index.html', food_photos=FOOD_PHOTOS, prices=FOOD_PRICES)

@app.route('/order', methods=['POST'])
def order():
    name = request.form.get('name') or "Customer"
    upi = request.form.get('upi') or ""
    # Fast + Daily dono pakad lo
    items = []
    items += request.form.getlist('items')
    items += request.form.getlist('fast_food')
    items += request.form.getlist('daily_food')
    # Duplicate hata do
    items = list(dict.fromkeys(items))

    total = 0
    for it in items:
        total += FOOD_PRICES.get(it, 0)

    fast_items = [x for x in items if x in ['Pizza','Burger','Maggie','Coffee']]
    daily_items = [x for x in items if x in ['Dal Bati','DalBati','Paneer']]

    orders.append({
        'name': name,
        'upi': upi,
        'total': total,
        'status': 'Pending',
        'items': items,
        'fast_food': fast_items,
        'daily_food': daily_items
    })
    return render_template('order.html', name=name, items=items, total=total, food_photos=FOOD_PHOTOS)

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
        Password: <input type="password" name="password" required>
        <button>Login</button>
    </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect('/admin-login')
    return render_template('admin.html', orders=orders, food_photos=FOOD_PHOTOS)

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

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
