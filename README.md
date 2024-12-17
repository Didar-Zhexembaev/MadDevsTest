# html- fragmentor

# Algorithm

Проверка идет от корня к потомкам

1. Проверяем `closed_tags`
	1.1. Вытаскиваем из стека `closed_tags`
		1.1.1. Добавляем в стек `opened_tags`
		1.1.2. Добавлем в список названия тега `get_key()`
		1.1.3. Создаем из списка строку c открывающими тегами и присваиваем `opening_tag` = `opened_tags_list_str`
		1.1.4. Создаем из списка строку c закрывающими тегами и присваиваем `closing_tag` += `closing_tag_list_str`
		1.1.5. Вычисляем длину `opening_tag_len`
		1.1.6. Вычисляем длину `closing_tag_len`
		1.1.7. `length` += `opening_tag_len` + `closing_tag_len`
		1.1.8. Проверяем `length` > `max_len`
			1.1.8.1. Выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`
		1.1.9. Вычисляем длину `after_tag_content_len`
		1.2.0. `length` += `after_tag_content_len`
		1.2.1. Проверяем `length` > `max_len`
			1.2.1.0 Выбрасываем `MaxLengthExceeded(f'{opening_tag}({after_tag_content_len}) + {after_tag_content}({after_tag_content_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`

2. Иначе добавляем в длину `length` += `opening_tag_len` + `closing_tag_len`

# Проверка для корневого элемента
3. Проверяем `length` > `max_len`
	2.1. Проверяем `opened_tags`
	2.2. Если пустое выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`

#  Проверка для корневого элемента и для потомка
3. Добавляем в длину `length` += `before_tag_content_len`
4. Проверяем `length` > `max_len`
	4.1. Проверяем `opened_tags`
	4.2. Если пустое выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {before_tag_content}({before_tag_content_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`
	4.3. Иначе вытаскиваем из стека `opened_tags` добавляем в `buffer` и в стек `closed_tags`
	4.4. Вытаскиваем данные из буфера `buffer.tounicode()`
	4.5. Очищаем буфер
	4.6. Обнуляем длину `length`
	4.7. (Yield) Возвращаем данные буфера

5. Вытаскиваем из стека `closed_tags`
	5.1. Добавляем в стек `opened_tags`
	5.2. Добавлем в список названия тега `get_key()`
	5.3. Создаем из списка строку c открывающими тегами и присваиваем `opening_tag` = `opened_tags_list_str` + `opening_tag`
	5.4. Создаем из списка строку c закрывающими тегами и присваиваем `closing_tag` += `closing_tag_list_str`
	5.5. Вычисляем длину `opening_tag_len`
	5.6. Вычисляем длину `closing_tag_len`
	5.7. (0) `length` += `opening_tag_len` + `closing_tag_len`
	5.8. Проверяем `length` > `max_len`
		6.6.1. Выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`
	5.9. `length` += `before_tag_content_len`
	5.10. Проверяем `length` > `max_len`
		6.8.1. Выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {before_tag_content}({before_tag_content_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`
	5.11. Добавляем в `buffer` `opening_tag` + `before_tag_content`

6. Проверяем количество потомков `child_nodes_count` == 0
	6.1. Добавляем в `buffer` `closing_tag`
	6.2. `length` += `after_tag_content_len`
	6.3. Проверяем `length` > `max_len`
		6.3.1. Проверяем `opened_tags`
		6.3.2. Если пустое выбрасываем `MaxLengthExceeded(f'{opening_tag}({opening_tag_len}) + {after_tag_content}({after_tag_content_len}) + {closing_tag}({closing_tag_len}) = {length} > {max_len}')`
		6.3.3. Иначе вытаскиваем из стека `opened_tags` добавляем в `buffer` и в стек `closed_tags`
		6.3.4. Вытаскиваем данные из буфера `buffer.tounicode()`
		6.3.5. Очищаем буфер
		6.3.6. Обнуляем длину `length`
		6.3.7. (Yield) Возвращаем данные буфера
	6.4. Вытаскиваем из стека `opened_tags` и декрементируем `closest_parent_tag.child_nodes_count`
		6.4.1. Проверяем `closest_parent_tag.child_nodes_count` <= 0
		6.4.2. Проверяем `closest_parent_tag.child_nodes_count` < 0
			6.4.2.1. `opened_tags.pop()`
			6.4.2.2. Переходим к следующему
		6.4.3. Добавляем в буфер `closed_tags`
		6.4.4. Вытаскиваем `opening_tags.pop()`
		6.4.5. `length` += `after_tag_content_len`
		6.4.6. Проверяем `length` > `max_len`
			6.4.6.1. Прерываем цикл break
		6.4.7. Записываем в буфер `after_tag_content`
		6.4.8. Очищаем `after_tag_content`
7. Иначе добавляем в `opened_tags` данные текущего тега `{tag_name, child_nodes_count}`
