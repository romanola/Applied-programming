import sqlite3
import pickle


class TreeDB:

    def __init__(self, filename):
        self.filename = filename


    def create(self):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        try:
            curs.execute("CREATE TABLE trees (kind TEXT, grade TEXT, year INT, place TEXT, harvest BLOB)")
        except:
            pass
        conn.commit()
        conn.close()


    def append(self, kind, grade, year, place, harvest: dict):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("INSERT INTO trees VALUES (?, ?, ?, ?, ?)",
                     (kind, grade, year, place, sqlite3.Binary(pickle.dumps(harvest))))

        conn.commit()
        conn.close()


    def find_by_kind(self, kind):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("SELECT * FROM trees WHERE kind = ?", (kind,))

        res = curs.fetchall()
        conn.commit()
        conn.close()

        ans = []
        for record in res:
            ans.append(' '.join(list(map(str, record[:4])) + [str(pickle.loads(record[4]))]))
        return ans

    def find_harvest_by_years(self, grade, year1, year2):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("SELECT harvest FROM trees WHERE grade = ?", (grade,))

        res = curs.fetchall()
        conn.commit()
        conn.close()

        ans = []
        for record in res:
            ans.append(pickle.loads(record[0]))

        s = 0
        for d in ans:
            for k, v in d.items():
                if year1 <= k <= year2:
                    s += v
        return s



if __name__ == '__main__':
    tdb = TreeDB("trees.db")
    tdb.create()
    tdb.append(kind="яблоня", grade="семеринка", year=1989, place="Киев", harvest={2000: 15, 2001: 18, 1990: 232})
    tdb.append(kind="яблоня", grade="голд", year=2000, place="Одесса", harvest={2001: 305, 2009: 1342, 2011: 215})
    tdb.append(kind="груша", grade="зимняя", year=2015, place="Васильков", harvest={2017: 315, 2018: 45, 2020: 48})
    print(tdb.find_by_kind(kind="яблоня"))
    print(tdb.find_by_kind(kind="груша"))
    print(tdb.find_harvest_by_years(grade="голд", year1=2001, year2=2010))
    print(tdb.find_harvest_by_years(grade="зимняя", year1=2018, year2=2030))