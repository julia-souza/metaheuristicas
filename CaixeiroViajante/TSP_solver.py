import random
import time
from math import sqrt
import tkinter
import tkinter.filedialog
from PIL import Image, ImageDraw, ImageTk
import matplotlib.pyplot as plt

class TSPSolver:
    escala          : float
    size_x          : int
    size_y          : int
    x_max           : float
    y_max           : float
    x_min           : float
    y_min           : float
    imageContainer  : int
    tkimg           : ImageTk.PhotoImage
    img             : Image
    img_draw        : ImageDraw
    canvas          : tkinter.Canvas

    def __init__(self):
        self.escala = None
        self.size_y = None
        self.size_x = None
        self.y_max = None
        self.x_max = None
        self.y_min = None
        self.x_min = None
        self.imageContainer = None
        self.tkimg = None
        self.img = None
        self.img_draw = None
        self.canvas = None
        self.button_busca_local = None
        self.button_gerar_solucao = None
        self.button_ils = None
        self.entry_escala = None
        self.label_escala = None
        self.button_abrir = None
        self.entry_instancia = None
        self.label_instancia = None
        self.frame = None
        self.root = None
        self.matriz_adj = None
        self.coords = None
        self.dimension = None
        self.comment = None
        self.name = None
        self.cria_interface_grafica()

    def selecionar_instancia(self):
        filename = tkinter.filedialog.askopenfilename(title="Selecionar Instância...")
        self.entry_instancia.delete(0, 'end')
        self.entry_instancia.insert(0, filename)

    def abrir_instancia(self):
        instance_file = self.entry_instancia.get()
        with open(instance_file) as f:
            self.name = f.readline().split()[2]  # NAME : name
            self.comment = f.readline()[10:]  # COMMENT : comment
            f.readline()  # TYPE : TSP
            self.dimension = int(f.readline().split()[2])  # DIMENSION : d
            edge_weight_type = f.readline().split()[2]  # EDGE_WEIGHT_TYPE : ewt
            if edge_weight_type == "ATT" or edge_weight_type == "EUC_2D":
                f.readline()  # NODE_COORD_SECTION
                self.coords = []
                for i in range(self.dimension):
                    l = f.readline().split()
                    c = dict()
                    c['x'] = float(l[1])
                    c['y'] = float(l[2])
                    self.coords.append(c)
        self.calcular_matriz_distancias_euclideanas()
        self.mostrar_imagem_base()

    def calcular_matriz_distancias_euclideanas(self):
        self.matriz_adj = []
        for i in range(len(self.coords)):
            l = [0] * len(self.coords)
            self.matriz_adj.append(l)
        for i in range(len(self.coords)):
            for j in range(i + 1, len(self.coords)):
                xi = self.coords[i]['x']
                yi = self.coords[i]['y']
                xj = self.coords[j]['x']
                yj = self.coords[j]['y']
                dist_ij = sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
                self.matriz_adj[i][j] = dist_ij
                self.matriz_adj[j][i] = dist_ij

    def cria_interface_grafica(self):
        self.root = tkinter.Tk()
        self.root.title("TSP Solver")
        self.frame = tkinter.Frame(self.root, padx=10, pady=10)
        self.frame.pack()
        self.label_instancia = tkinter.Label(self.frame, text="Instância: ", )
        self.entry_instancia = tkinter.Entry(self.frame, width=90)
        self.button_selecionar = tkinter.Button(self.frame, text="selecionar", command=self.selecionar_instancia)
        self.button_abrir = tkinter.Button(self.frame, text="abrir", command=self.abrir_instancia)
        self.label_escala = tkinter.Label(self.frame, text="Fator de escala:")
        self.entry_escala = tkinter.Entry(self.frame)
        self.button_gerar_solucao = tkinter.Button(self.frame, text="gerar solução", command=self.construir_solucao_e_mostrar)
        self.button_busca_local = tkinter.Button(self.frame, text="busca local", command=self.soluciona_com_busca_local)
        self.button_ils = tkinter.Button(self.frame, text="ILS", command=self.soluciona_com_ils)
        self.button_multistart = tkinter.Button(self.frame, text="Multistart", command=self.soluciona_com_multistart)
        self.button_grasp = tkinter.Button(self.frame, text="GRASP", command=self.soluciona_com_grasp)
        self.canvas = tkinter.Canvas(self.frame, width=800, height=700)
        self.img = Image.new("RGB", size=(800, 700), color=(255, 255, 255))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.imageContainer = self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.tkimg)
        self.canvas.itemconfig(self.imageContainer, image=self.tkimg)

        self.label_instancia.grid(      row=0, column=0,                            sticky=tkinter.W)
        self.entry_instancia.grid(      row=0, column=1, columnspan=5,              sticky=tkinter.W)
        self.button_selecionar.grid(    row=0, column=6,                            sticky=tkinter.W)
        self.button_abrir.grid(         row=0, column=7,                            sticky=tkinter.W)
        self.label_escala.grid(         row=1, column=0,                            sticky=tkinter.W)
        self.entry_escala.grid(         row=1, column=1,                            sticky=tkinter.W)
        self.button_gerar_solucao.grid( row=2, column=0,                            sticky=tkinter.W)
        self.button_busca_local.grid(   row=2, column=1,                            sticky=tkinter.W)
        self.button_ils.grid(           row=2, column=2,                            sticky=tkinter.W)
        self.button_multistart.grid(    row=2, column=3,                            sticky=tkinter.W)
        self.button_grasp.grid(         row=2, column=4,                            sticky=tkinter.W)
        self.canvas.grid(               row=3, column=0, columnspan=8, rowspan=5)

        self.root.mainloop()

    def compute_max_and_min_coords(self):
        self.x_max = -100000000
        self.x_min = 100000000
        self.y_max = -100000000
        self.y_min = 100000000
        for i in range(len(self.coords)):
            x = self.coords[i]['x']
            y = self.coords[i]['y']
            if x < self.x_min:
                self.x_min = x
            if y < self.y_min:
                self.y_min = y
            if x > self.x_max:
                self.x_max = x
            if y > self.y_max:
                self.y_max = y

    def aplicar_escala(self):
        self.x_min *= self.escala
        self.y_min *= self.escala
        self.x_max *= self.escala
        self.y_max *= self.escala
        self.size_x = int(self.x_max - self.x_min) + 20
        self.size_y = int(self.y_max - self.y_min) + 20

    def calcular_escala(self):
        if (len(self.entry_escala.get()) > 0):
            self.escala = float(self.entry_escala.get())
        else:
            suggested_width = 1000
            suggested_height = 700
            if (self.x_max - self.x_min) / (self.y_max - self.y_min) >= suggested_width / suggested_height:
                self.escala = suggested_width / (self.x_max - self.x_min)
            else:
                self.escala = suggested_height / (self.y_max - self.y_min)
            self.entry_escala.delete(0, 'end')
            self.entry_escala.insert(0, '{:.3f}'.format(self.escala))

    def gerar_imagem_base(self):
        self.compute_max_and_min_coords()
        self.calcular_escala()
        self.aplicar_escala()
        self.img = Image.new("RGB", size=(self.size_x, self.size_y), color=(255, 255, 255))
        self.img_draw = ImageDraw.Draw(self.img)
        self.img_draw.rectangle(xy=(0, 0, self.size_x, self.size_y), fill="#ffffff")
        for i in range(len(self.coords)):
            x = self.coords[i]['x'] * self.escala - self.x_min + 10
            y = self.size_y - (self.coords[i]['y'] * self.escala - self.y_min + 10)
            self.img_draw.ellipse(xy=(x - 3, y - 3, x + 3, y + 3), fill="#000000", width=5)

    def mostrar_imagem(self):
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.canvas['width'] = self.size_x
        self.canvas['height'] = self.size_y
        self.canvas.itemconfig(self.imageContainer, image=self.tkimg)

    def mostrar_imagem_base(self):
        self.gerar_imagem_base()
        self.mostrar_imagem()

    def mostrar_solucao(self, solucao):
        self.gerar_imagem_base()
        for i in range(self.dimension):
            p1 = solucao[i]
            p2 = solucao[(i + 1) % self.dimension]
            p1_coord = self.coords[p1]
            p2_coord = self.coords[p2]
            p1_x = p1_coord['x'] * self.escala - self.x_min + 10
            p1_y = self.size_y - (p1_coord['y'] * self.escala - self.y_min + 10)
            p2_x = p2_coord['x'] * self.escala - self.x_min + 10
            p2_y = self.size_y - (p2_coord['y'] * self.escala - self.y_min + 10)
            self.img_draw.line(xy=[(p1_x, p1_y), (p2_x, p2_y)], fill='#0000ff', width=2, joint='curve')
        self.mostrar_imagem()

    def construir_solucao(self):
        solucao = [-1] * self.dimension
        visitadas = [False] * self.dimension
        atual = random.randrange(0, self.dimension)
        solucao[0] = atual
        visitadas[atual] = True
        for i in range(self.dimension - 1):
            prox = -1
            menor_custo = 1000000000
            for j in range(self.dimension):
                if j == atual or visitadas[j]:
                    continue
                if self.matriz_adj[atual][j] < menor_custo:
                    prox = j
                    menor_custo = self.matriz_adj[atual][j]
            solucao[i + 1] = prox
            visitadas[prox] = True
            atual = prox
        return solucao

    def construir_solucao_e_mostrar(self):
        solucao = self.construir_solucao()
        self.mostrar_solucao(solucao)
        return solucao

    def custo_solucao(self, solucao):
        ultima_cidade = solucao[self.dimension - 1]
        primeira_cidade = solucao[0]
        custo = self.matriz_adj[ultima_cidade][primeira_cidade]
        for i in range(self.dimension - 1):
            cidade_atual = solucao[i]
            proxima_cidade = solucao[i + 1]
            custo += self.matriz_adj[cidade_atual][proxima_cidade]
        return custo

    def copia_solucao(self, origem, destino):
        for i in range(self.dimension):
            destino[i] = origem[i]

    def troca_2_cidades(self, solucao_atual, solucao_vizinha, p1, p2):
        self.copia_solucao(solucao_atual, solucao_vizinha)
        solucao_vizinha[p1] = solucao_atual[p2]
        solucao_vizinha[p2] = solucao_atual[p1]

    def busca_em_vizinhanca_troca_2_cidades(self, solucao_atual, melhor_vizinho):
        '''Busca em vizinhança com operador Troca-2-Cidades.'''
        valor_melhor_vizinho = self.custo_solucao(solucao_atual)
        vizinho = [0] * self.dimension
        encontrou_melhoria = False
        for p1 in range(self.dimension - 1):  # p1 = [0, 1, 2, 3] para n = 5
            for p2 in range(p1 + 1, self.dimension):  # se p1 = 0, p2 = [1, 2, 3, 4] para n = 5
                self.troca_2_cidades(solucao_atual, vizinho, p1, p2)
                custo_vizinho = self.custo_solucao(vizinho)
                #print("          Custo = {:.3f}, Solução: ".format(custo_vizinho), end='')
                #self.imprimir_solucao(vizinho)
                if custo_vizinho < valor_melhor_vizinho:
                    valor_melhor_vizinho = custo_vizinho
                    self.copia_solucao(vizinho, melhor_vizinho)
                    encontrou_melhoria = True
        return encontrou_melhoria

    def troca_2_arestas(self, solucao_atual, solucao_vizinha, p1, p2):
        self.copia_solucao(solucao_atual, solucao_vizinha)
        ind1 = p1
        ind2 = p2
        while ind1 != p2:
            solucao_vizinha[ind1] = solucao_atual[ind2]
            ind1 = (ind1 + 1) % self.dimension
            ind2 = (ind2 - 1) if ind2 > 0 else (self.dimension - 1)
        solucao_vizinha[p2] = solucao_atual[p1]

    def busca_em_vizinhanca_troca_2_arestas(self, solucao_atual, melhor_vizinho):
        '''Busca em vizinhança com operador Troca-2-Arestas.'''
        valor_melhor_vizinho = self.custo_solucao(solucao_atual)
        vizinho = [0] * self.dimension
        encontrou_melhoria = False
        for p1 in range(self.dimension):  # p1 = [0, 1, 2, 3, 4] para n = 5
            for i2 in range(1, self.dimension):  # se p1 = 0, p2 \in [1, 2, 3, 4] para n = 5; se p1 = 1, p2 \in [2, 3, 4, 0]
                p2 = (p1 + i2) % self.dimension
                self.troca_2_arestas(solucao_atual, vizinho, p1, p2)
                custo_vizinho = self.custo_solucao(vizinho)
                #print("          Custo = {:.3f}, Solução: ".format(custo_vizinho), end='')
                #self.imprimir_solucao(vizinho)
                if custo_vizinho < valor_melhor_vizinho:
                    valor_melhor_vizinho = custo_vizinho
                    self.copia_solucao(vizinho, melhor_vizinho)
                    encontrou_melhoria = True
        return encontrou_melhoria

    def imprimir_solucao(self, solucao):
        for i in range(self.dimension):
            print("{:3d} ".format(solucao[i]), end='')
        print()

    def busca_local(self, solucao_atual):
        self.passo_busca.append(len(self.passo_busca))
        self.valor_atual.append(self.custo_solucao(solucao_atual))

        # print("---> Busca local iniciada ---")
        melhor_vizinho = [0] * self.dimension
        solucao_otima_local = [0] * self.dimension
        self.copia_solucao(solucao_atual, solucao_otima_local)
        encontrou_melhoria = True
        while encontrou_melhoria:
            #encontrou_melhoria = self.busca_em_vizinhanca_troca_2_cidades(solucao_otima_local, melhor_vizinho)
            encontrou_melhoria = self.busca_em_vizinhanca_troca_2_arestas(solucao_otima_local, melhor_vizinho)
            if encontrou_melhoria:
                self.copia_solucao(melhor_vizinho, solucao_otima_local)
                custo_melhor_vizinho = self.custo_solucao(melhor_vizinho)
                # print("Melhoria: Custo = {:.3f}, Solução: ".format(custo_melhor_vizinho), end='')
                # self.imprimir_solucao(melhor_vizinho)

                self.passo_busca.append(len(self.passo_busca))
                self.valor_atual.append(custo_melhor_vizinho)
                
                self.mostrar_solucao(melhor_vizinho)
                self.canvas.update_idletasks()          # atualiza o canvas
                time.sleep(0.03)                         # pausa para o usuário observar a mudança
        # print("---> Busca local finalizada ---\n")

        return solucao_otima_local

    def soluciona_com_busca_local(self):
        solucao_inicial = self.construir_solucao_e_mostrar()
        solucao_final = self.busca_local(solucao_inicial)
        self.mostrar_solucao(solucao_final)

    def ordena_lista(self, atual, lista):
        for i in range(len(lista)):
            ind_menor = i
            valor_menor = self.matriz_adj[atual][lista[i]]
            for j in range(i + 1, len(lista)):
                if (self.matriz_adj[atual][lista[j]] < valor_menor):
                    ind_menor = j
                    valor_menor = self.matriz_adj[atual][lista[j]]
            if ind_menor != i:
                aux = lista[i]
                lista[i] = lista[ind_menor]
                lista[ind_menor] = aux

    def constroi_solucao_gulosa_aleatoria(self, solucao, alfa: float):
        '''Constroi solução gulosa com percentual de 
           aleatoriedade alfa. Cada passo do método construtivo
           guloso (vizinho mais próximo) deve criar uma
           lista das cidades ainda não visitadas, ordenadas
           pela distância para a cidade atual. Desta lista,
           devem ser consideradas as cidades entre as alfa*100 %
           primeiras e escolhida uma delas aleatoriamente.'''
        visitadas = [False] * self.dimension
        atual = random.randrange(0, self.dimension)
        solucao[0] = atual
        visitadas[atual] = True
        for i in range(self.dimension - 1):
            prox = -1
            vizinhas = []
            for j in range(self.dimension):
                if j == atual or visitadas[j]:
                    continue
                vizinhas.append(j)
            self.ordena_lista(atual, vizinhas)
            max = int(len(vizinhas) * alfa)
            if max == 0:
                max = 1
            ind_prox = random.randrange(0, max)
            prox = vizinhas[ind_prox]

            solucao[i + 1] = prox
            visitadas[prox] = True
            atual = prox

    def constroi_solucao_aleatoria(self, solucao):
        '''Preencher a lista solucao com valores de range(0, self.dimension),
           em ordem aleatória.'''
        for i in range(self.dimension):
            solucao[i] = i
        random.shuffle(solucao)

    def soluciona_com_multistart(self):
        '''Executa buscas locais a partir de soluções iniciais diferentes.'''
        self.passo_busca = []
        self.valor_atual = []

        solucao_inicial = [0] * self.dimension
        melhor_solucao_conhecida = [0] * self.dimension

        custo_melhor_solucao_conhecida = 1e300
        num_iteracoes = 100
        for i in range(num_iteracoes):
            # 1. gerar solução inicial aleatória
            self.constroi_solucao_aleatoria(solucao_inicial)
            # 2. realizar uma busca local
            solucao_otima_local = self.busca_local(solucao_inicial)
            custo_otima_local = self.custo_solucao(solucao_otima_local)
            if custo_otima_local < custo_melhor_solucao_conhecida:
                self.copia_solucao(solucao_otima_local, melhor_solucao_conhecida)
                custo_melhor_solucao_conhecida = custo_otima_local
                print("\nMelhor..: Custo = {:.3f}, Solução: ".format(custo_melhor_solucao_conhecida), end='')
                self.imprimir_solucao(melhor_solucao_conhecida)

        self.mostrar_solucao(melhor_solucao_conhecida)
        print("\nFinal...: Custo = {:.3f}, Solução: ".format(self.custo_solucao(melhor_solucao_conhecida)), end='')
        self.imprimir_solucao(melhor_solucao_conhecida)

        plt.plot(self.passo_busca, self.valor_atual)
        plt.xlabel("passo busca")
        plt.ylabel("custo")
        plt.show()

        return melhor_solucao_conhecida

    def soluciona_com_grasp(self):
        '''Executa buscas locais a partir de soluções iniciais criadas com método guloso randomizado.'''
        self.passo_busca = []
        self.valor_atual = []

        solucao_inicial = [0] * self.dimension
        melhor_solucao_conhecida = [0] * self.dimension

        custo_melhor_solucao_conhecida = 1e300
        num_iteracoes = 100
        for i in range(num_iteracoes):
            # 1. gerar solução inicial aleatória
            self.constroi_solucao_gulosa_aleatoria(solucao_inicial, 0.2)
            # 2. realizar uma busca local
            solucao_otima_local = self.busca_local(solucao_inicial)
            custo_otima_local = self.custo_solucao(solucao_otima_local)
            if custo_otima_local < custo_melhor_solucao_conhecida:
                self.copia_solucao(solucao_otima_local, melhor_solucao_conhecida)
                custo_melhor_solucao_conhecida = custo_otima_local
                print("\nMelhor..: Custo = {:.3f}, Solução: ".format(custo_melhor_solucao_conhecida), end='')
                self.imprimir_solucao(melhor_solucao_conhecida)

        self.mostrar_solucao(melhor_solucao_conhecida)
        print("\nFinal...: Custo = {:.3f}, Solução: ".format(self.custo_solucao(melhor_solucao_conhecida)), end='')
        self.imprimir_solucao(melhor_solucao_conhecida)

        plt.plot(self.passo_busca, self.valor_atual)
        plt.xlabel("passo busca")
        plt.ylabel("custo")
        plt.show()

        return melhor_solucao_conhecida

    def perturba_solucao_2_trocas_2_cidades(self, solucao_original, solucao_perturbada):
        self.copia_solucao(solucao_original, solucao_perturbada)
        p1 = random.randrange(0, self.dimension)
        dist = random.randrange(1, self.dimension)
        p2 = (p1 + dist) % self.dimension
        solucao_perturbada[p1] = solucao_original[p2]
        solucao_perturbada[p2] = solucao_original[p1]
        p1 = random.randrange(0, self.dimension)
        dist = random.randrange(1, self.dimension)
        p2 = (p1 + dist) % self.dimension
        aux = solucao_perturbada[p1]
        solucao_perturbada[p1] = solucao_perturbada[p2]
        solucao_perturbada[p2] = aux

    def perturba_solucao_2_trocas_2_arestas(self, solucao_original, solucao_perturbada):
        solucao_intermediaria = [0] * self.dimension
        p1 = random.randrange(0, self.dimension)
        dist = random.randrange(1, self.dimension)
        p2 = (p1 + dist) % self.dimension

# (Exemplo)
# solucao: [3, 5, 2, 7, 8, 4, 6, 1]
# indices:  0  1  2  3  4  5  6  7
#                          ^
#                          p1: 5 (escolhido aleatoriamente)
# dist: 4 (escolhido aleatoriamente)
# p2: (5 + 4) % 8 = 1

        self.troca_2_arestas(solucao_original, solucao_intermediaria, p1, p2)
        p1 = random.randrange(0, self.dimension)
        dist = random.randrange(1, self.dimension)
        p2 = (p1 + dist) % self.dimension
        self.troca_2_arestas(solucao_intermediaria, solucao_perturbada, p1, p2)

    def soluciona_com_ils(self):
        '''Iterated Local Search'''
        self.passo_busca = []
        self.valor_atual = []

        # 1. gerar solução inicial
        solucao_inicial = self.construir_solucao()
        # 2. realizar uma busca local
        solucao_otima_local = self.busca_local(solucao_inicial)
        melhor_solucao_conhecida = [0] * self.dimension
        self.copia_solucao(solucao_otima_local, melhor_solucao_conhecida)
        iteracoes_sem_melhoria = 0
        # 3. se critério de parada não satisfeito
        while iteracoes_sem_melhoria <= 100:
        # 4.    perturbar melhor solução conhecida
            #self.perturba_solucao_2_trocas_2_cidades(melhor_solucao_conhecida, solucao_inicial)
            self.perturba_solucao_2_trocas_2_arestas(melhor_solucao_conhecida, solucao_inicial)
        # 5.    voltar ao passo 2
            solucao_otima_local = self.busca_local(solucao_inicial)
            custo_otima_local = self.custo_solucao(solucao_otima_local)
            custo_melhor_conhecida = self.custo_solucao(melhor_solucao_conhecida)
            if custo_otima_local < custo_melhor_conhecida:
                self.copia_solucao(solucao_otima_local, melhor_solucao_conhecida)
                print("\nMelhor..: Custo = {:.3f}, Solução: ".format(custo_melhor_conhecida), end='')
                self.imprimir_solucao(melhor_solucao_conhecida)
                iteracoes_sem_melhoria = 0
            else:
                iteracoes_sem_melhoria += 1
        self.mostrar_solucao(melhor_solucao_conhecida)
        print("\nFinal...: Custo = {:.3f}, Solução: ".format(self.custo_solucao(melhor_solucao_conhecida)), end='')
        self.imprimir_solucao(melhor_solucao_conhecida)

        plt.plot(self.passo_busca, self.valor_atual)
        plt.xlabel("passo busca")
        plt.ylabel("custo")
        plt.show()

        return melhor_solucao_conhecida

tsp_solver = TSPSolver()
