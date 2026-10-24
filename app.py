from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "food123"

menu = [
    {"id": 1, "name": "Dal Bati Churma", "price": 120, "img": "/static/dalbati.jpg"},
    {"id": 2, "name": "Pizza Cheese Burst", "price": 199, "img": "/static/pizza.jpg"},
    {"id": 3, "name": "Burger Combo", "price": 99, "img": "/static/burger.jpg"},
    {"id": 4, "name": "Paneer Butter Masala", "price": 150, "img": "/static/paneer.jpg"},
    {"id": 5, "name": "Maggie Masala", "price": 60, "img": "/static/maggie.jpg"},
    {"id": 6, "name": "Cold Coffee", "price": 80, "img": "/static/coffee.jpg"},
]

orders = []

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

@app.route('/add/<int:id>')
def add(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    return redirect('/')

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    items = [m for m in menu if m['id'] in cart]
    total = sum(i['price'] for i in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    upi = request.form['upi']
    if len(upi) < 12 or not upi.isdigit():
        return "<h1>❌ 12 Digit daal - 123 se nahi chalega</h1><a href='/cart'>Wapas</a>"
    cart = session.get('cart', [])
    items = [m for m in menu if m['id'] in cart]
    total = sum(i['price'] for i in items)
    orders.append({"name": name, "items": items, "total": total, "upi": upi, "status": "PENDING"})
    session['cart'] = []
    return render_template('order.html', name=name, total=total)

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

# YE WALA HI APPROVE HAI - YE NAHI HOGA TOH BUTTON KAAM NAHI KAREGA
@app.route('/approve/<int:index>')
def approve(index):
    print("APPROVE DABAYA - ", index)
    orders[index]['status'] = "PAID ✅ - Order Bhej Do"
    return redirect('/admin')

@app.route('/delete/<int:index>')
def delete_order(index):
    if 0 <= index < len(orders):
        orders.pop(index)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
