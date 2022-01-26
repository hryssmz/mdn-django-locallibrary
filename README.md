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
pip install coverage
pip install flake8
pip install isort
pip install mypy
pip install pre-commit
```

#### 2.1.2. Django

---

```bash
pip install django
pip install djangorestframework
```

#### 2.1.3. MyPy Stubs

---

```bash
pip install django-stubs
pip install djangorestframework-stubs
```

## 3. Scripts

---

### 3.1. Check Linting and Formatting

---

```bash
# Test
clear && coverage run && coverage html && coverage report
# Check linting and formatting
black --check . && flake8 --quiet . && isort --check . && mypy .
```
