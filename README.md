# 2-SAT-team-4
Презентація: https://www.canva.com/design/DAF2-djWkRA/1R7PqAoFCmE13J6AL9GsJQ/edit?utm_content=DAF2-djWkRA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton





Звіт

Вступ:

Цей код реалізує процес перефарбовування графа за допомогою алгоритму 2-SAT (Two-Satisfiability). 2-SAT є проблемою задоволення булевої формули, яка має специфічну структуру, що полегшує її розв'язання.

Опис функцій:

csv_to_graph(path: str) -> Tuple[Dict[int, List[int]], Dict[int, int]]:

Зчитує граф із CSV-файлу та створює його представлення у вигляді списку суміжностей.
Повертає граф та словник, який містить відображення вершин на їхні кольори.
transform_to_cnf(graph: Dict[int, List[int]], colors: Dict[int, int]) -> List[List[int]]:

Перетворює заданий граф та колірну мапу в кон'юнктивну нормальну форму (CNF).
Виводить список клозів, які представляють умови перефарбовування вершин.
implication_graph(cnf: List[List[int]]) -> Dict[int, List[int]]:

Створює граф імплікацій на основі заданої CNF.
Виводить орієнтований граф, де вершини є літералами, а ребра вказують на імплікації.
reverse_graph(imp_graph: Dict[int, List[int]]) -> Dict[int, List[int]]:

Повертає транспонований граф заданого орієнтованого графа.
dfs(imp_graph: Dict[int, List[int]], start: int, visited: List[int]) -> List[int]:

Виконує пошук в глибину на заданому графі та повертає порядок відвідування вершин.
find_scc(graph: Dict[int, List[int]]) -> List[List[int]]:

Знаходить сильно зв'язані компоненти у заданому графі (алгоритм Тарьяна).
recolor_graph(graph: Dict[int, List[int]], colors: Dict[int, int]) -> List[Tuple[int, int]]:

Використовує алгоритм 2-SAT для перефарбовування графа.
Повертає нову колірну мапу для вершин графа.
Висновок:

Цей код реалізує ефективний метод перефарбовування графа за допомогою 2-SAT, що дозволяє знайти валідне рішення для задачі задоволення булевої формули. При відсутності рішення, повертає "No solution". Код є чітким та легким для розуміння.
