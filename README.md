Projekt awaryjny 2025
=====================
W czasie sesji 2025, możliwe jest oddanie uproszczonego projektu, za którego **samodzielne** i poprawne wykonanie można otrzymać **26 p.** Istotną zmianą w stosunku do zwykłego projektu jest **zakaz używania generowanego/cudzego kodu**. Aplikacja ma pozostać prosta.

Tematem projektu jest zbudowanie **bardzo prostej** aplikacji do przechowywania notatek Markdown.
Aplikacja powinna pozwalać na założenie konta w systemie oraz zalogowanie się do niego przy użyciu dwuetapowej autentykacji (2FA, dopuszczalnymi metodami są TOTP oraz HOTP).

_Zakres aplikacji_ to:
- rejestracja konta;
- logowanie użytkownika (wymagające podania drugiego składnika);
- dodanie własnej, prywatnej (**nieszyfrowanej**) notatki w formacie Markdown;
- usunięcie swojej notatki;
- obejrzenie notatki, gdzie format Markdown zostanie przetworzony do kodu HTML i wyświetlony na stronie.

_Wspierane elementy HTML notatek_ muszą pozwalać na następujące znaczniki HTML:
`p`, `h1`--`h6`, `blockquote`, `ul`, `ol`, `li`, `pre`, `hr`, `em`, `strong`, `code`, `a`, `img` oraz `br`. Dozwolone atrybuty HTML to jedynie: `href`, `title`, `src`, `alt` oraz `class`.

Należy wybrać (i prawidłowo wykorzystać) odpowiednie algorytmy, biblioteki i techniki zapewniające bezpieczeństwo danych użytkowników.
Niezbędne jest wdrożenie skutecznych mechanizmów autoryzacji i autentykacji wszystkich końcówek aplikacji.
Niesprecyzowane w tym dokumencie wymagania należy skonsultować z prowadzącym (dr inż. Bartosz Chaber).
Oczekiwana jest pełna wiedza dotycząca implementacji i konfiguracji wykorzystanych rozwiązań. 
Brak odpowiedniej znajomości swojego projektu stanowi podstawę do niezaliczenia projektu.

_Istotne elementy_, które należy uwzględnić w trakcie implementacji:
- walidacja (lub sanityzacja) **wszystkich** danych wejściowych kontrolowanych przez użytkownika,
- opóźnienia i limity prób (żeby utrudnić zdalne zgadywanie i atak brute-force),
- bezpieczne przechowywanie hasła (wykorzystanie aktualnie rekomendowanych, kryptograficznych funkcji mieszających, wykorzystanie soli, wielokrotne hashowanie).

_Wymagania techniczne_:
- skonteneryzowanie projektu przy pomocą Docker;
- wykorzystanie relacyjnej bazy danych (SQL, może być SQLite);
- bezpieczne połączenie z aplikacją (szyfrowane połączenie) wykorzystujące serwer WWW (NGINX, Apache HTTPd, Caddy) jako pośrednika (proxy).

Gotowy kod oddajemy do **13.02.2026, 8:00** (poprzez załączenie kodu w iSOD). Tego dnia też nastąpi osobista obrona projektu.
