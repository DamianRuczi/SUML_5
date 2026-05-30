

## Jak uruchomić projekt

## 0. Konfiguracja GitHub przez SSH (Jednorazowo)

Zanim pobierzesz lub wrzucisz kod na GitHub, skonfiguruj bezpieczne połączenie SSH bez wpisywania haseł.

### Krok 1: Generowanie klucza
Otwórz terminal i wygeneruj nowy klucz (podmień e-mail na swój z GitHuba):
```bash
ssh-keygen -t ed25519 -C "twój_email@example.com"
```
*Gdy system zapyta o ścieżkę i hasło (passphrase), wciskaj **Enter** (ustawienia domyślne).*

### Krok 2: Uruchomienie agenta i dodanie klucza
```bash
# Uruchomienie agenta w tle
eval "\$(ssh-agent -s)"

# Dodanie klucza prywatnego do agenta
ssh-add ~/.ssh/id_ed25519
```

### Krok 3: Dodanie klucza do konta GitHub
1. Wyświetl zawartość klucza publicznego i skopiuj go do schowka:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. Zaloguj się na **GitHub.com**.
3. Wejdź w **Settings** (prawy górny róg) -> **SSH and GPG keys** -> **New SSH key**.
4. Wklej skopiowany klucz, nadaj mu nazwę (np. "Mój Laptop") i zapisz.

### Krok 4: Test połączenia
```bash
ssh -T git@github.com
```
*Jeśli pojawi się pytanie o zaufanie do hosta, wpisz `yes`. Powinieneś zobaczyć komunikat powitalny ze swoim loginem GitHub.*


### 1. Przygotowanie środowiska (Conda)
Stwórz i aktywuj nowe środowisko, a następnie zainstaluj wymagane pakiety:

```bash
# Instalacja zależności
conda install --file requirements.txt
```

### 2. Uruchomienie aplikacji
Upewnij się, że jesteś w głównym folderze projektu (tam gdzie znajduje się `app.py`) i wpisz:

```bash
uvicorn app:app --reload
```

