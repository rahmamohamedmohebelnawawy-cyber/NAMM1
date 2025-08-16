from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات
conn = sqlite3.connect("bookings.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

# صفحة الإدخال
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>نموذج الحجز</title>
</head>
<body>
    <h2>أدخل بيانات الحجز</h2>
    <form method="POST" action="/add">
        الاسم: <input type="text" name="name" required><br><br>
        رقم الهاتف: <input type="text" name="phone" required><br><br>
        التاريخ: <input type="date" name="date" required><br><br>
        الوقت: <input type="time" name="time" required><br><br>
        <button type="submit">حجز</button>
    </form>
    <br>
    <a href="/show">عرض كل الحجوزات</a>
</body>
</html>
"""

# صفحة عرض الحجوزات مع البحث والحذف
show_html = """
<!DOCTYPE html>
<html>
<head>
    <title>الحجوزات</title>
</head>
<body>
    <h2>كل الحجوزات</h2>
    <form method="GET" action="/show">
        بحث بالاسم: <input type="text" name="search" value="{{ search }}">
        <button type="submit">بحث</button>
    </form>
    <br>
    <table border="1">
        <tr><th>ID</th><th>الاسم</th><th>الهاتف</th><th>التاريخ</th><th>الوقت</th><th>حذف</th></tr>
        {% for b in bookings %}
        <tr>
            <td>{{ b[0] }}</td>
            <td>{{ b[1] }}</td>
            <td>{{ b[2] }}</td>
            <td>{{ b[3] }}</td>
            <td>{{ b[4] }}</td>
            <td><a href="/delete/{{ b[0] }}" onclick="return confirm('هل أنت متأكد من الحذف؟');">🗑 حذف</a></td>
        </tr>
        {% endfor %}
    </table>
    <br>
    <a href="/">رجوع للنموذج</a>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(form_html)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    phone = request.form["phone"]
    date = request.form["date"]
    time = request.form["time"]

    cursor.execute("INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
                   (name, phone, date, time))
    conn.commit()
    return "<p>✅ تم حفظ الحجز!</p><a href='/'>رجوع</a>"

@app.route("/show")
def show():
    search = request.args.get("search", "")
    if search:
        cursor.execute("SELECT * FROM bookings WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    return render_template_string(show_html, bookings=bookings, search=search)

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
    conn.commit()
    return redirect("/show")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


