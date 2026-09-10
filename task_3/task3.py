class ItemStatus:
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class Book:
    def __init__(self, title, author, isbn, status=ItemStatus.AVAILABLE):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
        self.loan_period = 21

    def checkout(self):
        if self.status == ItemStatus.CHECKED_OUT:
            raise ValueError("Already checked out.")
        if self.status == ItemStatus.LOST:
            raise ValueError("Item is lost.")
        self.status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self.status == ItemStatus.AVAILABLE:
            raise ValueError("Item was not checked out.")
        self.status = ItemStatus.AVAILABLE

    def mark_lost(self):
        self.status = ItemStatus.LOST

    @classmethod
    def from_dict(cls, d):
        return cls(d["title"], d["author"], d["isbn"], d.get("status", ItemStatus.AVAILABLE))

    def to_dict(self):
        return {"type": "Book", "title": self.title, "author": self.author, "isbn": self.isbn, "status": self.status}

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __repr__(self):
        return "Book(title='" + self.title + "', status=" + self.status + ")"

    def __str__(self):
        return self.title + " (Book) - " + self.status


class DVD:
    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        self.title = title
        self.director = director
        self.status = status
        self.loan_period = 5

    def checkout(self):
        if self.status == ItemStatus.CHECKED_OUT:
            raise ValueError("Already checked out.")
        if self.status == ItemStatus.LOST:
            raise ValueError("Item is lost.")
        self.status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self.status == ItemStatus.AVAILABLE:
            raise ValueError("Item was not checked out.")
        self.status = ItemStatus.AVAILABLE

    def mark_lost(self):
        self.status = ItemStatus.LOST

    @classmethod
    def from_dict(cls, d):
        return cls(d["title"], d["director"], d.get("status", ItemStatus.AVAILABLE))

    def to_dict(self):
        return {"type": "DVD", "title": self.title, "director": self.director, "status": self.status}

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __repr__(self):
        return "DVD(title='" + self.title + "', status=" + self.status + ")"

    def __str__(self):
        return self.title + " (DVD) - " + self.status


class Magazine:
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        self.title = title
        self.issue = issue
        self.status = status
        self.loan_period = 14

    def checkout(self):
        if self.status == ItemStatus.CHECKED_OUT:
            raise ValueError("Already checked out.")
        if self.status == ItemStatus.LOST:
            raise ValueError("Item is lost.")
        self.status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self.status == ItemStatus.AVAILABLE:
            raise ValueError("Item was not checked out.")
        self.status = ItemStatus.AVAILABLE

    def mark_lost(self):
        self.status = ItemStatus.LOST

    @classmethod
    def from_dict(cls, d):
        return cls(d["title"], d["issue"], d.get("status", ItemStatus.AVAILABLE))

    def to_dict(self):
        return {"type": "Magazine", "title": self.title, "issue": self.issue, "status": self.status}

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __repr__(self):
        return "Magazine(title='" + self.title + "', status=" + self.status + ")"

    def __str__(self):
        return self.title + " (Magazine) - " + self.status


def parse_item(d):
    t = d.get("type", "").lower()
    if t == "book":
        return Book.from_dict(d)
    elif t == "dvd":
        return DVD.from_dict(d)
    elif t == "magazine":
        return Magazine.from_dict(d)
    else:
        raise ValueError("Unknown type: " + t)


def validate_isbn(code):
    c = code.replace("-", "").replace(" ", "")
    if len(c) != 13 or not c.isdigit():
        return False
    tot = 0
    for i in range(13):
        n = int(c[i])
        if i % 2 == 0:
            tot += n
        else:
            tot += n * 3
    return tot % 10 == 0


class Database:
    _inst = None

    def __new__(cls, path="database.txt"):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.path = path
        return cls._inst

    def load_items(self):
        res = []
        try:
            f = open(self.path, "r")
            for line in f:
                line = line.strip()
                if line != "":
                    d = {}
                    parts = line.split("|")
                    for p in parts:
                        if "=" in p:
                            k, v = p.split("=", 1)
                            d[k.strip()] = v.strip()
                    if d:
                        res.append(parse_item(d))
            f.close()
        except FileNotFoundError:
            pass
        return res

    def save_items(self, items):
        lines = []
        for i in items:
            d = i.to_dict()
            p = []
            for k, v in d.items():
                p.append(k + "=" + str(v))
            lines.append("|".join(p))
        f = open(self.path, "w")
        for line in lines:
            f.write(line + "\n")
        f.close()


class Library:
    def __init__(self, db=None):
        self.items = []
        self.db = db

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def find_by_title(self, title):
        res = []
        for i in self.items:
            if title.lower() in i.title.lower():
                res.append(i)
        return res

    def list_available(self):
        res = []
        for i in self.items:
            if i.status == ItemStatus.AVAILABLE:
                res.append(i)
        return res

    def list_all(self):
        return sorted(self.items)

    def load_from_db(self):
        if self.db:
            self.items = self.db.load_items()

    def save_to_db(self):
        if self.db:
            self.db.save_items(self.items)