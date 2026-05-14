# SQL-Assistant-MCP

SQL-Assistant-MCP is a simplified and refactored implementation inspired by the paper:
https://arxiv.org/pdf/2601.09393 (AINativeBench: Benchmarking AI-Native Applications and Agentic Architectures).

This project is NOT the original implementation from the paper. It has been rewritten and modularized so each component can be evaluated independently and inspected step-by-step.

The goal of this project is to provide a clear evaluation pipeline for agentic SQL systems, including generation, compliance checking, and result interpretation.

---

## Project Overview

This system consists of:

- MCP server for orchestration
- SQL generation agent (crew)
- SQL compliance checker agent (crew)
- Result interpreter agent (crew)
- Evaluation pipeline using test cases

Each component can be executed and evaluated independently.

---

## Requirements

This project uses uv as the Python package manager.

The following steps assume uv is already available in your environment.

---

## Setup Instructions

Run the following commands sequentially:

```
uv python install 3.12
uv venv --python 3.12
uv sync
source .venv/bin/activate
```

---

## Running the MCP Server

In one terminal, start the MCP server:
```
uv run python mcp_server.py
```
---

## Environment Variables

Before running the system, make sure you have:

- GROQ API Key (free tier can be used)
- Langfuse configured for tracing and observability

---

## Running Evaluation

In another terminal, start Jupyter Notebook:
```
jupyter notebook
```
Then open:
```
notebook_test.ipynb
```
This notebook runs the main evaluation pipeline.

It uses:

- test_cases folder
- database.sqlite (contains questions and ground truth answers)
- three crews:
  - SQL Generation Crew
  - Compliance Checker Crew
  - Result Interpreter Crew

The evaluation compares generated SQL outputs against ground truth results.

---

## Component-Level Testing

To analyze each part of the system independently, use the following notebooks:

- notebook_crew_sql_generation.ipynb
- notebook_crew_compliance_checker.ipynb
- notebook_crew_result_interpreter.ipynb

Each notebook allows you to inspect intermediate outputs and debug each crew separately.

---

## Purpose

This project is designed for:

- Benchmarking AI-native SQL agents
- Evaluating multi-agent workflows
- Debugging agentic pipelines step-by-step
- Reproducing structured evaluation similar to AINativeBench concepts

---

## Notes

- This project is for research and evaluation purposes
- It is intentionally simplified for modular inspection
- Not production-ready without further hardening and optimization
