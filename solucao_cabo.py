"""
Solução do Problema do Cabo Suspenso (Catenária)
Método do Tiro com Runge-Kutta de 4ª ordem e Método da Secante

Equação diferencial: d²y/dx² = C * sqrt(1 + (dy/dx)²)
Condições de contorno: y(0) = 15 m, y(20) = 10 m
Constante: C = 0.041 m⁻¹

Método: Tiro com RK4 e busca de raiz pelo método da secante
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
from pathlib import Path
import time


class CaboProblem:
    def __init__(self, C=0.041, x0=0, y0=15, xf=20, yf=10, h=0.01, tol=1e-5):
        """
        Inicializa o problema do cabo suspenso

        Parâmetros:
        -----------
        C : float, default=0.041
            Constante da equação diferencial (m⁻¹)
        x0, y0 : float, default=(0, 15)
            Condições iniciais
        xf, yf : float, default=(20, 10)
            Condições de contorno final
        h : float, default=0.01
            Passo de integração
        tol : float, default=1e-5
            Tolerância para convergência
        """
        # Validação dos parâmetros
        if C <= 0:
            raise ValueError("Constante C deve ser positiva")
        if h <= 0 or h >= (xf - x0):
            raise ValueError(
                "Passo h deve ser positivo e menor que o intervalo")
        if tol <= 0:
            raise ValueError("Tolerância deve ser positiva")
        if xf <= x0:
            raise ValueError("xf deve ser maior que x0")

        self.C = C
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf
        self.h = h
        self.tol = tol
        self.n_steps = int((self.xf - self.x0) / self.h)

        # Para estatísticas
        self.tempo_execucao = 0
        self.iteracoes_tiro = 0

    def sistema_edo(self, x, y):
        """
        Sistema de EDOs de primeira ordem
        y[0] = y, y[1] = dy/dx
        """
        _ = x  # x não é usado nesta EDO autônoma
        return np.array([y[1], self.C * np.sqrt(1 + y[1]**2)])

    def runge_kutta_4(self, y_inicial, dydx_inicial):
        """
        Integração usando Runge-Kutta de 4ª ordem

        Parâmetros:
        -----------
        y_inicial : float
            Valor inicial de y
        dydx_inicial : float
            Valor inicial de dy/dx

        Retorna:
        --------
        x_vals : ndarray
            Array de valores x
        y_vals : ndarray
            Array de valores y
        dydx_vals : ndarray
            Array de valores dy/dx
        """
        # Inicialização dos arrays (pré-alocação para eficiência)
        x_vals = np.linspace(self.x0, self.xf, self.n_steps + 1)
        y_vals = np.zeros(self.n_steps + 1)
        dydx_vals = np.zeros(self.n_steps + 1)

        # Condições iniciais
        y_vals[0] = y_inicial
        dydx_vals[0] = dydx_inicial

        # Estado inicial
        estado = np.array([y_inicial, dydx_inicial], dtype=np.float64)

        # Integração RK4
        for i in range(self.n_steps):
            x = x_vals[i]

            # Coeficientes RK4
            k1 = self.h * self.sistema_edo(x, estado)
            k2 = self.h * self.sistema_edo(x + self.h/2, estado + k1/2)
            k3 = self.h * self.sistema_edo(x + self.h/2, estado + k2/2)
            k4 = self.h * self.sistema_edo(x + self.h, estado + k3)

            # Atualização do estado
            estado = estado + (k1 + 2*k2 + 2*k3 + k4) / 6

            # Armazenamento dos valores
            y_vals[i+1] = estado[0]
            dydx_vals[i+1] = estado[1]

        return x_vals, y_vals, dydx_vals

    def funcao_erro(self, dydx_inicial):
        """
        Função de erro para o método do tiro
        Retorna a diferença entre y(xf) calculado e o valor alvo
        """
        _, y_vals, _ = self.runge_kutta_4(self.y0, dydx_inicial)
        return y_vals[-1] - self.yf

    def resolver_metodo_tiro(self):
        """
        Resolve o problema usando o método do tiro com método da secante

        Retorna:
        --------
        tuple
            (dydx_otimo, x_vals, y_vals, dydx_vals)
        """
        print("Iniciando método do tiro com método da secante...")
        inicio_tempo = time.time()

        # Implementação do método da secante conforme especificado no documento
        # Duas estimativas iniciais para a inclinação
        z0 = -1.0  # Primeira estimativa
        z1 = -0.5  # Segunda estimativa

        # Calcula F(z0) e F(z1)
        F_z0 = self.funcao_erro(z0)
        F_z1 = self.funcao_erro(z1)

        print(f"Estimativa inicial z0 = {z0:.6f}, F(z0) = {F_z0:.6f}")
        print(f"Estimativa inicial z1 = {z1:.6f}, F(z1) = {F_z1:.6f}")

        # Inicialização das variáveis do método da secante
        z_anterior = z0
        z_atual = z1
        F_anterior = F_z0
        F_atual = F_z1

        self.iteracoes_tiro = 0
        max_iteracoes = 100

        print("\nIterações do método da secante:")
        print("Iter\tz_n\t\tF(z_n)\t\tErro absoluto")
        print("-" * 55)

        # Laço do método da secante
        while abs(F_atual) > self.tol and self.iteracoes_tiro < max_iteracoes:
            # Fórmula do método da secante: z_{n+1} = z_n - F(z_n) * (z_n - z_{n-1}) / (F(z_n) - F(z_{n-1}))
            if abs(F_atual - F_anterior) < 1e-14:
                print("Aviso: Denominador muito pequeno no método da secante")
                break

            z_novo = z_atual - F_atual * \
                (z_atual - z_anterior) / (F_atual - F_anterior)
            F_novo = self.funcao_erro(z_novo)

            self.iteracoes_tiro += 1

            print(
                f"{self.iteracoes_tiro}\t{z_novo:.8f}\t{F_novo:.8f}\t{abs(F_novo):.2e}")

            # Atualização das variáveis para a próxima iteração
            z_anterior = z_atual
            z_atual = z_novo
            F_anterior = F_atual
            F_atual = F_novo

        dydx_otimo = z_atual

        # Verificação da convergência
        if self.iteracoes_tiro >= max_iteracoes:
            print(
                f"\nAviso: Número máximo de iterações ({max_iteracoes}) atingido")
            print(f"Erro final: {abs(F_atual):.2e}")
        else:
            print(
                f"\nConvergência atingida em {self.iteracoes_tiro} iterações")

        self.tempo_execucao = time.time() - inicio_tempo
        print(f"Inclinação inicial convergida: {dydx_otimo:.8f}")
        print(
            f"Tempo de execução do método do tiro: {self.tempo_execucao:.3f} segundos")

        # Solução final
        x_vals, y_vals, dydx_vals = self.runge_kutta_4(self.y0, dydx_otimo)

        # Verificação da precisão
        erro_final = abs(y_vals[-1] - self.yf)
        print(f"Erro final na condição de contorno: {erro_final:.2e}")

        if erro_final > self.tol * 10:
            warnings.warn(
                f"Erro final ({erro_final:.2e}) é maior que 10x a tolerância ({self.tol:.2e})")

        return dydx_otimo, x_vals, y_vals, dydx_vals

    def diferenciacao_numerica(self, x_vals, y_vals):
        """
        Calcula derivadas numéricas de ordem 2

        Retorna:
        dy_dx: primeira derivada numérica
        d2y_dx2: segunda derivada numérica
        """
        n = len(x_vals)
        dy_dx = np.zeros(n)
        d2y_dx2 = np.zeros(n)

        # Primeira derivada (diferenças centrais)
        for i in range(1, n-1):
            dy_dx[i] = (y_vals[i+1] - y_vals[i-1]) / (2 * self.h)

        # Pontos extremos (diferenças progressiva e regressiva)
        dy_dx[0] = (-3*y_vals[0] + 4*y_vals[1] - y_vals[2]) / (2 * self.h)
        dy_dx[-1] = (3*y_vals[-1] - 4*y_vals[-2] + y_vals[-3]) / (2 * self.h)

        # Segunda derivada (diferenças centrais)
        for i in range(1, n-1):
            d2y_dx2[i] = (y_vals[i+1] - 2*y_vals[i] +
                          y_vals[i-1]) / (self.h**2)

        # Pontos extremos para segunda derivada
        d2y_dx2[0] = (2*y_vals[0] - 5*y_vals[1] + 4 *
                      y_vals[2] - y_vals[3]) / (self.h**2)
        d2y_dx2[-1] = (2*y_vals[-1] - 5*y_vals[-2] + 4 *
                       y_vals[-3] - y_vals[-4]) / (self.h**2)

        return dy_dx, d2y_dx2

    def verificar_equacao_diferencial(self, x_vals, y_vals, dydx_vals):
        """
        Verifica se a solução satisfaz a equação diferencial
        usando diferenciação numérica
        """
        print("\n=== VERIFICAÇÃO POR DIFERENCIAÇÃO NUMÉRICA ===")

        # Calcula derivadas numéricas
        dy_dx_num, d2y_dx2_num = self.diferenciacao_numerica(x_vals, y_vals)

        # Calcula o lado direito da equação
        rhs = self.C * np.sqrt(1 + dy_dx_num**2)

        # Calcula resíduos
        residuos = np.abs(d2y_dx2_num - rhs)

        # Estatísticas
        residuo_max = np.max(residuos)
        residuo_medio = np.mean(residuos)
        residuo_rms = np.sqrt(np.mean(residuos**2))

        print(f"Resíduo máximo: {residuo_max:.2e}")
        print(f"Resíduo médio: {residuo_medio:.2e}")
        print(f"Resíduo RMS: {residuo_rms:.2e}")

        # Tabela de pontos específicos
        indices_amostra = [
            0, len(x_vals)//4, len(x_vals)//2, 3*len(x_vals)//4, -1]

        print("\nPontos de verificação:")
        print("x (m)\t\tLHS (d²y/dx²)\tRHS (C√(1+(dy/dx)²))\tResíduo")
        print("-" * 65)

        for i in indices_amostra:
            x = x_vals[i]
            lhs = d2y_dx2_num[i]
            rhs_val = rhs[i]
            res = residuos[i]
            print(f"{x:.2f}\t\t{lhs:.6f}\t\t{rhs_val:.6f}\t\t\t{res:.2e}")

        return residuos, dy_dx_num, d2y_dx2_num

    def calcular_propriedades_cabo(self, x_vals, y_vals, dydx_vals):
        """
        Calcula propriedades físicas adicionais do cabo

        Retorna:
        --------
        dict : Dicionário com propriedades calculadas
        """
        # Comprimento do arco do cabo
        ds = np.sqrt(1 + dydx_vals**2) * self.h
        comprimento_total = np.sum(ds[:-1])  # Remove o último ponto duplicado

        # Ponto mais baixo
        idx_min = np.argmin(y_vals)
        x_min = x_vals[idx_min]
        y_min = y_vals[idx_min]

        # Tensão ao longo do cabo (assumindo T_H = 1/C)
        T_H = 1.0 / self.C  # Componente horizontal da tensão
        tensao = T_H * np.sqrt(1 + dydx_vals**2)
        tensao_min = np.min(tensao)
        tensao_max = np.max(tensao)

        # Curvatura
        d2y_dx2 = np.gradient(np.gradient(y_vals, self.h), self.h)
        curvatura = np.abs(d2y_dx2) / (1 + dydx_vals**2)**(3/2)
        curvatura_max = np.max(curvatura)

        propriedades = {
            'comprimento_arco': comprimento_total,
            'ponto_mais_baixo': (x_min, y_min),
            'tensao_minima': tensao_min,
            'tensao_maxima': tensao_max,
            'curvatura_maxima': curvatura_max,
            'flecha': self.y0 - y_min,  # Deflexão máxima
            'parametro_a': 1.0 / self.C  # Parâmetro da catenária
        }

        return propriedades

    def regressao_polinomial(self, x_vals, y_vals):
        """
        Ajusta um polinômio de 4º grau aos dados e verifica a equação
        """
        print("\n=== VERIFICAÇÃO POR REGRESSÃO POLINOMIAL DE 4º GRAU ===")

        # Ajuste polinomial
        coeficientes = np.polyfit(x_vals, y_vals, 4)
        polinomio = np.poly1d(coeficientes)

        print("Coeficientes do polinômio P(x) = c₄x⁴ + c₃x³ + c₂x² + c₁x + c₀:")
        for i, coef in enumerate(coeficientes):
            print(f"c_{4-i} = {coef:.8e}")

        # Derivadas analíticas do polinômio
        dp_dx = np.polyder(polinomio, 1)  # primeira derivada
        d2p_dx2 = np.polyder(polinomio, 2)  # segunda derivada

        # Avalia as derivadas nos pontos x
        y_poli = polinomio(x_vals)
        dy_poli = dp_dx(x_vals)
        d2y_poli = d2p_dx2(x_vals)

        # Lado direito da equação usando o polinômio
        rhs_poli = self.C * np.sqrt(1 + dy_poli**2)

        # Resíduos
        residuos_poli = np.abs(d2y_poli - rhs_poli)

        # Estatísticas
        residuo_max_poli = np.max(residuos_poli)
        residuo_medio_poli = np.mean(residuos_poli)
        residuo_rms_poli = np.sqrt(np.mean(residuos_poli**2))

        print(f"\nResíduo máximo: {residuo_max_poli:.2e}")
        print(f"Resíduo médio: {residuo_medio_poli:.2e}")
        print(f"Resíduo RMS: {residuo_rms_poli:.2e}")

        # R² do ajuste
        ss_res = np.sum((y_vals - y_poli) ** 2)
        ss_tot = np.sum((y_vals - np.mean(y_vals)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        print(f"R² do ajuste polinomial: {r_squared:.8f}")

        # Tabela de pontos específicos
        indices_amostra = [
            0, len(x_vals)//4, len(x_vals)//2, 3*len(x_vals)//4, -1]

        print("\nPontos de verificação do polinômio:")
        print("x (m)\t\tLHS (P''(x))\tRHS (C√(1+(P'(x))²))\tResíduo")
        print("-" * 65)

        for i in indices_amostra:
            x = x_vals[i]
            lhs = d2y_poli[i]
            rhs_val = rhs_poli[i]
            res = residuos_poli[i]
            print(f"{x:.2f}\t\t{lhs:.6f}\t\t{rhs_val:.6f}\t\t\t{res:.2e}")

        return polinomio, residuos_poli, y_poli, dy_poli, d2y_poli

    def plotar_resultados(self, x_vals, y_vals, dydx_vals, residuos,
                          polinomio=None, y_poli=None, residuos_poli=None):
        """
        Plota os resultados da análise
        """
        # Configurações de estilo melhoradas
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 11,
            'axes.titlesize': 12,
            'axes.labelsize': 11,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 14
        })

        fig = plt.figure(figsize=(16, 10))

        # Criar um título principal para toda a figura
        fig.suptitle('Análise Completa do Cabo Suspenso (Catenária)',
                     fontsize=16, fontweight='bold', y=0.96)

        # Gráfico 1: Forma do cabo
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(x_vals, y_vals, 'b-', linewidth=2.5, label='Solução RK4')
        if polinomio is not None and y_poli is not None:
            ax1.plot(x_vals, y_poli, 'r--', linewidth=2,
                     label='Polinômio 4º grau')
        ax1.scatter([self.x0, self.xf], [self.y0, self.yf],
                    color='red', s=120, zorder=5, label='Condições de contorno',
                    edgecolor='darkred', linewidth=1)

        # Encontra e marca o ponto mais baixo
        idx_min = np.argmin(y_vals)
        ax1.scatter(x_vals[idx_min], y_vals[idx_min],
                    color='green', s=100, marker='v', zorder=5,
                    label='Ponto mais baixo', edgecolor='darkgreen', linewidth=1)

        ax1.set_xlabel('Posição x (m)', fontweight='bold')
        ax1.set_ylabel('Altura y (m)', fontweight='bold')
        ax1.set_title('Forma do Cabo Suspenso (Catenária)',
                      fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
        ax1.legend(loc='best', framealpha=0.9)
        ax1.invert_yaxis()  # Para mostrar o cabo "pendurado"

        # Melhorar o layout dos eixos
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Gráfico 2: Inclinação
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(x_vals, dydx_vals, 'g-', linewidth=2.5, label='dy/dx')
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.6, linewidth=1)
        ax2.set_xlabel('Posição x (m)', fontweight='bold')
        ax2.set_ylabel('Inclinação dy/dx', fontweight='bold')
        ax2.set_title('Inclinação do Cabo', fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)

        # Melhorar o layout dos eixos
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Gráfico 3: Resíduos da solução numérica
        ax3 = plt.subplot(2, 2, 3)
        ax3.semilogy(x_vals, residuos, 'b-', linewidth=2.5,
                     label='Diferenciação numérica')
        if residuos_poli is not None:
            ax3.semilogy(x_vals, residuos_poli, 'r--', linewidth=2,
                         label='Polinômio 4º grau')
        ax3.set_xlabel('Posição x (m)', fontweight='bold')
        ax3.set_ylabel('|Resíduo| (escala log)', fontweight='bold')
        ax3.set_title('Resíduos da Equação Diferencial',
                      fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)
        ax3.legend(loc='best', framealpha=0.9)

        # Melhorar o layout dos eixos
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)

        # Gráfico 4: Comparação y vs x (zoom na diferença)
        ax4 = plt.subplot(2, 2, 4)
        if polinomio is not None and y_poli is not None:
            diferenca = np.abs(y_vals - y_poli)
            ax4.semilogy(x_vals, diferenca, 'purple', linewidth=2.5)
            ax4.set_xlabel('Posição x (m)', fontweight='bold')
            ax4.set_ylabel('|y_RK4 - y_polinômio| (escala log)',
                           fontweight='bold')
            ax4.set_title('Diferença entre Solução RK4 e Polinômio',
                          fontweight='bold', pad=15)
        else:
            # Se não tiver polinômio, mostra a curvatura
            _, d2y_dx2_num = self.diferenciacao_numerica(x_vals, y_vals)
            ax4.plot(x_vals, d2y_dx2_num, 'orange', linewidth=2.5)
            ax4.set_xlabel('Posição x (m)', fontweight='bold')
            ax4.set_ylabel('d²y/dx² (m⁻¹)', fontweight='bold')
            ax4.set_title('Curvatura do Cabo', fontweight='bold', pad=15)

        ax4.grid(True, alpha=0.4, linestyle='-', linewidth=0.5)

        # Melhorar o layout dos eixos
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)

        # Ajustar espaçamento entre subplots
        plt.tight_layout(rect=[0, 0.02, 1, 0.94])

        # Salva com timestamp para evitar sobrescrever
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f'resultados_cabo_{timestamp}.png'
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"Gráficos salvos em: {nome_arquivo}")
        plt.show()

    def exportar_dados(self, x_vals, y_vals, dydx_vals, residuos, polinomio=None):
        """
        Exporta os dados para um arquivo CSV
        """
        # Preparação dos dados
        dados = {
            'x (m)': x_vals,
            'y (m)': y_vals,
            'dy/dx': dydx_vals,
            'residuo_numerico': residuos
        }

        if polinomio is not None:
            y_poli = polinomio(x_vals)
            dados['y_polinomio'] = y_poli
            dados['diferenca_abs'] = np.abs(y_vals - y_poli)

        # Criação do DataFrame
        df = pd.DataFrame(dados)

        # Exportação com timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f'dados_cabo_{timestamp}.csv'
        df.to_csv(nome_arquivo, index=False, float_format='%.8f')
        print(f"\nDados exportados para: {nome_arquivo}")

        # Calcula e mostra propriedades do cabo
        propriedades = self.calcular_propriedades_cabo(
            x_vals, y_vals, dydx_vals)

        print("\n" + "="*50)
        print("PROPRIEDADES FÍSICAS DO CABO")
        print("="*50)
        print(f"Comprimento do arco: {propriedades['comprimento_arco']:.6f} m")
        print(
            f"Ponto mais baixo: x = {propriedades['ponto_mais_baixo'][0]:.2f} m, y = {propriedades['ponto_mais_baixo'][1]:.6f} m")
        print(f"Flecha (deflexão máxima): {propriedades['flecha']:.6f} m")
        print(f"Tensão mínima: {propriedades['tensao_minima']:.3f} (T_H)")
        print(f"Tensão máxima: {propriedades['tensao_maxima']:.3f} (T_H)")
        print(f"Curvatura máxima: {propriedades['curvatura_maxima']:.6f} m⁻¹")
        print(
            f"Parâmetro da catenária (a = 1/C): {propriedades['parametro_a']:.3f} m")
        print("="*50)

        # Salva relatório completo
        nome_relatorio = f'relatorio_cabo_{timestamp}.txt'
        with open(nome_relatorio, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO COMPLETO - ANÁLISE DO CABO SUSPENSO\n")
            f.write("="*60 + "\n\n")
            f.write("PARÂMETROS DO PROBLEMA:\n")
            f.write(f"- Constante C: {self.C} m⁻¹\n")
            f.write(
                f"- Condições de contorno: y({self.x0}) = {self.y0} m, y({self.xf}) = {self.yf} m\n")
            f.write(f"- Passo de integração: {self.h}\n")
            f.write(f"- Tolerância: {self.tol}\n")
            f.write(
                f"- Tempo de execução: {self.tempo_execucao:.3f} segundos\n")
            f.write(
                f"- Número de iterações do método do tiro: {self.iteracoes_tiro}\n\n")

            f.write("PROPRIEDADES FÍSICAS:\n")
            for chave, valor in propriedades.items():
                if isinstance(valor, tuple):
                    f.write(
                        f"- {chave}: x = {valor[0]:.2f} m, y = {valor[1]:.6f} m\n")
                else:
                    f.write(f"- {chave}: {valor:.6f}\n")

        print(f"Relatório completo salvo em: {nome_relatorio}")

        return nome_arquivo, nome_relatorio

    def solucao_analitica_aproximada(self, x_vals, dydx_inicial):
        """
        Calcula uma aproximação da solução analítica para comparação

        A solução exata da catenária é: y = a*cosh((x-b)/a) + d
        onde a = 1/C, e b,d são determinados pelas condições de contorno

        Para fins de comparação, usamos a inclinação inicial encontrada
        numericamente para estimar os parâmetros.
        """
        a = 1.0 / self.C  # Parâmetro da catenária

        # Estimativa dos parâmetros b e d baseada na inclinação inicial
        # dy/dx(0) = sinh((0-b)/a) = sinh(-b/a) = dydx_inicial
        b = -a * np.arcsinh(dydx_inicial)

        # y(0) = a*cosh(-b/a) + d = y0
        d = self.y0 - a * np.cosh(-b/a)

        # Solução analítica
        y_analitica = a * np.cosh((x_vals - b) / a) + d

        return y_analitica, a, b, d


def main():
    """
    Função principal que resolve o problema completo
    """
    print("="*70)
    print("SOLUÇÃO AVANÇADA DO PROBLEMA DO CABO SUSPENSO (CATENÁRIA)")
    print("="*70)
    print("Parâmetros do problema:")
    print("- Equação: d²y/dx² = C√(1 + (dy/dx)²)")
    print("- Condições de contorno: y(0) = 15 m, y(20) = 10 m")
    print("- Constante: C = 0.041 m⁻¹")
    print("- Método: Tiro com RK4 e método da secante, h = 0.01, tolerância = 1e-5")
    print("="*70)

    try:
        # Criar instância do problema
        cabo = CaboProblem()

        # Resolver usando método do tiro
        dydx_otimo, x_vals, y_vals, dydx_vals = cabo.resolver_metodo_tiro()

        # Comparação com solução analítica aproximada
        y_analitica, a, b, d = cabo.solucao_analitica_aproximada(
            x_vals, dydx_otimo)
        erro_analitico = np.abs(y_vals - y_analitica)
        erro_max_analitico = np.max(erro_analitico)
        erro_rms_analitico = np.sqrt(np.mean(erro_analitico**2))

        print("\nComparação com solução analítica:")
        print(
            f"Parâmetros da catenária: a = {a:.3f} m, b = {b:.3f} m, d = {d:.3f} m")
        print(f"Erro máximo vs. analítica: {erro_max_analitico:.2e} m")
        print(f"Erro RMS vs. analítica: {erro_rms_analitico:.2e} m")

        # Verificação 1: Diferenciação numérica
        residuos, _, _ = cabo.verificar_equacao_diferencial(
            x_vals, y_vals, dydx_vals)

        # Verificação 2: Regressão polinomial
        polinomio, residuos_poli, y_poli, _, _ = cabo.regressao_polinomial(
            x_vals, y_vals)

        # Plotar resultados
        cabo.plotar_resultados(x_vals, y_vals, dydx_vals, residuos,
                               polinomio, y_poli, residuos_poli)

        # Exportar dados
        arquivo_csv, arquivo_relatorio = cabo.exportar_dados(
            x_vals, y_vals, dydx_vals, residuos, polinomio)

        print("\n" + "="*70)
        print(" ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("Arquivos gerados:")
        print(f"- {Path(arquivo_csv).name} (dados numéricos)")
        print("- resultados_cabo_*.png (gráficos)")
        print(f"- {arquivo_relatorio} (relatório completo)")
        print("="*70)

        # Resumo final
        propriedades = cabo.calcular_propriedades_cabo(
            x_vals, y_vals, dydx_vals)
        print("\n RESUMO EXECUTIVO:")
        print(f"Comprimento do cabo: {propriedades['comprimento_arco']:.2f} m")
        print(
            f"Ponto mais baixo em x = {propriedades['ponto_mais_baixo'][0]:.1f} m")
        print(f"Flecha: {propriedades['flecha']:.2f} m")
        print(f"Tempo de processamento: {cabo.tempo_execucao:.2f} s")
        print(f"Iterações do método do tiro: {cabo.iteracoes_tiro}")
        print(f"Inclinação inicial final: {dydx_otimo:.8f}")

    except Exception as e:
        print(f"\n ERRO na execução: {e}")
        print("Verifique os parâmetros de entrada e tente novamente.")
        raise


if __name__ == "__main__":
    # Configurações de warnings e numpy
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    np.seterr(over='warn', invalid='warn')

    main()
