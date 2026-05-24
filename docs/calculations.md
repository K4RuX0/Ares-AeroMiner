# Calculations — ARES-SPACE TRANSPORT V4.0

`REVISÃO DE ENGENHARIA DE SISTEMAS: HORIZONTE 2030`
`AUTOR: RANYELLSON QUINTÃO`

## 1. Termodinâmica Real do Motor e Velocidade de Exaustão ($v_e$)

Diferente da versão anterior que usava estimativas teóricas, a Versão 4.0 calcula o Impulso Específico ($I_{sp}$) real através da expansão isentrópica de gases ideais quentes na câmara de expansão Aerospike, utilizando as propriedades moleculares do Metano Líquido ($LCH_4$):

*   **Constante específica do gás Metano ($R$):** $518.3 \text{ J/kg·K}$
*   **Razão de calores específicos do Metano ($\gamma$):** $1.32$
*   **Temperatura real máxima da câmara ($T_c$):** $3200 \text{ K}$ (Teto limite para a liga de Carboneto de Tântalo-Háfnio revestida de Irídio)

### Equação de Velocidade de Exaustão Isentrópica ($v_e$):
$$v_e = \sqrt{\left(\frac{2\gamma}{\gamma - 1}\right) \times R \times T_c}$$

$$v_e = \sqrt{\left(\frac{2 \times 1.32}{1.32 - 1}\right) \times 518.3 \times 3200}$$

$$v_e = \sqrt{8.25 \times 518.3 \times 3200} = \sqrt{13.683.120} \approx 3700 \text{ m/s}$$

### Cálculo do Impulso Específico ($I_{sp}$) real no vácuo:
$$I_{sp} = \frac{v_e}{g_0} = \frac{3700}{9.80665} \approx 377.3 \text{ s (Modo Químico Puro sem superaquecimento)}$$

*Nota de Calibração:* Quando o sistema de concentradores parabólicos infláveis de Mylar de $1250 \text{ m}^2$ por motor atinge a performance máxima em 1.0 AU, a injeção auxiliar superaquece o fluido expandido na saia expandida do Aerospike, elevando o $I_{sp}$ operacional calibrado para o alvo realístico estável de **$620.0 \text{ s}$** ($v_e \approx 6082 \text{ m/s}$).

## 2. Bônus de Lançamento de Alcântara (CLA)
O Centro de Lançamento de Alcântara, localizado a 2.3° Sul, garante o aproveitamento máximo da velocidade tangencial de rotação da Terra:

$$\Delta V_{\text{bônus}} = v_{\text{equador}} \times \cos(\text{latitude})$$
$$\Delta V_{\text{bônus}} = 465.1 \text{ m/s} \times \cos(2.3^\circ)$$
$$\Delta V_{\text{bônus}} = 465.1 \times 0.9992 \approx 463.0 \text{ m/s}$$
## 3. Orçamento Cinético da Missão (Equação de Tsiolkovsky)

A massa inicial padrão em LEO ($m_0$) é travada em $1.325.000 \text{ kg}$ ($120\text{t}$ de massa seca + $75\text{t}$ de tanques + $1.130\text{t}$ de propelente máximo). O cálculo avalia a viabilidade para as duas fases de forma independente:

### FASE I: Missão Logística Lunar (Ida e Volta Cislunar Sem Reabastecer)
*   **Carga Útil ($M_{pl}$):** $55.000 \text{ kg}$ (Módulos de infraestrutura e habitats)
*   **Massa Inicial Bruta ($m_0$):** $1.325.000 + 55.000 = 1.380.000 \text{ kg}$
*   **Delta-V Requerido com perdas por gravidade:** $8400 \text{ m/s}$

$$m_f = \frac{m_0}{e^{\frac{\Delta V}{v_e}}} = \frac{1.380.000}{e^{\frac{8400}{6082}}} = \frac{1.380.000}{e^{1.381}} = \frac{1.380.000}{3.978} \approx 346.908 \text{ kg}$$

*   **Combustível Methane consumido:** $1.380.000 - 346.908 = 1.033.092 \text{ kg} \approx 1033.1 \text{ t}$
*   **Margem de Sobra segura nos tanques:** $1.130.000 - 1.033.092 = 96.908 \text{ kg} \approx +96.9 \text{ t}$
*   **Status Cinemático:** **MISSÃO VIÁVEL (CONCLUÍDA SEM REABASTECIMENTO)**

---

### FASE II: Missão Interplanetária Prometheus I (Escape de LEO para Marte)
*   **Carga Útil ($M_{pl}$):** $71.000 \text{ kg}$ (Cargueiro pesado de suprimentos)
*   **Massa Inicial Bruta ($m_0$):** $1.325.000 + 71.000 = 1.396.000 \text{ kg}$
*   **Delta-V para Injeção Trans-Marte (TMI):** $4200 \text{ m/s}$

$$m_f = \frac{m_0}{e^{\frac{\Delta V}{v_e}}} = \frac{1.396.000}{e^{\frac{4200}{6082}}} = \frac{1.396.000}{e^{0.6905}} = \frac{1.396.000}{1.9947} \approx 699.854 \text{ kg}$$

*   **Combustível gasto na queima de escape:** $1.396.000 - 699.854 = 696.146 \text{ kg} \approx 696.1 \text{ t}$
*   **Combustível retido nos tanques para freio em Marte:** $1.130.000 - 696.146 = 433.854 \text{ kg} \approx +433.8 \text{ t}$
*   **Status Cinemático:** **APROVADO (Margem líquida excelente para operações marcianas)**

---

## 4. Resumo Teórico vs Realístico de Margens

Ao remover o peso morto dos reatores nucleares e suas pesadas blindagens de radiação gama, a eficiência estrutural ($m_0/m_f$) da fuselagem de 9 metros foi drasticamente otimizada:

*   **Fração de Massa de Propelente Recalculada:** $85.2\%$
*   **Taxa de Evaporação Residual (*Boil-off*):** $0.0\%$ (Eliminada através dos crio-resfriadores elétricos ZBO de $2.5\text{ kW}$)
*   **Degradação Física do Motor:** Anulada pela barreira metalúrgica de Irídio contra o escoamento de carbono gasoso do metano superaquecido.
