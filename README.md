# html- fragmentor

## Описание проекта

Разделить на фрагменты html документ с ограничением на длину (`MAX_LEN`).
Если тег не входит во множество (`BLOCK_TAGS`)
допустимых тегов генерируется `TagCanNotBeSplittenError`
или длина тега превышает ограничение на длину `MAX_LEN` генерируется `MaxLengthExceededError`

## Используемые библиотеки

* click
* beautifulsoup4
* htmlentities
* six

## Запуск проекта

### Создаем виртуальную среду для python

```
python -m venv .venv
.venv/Scripts/activate
```

### Устанавливаем `poetry` (python packaging and dependency management) и зависимости (dependencies) для проекта

```
pip install poetry
poetry install
```

### Запуск проекта

```
Usage: split_msg.py [OPTIONS] FILENAME

Options:
  --max-len INTEGER  maximum length of fragmented message
  --help             Show this message and exit.
```

```
python .\split_msg.py --max-len=4096 .\test-1.html
```

### Запуск тестов (unittests)

```
python -m unittest .\tests\msg_split_test.py
```