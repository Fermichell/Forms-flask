from flask import Flask, request, render_template_string
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def register():
    errors = []
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        birthdate = request.form['birthdate']
        
        

        #val log
        if len(username) < 5:
            errors.append("Логін повинен містити мінімум 5 символів.")
        
        #val name
        if not name.isalpha():
            errors.append("Ім'я повинно містити лише літери.")
        
        #val post
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            errors.append("Невірний формат електронної пошти.")
        
        #val pass
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            errors.append("Пароль повинен містити хоча б одну велику літеру, одну цифру та мінімум 8 символів.")
        
        
        #val birth_day
        try:
            birthdate_dt = datetime.strptime(birthdate, "%Y-%m-%d")
            if birthdate_dt > datetime.now():
                errors.append("Дата народження не може бути в майбутньому.")
        except ValueError:
            errors.append("Невірний формат дати. Використовуйте формат YYYY-MM-DD.")
        
        if not errors:
            return "Реєстрація успішна!" 

    return render_template_string('''
    <form method="post">
        Логін: <input type="text" name="username"><br>
        Ім'я: <input type="text" name="name"><br>
        Електронна пошта: <input type="text" name="email"><br>
        Пароль: <input type="password" name="password"><br>
        Телефон: <input type="text" name="phone"><br>
        Дата народження: <input type="text" name="birthdate" placeholder="YYYY-MM-DD"><br>
        <input type="submit" value="Зареєструватися">
    </form>
    <ul>
        {% for error in errors %}
            <li>{{ error }}</li>
        {% endfor %}
    </ul>
    ''', errors=errors)

if __name__ == '__main__':
    app.run(debug=True)