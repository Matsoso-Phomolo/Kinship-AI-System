/* =========================================================
   KINSHIP AI
   Family Knowledge Base and Symbolic Reasoning Engine
========================================================= */


/* =========================================================
   PEOPLE / GENDER FACTS
========================================================= */

male(jack).
male(oliver).
male(ali).
male(james).
male(simon).
male(harry).

female(helen).
female(sophie).
female(jess).
female(lily).


/* =========================================================
   PARENT FACTS

   parent_of(Parent, Child).
========================================================= */

parent_of(jack, jess).
parent_of(jack, lily).

parent_of(helen, jess).
parent_of(helen, lily).

parent_of(oliver, james).
parent_of(sophie, james).

parent_of(jess, simon).
parent_of(ali, simon).

parent_of(lily, harry).
parent_of(james, harry).


/* =========================================================
   BASIC RELATIONSHIPS
========================================================= */

father_of(Father, Child) :-
    male(Father),
    parent_of(Father, Child).


mother_of(Mother, Child) :-
    female(Mother),
    parent_of(Mother, Child).


child_of(Child, Parent) :-
    parent_of(Parent, Child).


son_of(Son, Parent) :-
    male(Son),
    parent_of(Parent, Son).


daughter_of(Daughter, Parent) :-
    female(Daughter),
    parent_of(Parent, Daughter).


/* =========================================================
   SIBLING RELATIONSHIPS

   Two people are siblings when they share at least one
   parent and are not the same person.

   setof/3 is used by application queries to remove any
   duplicate answers that can arise when two siblings share
   both parents.
========================================================= */

sibling_of(Person, Sibling) :-
    parent_of(Parent, Person),
    parent_of(Parent, Sibling),
    Person \= Sibling.


brother_of(Brother, Person) :-
    male(Brother),
    sibling_of(Brother, Person).


sister_of(Sister, Person) :-
    female(Sister),
    sibling_of(Sister, Person).


/* =========================================================
   GRANDPARENTS
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
   AUNTS AND UNCLES

   An aunt/uncle is a sibling of one of the person's
   parents.

   This implementation fixes the direction problems in
   the previous rules.
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
   NIECES AND NEPHEWS
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
   COUSINS

   Two people are cousins when their parents are siblings.
========================================================= */

cousin_of(Person1, Person2) :-
    parent_of(Parent1, Person1),
    parent_of(Parent2, Person2),
    sibling_of(Parent1, Parent2),
    Person1 \= Person2.


/* =========================================================
   ANCESTORS

   Direct parent:
       Parent -> Child

   Recursive:
       Ancestor -> Parent -> ... -> Descendant
========================================================= */

ancestor_of(Ancestor, Person) :-
    parent_of(Ancestor, Person).


ancestor_of(Ancestor, Person) :-
    parent_of(Ancestor, Intermediate),
    ancestor_of(Intermediate, Person).


/* =========================================================
   DESCENDANTS

   descendant_of(Person, Ancestor)
========================================================= */

descendant_of(Descendant, Ancestor) :-
    ancestor_of(Ancestor, Descendant).


/* =========================================================
   GENERIC RELATIVE RELATIONSHIP

   Useful later for relationship discovery and graph
   traversal.
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
    cousin_of(Person1, Person2).


/* =========================================================
   PERSON

   A person exists if they have a gender fact.

   This gives the application a simple way to retrieve all
   known people later.
========================================================= */

person(Person) :-
    male(Person).

person(Person) :-
    female(Person).

/* =========================================================
   FAMILY GRAPH EDGE

   graph_edge(Parent, Child)
========================================================= */

graph_edge(Parent, Child) :-
    parent_of(Parent, Child).
