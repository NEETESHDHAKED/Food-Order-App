from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "best-one-secret"

# --- DATA ---
FOOD_ITEMS = [
    {'id': 1, 'name': 'Pizza', 'price': 199, 'photo': '/static/pizza.jpg', 'category': 'Fast Food'},
    {'id': 2, 'name': 'Burger', 'price': 99, 'photo': '/static/burger.jpg', 'category': 'Fast Food'},
    {'id': 3, 'name': 'Maggie', 'price': 49, 'photo': '/static/maggie.jpg', 'category': 'Fast Food'},
    {'id': 4, 'name': 'Coffee', 'price': 39, 'photo': '/static/coffee.jpg', 'category': 'Fast Food'},
    {'id': 5, 'name': 'Dal Bati', 'price': 129, 'photo': '/static/dalbati.jpg', 'category': 'Daily Food'},
    {'id': 6, 'name': 'Paneer', 'price': 149, 'photo': '/static/paneer.jpg', 'category': 'Daily Food'},
]

users = {'mudit': '1234'}  # pehle se 1 user: mudit / 1234
orders = []
next_food_id = 7

# --- HOME / MENU ---
@app.route('/')
def home():
    return render_template('index.html', items=FOOD_ITEMS, cart=session.get('cart', []), user=session.get('user'))

@app.route('/add_to_cart/<int:fid>')
def add_to_cart(fid):
    cart = session.get('cart', [])
    cart.append(fid)
    session['cart'] = cart
    return redirect('/')

@app.route('/remove_from_cart/<int:fid>')
def remove_from_cart(fid):
    cart = session.get('cart', [])
    if fid in cart:
        cart.remove(fid)
    session['cart'] = cart
    return redirect('/cart')

@app.route('/cart')
def cart_page():
    cart_ids = session.get('cart', [])
    cart_items = [x for x in FOOD_ITEMS if x['id'] in cart_ids]
    # quantity ke liye count
    total = sum([x['price'] for x in cart_items])
    return render_template('cart.html', cart_items=cart_items, total=total, user=session.get('user'))

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if not session.get('user'):
        return redirect('/login')
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return redirect('/')
    cart_items = [x for x in FOOD_ITEMS if x['id'] in cart_ids]
    total = sum([x['price'] for x in cart_items])
    if request.method == 'POST':
        upi = request.form.get('upi')
        orders.append({'user': session.get('user'), 'name': session.get('user'), 'upi': upi, 'total': total, 'items': cart_items, 'status': 'Pending'})
        session['cart'] = []
        return render_template('order.html', name=session.get('user'), items=cart_items, total=total)
    return render_template('checkout.html', cart_items=cart_items, total=total)

# --- USER LOGIN / REGISTER ---
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u in users:
            return "User pehle se hai! <a href='/login'>Login Karo</a>"
        users[u] = p
        session['user'] = u
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if users.get(u) == p:
            session['user'] = u
            return redirect('/')
        else:
            return "Galat Username/Password! <a href='/login'>Wapas</a>"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    return redirect('/')

@app.route('/history')
def history():
    if not session.get('user'):
        return redirect('/login')
    my_orders = [o for o in orders if o['user'] == session.get('user')]
    return render_template('history.html', orders=my_orders, user=session.get('user'))

# --- ADMIN ---
@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == 'admin123':
            session['is_admin'] = True
            return redirect('/admin')
        else:
            return "Galat Password! <a href='/admin-login'>Wapas</a>"
    return render_template('admin_login.html')

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect('/admin-login')
    return render_template('admin.html', items=FOOD_ITEMS, orders=orders)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    global next_food_id
    if not session.get('is_admin'):
        return redirect('/admin-login')
    name = request.form.get('name')
    price = int(request.form.get('price') or 0)
    photo = request.form.get('photo') or '/static/pizza.jpg'
    category = request.form.get('category') or 'Fast Food'
    FOOD_ITEMS.append({'id': next_food_id, 'name': name, 'price': price, 'photo': photo, 'category': category})
    next_food_id += 1
    return redirect('/admin')

@app.route('/admin/delete_food/<int:fid>')
def admin_delete_food(fid):
    global FOOD_ITEMS
    if not session.get('is_admin'):
        return redirect('/admin-login')
    FOOD_ITEMS = [x for x in FOOD_ITEMS if x['id'] != fid]
    return redirect('/admin')

@app.route('/approve/<int:i>')
def approve(i):
    if not session.get('is_admin'):
        return redirect('/admin-login')
    orders[i]['status'] = 'Approved'
    return redirect('/admin')

@app.route('/delete_order/<int:i>')
def delete_order(i):
    if not session.get('is_admin'):
        return redirect('/admin-login')
    orders.pop(i)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
