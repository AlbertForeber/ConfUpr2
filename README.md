ФИО: Шаймухаметов Альберт
Группа: ИКБО-41-24

# 1. Общее описание:
Программа реализует функционал построения графа зависимостей для пакета NuSpec
+ Возможен вывод в виде ASCII
+ Возможен вывод в виде фотографии

# 2. Описание всех функций и настроек
## graph_builder.py
Содержит класс GraphBuilder с полями:
+ test - хранит режим для построения графа (рабочий/тестовый)
+ path - хранит путь к файлу графа/API-адресу для получения .nuspec
+ package_id - содержит имя исходного пакета
+ version - содержит версию исходного пакета
+ filter - содержит фильтр-строку, содержащие которую пакеты исключаются
  
Методы:
+ build_one_layer_graph_from_nuspec - строит одноуровневый граф зависимостей исходного графа (без прохода по зависимостям)
+ build_graph - открытый метод построения графа, выбирает метод для построения в зависимости от переданной конфигурации
+ build_graph_from_nuspec - метод построения графа для рабочего режима
+ build_graph_from_test - метод построения графа для режима тестирования

Вспомогательные функции:
+ parse_dependencies_from_nuspec - извлекает все зависимости из дерева
+ from_xml_element_to_tuple - переводит xml-элемент одной зависимости в формат кортежа для использования в BFS-проходе

## nuspec_url_provider.py
Содержит класс NuspecUrlProvider с одним полем - nuspec_api_id, содержит адрес, по которому находятся end-points для обращения к API
Методы:
+ generate_nuspec - получает файл .nuspec для пакета определенной версии и переводит его в XML-дерево

## visualizer.py
Содержит класс Visualizer с одним полем graph - содержит граф, для которого строится визуальное представление
+ create_picture - cоздает представление в формате фотографии
+ draw_ascii - выводит ASCII-дерево зависимостей в терминал
+ draw_ascii_recursively - нужна для работоспособности draw_ascii, отвечатет за рекурсивную отрисовку

## main.py
Содержит класс DependencyTool с полями:
+ CONFIG_FILE_NAME - константа, хранащая имя конфигурационного файла
+ params - содержит параметры инструмента (имя, путь, режим, версия, ascii-режим, фильтр)
+ allowed_contents - допустимые аргументы для полей параметров
+ gb - содержит GraphBuilder инструмента
+ vis - содержит Visualizer инструмента

Методы:
+ load_config - загружает конфиг и заполняет поля параметров
+ check_field_content - проверка поля на соответствие допустимым значениям
+ start_up - начало работы инструмента - построение графа + отрисовка

# 3. Примеры использования
Запуск с конфигом:
```csv
name,Serilog
path,https://api.nuget.org/v3-flatcontainer
data_mode,url
version,2.2.1
show_ascii,true
filter,arp

```

ASCII-таблица
```shell
 └── Serilog (2.2.1)
     └── System.Collections (4.0.11)
         └── Microsoft.NETCore.Platforms (1.0.1)
         └── Microsoft.NETCore.Targets (1.0.1)
         └── System.Runtime (4.1.0)
     └── System.Dynamic.Runtime (4.0.11)
         └── System.Diagnostics.Debug (4.0.11)
         └── System.Globalization (4.0.11)
         └── System.Linq (4.1.0)
             └── System.Resources.ResourceManager (4.0.1)
         └── System.Linq.Expressions (4.1.0)
             └── System.IO (4.1.0)
                 └── System.Text.Encoding (4.0.11)
             └── System.Reflection.Emit.ILGeneration (4.0.1)
             └── System.Reflection.Emit.Lightweight (4.0.1)
             └── System.Reflection.Primitives (4.0.1)
             └── System.Reflection.TypeExtensions (4.1.0)
                 └── System.Diagnostics.Contracts (4.0.1)
             └── System.Resources.ResourceManager (4.1.0)
             └── System.ObjectModel (4.0.12)
             └── System.Reflection.Emit (4.0.1)
         └── System.ObjectModel (4.0.11)
         └── System.Reflection (4.1.0)
             └── System.IO (4.1.0)
             └── System.Reflection.Primitives (4.1.0)
         └── System.Reflection.TypeExtensions (4.0.11)
         └── System.Resources.ResourceManager (4.0.11)
         └── System.Runtime (4.0.11)
         └── System.Runtime.Extensions (4.1.0)
         └── System.Threading (4.0.11)
             └── System.Threading.Tasks (4.0.11)
         └── System.Reflection.Emit (4.0.11)
         └── System.Reflection.Emit.ILGeneration (4.0.11)
         └── System.Reflection.Primitives (4.0.11)
     └── System.Globalization (2.2.1)
     └── System.Linq (2.2.1)
     └── System.Reflection (2.2.1)
     └── System.Reflection.Extensions (4.0.1)
         └── Microsoft.NETCore.Platforms (4.0.1)
         └── Microsoft.NETCore.Targets (4.0.1)
         └── System.Runtime (4.0.1)
     └── System.Runtime (2.2.1)
     └── System.Runtime.Extensions (2.2.1)
     └── System.Text.RegularExpressions (4.1.0)
         └── System.Resources.ResourceManager (4.1.0)
         └── System.Threading (4.1.0)
     └── System.Threading (2.2.1)
----------------------------------------
 └── System.Collections (4.0.11)
     └── Microsoft.NETCore.Platforms (1.0.1)
     └── Microsoft.NETCore.Targets (1.0.1)
     └── System.Runtime (4.1.0)
----------------------------------------
 └── System.Dynamic.Runtime (4.0.11)
     └── System.Diagnostics.Debug (4.0.11)
     └── System.Globalization (4.0.11)
     └── System.Linq (4.1.0)
         └── System.Resources.ResourceManager (4.0.1)
     └── System.Linq.Expressions (4.1.0)
         └── System.IO (4.1.0)
             └── System.Text.Encoding (4.0.11)
         └── System.Reflection.Emit.ILGeneration (4.0.1)
         └── System.Reflection.Emit.Lightweight (4.0.1)
         └── System.Reflection.Primitives (4.0.1)
         └── System.Reflection.TypeExtensions (4.1.0)
             └── System.Diagnostics.Contracts (4.0.1)
         └── System.Resources.ResourceManager (4.1.0)
         └── System.ObjectModel (4.0.12)
         └── System.Reflection.Emit (4.0.1)
     └── System.ObjectModel (4.0.11)
     └── System.Reflection (4.1.0)
         └── System.IO (4.1.0)
         └── System.Reflection.Primitives (4.1.0)
     └── System.Reflection.TypeExtensions (4.0.11)
     └── System.Resources.ResourceManager (4.0.11)
     └── System.Runtime (4.1.0)
     └── System.Runtime.Extensions (4.1.0)
     └── System.Threading (4.0.11)
         └── System.Threading.Tasks (4.0.11)
     └── System.Reflection.Emit (4.0.11)
     └── System.Reflection.Emit.ILGeneration (4.0.11)
     └── System.Reflection.Primitives (4.0.11)
----------------------------------------
 └── System.Globalization (4.0.11)
----------------------------------------
 └── System.Linq (4.1.0)
     └── System.Resources.ResourceManager (4.0.1)
----------------------------------------
 └── System.Reflection (4.1.0)
     └── System.IO (4.1.0)
         └── System.Text.Encoding (4.0.11)
     └── System.Reflection.Primitives (4.0.1)
----------------------------------------
 └── System.Reflection.Extensions (4.0.1)
     └── Microsoft.NETCore.Platforms (1.0.1)
     └── Microsoft.NETCore.Targets (1.0.1)
     └── System.Runtime (4.1.0)
----------------------------------------
 └── System.Runtime (4.1.0)
----------------------------------------
 └── System.Runtime.Extensions (4.1.0)
----------------------------------------
 └── System.Text.RegularExpressions (4.1.0)
     └── System.Resources.ResourceManager (4.0.1)
     └── System.Threading (4.0.11)
         └── System.Threading.Tasks (4.0.11)
----------------------------------------
 └── System.Threading (4.0.11)
     └── System.Threading.Tasks (4.0.11)
----------------------------------------
 └── Microsoft.NETCore.Platforms (1.0.1)
----------------------------------------
 └── Microsoft.NETCore.Targets (1.0.1)
----------------------------------------
 └── System.Diagnostics.Debug (4.0.11)
----------------------------------------
 └── System.Linq.Expressions (4.1.0)
     └── System.IO (4.1.0)
         └── System.Text.Encoding (4.0.11)
     └── System.Reflection.Emit.ILGeneration (4.0.1)
     └── System.Reflection.Emit.Lightweight (4.0.1)
     └── System.Reflection.Primitives (4.0.1)
     └── System.Reflection.TypeExtensions (4.1.0)
         └── System.Diagnostics.Contracts (4.0.1)
     └── System.Resources.ResourceManager (4.0.1)
     └── System.ObjectModel (4.0.12)
     └── System.Reflection.Emit (4.0.1)
----------------------------------------
 └── System.ObjectModel (4.0.12)
----------------------------------------
 └── System.Reflection.TypeExtensions (4.1.0)
     └── System.Diagnostics.Contracts (4.0.1)
----------------------------------------
 └── System.Resources.ResourceManager (4.0.1)
----------------------------------------
 └── System.Reflection.Emit (4.0.1)
----------------------------------------
 └── System.Reflection.Emit.ILGeneration (4.0.1)
----------------------------------------
 └── System.Reflection.Primitives (4.0.1)
----------------------------------------
 └── System.IO (4.1.0)
     └── System.Text.Encoding (4.0.11)
----------------------------------------
 └── System.Threading.Tasks (4.0.11)
----------------------------------------
 └── System.Reflection.Emit.Lightweight (4.0.1)
----------------------------------------
 └── System.Diagnostics.Contracts (4.0.1)
----------------------------------------
 └── System.Text.Encoding (4.0.11)
----------------------------------------
```
