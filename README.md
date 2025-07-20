# Análise do Cabo Suspenso (Catenária)

## Descrição

Este projeto implementa a solução numérica do problema do cabo suspenso (catenária) usando métodos computacionais avançados. O problema é descrito pela equação diferencial:

```
d²y/dx² = C * √(1 + (dy/dx)²)
```

onde C = 0.041 m⁻¹ e as condições de contorno são y(0) = 15 m e y(20) = 10 m.

## Métodos Implementados

### Obs.1: Método do Tiro com Runge-Kutta 4ª Ordem
- **Integração**: Runge-Kutta de 4ª ordem com passo h = 0.01
- **Busca de raiz**: Método da Secante com tolerância 1e-5
- **Convergência**: Típicamente 3-4 iterações

### Obs.2: Verificação por Diferenciação Numérica
- **Método**: Diferenças finitas centrais de 2ª ordem
- **Verificação**: Calcula resíduos |y'' - C√(1+(y')²)|
- **Precisão**: Resíduos da ordem de 10⁻⁵

### Obs.3: Verificação por Regressão Polinomial
- **Ajuste**: Polinômio de 4º grau aos dados da solução
- **Verificação**: Aplica P(x) na EDO original
- **Resultado**: R² > 0.999 mas resíduos maiores (~10⁻⁴)

## Estrutura do Projeto

```
cabo-suspenso/
├── src/
│   └── solucao_cabo.py          # Código principal
├── docs/
│   ├── relatorio_cabo_final.txt # Relatório completo
│   ├── trabalho_markdown.md     # Enunciado do problema
│   └── trabalho.md              # Documentação detalhada
├── results/                     # Arquivos gerados (CSV, PNG)
└── README.md                    # Este arquivo
```

## Requisitos

- Python 3.7+
- NumPy
- Matplotlib
- Pandas

## Instalação

```bash
git clone https://github.com/[seu-usuario]/cabo-suspenso.git
cd cabo-suspenso
pip install numpy matplotlib pandas
```

## Uso

```bash
cd src
python solucao_cabo.py
```

## Resultados

- **Comprimento do cabo**: 21.17 m
- **Ponto mais baixo**: x = 15.87 m, y = 9.65 m
- **Flecha (deflexão)**: 5.35 m
- **Tempo de execução**: ~0.27 s
- **Iterações**: 3

## Arquivos Gerados

- `dados_cabo_YYYYMMDD_HHMMSS.csv`: Dados numéricos da solução
- `resultados_cabo_YYYYMMDD_HHMMSS.png`: Gráficos da análise
- `relatorio_cabo_YYYYMMDD_HHMMSS.txt`: Relatório detalhado

## Validação

O código foi validado através de:
1. Comparação com solução analítica (erro < 10⁻³)
2. Verificação dos resíduos da EDO (< 10⁻⁵)
3. Análise de convergência do método numérico

## Autores

- [Seus nomes aqui]

## Licença

MIT License - veja LICENSE para detalhes.

## Referências

- Problema baseado em exercício de Métodos Numéricos
- Teoria da catenária e equações diferenciais
