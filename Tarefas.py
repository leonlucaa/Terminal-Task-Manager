from datetime import date

class Tarefas:
    """
    Representa uma tarefa individual.
    Armazena detalhes da tarefa e serve como repositório global para todas as tarefas.
    """
    tasks_ID = {}          # {task_ID: Tarefas_objeto}
    tasks_description = {} # {task_ID: [title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID]}

    def __init__(self, ID, title, note, date_obj, tags, priority, frequency, conclusion, list_ID):
        """
        Inicializa uma nova instância de Tarefa.
        :param ID: ID único da tarefa.
        :param title: Título da tarefa.
        :param note: Nota detalhada da tarefa (opcional).
        :param date_obj: Data de conclusão da tarefa (objeto datetime.date, opcional).
        :param tags: Tags associadas à tarefa (string, ex: "trabalho, urgente").
        :param priority: Prioridade da tarefa (ex: "Alta", "Média").
        :param frequency: Frequência de repetição (ex: "Diária", "Semanal").
        :param conclusion: Estado de conclusão (booleano).
        :param list_ID: ID da lista à qual a tarefa pertence.
        """
        self.ID = ID
        self.title = title
        self.note = note
        self.date = date_obj
        self.tags = tags
        self.priority = priority
        self.frequency = frequency
        self.conclusion = conclusion
        self.list_ID = list_ID

