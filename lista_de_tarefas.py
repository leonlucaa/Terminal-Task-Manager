import Manager
import screens

def run_task_manager():
    """Função principal que inicia e gerencia o loop do Gerenciador de Tarefas."""
    Manager.load_archives()

    if not Manager.TList.list_IDs:
        print("Nenhuma lista encontrada. Adicionando uma lista inicial 'Minhas Tarefas'.")
        Manager.list_manager.add_list("Minhas Tarefas")
        Manager.update_archives()

    while True:
        proxima_acao = screens.pagina_principal(1)
        if proxima_acao == "sair":
            break

if __name__ == "__main__":
    run_task_manager()
