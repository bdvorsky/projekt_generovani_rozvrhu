class Clovek:
    def __init__(self, name, course, mozne_hodiny):
        self.name = name
        self.course = course
        self.mozne_hodiny = mozne_hodiny

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def vrat_jmeno(self):
        return self.name
    
    def vrat_kurz(self):
        return self.course

    def vrat_mozne_hodiny(self):
        return self.mozne_hodiny


class Student(Clovek):
    
    def __init__(self, name, course, mozne_hodiny, cas_kurzu, jeho_lektor):
        Clovek.__init__(self, name, course, mozne_hodiny)
        self.cas_kurzu = cas_kurzu
        self.jeho_lektor = jeho_lektor
    
    def vrat_cas_kurzu(self):
        return self.cas_kurzu
    
    def vrat_jeho_lektora(self):
        return self.jeho_lektor


class Lektor(Clovek):
    
    def __init__(self, name, course, mozne_hodiny, schedule):
        Clovek.__init__(self, name, course, mozne_hodiny)
        self.schedule = schedule

    def vrat_rozvrh(self):
        return self.schedule
