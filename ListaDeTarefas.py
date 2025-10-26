class ListaDeTarefas:
    """
    Representa uma lista de tarefas.
    Armazena e gerencia listas, tarefas associadas e títulos.
    """
    list_IDs = {}      # {list_ID: ListaDeTarefas_objeto}
    list_tasks = {}    # {list_ID: [{task_ID: Tarefas_objeto}, ...]}
    list_titles = {}   # {list_ID: list_title}

    def __init__(self, list_ID, list_title):
        """
        Inicializa uma nova instância de ListaDeTarefas.
        :param list_ID: ID único da lista.
        :param list_title: Título da lista.
        """
        self.list_ID = list_ID
        self.list_title = list_title
