import pandas as pd


# TŘÍDY
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

    def vrat_mozne_hodiny(self):
        return self.mozne_hodiny



class Student(Clovek):
    def pridej_studenta(self, name, course):
        student = Student(name, course)
        self.studenti.append(student)



class Lektor(Clovek):
    def vrat_rozvrh(self):
        return self.schedule
    # self.mozne_hodiny_lektor = pd.read_csv(mozne_hodiny_lektor, sep=';')        # načtení přes pandas anebo obyč načtení dole --->



# lektor1 = Lektor("Michaela Novotná", "vstup_var2_lektor1.csv")
# lektor2 = Lektor('Alena Vysušilová', 'vstup_var2_lektor2.csv')




# NACTENI VSTUPNICH SOUBORU S DATY STUDENTU A LEKTORŮ

def nacti(soubor, student):
    list_of_people = []
    with open(soubor, encoding="utf-8") as vstup:
        line_counter = 0
        for line in vstup:
            radek = line.strip().split(";")
            if line_counter == 0:
                seznam_prvni_radek = radek
            elif line_counter > 0:
                name = radek[0]
                course = radek[1]
                mozne_hodiny = radek[2:26]      # sloupce 2 az 26 v danem radku --> je to list - hodnoty "ano" nebo prazdna "" 
                if student:
                    clovek = Student(name, course, mozne_hodiny)
                else:
                    clovek = Lektor(name, course, mozne_hodiny)
                list_of_people.append(clovek)        # pridam studenta do seznamu studentu > vznikne seznam hodnot tridy student
            line_counter += 1
    return list_of_people


def nacti_studenty(soubor):
    return nacti(soubor, True)


def nacti_lektory(soubor):
    return nacti(soubor, False)



studenti = nacti_studenty("vstup_var2_studenti.csv")
print("Celkový počet studentů: " + str(len(studenti)))
print(studenti)


lektori = nacti_lektory("vstup_lektori.csv")
print("Celkový počet lektorů: " + str(len(lektori)))
print(lektori)



# kdyz budu chtit pracovat s necim u jednoho studenta
studenti[0].vrat_mozne_hodiny()





# VYSTUPY


days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# ROZVRH LEKTOR 1 - vytvoření zatím prázdného rozvrhu (nested dict: den - hodina - kurz)
# novy_rozvrh_lektor1 = {
#    "monday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "tuesday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "wednesday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "thursday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    "friday": {"13": "", "14": "", "15": "", "16": "", "17": ""},
#    }

# vytvoření (zatím) prázdného rozvrhu
def _create_nested_dict():
    """vytvoří slovník, kde klíčem je určitá hodina a hodnotou je prázdný string nachystaný pro kurz"""
    pole = {}
    for hour in range(13, 18):
        pole[hour] = ""
    return pole


def create_schedule():
    """vytvoří slovník, kde klíčem je den a hodnotou jiný slovník"""
    schedule_lektor = {}
    position_of_day = 0
    for i in range(len(days)):
        pole = _create_nested_dict()
        schedule_lektor[days[position_of_day]] = pole
        position_of_day += 1
    return schedule_lektor

# funkce na tisk
def print_dict(schedule):
    """vytiskne slovnik"""
    for key, value in schedule.items():
        print(key, value)


# ROZVRH LEKTOR 1: zavolat funkci create_schedule a vložit ji do proměnné
new_schedule_lektor1 = create_schedule()
# vytisknout slovník
print_dict(new_schedule_lektor1)

# ROZVRH LEKTOR 2 - stejně jako lektor 1:
new_schedule_lektor2 = create_schedule()
print_dict(new_schedule_lektor2)




# ROZVRH HROMADNÝ - možná zbytečné - místo str v hodnotě pro kurz je list (více kurzů)
# novy_rozvrh_hromadny = {
#    "pondeli": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "utery": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "streda": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "ctvrtek": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    "patek": {"13": [], "14": [], "15": [], "16": [], "17": []},
#    }


def _create_nested_dict_hromadny():
    """vytvoří slovník, kde klíčem je určitá hodina a hodnotou je prázdné pole nachystané pro kurzy"""
    pole = {}
    for hour in range(13, 18):
        pole[hour] = []
    return pole


def create_schedule_hromadny():
    """vytvoří slovník, kde klíčem je den a hodnotou jiný slovník"""
    schedule_hromadny = {}
    position_of_day = 0
    for i in range(len(days)):
        pole = _create_nested_dict_hromadny()
        schedule_hromadny[days[position_of_day]] = pole
        position_of_day += 1
    return schedule_hromadny


novy_rozvrh_hromadny2 = create_schedule_hromadny()
print_dict(novy_rozvrh_hromadny2)



# SEZNAM STUDENTŮ A KURZŮ
list_students_in_course = []
# for student in course:
    # list_students_in_course.append(student)
dict_courses = {}
# dict_courses[course] = list_students_in_course


