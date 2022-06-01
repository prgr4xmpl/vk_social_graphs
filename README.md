# vk_social_graphs
vk_social_graphs - проект, позволяющий получать и анализировать социальные графы ВКонтакте.
# Notes
## Установка
Все необходимые пакеты и их версии находятся в файле **requirements.txt** и могут быть установлены с помощью:
```
pip install -r requirements.txt
```
После, необходимо создать файл **local_settings.py** и добавить данные для логина во ВКонтакте в формате:
```python
LOGIN = 'MY_LOGIN'
PASSWORD = 'MY_PASSWORD'
```
## Использование
Запустите скрипт, передав (опционально) ему следующие параметры:
```
-input="somefile" или -i="somefile" ("user_list.in", если параметр не был передан)
-users=user1,user2,user2 или -u=user1, ... (-users имеет приоритет над -input)
-output="somefile" или -o="somefile" (Название выходного файла будет сгенерировано исходя из начальных пользователей, если параметр не был передан)
-depth=some_depth или "-d=some_depth" (Изначально 2, если параметр не был передан. Большая глубина не рекомендуется ввиду скорости работы)
```
Если скрипт успешно завершил свою работу, то в директории проекта появится файл с выходными данными в формате **JSON** объёкта.
Данный объект имеет следующую структуру:
```
{

  data: {} информация о социальном графе
  
  links: информация о связях в графе
  {
    [
      {
        source: id человека №1
        target: id человека #2
      }
    ]
  }
  
  nodes: информация о людях в графе
  {
    [
      {
        id: id человека
        data: {}
      }
    ]
  }
  
}
```
