# air-quality-client
Project for PIPR as an obligatory element to pass this subject.


## Subject:
Pobieranie danych o obecnym i historycznym stanie jakości powietrza ze stacji pomiarowych GIOŚ za pomocą [interfejsów API](https://powietrze.gios.gov.pl/pjp/content/api) i prezentowanie ich na wykresie.

### Funkcjonalność
 * wyświetlanie listy wszystkich dostępnych stacji pomiarowych
 * wyświetlanie listy wszystkich stanowisk pomiarowych dla danej stacji
 * pobieranie wybranych (oraz wszystkich) danych pomiarowych dla wybranej stacji
 * wizualizacja pobranych danych na wykresie z seriami (np. z użyciem pyplot). Oś X - czas; oś Y - wartość wskaźnika ze stanowiska pomiarowego. Dwa rodzaje wykresów:
    + wykres prezentujący dane z jednej stacji; każda seria to dane z innego stanowiska pomiarowego
    + wykres prezentujący dane z jednego rodzaju stanowiska pomiarowego; każda seria to dane z innej stacji pomiarowej
  * lokalne cache'owania pobieranych wyników (w celu ograniczenia liczby dostępów do API, pytanie o te same dane nie powinno być zadawane częściej niż co 10 minut)
 * integrowanie pobieranych wyników z lokalną bazą (odpowiedzi API nie zawierają pełnej historii, jedynie sprzed ostatnich kilku dni; lokalnie powinna być przechowywana pełna historia)
