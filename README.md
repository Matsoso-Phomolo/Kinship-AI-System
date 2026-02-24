# Kinship AI System

A web-based Artificial Intelligence system that answers questions about family relationships using Prolog and Flask.

## Technologies Used

- Python
- Flask
- SWI-Prolog
- PySwip
- HTML (Jinja2 Templates)

## Description

This system allows users to ask questions about family relationships in natural language.

Example questions:
- Who is the father of Jess?
- Who is the mother of Simon?
- Who is the grandfather of Harry?
- Who is the sister of Jess?
- Who is the grandfather of Harry?
- Who is the grandmother of Simon?
- Who is the aunt of Simon?
- Who is the uncle of Harry?
- Who is the ancestor of Harry?

The system processes the question, queries a Prolog knowledge base (familytree.pl), and returns an answer in natural language.

## Project Structure

kinship-ai-system/
│
├── app.py
├── familytree.pl
├── requirements.txt
├── runtime.txt
└── templates/
    └── index.html

## How It Works

1. User enters a question in the web interface.
2. Flask processes the question.
3. PySwip sends a query to SWI-Prolog.
4. Prolog evaluates family rules.
5. The result is returned to the user.

## Author

Matsoso Phomolo
