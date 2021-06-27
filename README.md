# Keskustelusovellus
Tässä keskustelusovelluksesta löytyy keskustelualueita (kanavia).
Keskustelualueita on viestiketjuja, jotka muodostuvat viesteistä.
Sovelluksella on kolmea käyttäjäroolia on vierailija, kirjautunut käyttäjä sekä ylläpitäjä.

## Sovelluksen [määrittelydokumentti](./documentation/README-fi.md)

## Documentation [in english](./documentation/README.md)

## Tämän hetkinen tilanne
Sovellus löytyy verkosta osoitteessa [https://powerful-everglades-12307.herokuapp.com](https://powerful-everglades-12307.herokuapp.com).
Sovellukseen voi kirjautua joko
 * tavallisena käyttäjänä käyttäjänimellä ```customer``` ja salasanalla ```password``` tai
 * ylläpitäjänä käyttäjänimellä ```admin``` ja salasanalla ```password```.

## Yleiskuvais sovelluksen toiminnallisuuksista:
- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- [x] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- [x] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- [x] Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- [x] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- [x] Käyttäjä voi tykätä viesteistä.
- [x] Käyttäjä voi arvioda kanavia.
- [x] Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- [x] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle
