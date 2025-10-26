from Manager import list_manager, task_manager, clear_screen
from ListaDeTarefas import ListaDeTarefas as TList
from Tarefas import Tarefas as Tf
from datetime import date, timedelta
import ViewHelpers

lm = list_manager()
tm = task_manager()

ITENS_POR_PAGINA = 10

def obter_entrada_numerica(prompt, min_val=1, max_val=None):
    """
    Obtém uma entrada numérica do usuário com validação de faixa.
    """
    while True:
        try:
            valor = int(input(prompt))
            if max_val is not None and (valor < min_val or valor > max_val):
                print(f"Por favor, escolha um número entre {min_val} e {max_val}.")
            elif valor < min_val:
                 print(f"Por favor, escolha um número maior ou igual a {min_val}.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

def obter_entrada_data(prompt):
    """
    Obtém uma entrada de data do usuário no formato DD/MM/AAAA.
    Permite entrada vazia para datas opcionais.
    """
    while True:
        data_str = input(prompt)
        if not data_str:
            return None
        try:
            dia, mes, ano = map(int, data_str.split('/'))
            return date(ano, mes, dia)
        except ValueError:
            print("Formato de data inválido. Por favor, use DD/MM/AAAA (ex: 04/07/2025).")

def obter_entrada_prioridade(prompt):
    """
    Obtém uma entrada de prioridade do usuário com validação.
    """
    prioridades_validas = ["sem prioridade", "baixa", "media", "alta"]
    while True:
        prioridade = input(prompt + " (Sem Prioridade, Baixa, Média, Alta): ").lower()
        if prioridade in prioridades_validas:
            return prioridade.capitalize()
        else:
            print("Prioridade inválida. Por favor, escolha uma das opções.")

def obter_entrada_frequencia(prompt):
    """
    Obtém uma entrada de frequência do usuário com validação.
    """
    frequencias_validas = ["nenhuma", "diaria", "semanal", "mensal", "anual"]
    while True:
        frequencia = input(prompt + " (Nenhuma, Diária, Semanal, Mensal, Anual): ").lower()
        if frequencia in frequencias_validas:
            return frequencia.capitalize()
        else:
            print("Frequência inválida. Por favor, escolha uma das opções.")

def obter_entrada_conclusao(prompt):
    """
    Obtém uma entrada de estado de conclusão (Pendente/Concluído) do usuário.
    """
    while True:
        conclusao = input(prompt + " (Pendente/Concluído): ").lower()
        if conclusao in ["pendente", "concluido"]:
            return True if conclusao == "concluido" else False
        else:
            print("Estado de conclusão inválido. Por favor, digite 'Pendente' ou 'Concluído'.")


def exibir_detalhes_tarefa(tarefa_obj, lista_obj_origem, pagina_origem):
    """
    Exibe todos os detalhes de uma tarefa específica.
    Permite voltar à tela anterior.
    """
    clear_screen()
    print(f"\n--- Detalhes da Tarefa: '{tarefa_obj.title}' ---")
    print(f"ID: {tarefa_obj.ID}")
    print(f"Título: {tarefa_obj.title}")
    print(f"Nota: {tarefa_obj.note if tarefa_obj.note else 'N/A'}")
    print(f"Data: {tarefa_obj.date.strftime('%d/%m/%Y') if tarefa_obj.date else 'N/A'}")
    print(f"Tags: {tarefa_obj.tags if tarefa_obj.tags else 'N/A'}")
    print(f"Prioridade: {tarefa_obj.priority}")
    print(f"Frequência: {tarefa_obj.frequency}")
    print(f"Concluída: {'Sim' if tarefa_obj.conclusion else 'Não'}")
    list_title_for_task = TList.list_titles.get(tarefa_obj.list_ID, "Lista Desconhecida")
    print(f"Pertence à Lista: {list_title_for_task}")

    input("\nPressione Enter para voltar...")
    return selecionar_lista_tela(lista_obj_origem, pagina_origem)


def adicionar_lista_tela():
    """Tela para adicionar uma nova lista de tarefas."""
    clear_screen()
    print("\n--- Adicionar Nova Lista ---")
    titulo = input("Digite o título da lista: ")
    while titulo in TList.list_titles.values():
        print("Já existe uma lista com esse título. Escolha outro, por favor.")
        titulo = input("Digite o título da lista: ")
    
    lm.add_list(titulo)
    print(f"Lista '{titulo}' adicionada com sucesso!")
    input("\nPressione Enter para continuar...")
    return pagina_principal(1)

def editar_lista_tela(objeto_lista):
    """
    Tela para editar o título de uma lista existente.
    """
    clear_screen()
    print(f"\n--- Editando Lista: '{objeto_lista.list_title}' ---")
    print("Digite o novo título da lista (deixe em branco para manter o atual):")
    novo_titulo = input(f"Novo título ({objeto_lista.list_title}): ")
    
    if not novo_titulo:
        print("Título não alterado.")
        input("\nPressione Enter para continuar...")
        return pagina_principal(1)

    if lm.edit_list(objeto_lista.list_ID, novo_titulo):
        print(f"Lista '{objeto_lista.list_title}' renomeada para '{novo_titulo}' com sucesso!")
    else:
        print("Não foi possível renomear a lista.")
    input("\nPressione Enter para continuar...")
    return pagina_principal(1)

def adicionar_tarefa_tela(objeto_lista):
    """
    Tela para adicionar uma nova tarefa a uma lista específica.
    """
    clear_screen()
    print(f"\n--- Adicionar Nova Tarefa na Lista: '{objeto_lista.list_title}' ---")
    titulo = input("Digite o título da tarefa: ")
    nota = input("Digite a nota (opcional): ")
    
    data_objeto = obter_entrada_data("Digite a data de conclusão (DD/MM/AAAA, opcional): ")
    
    tags = input("Digite as tags (separadas por vírgula, opcional): ")
    prioridade = obter_entrada_prioridade("Digite a prioridade")
    frequencia = obter_entrada_frequencia("Digite a frequência")
    conclusao_bool = obter_entrada_conclusao("Digite o estado de conclusão") 

    if tm.add_task(titulo, nota, data_objeto, tags, prioridade, frequencia, conclusao_bool, objeto_lista.list_ID):
        print("Tarefa adicionada com sucesso!")
    else:
        print("Não foi possível adicionar a tarefa.")
    input("\nPressione Enter para continuar...")
    return selecionar_lista_tela(objeto_lista, 1)

def editar_tarefa_tela(lista_original_obj, tarefa_obj):
    """
    Tela para editar os detalhes de uma tarefa existente.
    """
    clear_screen()
    print(f"\n--- Editando Tarefa: '{tarefa_obj.title}' (Lista: {lista_original_obj.list_title}) ---")
    print("Deixe o campo em branco para manter o valor atual.")

    novo_titulo = input(f"Novo título ({tarefa_obj.title}): ") or tarefa_obj.title
    nova_nota = input(f"Nova nota ({tarefa_obj.note}): ") or tarefa_obj.note
    
    data_atual_str = tarefa_obj.date.strftime('%d/%m/%Y') if tarefa_obj.date else "N/A"
    nova_data_input = input(f"Nova data ({data_atual_str}, DD/MM/AAAA, opcional): ")
    if nova_data_input == "":
        nova_data_objeto = tarefa_obj.date
    else:
        try:
            dia, mes, ano = map(int, nova_data_input.split('/'))
            nova_data_objeto = date(ano, mes, dia)
        except ValueError:
            print("Formato de data inválido. Mantendo a data atual.")
            nova_data_objeto = tarefa_obj.date

    novas_tags = input(f"Novas tags ({tarefa_obj.tags}): ") or tarefa_obj.tags
    nova_prioridade = obter_entrada_prioridade(f"Nova prioridade ({tarefa_obj.priority})") or tarefa_obj.priority
    nova_frequencia = obter_entrada_frequencia(f"Nova frequência ({tarefa_obj.frequency})") or tarefa_obj.frequency
    
    estado_conclusao_atual_str = "Concluído" if tarefa_obj.conclusion else "Pendente"
    nova_conclusao_bool = obter_entrada_conclusao(f"Novo estado de conclusão ({estado_conclusao_atual_str})") 


    clear_screen()
    print("\n--- Mover Tarefa para Outra Lista ---")
    print(f"Tarefa atual na lista: '{lista_original_obj.list_title}'")
    
    todas_listas_obj = list(TList.list_IDs.values())
    listas_exibiveis = [l_obj for l_obj in todas_listas_obj if l_obj.list_ID != lista_original_obj.list_ID]
    
    nova_lista_ID = lista_original_obj.list_ID

    if not listas_exibiveis:
        print("Nenhuma outra lista disponível para mover a tarefa.")
    else:
        lista_selecionada_obj = None
        pagina_listas = 1
        
        while lista_selecionada_obj is None:
            clear_screen()
            print(f"\n--- Selecione a Nova Lista para '{tarefa_obj.title}' (Página {pagina_listas}) ---")
            n_listas = ITENS_POR_PAGINA * (pagina_listas - 1)
            listas_da_pagina = listas_exibiveis[n_listas : n_listas + ITENS_POR_PAGINA]
            
            if not listas_da_pagina and n_listas == 0:
                print("Nenhuma outra lista disponível para mover a tarefa.")
                break 
            elif not listas_da_pagina and n_listas > 0:
                print("Não há mais páginas de listas. Voltando à última página.")
                pagina_listas -= 1
                input("Pressione Enter para continuar...")
                continue

            for i, l_obj in enumerate(listas_da_pagina):
                print(f"  {n_listas + i + 1}. {l_obj.list_title}")
            
            print("\nOpções: prox (próxima página), ant (página anterior), manter (manter na lista atual), ou digite o NÚMERO da lista.")
            escolha_lista_str = input("Sua escolha: ").lower()

            if escolha_lista_str == "manter" or escolha_lista_str == "":
                print("Tarefa permanecerá na lista atual.")
                break
            elif escolha_lista_str == "prox":
                if (n_listas + ITENS_POR_PAGINA) < len(listas_exibiveis):
                    pagina_listas += 1
                else:
                    print("Não existem mais páginas de listas!")
            elif escolha_lista_str == "ant":
                if pagina_listas > 1:
                    pagina_listas -= 1
                else:
                    print("Já está na primeira página de listas!")
            else:
                try:
                    num_lista_escolhida = int(escolha_lista_str)
                    if 1 <= num_lista_escolhida <= len(listas_exibiveis):
                        lista_selecionada_obj = listas_exibiveis[num_lista_escolhida - 1]
                        nova_lista_ID = lista_selecionada_obj.list_ID
                        print(f"Tarefa será movida para '{lista_selecionada_obj.list_title}'.")
                        break
                    else:
                        print("Número de lista inválido.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número ou uma opção válida.")
            input("\nPressione Enter para continuar...")

    if tm.edit_task(tarefa_obj.ID, novo_titulo, nova_nota, nova_data_objeto, novas_tags, nova_prioridade, nova_frequencia, nova_conclusao_bool, nova_lista_ID):
        print("Tarefa editada com sucesso!")
    else:
        print("Não foi possível editar a tarefa.")
    input("\nPressione Enter para continuar...")
    if nova_lista_ID != lista_original_obj.list_ID and nova_lista_ID in TList.list_IDs:
        return selecionar_lista_tela(TList.list_IDs[nova_lista_ID], 1)
    else:
        return selecionar_lista_tela(lista_original_obj, 1)

def exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj=None, origem_chamada_page=1):
    """
    Função auxiliar para exibir tarefas de forma genérica com paginação.
    Oferece opções para editar, remover, concluir tarefas e ver detalhes.
    """
    clear_screen()
    total_paginas = (total_itens_filtrados + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
    if total_paginas == 0 and total_itens_filtrados > 0:
        total_paginas = 1
    
    n = ITENS_POR_PAGINA * (pagina - 1)
    tarefas_da_pagina = tarefas_a_exibir[n : n + ITENS_POR_PAGINA]

    print(f"\n--- {titulo_tela} (Página {pagina}/{total_paginas if total_paginas > 0 else 1}) ---")
    if not tarefas_da_pagina:
        print("Nenhuma tarefa encontrada para os critérios selecionados.")
    else:
        for i, tarefa_obj in enumerate(tarefas_da_pagina):
            status = "Concluída" if tarefa_obj.conclusion else "Pendente"
            data_info = tarefa_obj.date.strftime('%d/%m/%Y') if tarefa_obj.date else "N/A"
            list_title_for_task = TList.list_titles.get(tarefa_obj.list_ID, "Lista Desconhecida")
            print(f"{n + i + 1}. [Lista: {list_title_for_task}] Título: {tarefa_obj.title} | Data: {data_info} | Prioridade: {tarefa_obj.priority} | Status: {status}")

    print("\nOpções: detalhes, editar, remover, concluir, prox (próxima página), ant (página anterior), voltar")
    opcao = input("Escolha uma opção: ").lower()

    while opcao not in ["detalhes", "editar", "remover", "concluir", "prox", "ant", "voltar"]:
        print("Não entendi. Digite novamente por favor.")
        opcao = input("Escolha uma opção: ").lower()

    if opcao == "detalhes":
        if not tarefas_da_pagina:
            print("Não há tarefas para ver detalhes nesta página.")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        
        num_tarefa = obter_entrada_numerica("Escolha o número da tarefa para ver detalhes: ", 1, len(tarefas_da_pagina))
        tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
        
        if origem_chamada_obj:
             return exibir_detalhes_tarefa(tarefa_selecionada, origem_chamada_obj, pagina)
        else:
             return exibir_detalhes_tarefa(tarefa_selecionada, None, None)

    elif opcao == "editar":
        if not tarefas_da_pagina:
            print("Não há tarefas para editar nesta página.")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        
        num_tarefa = obter_entrada_numerica("Escolha o número da tarefa que deseja editar: ", 1, len(tarefas_da_pagina))
        tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
        lista_obj_da_tarefa = TList.list_IDs.get(tarefa_selecionada.list_ID)
        if lista_obj_da_tarefa:
            return editar_tarefa_tela(lista_obj_da_tarefa, tarefa_selecionada)
        else:
            print("Erro: Lista da tarefa não encontrada.")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)

    elif opcao == "remover":
        if not tarefas_da_pagina:
            print("Não há tarefas para remover nesta página.")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        
        num_tarefa = obter_entrada_numerica("Escolha o número da tarefa que deseja remover: ", 1, len(tarefas_da_pagina))
        tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
        
        confirmar = input(f"Tem certeza que deseja remover a tarefa '{tarefa_selecionada.title}'? (s/n): ").lower()
        if confirmar == 's':
            if tm.pop_task(tarefa_selecionada.ID):
                print("Tarefa removida com sucesso!")
            else:
                print("Não foi possível remover a tarefa.")
        else:
            print("Remoção cancelada.")
        input("\nPressione Enter para continuar...")
        return pagina_principal(1)

    elif opcao == "concluir":
        if not tarefas_da_pagina:
            print("Não há tarefas para marcar como concluídas nesta página.")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        
        num_tarefa = obter_entrada_numerica("Escolha o número da tarefa que deseja marcar como concluída: ", 1, len(tarefas_da_pagina))
        tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
        
        if tm.complete_task(tarefa_selecionada.ID):
            pass
        input("\nPressione Enter para continuar...")
        return pagina_principal(1)

    elif opcao == "prox":
        if (n + ITENS_POR_PAGINA) < total_itens_filtrados:
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina + 1, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        else:
            print("Não existem mais tarefas nesta visualização!")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
    elif opcao == "ant":
        if pagina > 1:
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina - 1, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
        else:
            print("Já está no início das tarefas desta visualização!")
            input("\nPressione Enter para continuar...")
            return exibir_tarefas_comuns(tarefas_a_exibir, titulo_tela, pagina, total_itens_filtrados, origem_chamada_obj, origem_chamada_page)
    elif opcao == "voltar":
        return pagina_principal(1)

def selecionar_lista_tela(objeto_lista, pagina):
    """
    Tela para visualizar as tarefas de uma lista específica, com paginação e ordenação padrão.
    """
    clear_screen()
    
    todas_tarefas_da_lista = ViewHelpers.filter_tasks(
        ViewHelpers.get_all_tasks(),
        "por_lista",
        target_list_id=objeto_lista.list_ID
    )
    tarefas_ordenadas = ViewHelpers.sort_tasks(todas_tarefas_da_lista, "data")
    
    return exibir_tarefas_comuns(tarefas_ordenadas, 
                                 f"Tarefas da Lista: {objeto_lista.list_title}", 
                                 pagina, 
                                 len(tarefas_ordenadas), 
                                 origem_chamada_obj=objeto_lista,
                                 origem_chamada_page=pagina)


def pesquisar_tarefa_tela(termo_pesquisa=""):
    """
    Tela para pesquisar tarefas por título, nota ou tags.
    """
    clear_screen()
    if not termo_pesquisa:
        termo_pesquisa = input("Digite o termo para a pesquisa: ")
        if not termo_pesquisa:
            print("Termo de pesquisa vazio. Voltando ao menu principal.")
            input("\nPressione Enter para continuar...")
            return pagina_principal(1)

    todas_tarefas = ViewHelpers.get_all_tasks()
    tarefas_encontradas = [
        t for t in todas_tarefas if
        termo_pesquisa.lower() in t.title.lower() or
        termo_pesquisa.lower() in t.note.lower() or
        termo_pesquisa.lower() in t.tags.lower()
    ]
    
    tarefas_ordenadas = ViewHelpers.sort_tasks(tarefas_encontradas, "data")

    return exibir_tarefas_comuns(tarefas_ordenadas, 
                                 f"Resultados da Pesquisa por '{termo_pesquisa}'", 
                                 1,
                                 len(tarefas_ordenadas))

def visualizar_tarefas_tela(pagina=1):
    """
    Tela principal de visualização de tarefas, permitindo filtros e ordenações.
    """
    clear_screen()
    print("\n--- Visualizar Tarefas ---")
    print("Escolha o tipo de visualização:")
    print("  1. Todas as tarefas")
    print("  2. Tarefas com data até hoje (incluindo atrasadas)")
    print("  3. Tarefas com data até em 7 dias (incluindo atrasadas)")
    print("  4. Apenas tarefas não concluídas")
    print("  5. Ver por Lista")
    print("  6. Ver por Tag")
    print("  7. Ver tarefas concluídas")
    print("  8. Voltar ao menu principal")
    
    escolha_filtro = obter_entrada_numerica("Opção: ", 1, 8)
    
    titulo_visualizacao = ""
    filtro_tipo = "todas"
    lista_id_alvo = None
    tag_alvo = None
    todas_tarefas_brutas = ViewHelpers.get_all_tasks()
    tarefas_filtradas = []

    if escolha_filtro == 1:
        filtro_tipo = "todas"
        titulo_visualizacao = "Todas as Tarefas"
        tarefas_filtradas = todas_tarefas_brutas
    elif escolha_filtro == 2:
        filtro_tipo = "hoje"
        titulo_visualizacao = "Tarefas com Data até Hoje"
        tarefas_filtradas = ViewHelpers.filter_tasks(todas_tarefas_brutas, "hoje")
    elif escolha_filtro == 3:
        filtro_tipo = "7dias"
        titulo_visualizacao = "Tarefas com Data até 7 Dias"
        tarefas_filtradas = ViewHelpers.filter_tasks(todas_tarefas_brutas, "7dias")
    elif escolha_filtro == 4:
        filtro_tipo = "nao_concluidas"
        titulo_visualizacao = "Tarefas Não Concluídas"
        tarefas_filtradas = ViewHelpers.filter_tasks(todas_tarefas_brutas, "nao_concluidas")
    elif escolha_filtro == 5:
        clear_screen()
        print("\n--- Ver Tarefas por Lista ---")
        if not TList.list_IDs:
            print("Nenhuma lista encontrada.")
            input("\nPressione Enter para continuar...")
            return visualizar_tarefas_tela(1)

        list_objects = list(TList.list_IDs.values())
        for i, l_obj in enumerate(list_objects):
            print(f"  {i+1}. {l_obj.list_title}")
        
        num_lista = obter_entrada_numerica("Selecione o número da lista: ", 1, len(list_objects))
        lista_selecionada = list_objects[num_lista - 1]
        filtro_tipo = "por_lista"
        lista_id_alvo = lista_selecionada.list_ID
        titulo_visualizacao = f"Tarefas da Lista: {lista_selecionada.list_title}"
        tarefas_filtradas = ViewHelpers.filter_tasks(todas_tarefas_brutas, filtro_tipo, target_list_id=lista_id_alvo)
    elif escolha_filtro == 6:
        clear_screen()
        print("\n--- Ver Tarefas por Tag ---")
        tag_alvo = input("Digite a tag para filtrar: ")
        if not tag_alvo:
            print("Tag vazia. Voltando ao menu.")
            input("\nPressione Enter para continuar...")
            return visualizar_tarefas_tela(1)
        
        filtro_tipo = "por_tag"
        titulo_visualizacao = f"Tarefas com Tag: '{tag_alvo}'"
        tarefas_filtradas = ViewHelpers.filter_tasks(todas_tarefas_brutas, filtro_tipo, target_tag=tag_alvo)
    elif escolha_filtro == 7:
        return visualizar_tarefas_concluidas_tela()
    elif escolha_filtro == 8:
        return pagina_principal(1)

    print("\nEscolha a ordenação:")
    print("  1. Por Data (Padrão)")
    print("  2. Por Prioridade")
    
    escolha_ordenacao = obter_entrada_numerica("Opção: ", 1, 2)
    
    ordenacao_tipo = "data"
    if escolha_ordenacao == 1:
        ordenacao_tipo = "data"
    elif escolha_ordenacao == 2:
        ordenacao_tipo = "prioridade"
    
    tarefas_ordenadas = ViewHelpers.sort_tasks(tarefas_filtradas, ordenacao_tipo)

    return exibir_tarefas_comuns(tarefas_ordenadas, 
                                 titulo_visualizacao, 
                                 1,
                                 len(tarefas_ordenadas))


def visualizar_tarefas_concluidas_tela():
    """Tela para visualizar e gerenciar tarefas concluídas."""
    
    tarefas_concluidas = ViewHelpers.filter_tasks(ViewHelpers.get_all_tasks(), "concluidas")
    tarefas_ordenadas = ViewHelpers.sort_tasks(tarefas_concluidas, "data")

    total_paginas = (len(tarefas_ordenadas) + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
    if total_paginas == 0 and len(tarefas_ordenadas) > 0:
        total_paginas = 1
    pagina_atual = 1

    while True:
        clear_screen()
        n = ITENS_POR_PAGINA * (pagina_atual - 1)
        tarefas_da_pagina = tarefas_ordenadas[n : n + ITENS_POR_PAGINA]

        print(f"\n--- Tarefas Concluídas (Página {pagina_atual}/{total_paginas if total_paginas > 0 else 1}) ---")
        if not tarefas_da_pagina:
            print("Nenhuma tarefa concluída encontrada.")
        else:
            for i, tarefa_obj in enumerate(tarefas_da_pagina):
                list_title = TList.list_titles.get(tarefa_obj.list_ID, "Lista Desconhecida")
                data_info = tarefa_obj.date.strftime('%d/%m/%Y') if tarefa_obj.date else "N/A"
                print(f"{n + i + 1}. [Lista: {list_title}] Título: {tarefa_obj.title} | Data: {data_info}")

        print("\nOpções: desmarcar (desmarcar como concluída), remover (remover uma tarefa), limpar_todas (remover todas as concluídas), prox (próxima página), ant (página anterior), voltar")
        opcao = input("Escolha uma opção: ").lower()

        while opcao not in ["desmarcar", "remover", "limpar_todas", "prox", "ant", "voltar"]:
            print("Não entendi. Digite novamente por favor.")
            opcao = input("Escolha uma opção: ").lower()

        if opcao == "desmarcar":
            if not tarefas_da_pagina:
                print("Não há tarefas concluídas para desmarcar nesta página.")
                input("\nPressione Enter para continuar...")
                continue
            num_tarefa = obter_entrada_numerica("Escolha o número da tarefa para desmarcar: ", 1, len(tarefas_da_pagina))
            tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
            tarefa_selecionada.conclusion = False
            tm.update_archives()
            print(f"Tarefa '{tarefa_selecionada.title}' desmarcada como concluída.")
            input("\nPressione Enter para continuar...")
            tarefas_concluidas = ViewHelpers.filter_tasks(ViewHelpers.get_all_tasks(), "concluidas")
            tarefas_ordenadas = ViewHelpers.sort_tasks(tarefas_concluidas, "data")
            total_paginas = (len(tarefas_ordenadas) + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
            continue
        elif opcao == "remover":
            if not tarefas_da_pagina:
                print("Não há tarefas concluídas para remover nesta página.")
                input("\nPressione Enter para continuar...")
                continue
            num_tarefa = obter_entrada_numerica("Escolha o número da tarefa para remover: ", 1, len(tarefas_da_pagina))
            tarefa_selecionada = tarefas_da_pagina[num_tarefa - 1]
            
            confirmar = input(f"Tem certeza que deseja remover a tarefa '{tarefa_selecionada.title}'? (s/n): ").lower()
            if confirmar == 's':
                if tm.pop_task(tarefa_selecionada.ID):
                    print("Tarefa removida com sucesso!")
                else:
                    print("Não foi possível remover a tarefa.")
            else:
                print("Remoção cancelada.")
            input("\nPressione Enter para continuar...")
            tarefas_concluidas = ViewHelpers.filter_tasks(ViewHelpers.get_all_tasks(), "concluidas")
            tarefas_ordenadas = ViewHelpers.sort_tasks(tarefas_concluidas, "data")
            total_paginas = (len(tarefas_ordenadas) + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
            continue
        elif opcao == "limpar_todas":
            if not tarefas_concluidas:
                print("Não há tarefas concluídas para remover.")
                input("\nPressione Enter para continuar...")
                continue
            confirmar = input("Tem certeza que deseja remover TODAS as tarefas concluídas? (s/n): ").lower()
            if confirmar == 's':
                ids_para_remover = [item.ID for item in tarefas_concluidas]
                for tarefa_id in ids_para_remover:
                    tm.pop_task(tarefa_id, suppress_message=True)
                print("Todas as tarefas concluídas foram removidas.")
            else:
                print("Remoção de todas as tarefas concluídas cancelada.")
            input("\nPressione Enter para continuar...")
            return pagina_principal(1)
        elif opcao == "prox":
            if (n + ITENS_POR_PAGINA) < len(tarefas_ordenadas):
                pagina_atual += 1
            else:
                print("Não existem mais tarefas concluídas!")
                input("\nPressione Enter para continuar...")
            continue
        elif opcao == "ant":
            if pagina_atual > 1:
                pagina_atual -= 1
            else:
                print("Já está no início das tarefas concluídas!")
                input("\nPressione Enter para continuar...")
            continue
        elif opcao == "voltar":
            return pagina_principal(1)

def pagina_principal(pagina):
    """
    Tela principal do sistema, exibindo listas de tarefas e opções gerais.
    """
    clear_screen()
    n = ITENS_POR_PAGINA * (pagina - 1)
    
    all_list_objects = list(TList.list_IDs.values())

    ready_list_objects = all_list_objects[n : n + ITENS_POR_PAGINA]
    total_paginas = (len(all_list_objects) + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
    if total_paginas == 0 and len(all_list_objects) > 0:
        total_paginas = 1


    print(f"\n--- Suas Listas de Tarefas (Página {pagina}/{total_paginas if total_paginas > 0 else 1}) ---")
    if not ready_list_objects:
        print("Nenhuma lista de tarefas encontrada. Por favor, adicione uma.")
    else:
        for i, list_obj in enumerate(ready_list_objects):
            print(f"{n + i + 1}. {list_obj.list_title}")

    print("\nOpções:")
    print("  adicionar_lista (adicionar nova lista)")
    print("  editar_lista    (editar o título de uma lista)")
    print("  remover_lista   (remover uma lista e suas tarefas)")
    print("  visualizar      (ver tarefas com filtros e ordenações)")
    print("  pesquisar       (buscar tarefas por termo)")
    print("  selecionar      (selecionar uma lista para ver suas tarefas)")
    print("  prox            (próxima página de listas)")
    print("  ant             (página anterior de listas)")
    print("  sair            (sair do programa)")
    opcao = input("Escolha uma opção: ").lower()

    while opcao not in ["adicionar_lista", "editar_lista", "remover_lista", "visualizar", "pesquisar", "selecionar", "prox", "ant", "sair"]:
        print("Não entendi, pode repetir por favor.")
        opcao = input("Escolha uma opção: ").lower()

    if opcao == "adicionar_lista":
        return adicionar_lista_tela()
    elif opcao == "editar_lista":
        if not ready_list_objects:
            print("Não há listas para editar.")
            input("\nPressione Enter para continuar...")
            return pagina_principal(pagina)
        num_lista = obter_entrada_numerica("Qual lista você quer editar? (Digite o número): ", 1, len(ready_list_objects))
        lista_selecionada = ready_list_objects[num_lista - 1]
        return editar_lista_tela(lista_selecionada)
    elif opcao == "remover_lista":
        if not ready_list_objects:
            print("Não há listas para excluir.")
            input("\nPressione Enter para continuar...")
            return pagina_principal(pagina)
        num_lista = obter_entrada_numerica("Qual lista você quer excluir? (Digite o número): ", 1, len(ready_list_objects))
        lista_selecionada = ready_list_objects[num_lista - 1]
        lm.pop_list(lista_selecionada.list_ID)
        input("\nPressione Enter para continuar...")
        return pagina_principal(pagina)
    elif opcao == "visualizar":
        return visualizar_tarefas_tela(1)
    elif opcao == "pesquisar":
        return pesquisar_tarefa_tela()
    elif opcao == "selecionar":
        if not ready_list_objects:
            print("Não há listas para selecionar.")
            input("\nPressione Pressione Enter para continuar...")
            return pagina_principal(pagina)
        num_lista = obter_entrada_numerica("Qual lista você quer selecionar? (Digite o número): ", 1, len(ready_list_objects))
        lista_selecionada = ready_list_objects[num_lista - 1]
        return selecionar_lista_tela(lista_selecionada, 1)
    elif opcao == "prox":
        if (n + ITENS_POR_PAGINA) < len(all_list_objects):
            return pagina_principal(pagina + 1)
        else:
            print("Não existem mais listas!")
            input("\nPressione Enter para continuar...")
            return pagina_principal(pagina)
    elif opcao == "ant":
        if pagina > 1:
            return pagina_principal(pagina - 1)
        else:
            print("Já está no início das listas!")
            input("\nPressione Enter para continuar...")
            return pagina_principal(pagina)
    elif opcao == "sair":
        print("Saindo do programa. Até mais!")
        return "sair"
