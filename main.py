from functools import wraps

users = {
    "janek": {"haslo": "abc", "zalogowany": False, "poziom": 1, "saldo": 250},
    "admin": {"haslo": "123", "zalogowany": False, "poziom": 3, "saldo": 1000},
}
aktywny_user = None


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] witam w funkcji {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] koniec funkcji {func.__name__}")
        return result

    return wrapper


def zaloguj(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global aktywny_user
        login = input("Podaj login: ").strip()
        password = input("Podaj hasło: ").strip()
        if login in users and users[login]["haslo"] == password:
            print("Dane poprawne.")
            if aktywny_user and aktywny_user in users:
                users[aktywny_user]["zalogowany"] = False
            users[login]["zalogowany"] = True
            aktywny_user = login
            return func(*args, **kwargs)
        print("Hasło lub login niepoprawne. Spróbuj ponownie.")
        return None

    return wrapper


def wymaga_logowania(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = users.get(aktywny_user)
        if not user or not user.get("zalogowany"):
            print("Musisz się zalogować.")
            return None
        return func(*args, **kwargs)

    return wrapper


def poziom(min_poziom):
    def dekorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = users.get(aktywny_user)
            if not user or not user.get("zalogowany"):
                print("Musisz się zalogować, aby mieć dostęp.")
                return None
            if user["poziom"] < min_poziom:
                print("Brak dostępu — zbyt niskie uprawnienia.")
                return None
            return func(*args, **kwargs)

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
    print("✅ Rejestracja zakończona! Możesz się teraz zalogować.")


@wymaga_logowania
@log
def pokaz_saldo():
    print(f"💰 Saldo: {users[aktywny_user]['saldo']} zł")


@log
@zaloguj
def logowanie():
    print("Witamy w menu logowania.")


@log
@wymaga_logowania
@poziom(3)
def edytuj_dane():
    print("Witaj admin")


@wymaga_logowania
@log
def wykonaj_przelew():
    try:
        kwota = float(input("Podaj kwotę: "))
    except ValueError:
        print("Niepoprawne dane.")
        return
    if kwota < 0:
        print("Kwota nie może być mniejsza niż 0.")
        return
    if kwota > users[aktywny_user]["saldo"]:
        print("Nie masz na tyle środków.")
        return
    odbiorca = input("Podaj imię odbiorcy: ").strip()
    users[aktywny_user]["saldo"] -= kwota
    print(f"Przelano {kwota:.2f} do {odbiorca}.")


def wyloguj():
    global aktywny_user
    if not aktywny_user:
        print("Nikt nie jest zalogowany.")
        return
    users[aktywny_user]["zalogowany"] = False
    print(f"Użytkownik {aktywny_user} został wylogowany.")
    aktywny_user = None


def menu():
    while True:
        print("\n===== MENU GŁÓWNE =====")
        status = f"Zalogowany jako: {aktywny_user}" if aktywny_user else "Brak zalogowanego użytkownika"
        print(status)
        print("1. Zaloguj")
        print("2. Rejestracja")
        print("3. Pokaż saldo")
        print("4. Wykonaj przelew")
        print("5. Edytuj dane (admin)")
        print("6. Wyloguj")
        print("0. Wyjdź")
        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            logowanie()
        elif wybor == "2":
            register()
        elif wybor == "3":
            pokaz_saldo()
        elif wybor == "4":
            wykonaj_przelew()
        elif wybor == "5":
            edytuj_dane()
        elif wybor == "6":
            wyloguj()
        elif wybor == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nPrzerwano przez użytkownika.")
