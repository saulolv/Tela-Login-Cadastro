from PyQt5 import uic, QtWidgets
import sqlite3

app = QtWidgets.QApplication([])

login_screen = uic.loadUi("login_screen.ui")
screen2 = uic.loadUi("screen2.ui")
register_screen = uic.loadUi("register_screen.ui")



def main():
    login_screen.pushButton.clicked.connect(login)
    login_screen.pushButton_2.clicked.connect(open_register_screen)
    register_screen.pushButton.clicked.connect(register)
    
    

    login_screen.show()
    app.exec()


def login():
    login_screen.label_3.setText("")
    username = login_screen.lineEdit.text()
    password = login_screen.lineEdit_2.text()
    
    bd = sqlite3.connect("database.db")
    cursor = bd.cursor()
    try:
        cursor = bd.execute("SELECT password FROM users WHERE username = '"+username+"'")
        password_bd = cursor.fetchall()
        
        bd.close()
    except:
        print("Erro ao conectar no banco de dados!")
        
    if password == password_bd[0][0]:
        login_screen.label_3.setText("Login realizado com sucesso!")
        login_screen.close()
        screen2.show()
    else:
        login_screen.label_3.setText("Usuário ou senha incorretos!")


def open_register_screen():
    login_screen.close()
    register_screen.show()

def register():
    username = register_screen.lineEdit.text()
    email = register_screen.lineEdit_2.text()
    password = register_screen.lineEdit_3.text()
    password2 = register_screen.lineEdit_4.text()
    
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    
    # Verifica se o username já está em uso no banco de dados
    cursor.execute("SELECT * FROM users WHERE username = '"+username+"'")
    existing_user = cursor.fetchone()
    
    if existing_user:
        register_screen.label_6.setText("o Username já está sendo usado!")
        register_screen.lineEdit.setText("")
        db.close()
        return
    
    # Verifica se o email já está em uso no banco de dados
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    existing_email = cursor.fetchone()
    if existing_email:
        register_screen.label_7.setText("Este email já está sendo usado, tente outro!")
        register_screen.lineEdit_2.setText("")
        db.close()
        return
    
    elif username == "" or email == "" or password == "" or password2 == "":
        register_screen.label_5.setText("Preencha todos os campos!")
    elif password != password2:
        register_screen.label_8.setText("As senhas não coincidem!")
        register_screen.label_9.setText("As senhas não coincidem!")
    else:
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)")
            cursor.execute("INSERT INTO users VALUES ('"+username+"', '"+email+"', '"+password+"')")
            
            db.commit()
            db.close()
            
            register_screen.label_5.setText("Usuário cadastrado com sucesso!")
            register_screen.lineEdit.setText("")
            register_screen.lineEdit_2.setText("")
            register_screen.lineEdit_3.setText("")
            register_screen.lineEdit_4.setText("")
            
            register_screen.close()
            login_screen.show()
        except sqlite3.Error as erro:
            print("Erro ao conectar no banco de dados!", erro)

        db.close()

main()