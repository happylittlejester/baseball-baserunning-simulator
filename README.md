# Python Template

[![python](https://img.shields.io/badge/Python-3.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![ruff](https://github.com/wnowicki/pytemp/workflows/Ruff/badge.svg)](https://github.com/wnowicki/pytemp/actions?query=branch%3Amain)
[![pytest](https://github.com/wnowicki/pytemp/workflows/Pytest/badge.svg)](https://github.com/wnowicki/pytemp/actions?query=branch%3Amain)
[![pylint](https://github.com/wnowicki/pytemp/workflows/Pylint/badge.svg)](https://github.com/wnowicki/pytemp/actions?query=branch%3Amain)
[![markdown](https://github.com/wnowicki/pytemp/workflows/Markdown%20Lint/badge.svg)](https://github.com/wnowicki/pytemp/actions?query=branch%3Amain)
[![License: GPLv3](https://img.shields.io/badge/License-MIT-blue.svg)](https://license.md/licenses/mit-license/)

## About Project

This project simulates baserunning in baseball by estimating how far the runner can advance based on the ball’s landing spot and the outfielders’ reaction time.
Using A* algorithm to find the shortest route for defenders, the model predicts how far the runner can advance before the outfielders reach the ball.

## Setup

1. Clone repository

```shell
git clone https://github.com/happylittlejester/baseball-baserunning-simulator.git
```

1. Install UV

```shell
pip install uv
```

1. Enter project directory

```shell
cd baseball-baserunning-simulator
```

1. Create Python Virtual Environment

```shell
uv sync
```

1. Open project in Visual Studio Code

## Run

Run project

```shell
uv run python app/main.py
```

## Test

```shell
uv run pytest
```

## Security

If you discover any security-related issues, please email [email](mailto:email) instead of using the issue tracker.

---
Copyright (c) 2026 Natalia Obst
