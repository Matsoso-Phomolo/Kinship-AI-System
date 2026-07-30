"use strict";


document.addEventListener("DOMContentLoaded", () => {

    const peopleList =
        document.getElementById("peopleList");

    const peopleCount =
        document.getElementById("peopleCount");

    const peopleSearch =
        document.getElementById("peopleSearch");

    const personOne =
        document.getElementById("personOne");

    const personTwo =
        document.getElementById("personTwo");

    const discoverButton =
        document.getElementById("discoverButton");

    const relationshipResult =
        document.getElementById("relationshipResult");

    const treePeople =
        document.querySelectorAll(".tree-person");


    let people = [];


    async function loadPeople() {

        try {

            const response =
                await fetch("/api/people");

            if (!response.ok) {
                throw new Error(
                    "Unable to load people."
                );
            }

            const data =
                await response.json();

            people =
                Array.isArray(data.people)
                    ? data.people
                    : [];

            renderPeople(people);

            populateSelects(people);

            if (peopleCount) {
                peopleCount.textContent =
                    String(people.length);
            }

        } catch (error) {

            console.error(error);

            if (peopleList) {
                peopleList.innerHTML = `
                    <div class="people-error">
                        Family members could not be loaded.
                    </div>
                `;
            }
        }
    }


    function renderPeople(list) {

        if (!peopleList) {
            return;
        }

        if (!list.length) {

            peopleList.innerHTML = `
                <div class="people-empty">
                    No people found.
                </div>
            `;

            return;
        }


        peopleList.innerHTML =
            list
                .map((person) => `
                    <button
                        type="button"
                        class="person-list-item"
                        data-person="${escapeHtml(person.id)}"
                    >
                        <div class="person-avatar">
                            ${escapeHtml(
                                person.name.charAt(0)
                            )}
                        </div>

                        <div class="person-details">

                            <strong>
                                ${escapeHtml(person.name)}
                            </strong>

                            <span>
                                ${escapeHtml(person.gender)}
                            </span>

                        </div>

                    </button>
                `)
                .join("");


        const personButtons =
            peopleList.querySelectorAll(
                ".person-list-item"
            );


        personButtons.forEach((button) => {

            button.addEventListener(
                "click",
                () => {

                    selectPerson(
                        button.dataset.person
                    );

                }
            );

        });

    }


    function populateSelects(list) {

        if (!personOne || !personTwo) {
            return;
        }

        const options =
            list
                .map((person) => `
                    <option
                        value="${escapeHtml(person.id)}"
                    >
                        ${escapeHtml(person.title)}
                    </option>
                `)
                .join("");


        personOne.insertAdjacentHTML(
            "beforeend",
            options
        );

        personTwo.insertAdjacentHTML(
            "beforeend",
            options
        );

    }


    function selectPerson(personId) {

        if (!personOne || !personTwo) {
            return;
        }


        if (!personOne.value) {

            personOne.value =
                personId;

        } else if (!personTwo.value) {

            personTwo.value =
                personId;

        } else {

            personOne.value =
                personTwo.value;

            personTwo.value =
                personId;
        }


        highlightSelectedPeople();

    }


    function highlightSelectedPeople() {

        const selected =
            new Set([
                personOne?.value,
                personTwo?.value
            ]);


        treePeople.forEach((person) => {

            const personId =
                person.dataset.person;

            person.classList.toggle(
                "selected",
                selected.has(personId)
            );

        });

    }


    async function discoverRelationship() {

        if (
            !personOne?.value ||
            !personTwo?.value
        ) {

            showMessage(
                "Select two people first.",
                true
            );

            return;
        }


        if (
            personOne.value ===
            personTwo.value
        ) {

            showMessage(
                "Please select two different people.",
                true
            );

            return;
        }


        discoverButton.disabled =
            true;

        discoverButton.textContent =
            "Reasoning...";


        showLoading();


        try {

            const url =
                `/api/relationship/` +
                `${encodeURIComponent(personOne.value)}/` +
                `${encodeURIComponent(personTwo.value)}`;


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "Relationship lookup failed."
                );

            }


            const data =
                await response.json();


            showResult(
                data.result ||
                "No relationship result was returned."
            );


        } catch (error) {

            console.error(error);

            showMessage(
                "Kinship AI could not complete the relationship lookup.",
                true
            );

        } finally {

            discoverButton.disabled =
                false;

            discoverButton.textContent =
                "Discover Relationship";

        }

    }


    function showLoading() {

        relationshipResult.classList.remove(
            "empty",
            "error"
        );

        relationshipResult.innerHTML = `
            <div class="result-symbol">
                AI
            </div>

            <div>
                <h3>
                    Kinship AI is reasoning
                </h3>

                <p>
                    Checking symbolic family relationships...
                </p>
            </div>
        `;

    }


    function showResult(result) {

        relationshipResult.classList.remove(
            "empty",
            "error"
        );

        relationshipResult.innerHTML = `
            <div class="result-symbol">
                AI
            </div>

            <div>
                <h3>
                    Relationship discovered
                </h3>

                <p>
                    ${escapeHtml(result)}
                </p>
            </div>
        `;

    }


    function showMessage(
        message,
        isError = false
    ) {

        relationshipResult.classList.remove(
            "empty",
            "error"
        );


        if (isError) {
            relationshipResult.classList.add(
                "error"
            );
        }


        relationshipResult.innerHTML = `
            <div class="result-symbol">
                !
            </div>

            <div>
                <h3>
                    ${isError ? "Selection required" : "Kinship AI"}
                </h3>

                <p>
                    ${escapeHtml(message)}
                </p>
            </div>
        `;

    }


    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent =
            String(value);

        return div.innerHTML;

    }


    if (peopleSearch) {

        peopleSearch.addEventListener(
            "input",
            () => {

                const query =
                    peopleSearch.value
                        .trim()
                        .toLowerCase();


                const filtered =
                    people.filter(
                        (person) =>
                            person.name
                                .toLowerCase()
                                .includes(query)
                    );


                renderPeople(filtered);

            }
        );

    }


    if (personOne) {

        personOne.addEventListener(
            "change",
            highlightSelectedPeople
        );

    }


    if (personTwo) {

        personTwo.addEventListener(
            "change",
            highlightSelectedPeople
        );

    }


    if (discoverButton) {

        discoverButton.addEventListener(
            "click",
            discoverRelationship
        );

    }


    treePeople.forEach((person) => {

        person.addEventListener(
            "click",
            () => {

                selectPerson(
                    person.dataset.person
                );

            }
        );

    });


    loadPeople();

});
