from functools import wraps

users = {
    "janek": {"haslo": "abc", "zalogowany": False, "poziom": 1, "saldo": 250},
    "admin": {"haslo": "123", "zalogowany": False, "poziom": 3, "saldo": 1000},
}
aktywny_user = None


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] witam w funckji {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] koniec funkcji {func.__name__}")
        return result

    return wrapper


def zaloguj(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global aktywny_user
        login = input("Podaj login: ").strip()
        password = input("Podaj hasło:").strip()
        if login in users and users[login]["haslo"] == password:
            print("dane poprawne")
            users[login]["zalogowany"] = True
            aktywny_user = login
            results = func(*args, **kwargs)
            return results
        else:
            print("Hasło lub login nieporawne spróbuj ponownie")
            return

    return wrapper


def wymaga_logowania(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not aktywny_user or not users[aktywny_user]["zalogowny"]:
            print("musisz się zalogować")
            return
        results = func(*args, **kwargs)
        return results

    return wrapper


def poziom(min_poziom):
    def dekorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not aktywny_user or not aktywny_user["zalogowny"]:
                print("muszisz się zalogowac by mieć dostęp")
                return

            if aktywny_user["poziom"] < min_poziom:
                print("brak dostępu za niskie uprawnienia ")
                return
            results = func(*args, **kwargs)
            return results

        return wrapper

    return dekorator


def register():
    print("Witaj w menu rejestracji")
    login = input("Podaj login: ").strip()

    if login in users:
        print("❌ Użytkownik już istnieje!")
        return

    password = input("Podaj hasło: ").strip()
    users[login] = {"haslo": password, "zalogowany": False, "poziom": 1, "saldo": 0}
    print("✅ Rejestracja zakończona!")


@wymaga_logowania
@log
def pokaz_saldo():
    print(f"💰 Saldo: {users[aktywny_user]['saldo']} zł")


@log
def logowanie():
    print("witamy w menu logowowania ")


@log
@wymaga_logowania
@poziom(3)
def edytuj_dane():
    print("Witaj admin")


@wymaga_logowania
@log
def wykonaj_przelew():
    try:
        kwota = float(input("Podaj kwotę:"))

    except ValueError:
        print("nieporawne dane ")
        return

    odbiorca = input("Podaj imię odbiorcy: ").strip()

    if kwota < 0:
        print("Kwota nie może być mniejsza niż 0")

    if kwota > users[aktywny_user]["saldo"]:
        print("Nie masz na tyle środków")
        return
    users[aktywny_user]["saldo"] -= kwota
    print(f"przelano {kwota} do {odbiorca}")


def menu():
    while True:
        print("Witaj w menu")
        # uznajmy że dalej jest opcja wybroru itp bo już nie chce mi się klikać xd
