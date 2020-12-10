import pandas as pd
import pprint

from modul_nacteni_vstupu import nacti_studenty, nacti_lektory
from modul_vytvoreni_slovniku import create_schedule, print_dict
from modul_vytvoreni_hromadneho import create_schedule_hromadny


studenti = nacti_studenty("vstup_var2_studenti.csv")
print("Celkový počet studentů: " + str(len(studenti)))
print(studenti)


lektori = nacti_lektory("vstup_lektori.csv")
print("Celkový počet lektorů: " + str(len(lektori)))
print(lektori)


# kdyz budu chtit pracovat s necim u jednoho studenta
# print(str(studenti[10].vrat_jmeno()) + ": " + str(studenti[10].vrat_mozne_hodiny()))

# print jednoho lektora
# print(str(lektori[1].vrat_jmeno()) + ": " + str(lektori[1].vrat_mozne_hodiny()))


# VYSTUPY

# ROZVRH LEKTOR 1: zavolat funkci create_schedule a vložit ji do proměnné
new_schedule_lektor1 = create_schedule()
# vytisknout slovník
# print_dict(new_schedule_lektor1)

# ROZVRH LEKTOR 2 - stejně jako lektor 1:
new_schedule_lektor2 = create_schedule()
# print_dict(new_schedule_lektor2)


novy_rozvrh_hromadny2 = create_schedule_hromadny()
# print_dict(novy_rozvrh_hromadny2)


# SEZNAM STUDENTŮ A KURZŮ
list_students_in_course = []
# for student in course:
    # list_students_in_course.append(student)
dict_courses = {}
# dict_courses[course] = list_students_in_course


slovnik_kurzu = {}
for student in studenti:
    course = student.vrat_kurz()
    if course not in slovnik_kurzu.keys():
        slovnik_kurzu[course] = [student]
    else:
        slovnik_kurzu.get(course).append(student)

pprint.pprint(slovnik_kurzu)


for keys, values in slovnik_kurzu.items():
    pocet = len(values)
    print(keys, pocet)



# GENEROVANI ROZVRHU

for kurz, studenti in slovnik_kurzu.items():
    if len(studenti) < 7:
        pass
        # zkontroluj, jestli nemuzou ve stejny cas
        # zkontroluj, jestli v ten cas muze lektor 1 nebo lektor 2
        # pokud jeden z nich ano, zadej kurz do zaverecnyho rozvrhu new_schedule_lektor1
    else:
        # zjistit, jestli existuje moznost dat je po sesti (delitelne 6) a jestli maji lektori volno
            # pokud ano - vytvorit slovnik, kde klicem bude den+hodina a hodnotou bude seznam studentu, kteri muzou
            # jinak pass
        if len(studenti) % 6 == 0:
            novy_slovnik = {}
            for student in studenti:
                for hodina, TF in student.vrat_mozne_hodiny().items():
                    if TF == True:
                        if hodina not in novy_slovnik.keys():
                            novy_slovnik[hodina] = [student]
                        else:
                            novy_slovnik.get(hodina).append(student)
            print(kurz)
            pprint.pprint(novy_slovnik)
        else:
            print(kurz)
            print("počet není dělitelný 6")
