import sqlite3
from flask import Flask, request, redirect, url_for, session, render_template_string
import datetime

app = Flask(__name__)
app.secret_key = "dk_ultimate_master_key"

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('dk_business.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, item TEXT, qty INTEGER, total INTEGER, time TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS visitors 
                      (id INTEGER PRIMARY KEY, ip TEXT, time TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# --- CSS: Video, 3D Tilt, Glassmorphism, and Loader ---
STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');
    
    * { box-sizing: border-box; }
    body, html { margin: 0; padding: 0; font-family: 'Poppins', sans-serif; color: white; overflow-x: hidden; background: #000; }

    /* Fullscreen Video Background */
    #video-bg {
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1; filter: brightness(40%) contrast(1.2);
        object-fit: cover;
    }

    /* Professional Loader */
    #loader {
        position: fixed; width: 100%; height: 100%;
        background: #000; z-index: 9999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .spinner {
        width: 60px; height: 60px;
        border: 5px solid rgba(255,255,255,0.1);
        border-top: 5px solid #00adb5;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* Container & Glassmorphism */
    .container { padding: 40px 20px; max-width: 1200px; margin: auto; }
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        transition: 0.5s;
    }

    /* 3D Tilt Animation Effect */
    .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
    .card-3d {
        perspective: 1000px;
    }
    .card-3d:hover .glass-card {
        transform: rotateX(10deg) rotateY(10deg) translateY(-10px);
        border-color: #00adb5;
        box-shadow: 0 30px 60px rgba(0, 173, 181, 0.3);
    }

    .card img {
        width: 100%; border-radius: 20px; height: 200px; object-fit: cover;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }

    .btn {
        background: #00adb5; color: white; padding: 15px 30px;
        border-radius: 50px; text-decoration: none; font-weight: bold;
        display: inline-block; border: none; cursor: pointer; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .btn:hover { background: white; color: #00adb5; box-shadow: 0 0 20px #00adb5; transform: scale(1.05); }

    input {
        width: 100%; padding: 12px; margin: 10px 0;
        background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
        color: white; border-radius: 10px; font-size: 1rem;
    }
</style>

<script>
    window.addEventListener('load', function() {
        setTimeout(function() {
            document.getElementById('loader').style.opacity = '0';
            setTimeout(function() { document.getElementById('loader').style.display = 'none'; }, 500);
        }, 1500);
    });
</script>
"""

@app.route("/")
def home():
    # विज़िटर ट्रैक करें
    conn = sqlite3.connect('dk_business.db'); cursor = conn.cursor()
    cursor.execute("INSERT INTO visitors (ip, time) VALUES (?, ?)", (request.remote_addr, datetime.datetime.now()))
    conn.commit(); conn.close()
    
    return f"""<html><head>{STYLE}</head><body>
        <div id="loader"><div class="spinner"></div><p style="margin-top:20px;">DK Special Dabali Loading...</p></div>
        
        <video autoplay muted loop playsinline id="video-bg">
            <source src="https://assets.mixkit.co/videos/preview/mixkit-top-view-of-a-delicious-burger-1250-large.mp4" type="video/mp4">
        </video>

        <div class="container" style="height: 100vh; display: flex; align-items: center; justify-content: center;">
            <div class="glass-card" style="text-align: center; max-width: 700px;">
                <h1 style="font-size: 4.5rem; margin: 0; letter-spacing: 2px;">DK SPECIAL</h1>
                <h2 style="color: #00adb5; font-size: 2.5rem; margin: 0 0 20px 0;">DABALI</h2>
                <p style="font-size: 1.2rem; margin-bottom: 30px;">Experience the 3D Taste of Best Dabali in the World.</p>
                <a href="/menu" class="btn">View Our Menu</a>
            </div>
        </div>
    </body></html>"""

@app.route("/menu")
def menu():
    products = [
        {"name": "Classic Dabali", "price": 20, "img": "item1.jpg"},
        {"name": "Cheese Special", "price": 40, "img": "item2.jpg"},
        {"name": "Butter Dabali", "price": 30, "img": "item3.jpg"},
        {"name": "Maharaja Combo", "price": 150, "img": "item4.jpg"}
    ]
    html = f"<html><head>{STYLE}</head><body style='background: #0a0a0a;'>"
    html += '<div class="container"><h1 style="text-align:center; margin-bottom:50px;">OUR PRODUCTS</h1><div class="product-grid">'
    for p in products:
        html += f'''
        <div class="card-3d">
            <div class="glass-card card">
                <img src="/static/{p['img']}">
                <h3>{p['name']}</h3>
                <p style="color:#00adb5; font-size:1.8rem; font-weight:bold;">₹{p['price']}</p>
                <a href="/order?item={p['name']}&price={p['price']}" class="btn" style="width:100%;">Order Now</a>
            </div>
        </div>
        '''
    return html + "</div><div style='text-align:center; margin-top:50px;'><a href='/' style='color:white; text-decoration:none;'>← Back to Home</a></div></div></body></html>"

@app.route("/order")
def order():
    item = request.args.get('item'); price = int(request.args.get('price'))
    return f"""<html><head>{STYLE}</head><body style='background: #0a0a0a;'>
        <div class="container" style="height:90vh; display:flex; align-items:center;">
            <div class="glass-card" style="max-width:500px; margin:auto; width:100%;">
                <h2 style="color:#00adb5;">Confirm Order</h2>
                <h3>Item: {item}</h3>
                <p>Price: ₹{price}</p>
                <hr style="opacity:0.2;">
                <form action="/save" method="post">
                    <input type="hidden" name="item" value="{item}">
                    <input type="hidden" name="price" value="{price}">
                    <input type="text" name="n" placeholder="Your Full Name" required>
                    <input type="text" name="p" placeholder="Mobile Number" required>
                    <input type="number" name="q" value="1" min="1" style="width:100%; padding:12px; margin:10px 0; background:rgba(255,255,255,0.1); color:white; border-radius:10px; border:1px solid rgba(255,255,255,0.2);">
                    <button type="submit" class="btn" style="width:100%; margin-top:20px;">Place Order</button>
                </form>
            </div>
        </div>
    </body></html>"""

@app.route("/save", methods=["POST"])
def save():
    n, p, i, q, pr = request.form['n'], request.form['p'], request.form['item'], int(request.form['q']), int(request.form['price'])
    total = q * pr
    conn = sqlite3.connect('dk_business.db'); cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (name, phone, item, qty, total, time) VALUES (?, ?, ?, ?, ?, ?)", (n, p, i, q, total, datetime.datetime.now()))
    conn.commit(); conn.close()
    return f"<html><head>{STYLE}</head><body style='background:#0a0a0a;'><div class='container glass-card' style='text-align:center; margin-top:100px;'><h1>Order Received!</h1><p>Vikas will contact you shortly on {p}.</p><a href='/menu' class='btn'>Go Back</a></div></body></html>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form['u'] == 'admin' and request.form['p'] == 'dk123':
            session['admin'] = True
            return redirect(url_for('admin'))
    return f'<html><head>{STYLE}</head><body style="background:#0a0a0a;"><div class="container"><form method="post" class="glass-card" style="max-width:400px; margin:auto; text-align:center;"><h2>Business Login</h2><input name="u" placeholder="Admin Username"><input name="p" type="password" placeholder="Password"><br><br><button class="btn" style="width:100%;">Login</button></form></div></body></html>'

@app.route("/admin")
def admin():
    if not session.get('admin'): return redirect(url_for('login'))
    conn = sqlite3.connect('dk_business.db'); cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitors"); visits = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM orders ORDER BY id DESC"); orders = cursor.fetchall(); conn.close()
    
    rows = "".join([f"<tr><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>₹{r[5]}</td><td>{r[6]}</td></tr>" for r in orders])
    return f"""<html><head>{STYLE}</head><body style="background:#0a0a0a;"><div class="container">
        <h1 class="glass-card" style="text-align:center;">DK BUSINESS ANALYTICS</h1>
        <div class="product-grid" style="margin-top:40px;">
            <div class="glass-card"><h3>Site Visits</h3><h1 style="color:#00adb5;">{visits}</h1></div>
            <div class="glass-card"><h3>Total Orders</h3><h1 style="color:#00adb5;">{len(orders)}</h1></div>
        </div>
        <br><table style="width:100%; border-collapse:collapse; margin-top:40px;" border="1">
            <tr><th>Name</th><th>Phone</th><th>Item</th><th>Qty</th><th>Total</th><th>Date/Time</th></tr>{rows}
        </table>
        <br><br><a href="/logout" class="btn">Logout</a>
    </div></body></html>"""

@app.route("/logout")
def logout(): session.pop('admin', None); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)