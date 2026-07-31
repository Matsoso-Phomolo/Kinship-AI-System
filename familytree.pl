/* =========================================================
   KINSHIP AI
   LELOKO LA NTATE MOLELEKI MATSOSO

   Family Knowledge Base and Symbolic Reasoning Engine
========================================================= */


/* =========================================================
   PEOPLE / GENDER FACTS
========================================================= */


/* ---------------------------------------------------------
   Generation 1
--------------------------------------------------------- */

male(ntsonyana).
female(mamoleleki).


/* ---------------------------------------------------------
   Generation 2
--------------------------------------------------------- */

male(moleleki).
female(mankole).


/* ---------------------------------------------------------
   Generation 3
   Children of Moleleki Matsoso and Mankole Matsoso
--------------------------------------------------------- */

female(nkole).
female(koba).
male(seabata).
female(mapitso).
male(nkujoana).
female(lipuo).
male(lephoto).
female(puleng).


/* ---------------------------------------------------------
   Spouses / former spouses / partners
--------------------------------------------------------- */

male(nkopane_spouse).

female(matsabo).

female(mamorena).
female(masekoati).
female(makatleho).

female(mamojalefa).
female(mamojakisane).

male(sipho_dangala).


/* ---------------------------------------------------------
   Generation 4
--------------------------------------------------------- */

/* Koba's children */

male(nare_nkopane).
male(lebohang_nkopane).


/* Mapitso's children */

male(lehlohonolo).
male(rorisang).


/* Nkujoana + 'Mamorena */

male(morena).
female(lisemelo).
female(khabane).


/* 'Masekoati's daughter */

female(lieketseng).


/* 'Makatleho's children from before current marriage */

male(katleho_makatleho_son).
female(nthabiseng).


/* Nkujoana + 'Makatleho */

male(eketsang).


/* Lipuo's children */

female(likeleli).
female(nthatuoa).
male(letlotlo).
female(mamosa).


/* Lephoto + 'Mamojalefa */

male(mojalefa).
male(tsepiso).


/* Puleng's children */

female(nthati).
male(phomolo).
female(lintle).


/* ---------------------------------------------------------
   Generation 5
--------------------------------------------------------- */

/* Morena + 'Mamojakisane */

male(mojakisane).
male(amohelang).


/* Lisemelo's child */

male(reitumetse_mokiti).


/* Likeleli's child */

male(katleho_likeleli_son).


/* Nthatuoa + Sipho Dangala */

male(lukhanyo_dangala).
male(leviwe_dangala).


/* Nthati's child */

female(atlehang).


/* =========================================================
   DISPLAY NAMES

   Internal IDs remain unique and simple.
   Human-facing names may contain spaces, apostrophes,
   surname changes, or duplicate current names.
========================================================= */


/* Generation 1 */

display_name(ntsonyana, "Nts'onyana Matsoso").
display_name(mamoleleki, "Mamoleleki Matsoso").


/* Generation 2 */

display_name(moleleki, "Moleleki Matsoso").
display_name(mankole, "Mankole Matsoso").


/* Generation 3 */

display_name(nkole, "Nkole Matsoso").
display_name(koba, "Koba Matsoso").
display_name(seabata, "Seabata Matsoso").
display_name(mapitso, "Mapitso Matsoso").
display_name(nkujoana, "Nkujoana Matsoso").
display_name(lipuo, "Lipuo Matsoso").
display_name(lephoto, "Lephoto Matsoso").
display_name(puleng, "Puleng Matsoso").


/* Spouses / former spouses */

display_name(nkopane_spouse, "Mr Nkopane").

display_name(matsabo, "'Mats'abo Matsoso").

display_name(mamorena, "'Mamorena Matsoso").
display_name(masekoati, "'Masekoati Matsoso").
display_name(makatleho, "'Makatleho Matsoso").

display_name(mamojalefa, "'Mamojalefa Matsoso").
display_name(mamojakisane, "'Mamojakisane Matsoso").

display_name(sipho_dangala, "Sipho Dangala").


/* Generation 4 */

display_name(nare_nkopane, "Nare Nkopane").
display_name(lebohang_nkopane, "Lebohang Nkopane").

display_name(lehlohonolo, "Lehlohonolo Matsoso").
display_name(rorisang, "Rorisang Matsoso").

display_name(morena, "Morena Matsoso").
display_name(lisemelo, "Lisemelo Matsoso").
display_name(khabane, "Khabane Matsoso").

display_name(lieketseng, "Lieketseng").

display_name(
    katleho_makatleho_son,
    "Katleho Matsoso"
).

display_name(
    nthabiseng,
    "Nthabiseng Matsoso"
).

display_name(eketsang, "Eketsang Matsoso").

display_name(likeleli, "Likeleli Matsoso").
display_name(nthatuoa, "Nthatuoa Matsoso").
display_name(letlotlo, "Letlotlo Matsoso").
display_name(mamosa, "Mamosa Matsoso").

display_name(mojalefa, "Mojalefa Matsoso").
display_name(tsepiso, "Ts'episo Matsoso").

display_name(nthati, "Nthati Matsoso").
display_name(phomolo, "Phomolo Matsoso").
display_name(lintle, "Lintle Matsoso").


/* Generation 5 */

display_name(mojakisane, "Mojakisane Matsoso").
display_name(amohelang, "Amohelang Matsoso").

display_name(
    reitumetse_mokiti,
    "Reitumetse Mokiti"
).

display_name(
    katleho_likeleli_son,
    "Katleho Matsoso"
).

display_name(
    lukhanyo_dangala,
    "Luk'hanyo Dangala"
).

display_name(
    leviwe_dangala,
    "Leviwe Dangala"
).

display_name(
    atlehang,
    "Atlehang Matsoso"
).


/* =========================================================
   ALIASES / FORMER NAMES / MARRIAGE NAMES
========================================================= */


/* Nthatuoa's marriage name */

alias(
    nthatuoa,
    "Nok'hanyo Dangala"
).


/* Katleho Matsoso:
   child of 'Makatleho Matsoso
   formerly Mokoena Mariti
*/

former_name(
    katleho_makatleho_son,
    "Mokoena Mariti"
).


/* Nthabiseng Matsoso:
   formerly Nthabiseng Mariti
*/

former_name(
    nthabiseng,
    "Nthabiseng Mariti"
).


/* =========================================================
   PARENT FACTS

   parent_of(Parent, Child).
========================================================= */


/* ---------------------------------------------------------
   Nts'onyana + Mamoleleki -> Moleleki
--------------------------------------------------------- */

parent_of(
    ntsonyana,
    moleleki
).

parent_of(
    mamoleleki,
    moleleki
).


/* ---------------------------------------------------------
   Moleleki + Mankole -> 8 children
--------------------------------------------------------- */

parent_of(moleleki, nkole).
parent_of(mankole, nkole).

parent_of(moleleki, koba).
parent_of(mankole, koba).

parent_of(moleleki, seabata).
parent_of(mankole, seabata).

parent_of(moleleki, mapitso).
parent_of(mankole, mapitso).

parent_of(moleleki, nkujoana).
parent_of(mankole, nkujoana).

parent_of(moleleki, lipuo).
parent_of(mankole, lipuo).

parent_of(moleleki, lephoto).
parent_of(mankole, lephoto).

parent_of(moleleki, puleng).
parent_of(mankole, puleng).


/* ---------------------------------------------------------
   Koba -> Nare and Lebohang

   The spouse is known to exist, but his first name was
   not provided, so biological parenthood is not invented.
--------------------------------------------------------- */

parent_of(
    koba,
    nare_nkopane
).

parent_of(
    koba,
    lebohang_nkopane
).


/* ---------------------------------------------------------
   Mapitso -> Lehlohonolo and Rorisang
--------------------------------------------------------- */

parent_of(
    mapitso,
    lehlohonolo
).

parent_of(
    mapitso,
    rorisang
).


/* ---------------------------------------------------------
   Nkujoana + 'Mamorena -> Morena, Lisemelo, Khabane
--------------------------------------------------------- */

parent_of(
    nkujoana,
    morena
).

parent_of(
    mamorena,
    morena
).

parent_of(
    nkujoana,
    lisemelo
).

parent_of(
    mamorena,
    lisemelo
).

parent_of(
    nkujoana,
    khabane
).

parent_of(
    mamorena,
    khabane
).


/* ---------------------------------------------------------
   'Masekoati's daughter Lieketseng

   Nkujoana is not recorded as biological parent.
--------------------------------------------------------- */

parent_of(
    masekoati,
    lieketseng
).


/* ---------------------------------------------------------
   'Makatleho's children before marriage to Nkujoana

   Katleho Matsoso formerly Mokoena Mariti
   Nthabiseng Matsoso formerly Nthabiseng Mariti

   Nkujoana is not recorded as biological parent.
--------------------------------------------------------- */

parent_of(
    makatleho,
    katleho_makatleho_son
).

parent_of(
    makatleho,
    nthabiseng
).


/* ---------------------------------------------------------
   Nkujoana + 'Makatleho -> Eketsang
--------------------------------------------------------- */

parent_of(
    nkujoana,
    eketsang
).

parent_of(
    makatleho,
    eketsang
).


/* ---------------------------------------------------------
   Lipuo -> 4 children
--------------------------------------------------------- */

parent_of(
    lipuo,
    likeleli
).

parent_of(
    lipuo,
    nthatuoa
).

parent_of(
    lipuo,
    letlotlo
).

parent_of(
    lipuo,
    mamosa
).


/* ---------------------------------------------------------
   Lephoto + 'Mamojalefa -> 2 sons
--------------------------------------------------------- */

parent_of(
    lephoto,
    mojalefa
).

parent_of(
    mamojalefa,
    mojalefa
).

parent_of(
    lephoto,
    tsepiso
).

parent_of(
    mamojalefa,
    tsepiso
).


/* ---------------------------------------------------------
   Puleng -> Nthati, Phomolo, Lintle
--------------------------------------------------------- */

parent_of(
    puleng,
    nthati
).

parent_of(
    puleng,
    phomolo
).

parent_of(
    puleng,
    lintle
).


/* ---------------------------------------------------------
   Morena + 'Mamojakisane -> 2 sons
--------------------------------------------------------- */

parent_of(
    morena,
    mojakisane
).

parent_of(
    mamojakisane,
    mojakisane
).

parent_of(
    morena,
    amohelang
).

parent_of(
    mamojakisane,
    amohelang
).


/* ---------------------------------------------------------
   Lisemelo -> Reitumetse Mokiti
--------------------------------------------------------- */

parent_of(
    lisemelo,
    reitumetse_mokiti
).


/* ---------------------------------------------------------
   Likeleli -> Katleho Matsoso

   This is the second distinct person whose current name
   is also Katleho Matsoso.
--------------------------------------------------------- */

parent_of(
    likeleli,
    katleho_likeleli_son
).


/* ---------------------------------------------------------
   Nthatuoa + Sipho Dangala -> 2 sons
--------------------------------------------------------- */

parent_of(
    nthatuoa,
    lukhanyo_dangala
).

parent_of(
    sipho_dangala,
    lukhanyo_dangala
).

parent_of(
    nthatuoa,
    leviwe_dangala
).

parent_of(
    sipho_dangala,
    leviwe_dangala
).


/* ---------------------------------------------------------
   Nthati -> Atlehang
--------------------------------------------------------- */

parent_of(
    nthati,
    atlehang
).


/* =========================================================
   MARRIAGE FACTS

   married_to(Person1, Person2)

   Current marriages only.
========================================================= */


/* Moleleki + Mankole */

married_to(
    moleleki,
    mankole
).

married_to(
    mankole,
    moleleki
).


/* Koba + Nkopane spouse */

married_to(
    koba,
    nkopane_spouse
).

married_to(
    nkopane_spouse,
    koba
).


/* Seabata + 'Mats'abo */

married_to(
    seabata,
    matsabo
).

married_to(
    matsabo,
    seabata
).


/* Nkujoana + 'Makatleho */

married_to(
    nkujoana,
    makatleho
).

married_to(
    makatleho,
    nkujoana
).


/* Lephoto + 'Mamojalefa */

married_to(
    lephoto,
    mamojalefa
).

married_to(
    mamojalefa,
    lephoto
).


/* Morena + 'Mamojakisane */

married_to(
    morena,
    mamojakisane
).

married_to(
    mamojakisane,
    morena
).


/* Nthatuoa + Sipho Dangala */

married_to(
    nthatuoa,
    sipho_dangala
).

married_to(
    sipho_dangala,
    nthatuoa
).


/* =========================================================
   PREVIOUS MARRIAGES

   Used for marriage history.
========================================================= */


/* Nkujoana + 'Mamorena */

previously_married_to(
    nkujoana,
    mamorena
).

previously_married_to(
    mamorena,
    nkujoana
).


/* Nkujoana + 'Masekoati */

previously_married_to(
    nkujoana,
    masekoati
).

previously_married_to(
    masekoati,
    nkujoana
).


/* =========================================================
   STEP-PARENT RELATIONSHIPS

   These are intentionally separate from biological
   parent_of/2 facts.
========================================================= */


/* Nkujoana became step-parent to 'Masekoati's daughter */

step_parent_of(
    nkujoana,
    lieketseng
).


/* Nkujoana became step-parent to 'Makatleho's children */

step_parent_of(
    nkujoana,
    katleho_makatleho_son
).

step_parent_of(
    nkujoana,
    nthabiseng
).


/* =========================================================
   BIRTH ORDER

   birth_order(Person, Position)
========================================================= */


/* ---------------------------------------------------------
   Children of Moleleki + Mankole
--------------------------------------------------------- */

birth_order(nkole, 1).
birth_order(koba, 2).
birth_order(seabata, 3).
birth_order(mapitso, 4).
birth_order(nkujoana, 5).
birth_order(lipuo, 6).
birth_order(lephoto, 7).
birth_order(puleng, 8).


/* ---------------------------------------------------------
   Koba's children
--------------------------------------------------------- */

birth_order(nare_nkopane, 1).
birth_order(lebohang_nkopane, 2).


/* ---------------------------------------------------------
   Mapitso's children
--------------------------------------------------------- */

birth_order(lehlohonolo, 1).
birth_order(rorisang, 2).


/* ---------------------------------------------------------
   Nkujoana + 'Mamorena
--------------------------------------------------------- */

birth_order(morena, 1).
birth_order(lisemelo, 2).
birth_order(khabane, 3).


/* ---------------------------------------------------------
   'Makatleho's children from before Nkujoana

   Known order from your description.
--------------------------------------------------------- */

birth_order(
    katleho_makatleho_son,
    1
).

birth_order(
    nthabiseng,
    2
).


/* ---------------------------------------------------------
   Nkujoana + 'Makatleho

   First child together
--------------------------------------------------------- */

birth_order(
    eketsang,
    1
).


/* ---------------------------------------------------------
   Lipuo's children
--------------------------------------------------------- */

birth_order(likeleli, 1).
birth_order(nthatuoa, 2).
birth_order(letlotlo, 3).
birth_order(mamosa, 4).


/* ---------------------------------------------------------
   Lephoto + 'Mamojalefa
--------------------------------------------------------- */

birth_order(mojalefa, 1).
birth_order(tsepiso, 2).


/* ---------------------------------------------------------
   Puleng's children
--------------------------------------------------------- */

birth_order(nthati, 1).
birth_order(phomolo, 2).
birth_order(lintle, 3).


/* ---------------------------------------------------------
   Morena + 'Mamojakisane
--------------------------------------------------------- */

birth_order(mojakisane, 1).
birth_order(amohelang, 2).


/* ---------------------------------------------------------
   Nthatuoa + Sipho Dangala
--------------------------------------------------------- */

birth_order(
    lukhanyo_dangala,
    1
).

birth_order(
    leviwe_dangala,
    2
).


/* =========================================================
   BASIC RELATIONSHIP RULES
========================================================= */


/* Father */

father_of(Father, Child) :-
    male(Father),
    parent_of(Father, Child).


/* Mother */

mother_of(Mother, Child) :-
    female(Mother),
    parent_of(Mother, Child).


/* Child */

child_of(Child, Parent) :-
    parent_of(Parent, Child).


/* Son */

son_of(Son, Parent) :-
    male(Son),
    parent_of(Parent, Son).


/* Daughter */

daughter_of(Daughter, Parent) :-
    female(Daughter),
    parent_of(Parent, Daughter).


/* =========================================================
   SIBLING RELATIONSHIPS
========================================================= */


/*
   Two people are siblings if they share at least one
   biological parent and they are not the same person.

   Duplicate logical solutions may arise where both parents
   are shared, but the Python layer deduplicates results.
*/

sibling_of(Person1, Person2) :-
    parent_of(Parent, Person1),
    parent_of(Parent, Person2),
    Person1 \= Person2.


brother_of(Brother, Person) :-
    male(Brother),
    sibling_of(Brother, Person).


sister_of(Sister, Person) :-
    female(Sister),
    sibling_of(Sister, Person).


/* =========================================================
   GRANDPARENT RELATIONSHIPS
========================================================= */

grandparent_of(Grandparent, Person) :-
    parent_of(Grandparent, Parent),
    parent_of(Parent, Person).


grandfather_of(Grandfather, Person) :-
    male(Grandfather),
    grandparent_of(Grandfather, Person).


grandmother_of(Grandmother, Person) :-
    female(Grandmother),
    grandparent_of(Grandmother, Person).


grandchild_of(Grandchild, Grandparent) :-
    grandparent_of(Grandparent, Grandchild).


grandson_of(Grandson, Grandparent) :-
    male(Grandson),
    grandchild_of(Grandson, Grandparent).


granddaughter_of(Granddaughter, Grandparent) :-
    female(Granddaughter),
    grandchild_of(Granddaughter, Grandparent).


/* =========================================================
   AUNT / UNCLE RELATIONSHIPS
========================================================= */

uncle_of(Uncle, Person) :-
    male(Uncle),
    parent_of(Parent, Person),
    sibling_of(Uncle, Parent).


aunt_of(Aunt, Person) :-
    female(Aunt),
    parent_of(Parent, Person),
    sibling_of(Aunt, Parent).


/* =========================================================
   NIECE / NEPHEW RELATIONSHIPS
========================================================= */

niece_of(Niece, Person) :-
    female(Niece),
    parent_of(Parent, Niece),
    sibling_of(Parent, Person).


nephew_of(Nephew, Person) :-
    male(Nephew),
    parent_of(Parent, Nephew),
    sibling_of(Parent, Person).


/* =========================================================
   COUSIN RELATIONSHIPS
========================================================= */

cousin_of(Person1, Person2) :-
    parent_of(Parent1, Person1),
    parent_of(Parent2, Person2),
    sibling_of(Parent1, Parent2),
    Person1 \= Person2.


/* =========================================================
   ANCESTOR RELATIONSHIPS
========================================================= */


/* Direct ancestor */

ancestor_of(Ancestor, Person) :-
    parent_of(Ancestor, Person).


/* Recursive ancestor */

ancestor_of(Ancestor, Person) :-
    parent_of(Ancestor, Intermediate),
    ancestor_of(Intermediate, Person).


/* =========================================================
   DESCENDANT RELATIONSHIPS
========================================================= */

descendant_of(Descendant, Ancestor) :-
    ancestor_of(Ancestor, Descendant).


/* =========================================================
   MARRIAGE RELATIONSHIPS
========================================================= */

spouse_of(Person1, Person2) :-
    married_to(Person1, Person2).


former_spouse_of(Person1, Person2) :-
    previously_married_to(Person1, Person2).


/* =========================================================
   STEP RELATIONSHIPS
========================================================= */

step_child_of(Child, StepParent) :-
    step_parent_of(StepParent, Child).


step_father_of(StepFather, Child) :-
    male(StepFather),
    step_parent_of(StepFather, Child).


step_mother_of(StepMother, Child) :-
    female(StepMother),
    step_parent_of(StepMother, Child).


/* =========================================================
   BIRTH ORDER HELPERS
========================================================= */

first_born(Person) :-
    birth_order(Person, 1).


older_sibling_of(Older, Younger) :-
    sibling_of(Older, Younger),
    birth_order(Older, OlderPosition),
    birth_order(Younger, YoungerPosition),
    OlderPosition < YoungerPosition.


younger_sibling_of(Younger, Older) :-
    sibling_of(Younger, Older),
    birth_order(Younger, YoungerPosition),
    birth_order(Older, OlderPosition),
    YoungerPosition > OlderPosition.


/* =========================================================
   GENERIC FAMILY RELATIONSHIP
========================================================= */

relative_of(Person1, Person2) :-
    parent_of(Person1, Person2).

relative_of(Person1, Person2) :-
    parent_of(Person2, Person1).

relative_of(Person1, Person2) :-
    sibling_of(Person1, Person2).

relative_of(Person1, Person2) :-
    grandparent_of(Person1, Person2).

relative_of(Person1, Person2) :-
    grandparent_of(Person2, Person1).

relative_of(Person1, Person2) :-
    uncle_of(Person1, Person2).

relative_of(Person1, Person2) :-
    aunt_of(Person1, Person2).

relative_of(Person1, Person2) :-
    niece_of(Person1, Person2).

relative_of(Person1, Person2) :-
    nephew_of(Person1, Person2).

relative_of(Person1, Person2) :-
    cousin_of(Person1, Person2).

relative_of(Person1, Person2) :-
    spouse_of(Person1, Person2).

relative_of(Person1, Person2) :-
    step_parent_of(Person1, Person2).

relative_of(Person1, Person2) :-
    step_child_of(Person1, Person2).


/* =========================================================
   PERSON

   A person exists when a gender fact exists.
========================================================= */

person(Person) :-
    male(Person).

person(Person) :-
    female(Person).


/* =========================================================
   FAMILY GRAPH

   Biological parent-child edges only.

   Marriage and step relationships remain available as
   separate predicates and can later be visualized using
   different edge types.
========================================================= */

graph_edge(Parent, Child) :-
    parent_of(Parent, Child).


/* =========================================================
   OPTIONAL GRAPH EDGE TYPES
========================================================= */

marriage_edge(Person1, Person2) :-
    married_to(Person1, Person2).


step_edge(StepParent, StepChild) :-
    step_parent_of(StepParent, StepChild).
