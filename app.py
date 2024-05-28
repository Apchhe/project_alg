from flask import Flask, request, render_template, redirect, url_for, flash
import db
import base64

app = Flask(__name__)
app.secret_key = "SuperSecretKey"


def index():
    if request.method == "POST":
        search_username = request.form["search_username"]
        return redirect(url_for("user", username=search_username))
    return render_template("index.html")


def create():
    """
    Представление для создания карточки
    """

    if request.method == "POST":  # Если пришла форма
        # Получаем данные из формы и запоминаем
        username = request.form["username"]
        password = request.form["password"]
        age = request.form["age"]
        text_1 = request.form["text_1"]
        text_2 = request.form["text_2"]
        text_3 = request.form["text_3"]
        # Получаем картинки из формы
        image_1 = request.files["image_1"].read() if request.files["image_1"] else None
        image_2 = request.files["image_2"].read() if request.files["image_2"] else None
        image_3 = request.files["image_3"].read() if request.files["image_3"] else None
        link_1 = request.form["link_1"]
        link_2 = request.form["link_2"]
        link_3 = request.form["link_3"]
        link_4 = request.form["link_4"]

        if db.user_exists(username):
            flash("Это имя пользователя уже занято. Пожалуйста, выберите другое имя.")
            return render_template("create.html")

        db.create_card(
            username,
            age,
            password,
            text_1,
            text_2,
            text_3,
            image_1,
            image_2,
            image_3,
            link_1,
            link_2,
            link_3,
            link_4,
        )  # Создаем карточку
        return redirect(url_for("user", username=username))  # Открываем пользователя
    return render_template("create.html")


def user(username):
    """
    Представление для отображения карточки пользователя
    """

    card = db.get_card(username)
    if card:
        card = {
            "username": card[0],
            "age": card[1],
            "text_1": card[2],
            "text_2": card[3],
            "text_3": card[4],
            # Открываем картинки с помощью библиотеки base64
            "image_1": base64.b64encode(card[5]).decode("utf-8") if card[5] else None,
            "image_2": base64.b64encode(card[6]).decode("utf-8") if card[6] else None,
            "image_3": base64.b64encode(card[7]).decode("utf-8") if card[7] else None,
            "link_1": card[8],
            "link_2": card[9],
            "link_3": card[10],
            "link_4": card[11],
        }
        return render_template("card.html", card=card)
    else:
        flash("Пользователь не найден!")
        return render_template("error.html")


def delete():
    """
    Представление для удаления карточки
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.check_password(username, password):
            db.delete_card(username)
            return redirect(url_for("index"))
        else:
            flash("Неверный пароль или имя пользователя.")
            return render_template("error.html")
    return render_template("delete.html")


app.add_url_rule("/", "index", index, methods=["GET", "POST"])
app.add_url_rule("/create", "create", create, methods=["GET", "POST"])
app.add_url_rule("/user/<username>", "user", user)
app.add_url_rule("/delete", "delete", delete, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)
