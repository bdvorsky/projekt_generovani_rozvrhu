import pandas as pd
import pprint
import random
import string


# NACTENI VSTUPU

from modul_nacteni_vstupu import nacti_studenty, nacti_lektory
from modul_tridy import Kurz

studenti = nacti_studenty("vstup_var2_studenti.csv")
studenti = random.sample(studenti, len(studenti))   # nahodne zamicham studenty v seznamu

lektori = nacti_lektory("vstup_lektori.csv")

kurzy = []


# GENEROVANI ROZVRHU

def _make_dict_courses():
    """vrati slovnik, kde klicem je kurz a hodnotou seznam danych studentu"""
    slovnik_kurzu = {}
    for student in studenti:
        course = student.course
        if course not in slovnik_kurzu.keys():
            slovnik_kurzu[course] = [student]
        else:
            slovnik_kurzu.get(course).append(student)
    return slovnik_kurzu


# funkce pro rozdeleni na 6:
def divisible_by_six_or_five(list, cislo_na_rozpuleni):
    delka_list = len(list)
    if delka_list % 6 == 0:
        return 6
    elif delka_list % 5 == 0:
        return 5
    else:
        return 0


def divide_slovnik_kurzu(slovnik_kurzu, cislo_na_rozpuleni):
    pprint.pprint(slovnik_kurzu)
    novy_slovnik_kurzu = {}
    for kurz, seznam_studentu in slovnik_kurzu.items():
        if len(seznam_studentu) > 6:
            n = divisible_by_six_or_five(seznam_studentu, cislo_na_rozpuleni)
            if n != 0:
                n_lists = []
                for i in range(0, len(seznam_studentu), n):
                    n_lists.append(seznam_studentu[i:i + n])
                i = 1
                for lst in n_lists:
                    novy_slovnik_kurzu[kurz + "_" + str(i)] = lst
                    i = i + 1
                print(novy_slovnik_kurzu)
            else:
                n_lists = []
                n_lists.append(seznam_studentu[0:6])
                print("halo", kurz)
                print(n_lists)
                del seznam_studentu[0:6]
                print(seznam_studentu)
                if len(seznam_studentu) % 5 == 0:
                    for i in range(0, len(seznam_studentu), 5):
                        n_lists.append(seznam_studentu[i:i+5])
                elif len(seznam_studentu) % 4 == 0:
                    for i in range(0, len(seznam_studentu), 4):
                        n_lists.append(seznam_studentu[i:i+4])
                i = 1
                for lst in n_lists:
                    novy_slovnik_kurzu[kurz + "_" + str(i)] = lst
                    i = i + 1
                
                # vem kurz a najdi šest
                # pokud je zbytek větší než 6
                    # pokud je zbytek dělitelný pěti tak ok
                    # pokud je zbytek dělitelný 4 tak ok
                # jinak najdi 5
                    # pokud je zbytek delitelnej 4 tak ok
    print(novy_slovnik_kurzu)
    return novy_slovnik_kurzu


def _make_dict_main(slovnik_kurzu):
    """vrati slovnik, klicem je kurz, hodnoutou je slovnik
    v nested slovniku je klicem cas
    a hodnotou je seznam studentu z daneho kurzu, kteri muzou v dany cas"""
    slovnik_kurz_cas_studenti = {}
    for kurz, studenti in slovnik_kurzu.items():
        novy_slovnik = {}
        for student in studenti:
            for hodina, TF in student.mozne_hodiny.items():
                if TF:
                    if hodina not in novy_slovnik.keys():
                        novy_slovnik[hodina] = [student]
                    else:
                        novy_slovnik.get(hodina).append(student)
        slovnik_kurz_cas_studenti[kurz] = novy_slovnik
    return slovnik_kurz_cas_studenti


def _lektor_available(cas):
    """zkontroluje, jestli v dany cas alespon jeden z lektoru muze
    a vrati bool"""
    TF = False
    for lektor in lektori:
        TF = lektor.mozne_hodiny[cas]
        if TF:
            return True
    return TF


def _longest_in_dict(slovnik):
    """vstup - slovnik = hodina: seznam studentů co můžou"""
    """vrati slovnik casu, kdy muze nejvic studentu z daneho kurzu a
    seznam techto studentu"""
    nejdelsi = 0
    slovnik_casu_a_seznam_studentu = {}
    for key in slovnik.keys():
        TF = _lektor_available(key)
        if TF:
            podseznam_studenti = slovnik.get(key)
            if len(podseznam_studenti) > nejdelsi:
                nejdelsi = len(podseznam_studenti)
                slovnik_casu_a_seznam_studentu = {}
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
            elif len(podseznam_studenti) == nejdelsi:
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
    return slovnik_casu_a_seznam_studentu


def _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti):
    """vytvori slovnik, kde je klicem kurz a hodnotou slovnik,
    kde je klic cas, ve ktery muze nejvic studentu, hodnotou studenti,
    kteri muzou. Zaroven kontroluje jestli v dany cas muzou lektori
    a vraci jen casy kdy ano"""
    dict_of_courses_and_possible_times = {}
    for key, value in slovnik_kurz_cas_studenti.items():
        dict_of_times = _longest_in_dict(value)
        dict_of_courses_and_possible_times[key] = dict_of_times
    return dict_of_courses_and_possible_times


def rearrange_dict(dict):
    """funkce presklada slovnik -
    na prvni misto da kurzy s nejmene moznostmi na vyber"""
    # TODO: pridat druhe kriterium - cim delsi seznam studentu v hodnote, tim driv ho dat
    sorted_dict = {}
    for i in range(26):
        for klic, hodnota in dict.items():
            if len(hodnota) == i:
                sorted_dict[klic] = hodnota
    return sorted_dict


def _course_not_in_schedule(kurz):
    """zkontroluje, jestli v dany cas alespon jeden z lektoru muze
    a vrati bool"""
    for lektor in lektori:
        if kurz in lektor.schedule.values():
            return False
    return True


def register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz):
    for i in range(len(lektori)):
        if _course_not_in_schedule(kurz + str(varka)):           # pokud kurz ještě není v rozvrhu lektoru
            if lektori[i].mozne_hodiny[cas]:                # if True (jestli lektor v dany cas muze; je uprednostnen lektor 1)
                if lektori[i].schedule[cas] == "":          # pokud čas v rozvrhu ještě není obsazený
                    lektori[i].schedule[cas] = kurz + str(varka)         # pridej do schedule lektora kurz
                    course = Kurz(kurz + str(varka), cas, lektori[i], studenti_konkr_kurz)
                    kurzy.append(course)
                    for student in studenti_konkr_kurz:
                        student.cas_kurzu = cas                 # pridat cas kurzu do atributu tridy Student
                        student.jeho_kurz = kurz + str(varka)
                        student.jeho_lektor = lektori[i]

def main_algorithm(slovnik, varka):
    for kurz, cas_studenti in slovnik.items():           # cas_studenti je vnořený slovník, proto ho rozvíjím o řádek níž
        for cas, studenti_konkr_kurz in cas_studenti.items():                       # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
            register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def find_next_longest(kurz, varka, slovnik):
    slovnik_moznych_casu_kurzu = slovnik[kurz]          # extract dict for one particular course, put it in a new dict
    nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)             # find the longest options in the new dict
    for cas in nejdelsi.keys():
        del slovnik_moznych_casu_kurzu[cas]                             # delete the longest from the new dict
    dalsi_nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)
    for cas, studenti_konkr_kurz in dalsi_nejdelsi.items():           # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
        register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)
    return slovnik_moznych_casu_kurzu


def look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani):
    """mezi zbylymi studenty hleda dalsi pruniky"""
    find_next_longest(kurz, varka, slovnik_kurz_cas_studenti)
    if _course_not_in_schedule(kurz + str(varka)):  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není:
        if opakovani < 10:
            opakovani += 1
            look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani)
        else:
            pass


def all_students_placed(kurz):
    for student in studenti:
        if student.course == kurz and student.jeho_kurz == "":
            return False
    return True


def print_to_html():
    data = []
    for i in range(len(lektori)):
        data = lektori[i].schedule
        df = pd.DataFrame(data, index=[""])
        df = df.fillna('').T
        df.to_html("vystup_lektor" + str(i) + ".html")


def make_schedule():
    # TODO: ošetřit, aby se nevypisovaly nový kurzy s 0 nebo s 1 studenty
    # TODO: zahrnout pocet studentu max 6 na kurz
    slovnik_kurzu = _make_dict_courses()
    slovnik_kurzu = divide_slovnik_kurzu(slovnik_kurzu, 6)

    for i in range(0, 10):
        varka = string.ascii_lowercase[i]

        slovnik_kurz_cas_studenti = _make_dict_main(slovnik_kurzu)
        dict_of_courses_and_possible_times = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti)
        dict_of_courses_and_possible_times = rearrange_dict(dict_of_courses_and_possible_times)

        main_algorithm(dict_of_courses_and_possible_times, varka)
        for kurz, cas_studenti in dict_of_courses_and_possible_times.items():
            if not all_students_placed(kurz):
                if _course_not_in_schedule(kurz + str(varka)):  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet
                    look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani=0)

        the_rest = {}
        for kurz, seznam_studenti in slovnik_kurzu.items():
            students = []
            for student in seznam_studenti:
                if student.cas_kurzu == "":
                    students.append(student)
            the_rest[kurz] = students

        slovnik_kurzu = the_rest

    for lektor in lektori:
        print(lektor)
        pprint.pprint(lektor.schedule)

    for student in studenti:
        if student.jeho_kurz == "":
            print(str(student) + " patřící do kurzu " + str(student.course) + " se nikam nevlezl.")

    print_to_html()


    # zaverecny slovnik, pro kazdeho lektora jeden: cas-kurz-seznam studentu
    slovnik_naprosto_vse = {}
    for lektor in lektori:
        zaverecny_slovnik = {}
        for cas, kurz in lektor.schedule.items():
            if lektor.schedule[cas] != "":
                kurz = lektor.schedule[cas]
                nested_slovnik = {}
                for student in studenti:
                    if student.jeho_kurz == kurz:
                        if kurz not in nested_slovnik.keys():
                            nested_slovnik[kurz] = [student]
                        else:
                            nested_slovnik.get(kurz).append(student)
                zaverecny_slovnik[cas] = nested_slovnik
        slovnik_naprosto_vse[lektor] = zaverecny_slovnik
    # pprint.pprint(slovnik_naprosto_vse)


make_schedule()


# poznamky: