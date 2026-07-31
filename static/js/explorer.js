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

    const familyTreeCanvas =
        document.getElementById("familyTreeCanvas");


    let people = [];
    let graph = {
        nodes: [],
        edges: []
    };


    /* =====================================================
       LOAD DATA
    ===================================================== */

    async function loadExplorerData() {

        try {

            const [
                peopleResponse,
                graphResponse
            ] = await Promise.all([
                fetch("/api/people"),
                fetch("/api/graph")
            ]);


            if (
                !peopleResponse.ok ||
                !graphResponse.ok
            ) {
                throw new Error(
                    "Explorer data could not be loaded."
                );
            }


            const peopleData =
                await peopleResponse.json();

            const graphData =
                await graphResponse.json();


            people =
                Array.isArray(
                    peopleData.people
                )
                    ? peopleData.people
                    : [];


            graph = {
                nodes:
                    Array.isArray(
                        graphData.nodes
                    )
                        ? graphData.nodes
                        : [],

                edges:
                    Array.isArray(
                        graphData.edges
                    )
                        ? graphData.edges
                        : []
            };


            renderPeople(people);

            populateSelects(people);

            renderGraph(graph);


            if (peopleCount) {
                peopleCount.textContent =
                    String(
                        people.length
                    );
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


            if (familyTreeCanvas) {

                familyTreeCanvas.innerHTML = `
                    <div class="graph-error">
                        Family graph could not be loaded.
                    </div>
                `;

            }

        }

    }


    /* =====================================================
       PEOPLE LIST
    ===================================================== */

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
                .map(
                    (person) => `
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
                    `
                )
                .join("");


        const buttons =
            peopleList.querySelectorAll(
                ".person-list-item"
            );


        buttons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        selectPerson(
                            button.dataset.person
                        );

                    }
                );

            }
        );

    }


    /* =====================================================
       SELECT OPTIONS
    ===================================================== */

    function populateSelects(list) {

        if (
            !personOne ||
            !personTwo
        ) {
            return;
        }


        const options =
            list
                .map(
                    (person) => `
                        <option
                            value="${escapeHtml(person.id)}"
                        >
                            ${escapeHtml(person.title)}
                        </option>
                    `
                )
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


    /* =====================================================
       FAMILY GRAPH
    ===================================================== */

    function renderGraph(graphData) {

        if (!familyTreeCanvas) {
            return;
        }


        if (!graphData.nodes.length) {

            familyTreeCanvas.innerHTML = `
                <div class="graph-empty">
                    The knowledge base contains no people.
                </div>
            `;

            return;

        }


        const generations =
            buildGenerations(
                graphData.nodes,
                graphData.edges
            );


        familyTreeCanvas.innerHTML =
            generations
                .map(
                    (
                        generation,
                        index
                    ) => {

                        const peopleMarkup =
                            generation
                                .map(
                                    (person) => `
                                        <button
                                            type="button"
                                            class="tree-person dynamic-tree-person"
                                            data-person="${escapeHtml(person.id)}"
                                        >

                                            <span class="tree-role">
                                                ${escapeHtml(person.gender)}
                                            </span>

                                            <strong>
                                                ${escapeHtml(person.name)}
                                            </strong>

                                        </button>
                                    `
                                )
                                .join("");


                        return `
                            <div class="generation-block">

                                <div class="generation-title">
                                    Generation ${index + 1}
                                </div>

                                <div class="dynamic-generation">
                                    ${peopleMarkup}
                                </div>

                            </div>
                        `;

                    }
                )
                .join("");


        const graphPeople =
            familyTreeCanvas.querySelectorAll(
                ".tree-person"
            );


        graphPeople.forEach(
            (person) => {

                person.addEventListener(
                    "click",
                    () => {

                        selectPerson(
                            person.dataset.person
                        );

                    }
                );

            }
        );


        highlightSelectedPeople();

    }


    function buildGenerations(
        nodes,
        edges
    ) {

        const nodeMap =
            new Map(
                nodes.map(
                    (node) => [
                        node.id,
                        node
                    ]
                )
            );


        const parentsOf =
            new Map();

        const childrenOf =
            new Map();


        nodes.forEach(
            (node) => {

                parentsOf.set(
                    node.id,
                    []
                );

                childrenOf.set(
                    node.id,
                    []
                );

            }
        );


        edges.forEach(
            (edge) => {

                if (
                    parentsOf.has(
                        edge.target
                    )
                ) {

                    parentsOf
                        .get(edge.target)
                        .push(edge.source);

                }


                if (
                    childrenOf.has(
                        edge.source
                    )
                ) {

                    childrenOf
                        .get(edge.source)
                        .push(edge.target);

                }

            }
        );


        const roots =
            nodes
                .filter(
                    (node) =>
                        parentsOf
                            .get(node.id)
                            .length === 0
                )
                .map(
                    (node) =>
                        node.id
                );


        const generationIndex =
            new Map();


        roots.forEach(
            (root) => {

                generationIndex.set(
                    root,
                    0
                );

            }
        );


        const queue = [
            ...roots
        ];


        while (
            queue.length
        ) {

            const current =
                queue.shift();

            const currentGeneration =
                generationIndex.get(
                    current
                ) ?? 0;


            const children =
                childrenOf.get(
                    current
                ) || [];


            children.forEach(
                (child) => {

                    const nextGeneration =
                        currentGeneration + 1;


                    const existingGeneration =
                        generationIndex.get(
                            child
                        );


                    if (
                        existingGeneration === undefined ||
                        nextGeneration >
                        existingGeneration
                    ) {

                        generationIndex.set(
                            child,
                            nextGeneration
                        );

                    }


                    if (
                        !queue.includes(child)
                    ) {
                        queue.push(child);
                    }

                }
            );

        }


        nodes.forEach(
            (node) => {

                if (
                    !generationIndex.has(
                        node.id
                    )
                ) {

                    generationIndex.set(
                        node.id,
                        0
                    );

                }

            }
        );


        const maxGeneration =
            Math.max(
                ...generationIndex.values()
            );


        const generations =
            Array.from(
                {
                    length:
                        maxGeneration + 1
                },
                () => []
            );


        generationIndex.forEach(
            (
                generation,
                personId
            ) => {

                const person =
                    nodeMap.get(
                        personId
                    );


                if (person) {

                    generations[
                        generation
                    ].push(person);

                }

            }
        );


        generations.forEach(
            (generation) => {

                generation.sort(
                    (a, b) =>
                        a.name.localeCompare(
                            b.name
                        )
                );

            }
        );


        return generations;

    }


    /* =====================================================
       PERSON SELECTION
    ===================================================== */

    function selectPerson(personId) {

        if (
            !personOne ||
            !personTwo ||
            !personId
        ) {
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
            new Set(
                [
                    personOne?.value,
                    personTwo?.value
                ].filter(Boolean)
            );


        const graphPeople =
            document.querySelectorAll(
                ".tree-person"
            );


        graphPeople.forEach(
            (person) => {

                person.classList.toggle(
                    "selected",
                    selected.has(
                        person.dataset.person
                    )
                );

            }
        );

    }


    /* =====================================================
       RELATIONSHIP DISCOVERY
    ===================================================== */

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


    /* =====================================================
       RESULT STATES
    ===================================================== */

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
                    Evaluating symbolic family relationships...
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
                    ${isError
                        ? "Action required"
                        : "Kinship AI"}
                </h3>

                <p>
                    ${escapeHtml(message)}
                </p>
            </div>
        `;

    }


    /* =====================================================
       SEARCH
    ===================================================== */

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


                renderPeople(
                    filtered
                );

            }
        );

    }


    /* =====================================================
       EVENT LISTENERS
    ===================================================== */

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


    /* =====================================================
       SECURITY
    ===================================================== */

    function escapeHtml(value) {

        const element =
            document.createElement(
                "div"
            );

        element.textContent =
            String(value);

        return element.innerHTML;

    }


    /* =====================================================
       INITIALIZE
    ===================================================== */

    loadExplorerData();

});
