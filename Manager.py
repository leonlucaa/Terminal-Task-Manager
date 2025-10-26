from random import randint
from ListaDeTarefas import ListaDeTarefas as TList
from Tarefas import Tarefas as Tf
import os
import pickle
from datetime import date, timedelta

max_size = 2**32

def clear_screen():
    '''Limpa a tela do terminal.'''
    os.system('cls' if os.name == 'nt' else 'clear')

def update_archives():
    '''Atualiza os arquivos com os dados atuais do sistema.'''
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    archives_path = os.path.join(abs_dir, "archives")

    os.makedirs(archives_path, exist_ok=True)

    try:
        with open(os.path.join(archives_path, "list_IDs.pkl"), "wb") as f:
            pickle.dump(TList.list_IDs, f)
        with open(os.path.join(archives_path, "list_tasks.pkl"), "wb") as f:
            pickle.dump(TList.list_tasks, f)
        with open(os.path.join(archives_path, "list_titles.pkl"), "wb") as f:
            pickle.dump(TList.list_titles, f)
        with open(os.path.join(archives_path, "tasks_ID.pkl"), "wb") as f:
            pickle.dump(Tf.tasks_ID, f)
        
        serializable_tasks_description = {}
        for task_id, desc_list in Tf.tasks_description.items():
            temp_desc_list = desc_list[:]
            if len(temp_desc_list) > 2 and isinstance(temp_desc_list[2], date):
                temp_desc_list[2] = temp_desc_list[2].isoformat()
            if len(temp_desc_list) > 6 and isinstance(temp_desc_list[6], bool):
                temp_desc_list[6] = str(temp_desc_list[6])
            serializable_tasks_description[task_id] = temp_desc_list
            
        with open(os.path.join(archives_path, "tasks_description.pkl"), "wb") as f:
            pickle.dump(serializable_tasks_description, f)

    except Exception as e:
        print(f"Erro ao atualizar arquivos: {e}")


def load_archives():
    '''Carrega os dados salvos dos arquivos para o sistema na inicialização.'''
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    archives_path = os.path.join(abs_dir, "archives")

    try:
        with open(os.path.join(archives_path, "list_IDs.pkl"), "rb") as f:
            TList.list_IDs.update(pickle.load(f))
        with open(os.path.join(archives_path, "list_tasks.pkl"), "rb") as f:
            TList.list_tasks.update(pickle.load(f))
        with open(os.path.join(archives_path, "list_titles.pkl"), "rb") as f:
            TList.list_titles.update(pickle.load(f))
        with open(os.path.join(archives_path, "tasks_ID.pkl"), "rb") as f:
            Tf.tasks_ID.update(pickle.load(f))
        
        with open(os.path.join(archives_path, "tasks_description.pkl"), "rb") as f:
            loaded_desc = pickle.load(f)
            for task_id, desc_list in loaded_desc.items():
                if len(desc_list) > 2 and isinstance(desc_list[2], str):
                    try:
                        desc_list[2] = date.fromisoformat(desc_list[2])
                    except ValueError:
                        desc_list[2] = None
                if len(desc_list) > 6 and isinstance(desc_list[6], str):
                    desc_list[6] = True if desc_list[6].lower() == 'true' else False
                Tf.tasks_description[task_id] = desc_list

    except FileNotFoundError:
        print("Arquivos de dados não encontrados. Criando novos arquivos.")
        update_archives()
        if not TList.list_IDs:
            print("Adicionando uma lista inicial 'Minhas Tarefas'...")
            list_manager.add_list("Minhas Tarefas")

    except Exception as e:
        print(f"Erro ao carregar arquivos: {e}. Alguns dados podem não ter sido carregados corretamente.")


class list_manager:
    """Gerencia operações relacionadas às listas de tarefas."""

    @staticmethod
    def add_list(list_title):
        """
        Adiciona uma nova lista de tarefas ao sistema.
        :param list_title: Título da nova lista.
        :return: O ID da lista recém-criada.
        """
        ID = randint(1, max_size)
        while ID in TList.list_IDs.keys():
            ID = randint(1, max_size)

        new_list = TList(ID, list_title)
        TList.list_IDs[ID] = new_list
        TList.list_tasks[ID] = []
        TList.list_titles[ID] = list_title
        update_archives()
        return ID

    @staticmethod
    def pop_list(list_ID, suppress_message=False):
        """
        Remove uma lista de tarefas e todas as suas tarefas associadas.
        Impede a remoção da última lista.
        :param list_ID: ID da lista a ser removida.
        :param suppress_message: Se True, não imprime mensagens de sucesso/erro.
        :return: True se a remoção foi bem-sucedida, False caso contrário.
        """
        try:
            if len(TList.list_IDs) <= 1:
                if not suppress_message:
                    print("Não é possível remover a última lista. O sistema precisa de pelo menos uma lista.")
                return False

            if not suppress_message:
                confirm = input(f"Tem certeza que deseja remover a lista '{TList.list_titles.get(list_ID, 'Desconhecida')}' e TODAS as suas tarefas? (s/n): ").lower()
                if confirm != 's':
                    print("Remoção cancelada.")
                    return False

            actual_list_obj = TList.list_IDs.get(list_ID)
            if not actual_list_obj:
                if not suppress_message:
                    print("A lista não existe!")
                return False

            tasks_to_remove = list(TList.list_tasks.get(list_ID, []))
            for task_dict in tasks_to_remove:
                task_id = list(task_dict.keys())[0]
                task_manager.pop_task(task_id, suppress_message=True)

            TList.list_IDs.pop(list_ID)
            TList.list_titles.pop(list_ID)
            TList.list_tasks.pop(list_ID)
            update_archives()
            if not suppress_message:
                print(f"Lista '{actual_list_obj.list_title}' removida com sucesso!")
            return True
        except Exception as erro:
            if not suppress_message:
                print(f"Erro ao remover lista: {erro}.")
            return False

    @staticmethod
    def edit_list(list_ID, new_list_title):
        """
        Edita o título de uma lista de tarefas existente.
        Impede a alteração para um título já existente em outra lista.
        :param list_ID: ID da lista a ser editada.
        :param new_list_title: Novo título para a lista.
        :return: True se a edição foi bem-sucedida, False caso contrário.
        """
        try:
            current_title = TList.list_titles.get(list_ID)
            if new_list_title in TList.list_titles.values() and current_title != new_list_title:
                print("Já existe uma lista com esse título. Escolha outro, por favor.")
                return False

            lista_atual = TList.list_IDs.get(list_ID)
            if not lista_atual:
                print("A lista não existe!")
                return False

            lista_atual.list_title = new_list_title
            TList.list_titles[list_ID] = new_list_title
            update_archives()
            return True
        except Exception as erro:
            print(f"Erro ao editar lista: {erro}.")
            return False

class task_manager:
    """Gerencia operações relacionadas às tarefas."""

    @staticmethod
    def add_task(title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID):
        """
        Adiciona uma nova tarefa ao sistema.
        :param title: Título da tarefa.
        :param note: Nota da tarefa.
        :param date_obj: Objeto datetime.date da tarefa.
        :param tags: Tags da tarefa.
        :param priority: Prioridade da tarefa.
        :param frequency: Frequência de repetição da tarefa.
        :param conclusion_bool: Estado de conclusão (booleano).
        :param list_ID: ID da lista à qual a tarefa pertence.
        :return: True se a adição foi bem-sucedida, False caso contrário.
        """
        try:
            ID = randint(1, max_size)
            while ID in Tf.tasks_ID.keys():
                ID = randint(1, max_size)

            new_task = Tf(ID, title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID)
            
            Tf.tasks_ID[ID] = new_task
            TList.list_tasks.setdefault(list_ID, []).append({ID: new_task})
            
            Tf.tasks_description[ID] = [title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID]
            update_archives()
            return True
        except Exception as erro:
            print(f"Erro ao adicionar tarefa: {erro}.")
            return False

    @staticmethod
    def pop_task(ID, suppress_message=False):
        """
        Remove uma tarefa do sistema.
        :param ID: ID da tarefa a ser removida.
        :param suppress_message: Se True, não imprime mensagens de sucesso/erro.
        :return: True se a remoção foi bem-sucedida, False caso contrário.
        """
        try:
            actual_task = Tf.tasks_ID.get(ID)
            if not actual_task:
                if not suppress_message:
                    print("A tarefa não existe.")
                return False

            list_ID = actual_task.list_ID
            
            if list_ID in TList.list_tasks:
                TList.list_tasks[list_ID] = [t for t in TList.list_tasks[list_ID] if list(t.keys())[0] != ID]
            
            Tf.tasks_ID.pop(actual_task.ID)
            Tf.tasks_description.pop(actual_task.ID, None)
            update_archives()
            if not suppress_message:
                print(f"Tarefa '{actual_task.title}' removida com sucesso!")
            return True
        except Exception as erro:
            if not suppress_message:
                print(f"Erro ao remover tarefa: {erro}.")
            return False

    @staticmethod
    def edit_task(ID, title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID):
        """
        Edita os detalhes de uma tarefa existente, incluindo a possibilidade de movê-la para outra lista.
        :param ID: ID da tarefa a ser editada.
        :param title: Novo título da tarefa.
        :param note: Nova nota da tarefa.
        :param date_obj: Novo objeto datetime.date da tarefa.
        :param tags: Novas tags da tarefa.
        :param priority: Nova prioridade da tarefa.
        :param frequency: Nova frequência de repetição da tarefa.
        :param conclusion_bool: Novo estado de conclusão (booleano).
        :param list_ID: Novo ID da lista à qual a tarefa pertence.
        :return: True se a edição foi bem-sucedida, False caso contrário.
        """
        try:
            actual_task = Tf.tasks_ID.get(ID)
            if not actual_task:
                print("A tarefa não existe!")
                return False

            old_list_ID = actual_task.list_ID

            actual_task.title = title
            actual_task.note = note
            actual_task.date = date_obj
            actual_task.tags = tags
            actual_task.priority = priority
            actual_task.frequency = frequency
            actual_task.conclusion = conclusion_bool

            if old_list_ID != list_ID:
                if old_list_ID in TList.list_tasks:
                    TList.list_tasks[old_list_ID] = [t for t in TList.list_tasks[old_list_ID] if list(t.keys())[0] != ID]
                
                actual_task.list_ID = list_ID
                TList.list_tasks.setdefault(list_ID, []).append({ID: actual_task})
            
            Tf.tasks_description[ID] = [title, note, date_obj, tags, priority, frequency, conclusion_bool, list_ID]
            update_archives()
            return True
        except Exception as erro:
            print(f"Erro ao editar tarefa: {erro}.")
            return False

    @staticmethod
    def complete_task(ID):
        """
        Marca uma tarefa como concluída e gera uma nova instância se for uma tarefa repetitiva.
        :param ID: ID da tarefa a ser concluída.
        :return: True se a operação foi bem-sucedida, False caso contrário.
        """
        try:
            actual_task = Tf.tasks_ID.get(ID)
            if not actual_task:
                print("A tarefa não existe!")
                return False

            if actual_task.conclusion:
                print(f"Tarefa '{actual_task.title}' já está concluída.")
                return False

            actual_task.conclusion = True
            print(f"Tarefa '{actual_task.title}' marcada como concluída!")

            if actual_task.frequency != "Nenhuma" and actual_task.date:
                new_date = actual_task.date
                
                if actual_task.frequency == "Diária":
                    new_date += timedelta(days=1)
                elif actual_task.frequency == "Semanal":
                    new_date += timedelta(weeks=1)
                elif actual_task.frequency == "Mensal":
                    try:
                        new_date = new_date.replace(month=new_date.month + 1)
                    except ValueError:
                        if new_date.month == 12:
                            new_date = new_date.replace(year=new_date.year + 1, month=1)
                        else:
                            new_date = (new_date.replace(day=1, month=new_date.month + 2) - timedelta(days=1))
                elif actual_task.frequency == "Anual":
                    new_date = new_date.replace(year=new_date.year + 1)
                
                print(f"Gerando nova instância da tarefa '{actual_task.title}' para {new_date.strftime('%d/%m/%Y')}.")
                task_manager.add_task(
                    title=actual_task.title,
                    note=actual_task.note,
                    date_obj=new_date,
                    tags=actual_task.tags,
                    priority=actual_task.priority,
                    frequency=actual_task.frequency,
                    conclusion_bool=False,
                    list_ID=actual_task.list_ID
                )
            update_archives()
            return True
        except Exception as erro:
            print(f"Erro ao concluir tarefa: {erro}.")
            return False
