#  E-Learning Nyilvántartó Rendszer (Django Webalkalmazás)

Ez a Django-alapú projekt egy egyszerű e-learning rendszert valósít meg, amely kezeli a Tanárokat, a Kurzusokat és a Hallgatók kurzusfelvételeit. A fejlesztés során hangsúlyt fektettünk az adatbázis-kapcsolatok, a biztonság és a modern, aszinkron interakciók megvalósítására.

##  Projektkövetelmények Teljesítése

A rendszer az alábbi fő követelményeket teljesíti:

| Követelmény | Megvalósítás |
| :--- | :--- |
| **1. és 2. CRUD/Kapcsolatok** | Teljes CRUD a `Tanár`, `Kurzus`, `Hallgató` entitásokra. **N:M** kapcsolat valósult meg a Hallgatók és Kurzusok között (`HallgatoKurzus` köztes tábla). |
| **3. Biztonság** | A Hallgatói felület (`kurzus_list`) a **`LoginRequiredMixin`** használatával védett. Belépés nélkül átirányítás a `/login/` útvonalra. |
| **4. Esztétika** | **Bootstrap 5** alapú reszponzív felület. Az Admin felület **nyelvhelyességi javításai** a `verbose_name_plural` használatával történtek. |
| **5. Aszinkron Interakció** | A kurzusfelvétel **JavaScript (Fetch API)** hívással történik egy háttérbeli API végpontra, oldalfrissítés nélkül. |

---

##  Telepítési Útmutató (Helyi Környezet)

A projekt futtatásához szükséges technológiák: **Python 3.x** és **Django**.

### 1. Git/Környezet Előkészítése

Ha ez a kód már egy Git repositoryban van, ugorjon a 2. lépésre.

```bash
# Lépjen be a projekt főkönyvtárába
cd [projekt_mappa_neve]

# 1. Lokális Git repository inicializálása
git init

# 2. Virtuális környezet létrehozása és aktiválása (ajánlott)
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# 3. Django telepítése (ha nem biztos, hogy telepítve van)
pip install django