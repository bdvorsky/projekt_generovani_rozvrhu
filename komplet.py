import pandas as pd
import pprint


# NACTENI VSTUPU

from modul_nacteni_vstupu import nacti_studenty, nacti_lektory

studenti = nacti_studenty("vstup_var2_lektori.csv")

lektori = nacti_lektory("vstup_lektori.csv")


# GENEROVANI ROZVRHU

def _make_dict_courses(studenti):
    """vrati slovnik, kde klicem je kurz a hodnotou seznam danych studentu"""
    slovnik_kurzu = {}
    for student in studenti:
        course = student.course
        if course not in slovnik_kurzu.keys():
            slovnik_kurzu[course] = [student]
        else:
            slovnik_kurzu.get(course).append(student)
    return slovnik_kurzu


def _make_dict_main(slovnik_kurzu):
    """ vrati slovnik, klicem je kurz, hodnoutou je slovnik
    v nested slovniku je klicem cas a hodnotou je seznam studentu z daneho kurzu, kteri muzou v dany cas"""
    slovnik_kurz_cas_studenti = {}
    for kurz, studenti in slovnik_kurzu.items():
        novy_slovnik = {}
        for student in studenti:
            for hodina, TF in student.mozne_hodiny.items():
                if TF == True:
                    if hodina not in novy_slovnik.keys():
                        novy_slovnik[hodina] = [student]
                    else:
                        novy_slovnik.get(hodina).append(student)
        slovnik_kurz_cas_studenti[kurz] = novy_slovnik
    return slovnik_kurz_cas_studenti


def _lektor_available(cas):
    """zkontroluje, jestli v dany cas alespon jeden z lektoru muze a vrati bool"""
    TF = False
    for lektor in lektori:
        TF = lektor.mozne_hodiny[cas]
        if TF:
            return True
    return TF


def _longest_in_dict(slovnik):
    """vstup - slovnik = hodina: seznam studentů co můžou"""
    """vrati slovnik casu, kdy muze nejvic studentu z daneho kurzu a seznam techto studentu"""
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
    kde je klic cas, ve ktery muze nejvic studentu, a hodnotou studenti, kteri muzou.
    Zaroven kontroluje jestli v dany cas muzou lektori a vraci jen casy kdy ano"""
    dict_of_courses_and_possible_times = {}
    for key, value in slovnik_kurz_cas_studenti.items():
        dict_of_times = _longest_in_dict(value)
        dict_of_courses_and_possible_times[key] = dict_of_times
    return dict_of_courses_and_possible_times


def rearrange_dict(dict):
    """funkce presklada slovnik - na prvni misto da kurzy s nejmene moznostmi na vyber"""
    # TODO: pridat kriterium - cim delsi seznam studentu v hodnote, tim driv ho dat
    sorted_dict = {}
    pocet_klicu = len(dict)
    for i in range(26):
        for klic, hodnota in dict.items():
            if len(hodnota) == i:
                sorted_dict[klic] = hodnota
    return sorted_dict


def register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz):
    for i in range(len(lektori)):
        if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():            # pokud kurz ještě není v rozvrhu lektora --> aby se nevypsal dvakrát, !limitováno 2 lektory - pokud kurz nebyl zapsán u předchozího lektora --> vymyslet jinak
            if lektori[i].mozne_hodiny[cas]:                # if True (jestli lektor v dany cas muze, je uprednostnen lektor 1)
                if lektori[i].schedule[cas] == "":          # pokud čas v rozvrhu ještě není obsazený
                    lektori[i].schedule[cas] = kurz + str(varka)         # pridej do schedule lektora kurz
                    for student in studenti_konkr_kurz:
                        student.cas_kurzu = cas
                        student.jeho_kurz = kurz + str(varka)
                        student.jeho_lektor = lektori[i]             # pridat cas kurzu do atributu tridy Student


def main_algorithm(slovnik, varka):
    for kurz, cas_studenti in slovnik.items():           # cas_studenti je vnořený slovník, proto ho rozvíjím o řádek níž
        for cas, studenti_konkr_kurz in cas_studenti.items():                       # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
            register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def find_next_longest(kurz, varka, slovnik):
    slovnik_moznych_casu_kurzu = slovnik[kurz]          # extract dict for one particular course, put it in a new dict                     
    nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)             # find the longest options in the new dict
    print(str(kurz) + " nejdelší: " + str(nejdelsi))
    for cas in nejdelsi.keys():
        del slovnik_moznych_casu_kurzu[cas]                             # delete the longest from the new dict
    dalsi_nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)
    print(str(kurz) + " další nejdelší: " + str(dalsi_nejdelsi))
    for cas, studenti_konkr_kurz in dalsi_nejdelsi.items():           # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
        register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)
    return slovnik_moznych_casu_kurzu


def look_for_next(kurz, varka, slovnik_kurz_cas_studenti):
    """mezi zbylymi studenty hleda dalsi pruniky"""
    print(kurz, varka)
    bez_nejdelsiho = find_next_longest(kurz, varka, slovnik_kurz_cas_studenti)
    i = 0
    if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není:
        if i < 10:
            bez_nejdelsiho = look_for_next(kurz, varka, bez_nejdelsiho)
        else:
            print("Nebylo možné najít další nejdelší a umístit kurz.")


def all_students_placed(kurz):
    for student in studenti:
        if student.course == kurz:
            if student.jeho_kurz == "":
                return False
    return True



def make_schedule():
    # TODO: ošetřit, aby se nevypisovaly nový kurzy s 0 nebo s 1 studenty
    # TODO: zahrnout pocet studentu max 6 na kurz
    # TODO: zjistit, proc se nechce vypsat key (najit dalsi moznost nejdelsiho)
    # problem bude asi v tech funkcich longest a a find next longest -- asi špatně zadané vstupy, line 175?
    slovnik_kurzu = _make_dict_courses(studenti)

    # print("Počet studentů v kurzu")
    # for keys, values in slovnik_kurzu.items():
        # print((str(keys)) + ": " + str(len(values)))

    slovnik_kurz_cas_studenti = _make_dict_main(slovnik_kurzu)
    # print(slovnik_kurz_cas_studenti)
    dict_of_courses_and_possible_times = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti)
    # pprint.pprint(dict_of_courses_and_possible_times)
    dict_of_courses_and_possible_times = rearrange_dict(dict_of_courses_and_possible_times)


    # TODO: udělat for cyklus for varka in range(5)
    varka = 1
    main_algorithm(dict_of_courses_and_possible_times, varka)
    for kurz, cas_studenti in dict_of_courses_and_possible_times.items():
        if not all_students_placed(kurz):
            if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet   
                look_for_next(kurz, varka, slovnik_kurz_cas_studenti)

    the_rest = {}
    for kurz, seznam_studenti in slovnik_kurzu.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
        the_rest[kurz] = students
    print()
    print("the_rest:")
    print(the_rest)
    slovnik_kurz_cas_studenti2 = _make_dict_main(the_rest)
    dict_of_courses_and_possible_times2 = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti2)
    dict_of_courses_and_possible_times2 = rearrange_dict(dict_of_courses_and_possible_times2)
    print(dict_of_courses_and_possible_times2)
    

    varka = 2
    main_algorithm(dict_of_courses_and_possible_times2, varka)
    for kurz, cas_studenti in dict_of_courses_and_possible_times2.items():
        if not all_students_placed(kurz):
            if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet   
                look_for_next(kurz, varka, slovnik_kurz_cas_studenti)


    the_rest_rest = {}
    for kurz, seznam_studenti in slovnik_kurzu.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
            the_rest_rest[kurz] = students
    print()
    print("the_rest_rest:")
    print(the_rest_rest)
    slovnik_kurz_cas_studenti3 = _make_dict_main(the_rest_rest)
    dict_of_courses_and_possible_times3 = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti3)
    dict_of_courses_and_possible_times3 = rearrange_dict(dict_of_courses_and_possible_times3)
    print(dict_of_courses_and_possible_times3)

    varka = 3
    main_algorithm(dict_of_courses_and_possible_times3, varka)
    for kurz, cas_studenti in dict_of_courses_and_possible_times3.items():
        if not all_students_placed(kurz):
            if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet   
                print(kurz)
                print(209)
                # look_for_next(kurz, varka, slovnik_kurz_cas_studenti)


    the_rest_rest_rest = {}
    for kurz, seznam_studenti in slovnik_kurzu.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
            the_rest_rest_rest[kurz] = students
    print()
    print("the_rest_rest_rest:")
    print(the_rest_rest_rest)
    slovnik_kurz_cas_studenti4 = _make_dict_main(the_rest_rest_rest)
    dict_of_courses_and_possible_times4 = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti4)
    dict_of_courses_and_possible_times4 = rearrange_dict(dict_of_courses_and_possible_times4)

    varka = 4
    main_algorithm(dict_of_courses_and_possible_times4, varka)
    for kurz, cas_studenti in dict_of_courses_and_possible_times4.items():
        if not all_students_placed(kurz):
            if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet   
                print(kurz + str(varka))
            # look_for_next(kurz, varka, slovnik_kurz_cas_studenti)
    

    the_rest_rest_rest_rest = {}
    for kurz, seznam_studenti in slovnik_kurzu.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
            the_rest_rest_rest_rest[kurz] = students
    print()
    print("the_rest_rest_rest_rest:")
    print(the_rest_rest_rest_rest)
    slovnik_kurz_cas_studenti5 = _make_dict_main(the_rest_rest_rest_rest)
    dict_of_courses_and_possible_times5 = _make_dict_of_courses_and_possible_times(slovnik_kurz_cas_studenti5)
    dict_of_courses_and_possible_times5 = rearrange_dict(dict_of_courses_and_possible_times5)

    varka = 5
    main_algorithm(dict_of_courses_and_possible_times5, varka)
    for kurz, cas_studenti in dict_of_courses_and_possible_times.items():
        if not all_students_placed(kurz):
            if kurz + str(varka) not in lektori[0].schedule.values() and kurz + str(varka) not in lektori[1].schedule.values():  # pokud si vyzkoušel všechny lektory i casy a kurz tam pořád není: - u mych dat pro pet   
                print(kurz + str(varka))
                # look_for_next(kurz, varka, slovnik_kurz_cas_studenti)

    for lektor in lektori:
        print(lektor)
        pprint.pprint(lektor.schedule)



    # for student in studenti:
        # print(student)
        # print(student.jeho_kurz)


    # PRINT TO HTML

    # data = []
    # dat = lektor.schedule
    # df = pd.DataFrame(data, index=[""])
    # df = df.fillna('').T
    # df.to_html("vystup.html")
        
make_schedule()



# poznamky:


# funkce pro rozdeleni na 6: 
# def chunks(lst, n):
# """Yield successive n-sized chunks from lst."""
    # for i in range(0, len(lst), n):
    # yield lst[i:i + n]

# def find_chunk_size(list, cislo_na_rozpuleni):
    # delka_list = len(list)
    # if delka_list/2 > cislo_na_rozpuleni:
        # if delka_list/3 > cislo_na_rozpuleni:
            # return delka_list//4
        # else:
            # return delka_list//3
    # else:
        # return delka_list//2  

# def rozsekej_slovnik_kurzu(slovnik_kurzu, cislo_na_rozpuleni):
    # for key in list(slovnik_kurzu):
        # if len(slovnik_kurzu.get(key)) > 6:
            # n_lists = chunks(slovnik_kurzu.get(key),find_chunk_size(slovnik_kurzu.get(key),cislo_na_rozpuleni))
            # i = 1
            # for lst in n_lists:
                # slovnik_kurzu[key + "_" + str(i)] = lst
                # i = i + 1
            # del slovnik_kurzu[key]
        
# rozsekej_slovnik_kurzu(slovnik_kurzu,6)


    # for klic, hodnota in dict_of_courses_and_possible_times.items():      # klicem je kurz
        # najdi studenty, kteri maji ve slovnik_kurz_cas_studenti dany klic
        # najdi studenty, kteri NEmaji v dany cas cas a hledej, jestli maji nejaky spolecny
        # pro key, value in hodnota.items():
            # 


# najdi ostatní studenty pro první, jestli mají společný termín a může v něm lektor
# pokud ano, zapiš je do rozvrhu lektora
# najdi ostatní studenty pro druhý kurz


    # preskladej kurzy ve slovniku podle delky hodnoty
    # vezmi prvni den a dej ho do výsledného rozvrhu prvniho lektora, ktery muze
    # vezmi dalsi a dalsi den a dej ho do vysledneho rozvrhu lektora
        # pokud je tam uz obsazeno
            # zjisti, jestli je moznost u druheho lektora a dej ho druhemu lektorovi
            # pokud lektor nemuze, zjisti dalsi casovou moznost pro kurz
            # pokud dany kurz nema dalsi moznost, pro kterou by bylo volno
                # vrat se k obsazenemu policku a zjisti, jestli kurz v dany cas nema jinou casovou moznost a presun jej
    # pokud neni jina casovy moznost, najdi cas, kdy muze druhy nejvyssi pocet studentu


# rozdelit podle poctu v kurzu
# menší než 7
    # if len(studenti) < 7:
# existuje moznost dat je po 6? --> dělitelný 6?
    # if len(studenti) % 6 == 0: