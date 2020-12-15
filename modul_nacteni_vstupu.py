from modul_tridy import Student, Lektor


def _pridej_do_dict_moznych_hod(nadpisy_hodin, mozne_hodiny, casove_moznosti):
    for i in range(0, 25):
        if casove_moznosti[i] == "ano":
            dostupny = True
        elif casove_moznosti[i] == "":
            dostupny = False
        mozne_hodiny[nadpisy_hodin[i]] = dostupny


def nacti(soubor, je_student):
    """nacte vstupni soubor radek po radku a rozdeli dle sloupcu na jmeno, kurz a casove moznosti, 
    a priradi kazdemu cloveku tridu student nebo lektor a zaradi je do listu"""
    list_of_people = []
    with open(soubor, encoding="utf-8") as vstup:
        line_counter = 0
        for line in vstup:
            mozne_hodiny = {}
            radek = line.strip().split(";")
            if line_counter == 0:
                nadpisy_hodin = radek[2:27]
            elif line_counter > 0:
                name = radek[0]
                course = radek[1]
                _pridej_do_dict_moznych_hod(nadpisy_hodin, mozne_hodiny, casove_moznosti=radek[2:27])
                if je_student:
                    clovek = Student(name, course, mozne_hodiny, cas_kurzu="")
                else:
                    clovek = Lektor(name, course, mozne_hodiny, schedule={})
                list_of_people.append(clovek)        # pridam studenta do seznamu studentu -> vznikne seznam hodnot tridy student
            line_counter += 1
    return list_of_people


def nacti_studenty(soubor):
    return nacti(soubor, True)


def nacti_lektory(soubor):
    return nacti(soubor, False)
