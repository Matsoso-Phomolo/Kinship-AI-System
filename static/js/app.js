"use strict";

/* =========================================================
   KINSHIP AI
   Frontend Interaction
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const mobileMenuButton = document.getElementById("mobileMenuButton");
    const mobileNav = document.getElementById("mobileNav");

    const questionForm = document.getElementById("questionForm");
    const questionInput = document.getElementById("question");
    const askButton = document.getElementById("askButton");

    const exampleButtons = document.querySelectorAll(".example-button");


    /* =====================================================
       MOBILE NAVIGATION
    ===================================================== */

    function closeMobileMenu() {
        if (!mobileMenuButton || !mobileNav) {
            return;
        }

        mobileMenuButton.classList.remove("active");
        mobileNav.classList.remove("active");

        mobileMenuButton.setAttribute("aria-expanded", "false");
        mobileMenuButton.setAttribute(
            "aria-label",
            "Open navigation menu"
        );
    }


    function openMobileMenu() {
        if (!mobileMenuButton || !mobileNav) {
            return;
        }

        mobileMenuButton.classList.add("active");
        mobileNav.classList.add("active");

        mobileMenuButton.setAttribute("aria-expanded", "true");
        mobileMenuButton.setAttribute(
            "aria-label",
            "Close navigation menu"
        );
    }


    if (mobileMenuButton && mobileNav) {
        mobileMenuButton.addEventListener("click", () => {
            const isOpen =
                mobileMenuButton.classList.contains("active");

            if (isOpen) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });


        const mobileNavLinks =
            mobileNav.querySelectorAll("a");

        mobileNavLinks.forEach((link) => {
            link.addEventListener("click", () => {
                closeMobileMenu();
            });
        });


        window.addEventListener("resize", () => {
            if (window.innerWidth > 760) {
                closeMobileMenu();
            }
        });


        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeMobileMenu();
            }
        });
    }


    /* =====================================================
       EXAMPLE QUESTIONS
    ===================================================== */

    exampleButtons.forEach((button) => {
        button.addEventListener("click", () => {
            if (!questionInput) {
                return;
            }

            const question =
                button.dataset.question?.trim();

            if (!question) {
                return;
            }

            questionInput.value = question;

            questionInput.focus();

            questionInput.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        });
    });


    /* =====================================================
       QUESTION FORM
    ===================================================== */

    if (questionForm && questionInput && askButton) {
        questionForm.addEventListener("submit", (event) => {
            const question = questionInput.value.trim();

            if (!question) {
                event.preventDefault();

                questionInput.focus();

                return;
            }

            askButton.disabled = true;
            askButton.textContent = "Reasoning...";
        });
    }


    /* =====================================================
       RESTORE BUTTON AFTER BACK/FORWARD NAVIGATION
    ===================================================== */

    window.addEventListener("pageshow", () => {
        if (!askButton) {
            return;
        }

        askButton.disabled = false;
        askButton.textContent = "Ask";
    });


    /* =====================================================
       AUTO-SCROLL TO RESULT AFTER SERVER RESPONSE
    ===================================================== */

    const answerPanel =
        document.querySelector(".answer-panel");

    if (answerPanel) {
        setTimeout(() => {
            answerPanel.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }, 150);
    }


    /* =====================================================
       ACTIVE NAVIGATION SECTION
    ===================================================== */

    const sections = [
        "home",
        "ask",
        "capabilities",
        "technology"
    ];

    const desktopLinks =
        document.querySelectorAll(".desktop-nav a");

    function updateActiveNavigation() {
        const position =
            window.scrollY + 140;

        let activeSection = "home";

        sections.forEach((sectionId) => {
            const section =
                document.getElementById(sectionId);

            if (!section) {
                return;
            }

            if (section.offsetTop <= position) {
                activeSection = sectionId;
            }
        });

        desktopLinks.forEach((link) => {
            const href =
                link.getAttribute("href");

            link.classList.toggle(
                "active",
                href === `#${activeSection}`
            );
        });
    }


    window.addEventListener(
        "scroll",
        updateActiveNavigation,
        { passive: true }
    );

    updateActiveNavigation();
});
