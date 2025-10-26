from Tarefas import Tarefas as Tf
from datetime import date, timedelta

def get_all_tasks():
    """
    Retorna uma lista de todos os objetos Tarefa atualmente no sistema.
    """
    return list(Tf.tasks_ID.values())

def filter_tasks(tasks, filter_type, target_list_id=None, target_tag=None):
    """
    Filtra uma lista de tarefas baseada em diversos critérios.
    :param tasks: Lista de objetos Tarefa para filtrar.
    :param filter_type: Tipo de filtro ("todas", "hoje", "7dias", "nao_concluidas", "concluidas", "por_lista", "por_tag").
    :param target_list_id: ID da lista para filtro "por_lista".
    :param target_tag: Tag para filtro "por_tag".
    :return: Lista de objetos Tarefa filtrados.
    """
    filtered = []
    today = date.today()

    for task_obj in tasks:
        include = True

        if filter_type == "hoje":
            if not task_obj.date or task_obj.date > today:
                include = False
        elif filter_type == "7dias":
            seven_days_from_now = today + timedelta(days=7)
            if not task_obj.date or task_obj.date > seven_days_from_now:
                include = False
        elif filter_type == "nao_concluidas":
            if task_obj.conclusion:
                include = False
        elif filter_type == "concluidas":
            if not task_obj.conclusion:
                include = False
        elif filter_type == "por_lista":
            if task_obj.list_ID != target_list_id:
                include = False
        elif filter_type == "por_tag":
            if target_tag and target_tag.lower() not in task_obj.tags.lower():
                include = False

        if include:
            filtered.append(task_obj)
            
    return filtered

def sort_tasks(tasks, sort_by="data"):
    """
    Ordena uma lista de tarefas com base em critérios definidos.
    :param tasks: Lista de objetos Tarefa para ordenar.
    :param sort_by: Critério de ordenação ("data" ou "prioridade").
    :return: Lista de objetos Tarefa ordenada.
    """
    priority_map = {"Alta": 1, "Média": 2, "Baixa": 3, "Sem Prioridade": 4}

    if sort_by == "data":
        return sorted(tasks, key=lambda task: (
            task.date if task.date else date.max,
            priority_map.get(task.priority, 5),
            task.list_ID
        ))
    elif sort_by == "prioridade":
        return sorted(tasks, key=lambda task: (
            priority_map.get(task.priority, 5),
            task.date if task.date else date.max,
            task.list_ID
        ))
    else:
        return tasks
