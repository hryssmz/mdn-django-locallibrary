# mdn-django-locallibrary

A simple Django local library app provided by MDN.

## 1. Getting Started

---

```bash
cd mdn-django-locallibrary

# Create virtual env and install Python packages.
python -m venv venv
. ./venv/bin/activate
pip install -r requirement.txt

# Install Node.js library.
npm install
```

## 2. From Scratch

---

### 2.1. Install Python Library

---

```bash
# Create virtual env and install Python packages.
python -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
```

#### 2.1.1. Development Tools

---

```bash
pip install black
pip install flake8
pip install isort
pip install mypy
```

#### 2.1.2. Django

---

```bash
pip install django
pip install django-stubs
pip install djangorestframework
```

## 3. Scripts

---

### 3.1. Check Linting and Formatting

---

```bash
# Black
black --check .

# Flake8
flake8 --quiet .

# Isort
isort --check .

# MyPy
mypy .

# All
black --check . && flake8 --quiet . && isort --check . && mypy .
```
