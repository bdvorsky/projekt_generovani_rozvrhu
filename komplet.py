import pandas as pd

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

print(slovnik_kurzu)


for keys, values in slovnik_kurzu.items():
    pocet = len(values)
    print(pocet)



