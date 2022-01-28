import pandas as pd
import pprint
import os


# NACTENI VSTUPU


from modul_nacteni_vstupu import nacti_studenty, nacti_lektory
from modul_tridy import Kurz

studenti = nacti_studenty("vstup_var2_studenti.csv")

lektori = nacti_lektory("vstup_lektori.csv")

kurzy = []


# FUNKCE PRO GENEROVANI ROZVRHU

def _make_dict_courses():
    """vrátí slovník, kde klíčem je kurz a hodnotou je
    seznam všech studentů, kteří chtějí studovat tento kurz"""
    slovnik_kurzu = {}
    for student in studenti:
        course = student.course
        if course not in slovnik_kurzu.keys():
            slovnik_kurzu[course] = [student]
        else:
            slovnik_kurzu.get(course).append(student)
    return slovnik_kurzu


def _make_dict_main(slovnik_kurzu):
    """vrati slovnik, klicem je kurz, hodnoutou je nested
    slovnik - v nested slovniku je klicem cas a hodnotou je
    seznam studentu z daneho kurzu, kteri muzou v dany cas"""
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
    """vstup - slovnik = hodina: seznam studentů, kteří můžou"""
    """vrati slovnik casu, kdy muze nejvic studentu z daneho
    kurzu a seznam techto studentu"""
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
    """vytvori slovnik, kde je klicem kurz a hodnotou nested slovnik,
    kde je klic cas, ve ktery muze nejvic studentu, hodnotou studenti,
    kteri muzou. Zaroven kontroluje jestli v dany cas muzou lektori
    a vraci jen casy kdy ano"""
    dict_of_courses_and_possible_times = {}
    for key, value in slovnik_kurz_cas_studenti.items():
        dict_of_times = _longest_in_dict(value)
        dict_of_courses_and_possible_times[key] = dict_of_times
    return dict_of_courses_and_possible_times


def rearrange_dict(dict):
    """funkce presklada slovnik - na prvni
    misto da kurzy s nejmene moznostmi na vyber"""
    sorted_dict = {}
    for i in range(26):
        for klic, hodnota in dict.items():
            if len(hodnota) == i:
                sorted_dict[klic] = hodnota
    return sorted_dict


def _course_not_in_schedule(kurz):
    """zkontroluje, jestli v dany cas alespon
    jeden z lektoru muze a vrati bool"""
    for lektor in lektori:
        if kurz in lektor.schedule.values():
            return False
    return True


def _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz):
    for i in range(len(lektori)):
        # pokud kurz ještě není v rozvrhu lektoru
        if _course_not_in_schedule(kurz + str(varka)):
            # if True (jestli lektor v dany cas muze; je uprednostnen lektor 1)
            if lektori[i].mozne_hodiny[cas]:
                # pokud čas v rozvrhu ještě není obsazený
                if lektori[i].schedule[cas] == "":
                    # pridej do schedule lektora kurz
                    lektori[i].schedule[cas] = kurz + str(varka)
                    course = Kurz(kurz, kurz + str(varka), cas, lektori[i], studenti_konkr_kurz)
                    kurzy.append(course)
                    for student in studenti_konkr_kurz: # pridat atributy
                        student.cas_kurzu = cas
                        student.jeho_kurz = kurz + str(varka)
                        student.jeho_lektor = lektori[i]


def main_algorithm(slovnik, varka):
    for kurz, cas_studenti in slovnik.items():           # cas_studenti je vnořený slovník, proto ho rozvíjím o řádek níž
        for cas, studenti_konkr_kurz in cas_studenti.items():     # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
            _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def find_next_longest(kurz, varka, slovnik):
    slovnik_moznych_casu_kurzu = slovnik[kurz]        # extract dict for one particular course, put it in a new dict
    nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)       # find the longest options in new dict
    for cas in nejdelsi.keys():
        del slovnik_moznych_casu_kurzu[cas]      # delete longest from new dict
    dalsi_nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)
    for cas, studenti_konkr_kurz in dalsi_nejdelsi.items():       # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
        _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def _look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani):
    """mezi zbylymi studenty hleda dalsi pruniky"""
    find_next_longest(kurz, varka, slovnik_kurz_cas_studenti)
    if _course_not_in_schedule(kurz + str(varka)):  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není:
        if opakovani < 10:
            opakovani += 1
            _look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani)


def all_students_placed(kurz):
    for student in studenti:
        if student.course == kurz and student.jeho_kurz == "":
            return False
    return True


def the_rest(slovnik_kurzu):
    """najde studenty, kteri jeste nikde nejsou, a da
    je do slovniku: klicem je kurz a hodnotou je seznam
    studentu z tohoto kurzu, kteri jeste nikde nejsou"""
    the_rest = {}
    for kurz, seznam_studenti in slovnik_kurzu.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
        the_rest[kurz] = students
    return the_rest


def make_final_dict():
    """vytvoří zanořený slovník lektor-čas-kurz-seznam studentů"""
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
    return slovnik_naprosto_vse


def _go_through_courses(course, cas, ucitel):
    for kurz in kurzy:
        for student in kurz.seznam_studentu:
            if str(student.course) in str(course) and student.mozne_hodiny[cas]:
                if str(kurz.original) in str(course):
                    for leccion in kurzy:
                        if str(leccion) == str(course):
                            pocet_zaku = len(leccion.seznam_studentu)
                            if len(kurz.seznam_studentu) > pocet_zaku and student.jeho_kurz != course:
                                    kurz.seznam_studentu.remove(student)
                                    student.cas_kurzu = cas
                                    student.jeho_kurz = course
                                    student.jeho_lektor = ucitel
                                    leccion.seznam_studentu.append(student)


def regroup_students(slovnik_naprosto_vse):
    """Přeskládá studenty v kurzech na rovnoměrné počty"""
    for i in range(7):
        for ucitel, vse in slovnik_naprosto_vse.items():
            for cas, slovnik in vse.items():
                for course, seznam_st in slovnik.items():
                    if i == len(seznam_st):
                        _go_through_courses(course, cas, ucitel)


def print_to_html():
    data = []
    for i in range(len(lektori)):
        data = lektori[i].schedule
        df = pd.DataFrame(data, index=[""])
        df = df.fillna('').T
        df.to_html("vystup_lektor" + str(i) + ".html")
        os.startfile("vystup_lektor" + str(i) + ".html")


def make_schedule():
    """volá všechny funkce tak, aby se vytvořil
    závěrečný slovník a vytiskl se do html"""
    slovnik_kurzu = _make_dict_courses()
    for varka in range(1, 10):
        slovnik_kurz_cas_studenti = _make_dict_main(slovnik_kurzu)
        dict_of_courses_and_possible_times = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti)
        dict_of_courses_and_possible_times = rearrange_dict(dict_of_courses_and_possible_times)
        main_algorithm(dict_of_courses_and_possible_times, varka)
        for kurz, cas_studenti in dict_of_courses_and_possible_times.items():
            if not all_students_placed(kurz):
                if _course_not_in_schedule(kurz + str(varka)):  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není
                    _look_for_next(kurz, varka, slovnik_kurz_cas_studenti, opakovani=0)
        slovnik_kurzu = the_rest(slovnik_kurzu)
    for student in studenti:
        if student.jeho_kurz == "":
            print(str(student) + " patřící do kurzu " + str(student.course) + " se nikam nevlezl.")

    print_to_html()

    # zaverecny slovnik, pro kazdeho lektora: lektor-cas-kurz-seznam studentu
    slovnik_naprosto_vse = make_final_dict()

    # rozdeleni podle poctu studentu v kurzu - cil najit rovnomernou kombinace
    regroup_students(slovnik_naprosto_vse)

    # zaverecny slovnik znovu pro print
    slovnik_naprosto_vse = make_final_dict()
    pprint.pprint(slovnik_naprosto_vse)


make_schedule()