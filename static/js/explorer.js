"use strict";


document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       DOM REFERENCES
    ===================================================== */

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


    /* =====================================================
       STATE
    ===================================================== */

    let people = [];

    let graph = {
        nodes: [],
        edges: [],
        marriage_edges: [],
        step_edges: []
    };


    /* =====================================================
       INITIAL DATA LOAD
    ===================================================== */

    async function loadExplorerData() {

        setGraphLoading();

        try {

            const [
                peopleResponse,
                graphResponse
            ] = await Promise.all([
                fetch("/api/people"),
                fetch("/api/graph")
            ]);


            if (!peopleResponse.ok) {
                throw new Error(
                    "Could not load family members."
                );
            }


            if (!graphResponse.ok) {
                throw new Error(
                    "Could not load family graph."
                );
            }


            const peopleData =
                await peopleResponse.json();

            const graphData =
                await graphResponse.json();


            people =
                Array.isArray(peopleData.people)
                    ? peopleData.people
                    : [];


            graph = {
                nodes:
                    Array.isArray(graphData.nodes)
                        ? graphData.nodes
                        : [],

                edges:
                    Array.isArray(graphData.edges)
                        ? graphData.edges
                        : [],

                marriage_edges:
                    Array.isArray(
                        graphData.marriage_edges
                    )
                        ? graphData.marriage_edges
                        : [],

                step_edges:
                    Array.isArray(
                        graphData.step_edges
                    )
                        ? graphData.step_edges
                        : []
            };


            updatePeopleCount();

            renderPeople(people);

            populateSelectors(people);

            renderFamilyGraph(graph);

        } catch (error) {

            console.error(
                "Kinship AI Explorer:",
                error
            );

            showPeopleError();

            showGraphError();

        }

    }


    /* =====================================================
       PEOPLE COUNT
    ===================================================== */

    function updatePeopleCount() {

        if (!peopleCount) {
            return;
        }

        peopleCount.textContent =
            String(people.length);

    }


    /* =====================================================
       PERSON CONTEXT

       This helps distinguish people who share a name,
       especially the two Katleho Matsoso records.
    ===================================================== */

    function getParents(personId) {

        const parentIds =
            graph.edges
                .filter(
                    edge =>
                        edge.target === personId
                )
                .map(
                    edge =>
                        edge.source
                );


        return parentIds
            .map(getPerson)
            .filter(Boolean);

    }


    function getPerson(personId) {

        return people.find(
            person =>
                person.id === personId
        ) || null;

    }


    function getPersonContext(person) {

        const parents =
            getParents(person.id);


        if (parents.length) {

            const parentNames =
                parents
                    .map(
                        parent =>
                            parent.name
                    )
                    .join(" & ");


            return `Child of ${parentNames}`;

        }


        if (
            Array.isArray(
                person.former_names
            ) &&
            person.former_names.length
        ) {

            return (
                `Formerly ${
                    person.former_names.join(", ")
                }`
            );

        }


        return capitalize(
            person.gender || "person"
        );

    }


    function buildOptionLabel(person) {

        const duplicateCount =
            people.filter(
                entry =>
                    entry.name === person.name
            ).length;


        if (duplicateCount <= 1) {
            return person.title || person.name;
        }


        return (
            `${person.name} — ` +
            `${getPersonContext(person)}`
        );

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
                    No matching family members.
                </div>
            `;

            return;

        }


        peopleList.innerHTML =
            list
                .map(person => {

                    const duplicateCount =
                        people.filter(
                            entry =>
                                entry.name ===
                                person.name
                        ).length;


                    const context =
                        duplicateCount > 1
                            ? getPersonContext(person)
                            : capitalize(
                                person.gender
                            );


                    return `
                        <button
                            type="button"
                            class="person-list-item"
                            data-person="${escapeHtml(person.id)}"
                            aria-label="Select ${escapeHtml(person.name)}"
                        >

                            <div
                                class="person-avatar"
                                data-gender="${escapeHtml(person.gender)}"
                            >
                                ${escapeHtml(
                                    person.name.charAt(0)
                                )}
                            </div>

                            <div class="person-details">

                                <strong>
                                    ${escapeHtml(person.name)}
                                </strong>

                                <span>
                                    ${escapeHtml(context)}
                                </span>

                                ${
                                    person.former_names?.length
                                        ? `
                                            <small>
                                                Formerly:
                                                ${escapeHtml(
                                                    person.former_names.join(", ")
                                                )}
                                            </small>
                                        `
                                        : ""
                                }

                            </div>

                        </button>
                    `;

                })
                .join("");


        peopleList
            .querySelectorAll(
                ".person-list-item"
            )
            .forEach(button => {

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


    /* =====================================================
       SELECTORS
    ===================================================== */

    function populateSelectors(list) {

        if (
            !personOne ||
            !personTwo
        ) {
            return;
        }


        personOne.innerHTML = `
            <option value="">
                Select person
            </option>
        `;


        personTwo.innerHTML = `
            <option value="">
                Select person
            </option>
        `;


        const sorted =
            [...list].sort(
                (a, b) =>
                    a.name.localeCompare(
                        b.name
                    )
            );


        sorted.forEach(person => {

            const label =
                buildOptionLabel(person);


            const optionOne =
                document.createElement(
                    "option"
                );

            optionOne.value =
                person.id;

            optionOne.textContent =
                label;


            const optionTwo =
                document.createElement(
                    "option"
                );

            optionTwo.value =
                person.id;

            optionTwo.textContent =
                label;


            personOne.appendChild(
                optionOne
            );

            personTwo.appendChild(
                optionTwo
            );

        });

    }


    /* =====================================================
       FAMILY GRAPH GENERATIONS
    ===================================================== */

    function buildGenerations(
        nodes,
        edges
    ) {

        const nodeMap =
            new Map(
                nodes.map(
                    node => [
                        node.id,
                        node
                    ]
                )
            );


        const parentsOf =
            new Map();

        const childrenOf =
            new Map();


        nodes.forEach(node => {

            parentsOf.set(
                node.id,
                []
            );

            childrenOf.set(
                node.id,
                []
            );

        });


        edges.forEach(edge => {

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

        });


        const roots =
            nodes
                .filter(
                    node =>
                        (
                            parentsOf.get(
                                node.id
                            ) || []
                        ).length === 0
                )
                .map(
                    node =>
                        node.id
                );


        const generation =
            new Map();


        roots.forEach(root => {

            generation.set(
                root,
                0
            );

        });


        const queue =
            [...roots];


        const processed =
            new Map();


        while (queue.length) {

            const current =
                queue.shift();


            const currentGeneration =
                generation.get(
                    current
                ) ?? 0;


            const children =
                childrenOf.get(
                    current
                ) || [];


            children.forEach(child => {

                const proposed =
                    currentGeneration + 1;


                const existing =
                    generation.get(child);


                if (
                    existing === undefined ||
                    proposed > existing
                ) {

                    generation.set(
                        child,
                        proposed
                    );

                }


                const processCount =
                    processed.get(child)
                    || 0;


                if (processCount < 3) {

                    processed.set(
                        child,
                        processCount + 1
                    );

                    queue.push(child);

                }

            });

        }


        nodes.forEach(node => {

            if (
                !generation.has(
                    node.id
                )
            ) {

                generation.set(
                    node.id,
                    0
                );

            }

        });


        const generations =
            new Map();


        generation.forEach(
            (
                generationNumber,
                personId
            ) => {

                if (
                    !generations.has(
                        generationNumber
                    )
                ) {

                    generations.set(
                        generationNumber,
                        []
                    );

                }


                const person =
                    nodeMap.get(
                        personId
                    );


                if (person) {

                    generations
                        .get(generationNumber)
                        .push(person);

                }

            }
        );


        return [...generations.entries()]
            .sort(
                (a, b) =>
                    a[0] - b[0]
            )
            .map(
                ([number, members]) => ({
                    number,
                    members:
                        members.sort(
                            (a, b) =>
                                compareFamilyOrder(
                                    a,
                                    b
                                )
                        )
                })
            );

    }


    function compareFamilyOrder(
        personA,
        personB
    ) {

        const orderA =
            personA.birth_order;

        const orderB =
            personB.birth_order;


        if (
            orderA !== null &&
            orderA !== undefined &&
            orderB !== null &&
            orderB !== undefined &&
            orderA !== orderB
        ) {

            return orderA - orderB;

        }


        return personA.name.localeCompare(
            personB.name
        );

    }


    /* =====================================================
       GRAPH RENDERING
    ===================================================== */

    function renderFamilyGraph(
        graphData
    ) {

        if (!familyTreeCanvas) {
            return;
        }


        if (
            !graphData.nodes.length
        ) {

            familyTreeCanvas.innerHTML = `
                <div class="graph-empty">
                    No family members are currently available.
                </div>
            `;

            return;

        }


        const generations =
            buildGenerations(
                graphData.nodes,
                graphData.edges
            );


        const generationMarkup =
            generations
                .map(generation => {

                    const members =
                        generation.members
                            .map(person =>
                                renderGraphPerson(
                                    person
                                )
                            )
                            .join("");


                    return `
                        <section
                            class="generation-block"
                            data-generation="${generation.number}"
                        >

                            <div class="generation-title">
                                Generation ${generation.number + 1}
                            </div>

                            <div class="dynamic-generation">
                                ${members}
                            </div>

                        </section>
                    `;

                })
                .join("");


        familyTreeCanvas.innerHTML = `

            <div class="graph-summary">

                <div>
                    <strong>
                        ${graphData.nodes.length}
                    </strong>
                    <span>People</span>
                </div>

                <div>
                    <strong>
                        ${graphData.edges.length}
                    </strong>
                    <span>Parent links</span>
                </div>

                <div>
                    <strong>
                        ${graphData.marriage_edges.length}
                    </strong>
                    <span>Marriages</span>
                </div>

                <div>
                    <strong>
                        ${graphData.step_edges.length}
                    </strong>
                    <span>Step links</span>
                </div>

            </div>


            <div class="graph-legend">

                <span>
                    <i class="legend-dot biological"></i>
                    Biological family
                </span>

                <span>
                    <i class="legend-dot marriage"></i>
                    Marriage
                </span>

                <span>
                    <i class="legend-dot step"></i>
                    Step-family
                </span>

            </div>


            <div class="generations-container">
                ${generationMarkup}
            </div>
        `;


        familyTreeCanvas
            .querySelectorAll(
                ".tree-person"
            )
            .forEach(person => {

                person.addEventListener(
                    "click",
                    () => {

                        selectPerson(
                            person.dataset.person
                        );

                    }
                );

            });


        highlightSelectedPeople();

    }


    function renderGraphPerson(
        person
    ) {

        const duplicateCount =
            people.filter(
                entry =>
                    entry.name === person.name
            ).length;


        const context =
            duplicateCount > 1
                ? getPersonContext(person)
                : (
                    person.birth_order
                        ? ordinalBirthOrder(
                            person.birth_order
                        )
                        : capitalize(
                            person.gender
                        )
                );


        return `
            <button
                type="button"
                class="tree-person dynamic-tree-person"
                data-person="${escapeHtml(person.id)}"
            >

                <span
                    class="tree-person-gender"
                    data-gender="${escapeHtml(person.gender)}"
                >
                    ${escapeHtml(
                        capitalize(person.gender)
                    )}
                </span>

                <strong>
                    ${escapeHtml(person.name)}
                </strong>

                <small>
                    ${escapeHtml(context)}
                </small>

                ${
                    person.former_names?.length
                        ? `
                            <span class="former-name">
                                Formerly
                                ${escapeHtml(
                                    person.former_names.join(", ")
                                )}
                            </span>
                        `
                        : ""
                }

            </button>
        `;

    }


    /* =====================================================
       PERSON SELECTION
    ===================================================== */

    function selectPerson(
        personId
    ) {

        if (
            !personId ||
            !personOne ||
            !personTwo
        ) {
            return;
        }


        if (!personOne.value) {

            personOne.value =
                personId;

        } else if (!personTwo.value) {

            if (
                personOne.value ===
                personId
            ) {

                showMessage(
                    "Choose a different second person.",
                    true
                );

                return;

            }


            personTwo.value =
                personId;

        } else {

            personOne.value =
                personTwo.value;

            personTwo.value =
                personId;

        }


        highlightSelectedPeople();

        clearOldResult();

    }


    function highlightSelectedPeople() {

        const first =
            personOne?.value;

        const second =
            personTwo?.value;


        document
            .querySelectorAll(
                ".tree-person"
            )
            .forEach(element => {

                element.classList.remove(
                    "selected",
                    "selected-first",
                    "selected-second"
                );


                if (
                    element.dataset.person ===
                    first
                ) {

                    element.classList.add(
                        "selected",
                        "selected-first"
                    );

                }


                if (
                    element.dataset.person ===
                    second
                ) {

                    element.classList.add(
                        "selected",
                        "selected-second"
                    );

                }

            });


        document
            .querySelectorAll(
                ".person-list-item"
            )
            .forEach(element => {

                element.classList.toggle(
                    "selected",
                    element.dataset.person === first ||
                    element.dataset.person === second
                );

            });

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
                "Select two family members first.",
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


        setDiscoverLoading(
            true
        );

        showReasoningState();


        try {

            const url =
                `/api/relationship/` +
                `${encodeURIComponent(personOne.value)}/` +
                `${encodeURIComponent(personTwo.value)}`;


            const response =
                await fetch(url);


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.message ||
                    "Relationship lookup failed."
                );

            }


            showRelationshipResult(
                data
            );

        } catch (error) {

            console.error(
                "Relationship discovery:",
                error
            );


            showMessage(
                error.message ||
                "Kinship AI could not complete the relationship lookup.",
                true
            );

        } finally {

            setDiscoverLoading(
                false
            );

        }

    }


    function showRelationshipResult(
        data
    ) {

        if (!relationshipResult) {
            return;
        }


        const firstPerson =
            data.person1;

        const secondPerson =
            data.person2;


        relationshipResult.classList.remove(
            "empty",
            "error"
        );


        relationshipResult.innerHTML = `

            <div class="result-symbol">
                AI
            </div>

            <div class="relationship-result-content">

                <h3>
                    Relationship discovered
                </h3>

                <div class="relationship-pair">

                    <span>
                        ${escapeHtml(
                            firstPerson?.name || ""
                        )}
                    </span>

                    <strong>→</strong>

                    <span>
                        ${escapeHtml(
                            secondPerson?.name || ""
                        )}
                    </span>

                </div>

                <p class="relationship-answer">
                    ${escapeHtml(
                        data.result ||
                        "No result returned."
                    )}
                </p>

                <small>
                    Reasoned using the Moleleki Matsoso
                    symbolic family knowledge base.
                </small>

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
                    normalizeSearchText(
                        peopleSearch.value
                    );


                if (!query) {

                    renderPeople(
                        people
                    );

                    highlightSelectedPeople();

                    return;

                }


                const filtered =
                    people.filter(person => {

                        const searchable = [
                            person.name,
                            person.id,
                            ...(person.aliases || []),
                            ...(person.former_names || []),
                            getPersonContext(person)
                        ]
                            .map(
                                normalizeSearchText
                            )
                            .join(" ");


                        return searchable.includes(
                            query
                        );

                    });


                renderPeople(
                    filtered
                );

                highlightSelectedPeople();

            }
        );

    }


    /* =====================================================
       SELECT EVENTS
    ===================================================== */

    if (personOne) {

        personOne.addEventListener(
            "change",
            () => {

                highlightSelectedPeople();

                clearOldResult();

            }
        );

    }


    if (personTwo) {

        personTwo.addEventListener(
            "change",
            () => {

                highlightSelectedPeople();

                clearOldResult();

            }
        );

    }


    if (discoverButton) {

        discoverButton.addEventListener(
            "click",
            discoverRelationship
        );

    }


    /* =====================================================
       RESULT STATES
    ===================================================== */

    function showReasoningState() {

        if (!relationshipResult) {
            return;
        }


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
                    Evaluating biological, extended,
                    marriage and step-family relationships...
                </p>
            </div>
        `;

    }


    function showMessage(
        message,
        error = false
    ) {

        if (!relationshipResult) {
            return;
        }


        relationshipResult.classList.remove(
            "empty",
            "error"
        );


        if (error) {

            relationshipResult.classList.add(
                "error"
            );

        }


        relationshipResult.innerHTML = `
            <div class="result-symbol">
                ${error ? "!" : "AI"}
            </div>

            <div>
                <h3>
                    ${error
                        ? "Action required"
                        : "Kinship AI"}
                </h3>

                <p>
                    ${escapeHtml(message)}
                </p>
            </div>
        `;

    }


    function clearOldResult() {

        if (!relationshipResult) {
            return;
        }


        relationshipResult.classList.add(
            "empty"
        );

        relationshipResult.classList.remove(
            "error"
        );


        relationshipResult.innerHTML = `
            <div class="result-symbol">
                ?
            </div>

            <div>
                <h3>
                    Ready to discover
                </h3>

                <p>
                    Select two family members and click
                    Discover Relationship.
                </p>
            </div>
        `;

    }


    function setDiscoverLoading(
        loading
    ) {

        if (!discoverButton) {
            return;
        }


        discoverButton.disabled =
            loading;


        discoverButton.textContent =
            loading
                ? "Reasoning..."
                : "Discover Relationship";

    }


    /* =====================================================
       GRAPH STATES
    ===================================================== */

    function setGraphLoading() {

        if (!familyTreeCanvas) {
            return;
        }


        familyTreeCanvas.innerHTML = `
            <div class="graph-loading">
                Loading Leloko la Ntate Moleleki Matsoso...
            </div>
        `;

    }


    function showGraphError() {

        if (!familyTreeCanvas) {
            return;
        }


        familyTreeCanvas.innerHTML = `
            <div class="graph-error">
                Family knowledge graph could not be loaded.
            </div>
        `;

    }


    function showPeopleError() {

        if (!peopleList) {
            return;
        }


        peopleList.innerHTML = `
            <div class="people-error">
                Family members could not be loaded.
            </div>
        `;

    }


    /* =====================================================
       UTILITIES
    ===================================================== */

    function escapeHtml(
        value
    ) {

        const element =
            document.createElement(
                "div"
            );

        element.textContent =
            String(value ?? "");

        return element.innerHTML;

    }


    function capitalize(
        value
    ) {

        if (!value) {
            return "";
        }


        return (
            value.charAt(0).toUpperCase()
            + value.slice(1)
        );

    }


    function normalizeSearchText(
        value
    ) {

        return String(value || "")
            .toLowerCase()
            .replace(/[’‘`´]/g, "'")
            .replace(/\s+/g, " ")
            .trim();

    }


    function ordinalBirthOrder(
        number
    ) {

        const numeric =
            Number(number);


        if (!Number.isFinite(numeric)) {
            return "";
        }


        const mod100 =
            numeric % 100;


        if (
            mod100 >= 11 &&
            mod100 <= 13
        ) {

            return `${numeric}th born`;

        }


        switch (numeric % 10) {

            case 1:
                return `${numeric}st born`;

            case 2:
                return `${numeric}nd born`;

            case 3:
                return `${numeric}rd born`;

            default:
                return `${numeric}th born`;

        }

    }


    /* =====================================================
       START
    ===================================================== */

    loadExplorerData();

});
