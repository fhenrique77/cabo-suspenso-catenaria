# Trabalho

## Problema 1

**Enunciado:**

Um cabo flexível de densidade uniforme está suspenso entre dois pontos conforme mostra a figura. A forma do cabo, y(x), é descrita pela equação diferencial:

$\frac{d^2y}{dx^2} = C \sqrt{1 + \left(\frac{dy}{dx}\right)^2}$

onde C é uma constante igual à relação entre o peso por unidade de comprimento do cabo e a amplitude da componente horizontal da tensão no cabo em seu ponto mais baixo. O cabo está pendurado entre dois pontos especificados por y(0) = 15 m e y(20) = 10 m e C = 0,041 m⁻¹. Traçar a forma do cabo entre x = 0 e x = 20 m.

Resolva o seguinte problema com linguagem de programação:

### Observações:

**Obs.1:** Utilize o método de Runge-Kutta de quarta ordem com passo de 0,01 no método do Tiro, e uma tolerância de 0.00001 para o critério de parada.

**Obs.2:** Após a solução do problema e de posse do conjunto de pares ordenados x e y, faça a diferenciação numérica com erro de ordem 2 e verifique se as derivadas numéricas satisfazem a equação diferencial acima.

**Obs.3:** Também a partir do conjunto de pares ordenados x e y resultantes da solução do problema, faça uma regressão polinomial de quarto grau, e aplique a função na equação acima e verifique se a satisfaz.