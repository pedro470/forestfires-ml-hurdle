# -*- coding: utf-8 -*-
"""
Gera o PDF (handout) do trabalho Forest Fires — Regressão Linear e Ridge, versão 2.
Mesmo layout do gerar_pdf.py original; conteúdo, números e figuras vêm do
analise_forestfires_v2_executado.ipynb.

Uso:  python gerar_pdf_v2.py [pasta_das_figuras]
As figuras (fig_*.png) são extraídas do notebook executado por extrair_figuras.py.
"""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, PageBreak, Image, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

FIGDIR = sys.argv[1] if len(sys.argv) > 1 else '.'

C_PRIMARY   = colors.HexColor('#1A3C5E')
C_ACCENT    = colors.HexColor('#E84637')
C_LIGHT     = colors.HexColor('#EAF2FB')
C_GRAY      = colors.HexColor('#5A6472')
C_LIGHTGRAY = colors.HexColor('#F4F6F8')
C_WHITE     = colors.white
C_BLACK     = colors.HexColor('#1C1C1C')
C_GREEN_BG  = colors.HexColor('#D4EDDA')
C_GREEN_BD  = colors.HexColor('#28A745')
C_YELLOW_BG = colors.HexColor('#FFF3CD')
C_YELLOW_BD = colors.HexColor('#FFC107')

def ms(name, **kw): return ParagraphStyle(name, **kw)

sty_cover_title = ms('CoverTitle', fontName='Helvetica-Bold', fontSize=32, textColor=C_WHITE, alignment=TA_CENTER, leading=40, spaceAfter=10)
sty_cover_sub   = ms('CoverSub', fontName='Helvetica', fontSize=15, textColor=colors.HexColor('#BDD5EA'), alignment=TA_CENTER, leading=22, spaceAfter=8)
sty_cover_meta  = ms('CoverMeta', fontName='Helvetica', fontSize=11, textColor=colors.HexColor('#BDD5EA'), alignment=TA_CENTER, leading=17)
sty_section     = ms('Section', fontName='Helvetica-Bold', fontSize=15, textColor=C_WHITE, alignment=TA_LEFT, leading=20)
sty_subsection  = ms('Subsection', fontName='Helvetica-Bold', fontSize=12, textColor=C_PRIMARY, leading=16, spaceAfter=5, spaceBefore=10)
sty_body        = ms('Body', fontName='Helvetica', fontSize=10.5, textColor=C_BLACK, leading=15.5, spaceAfter=5, alignment=TA_JUSTIFY)
sty_bullet      = ms('Bullet', fontName='Helvetica', fontSize=10.5, textColor=C_BLACK, leading=15, spaceAfter=4, leftIndent=14, firstLineIndent=-10)
sty_note        = ms('Note', fontName='Helvetica-Oblique', fontSize=9.5, textColor=C_GRAY, leading=13, spaceAfter=4, leftIndent=6)
sty_caption     = ms('Caption', fontName='Helvetica-Oblique', fontSize=9, textColor=C_GRAY, leading=12, alignment=TA_CENTER, spaceAfter=8)

def sec_hdr(num, title):
    t = Table([[Paragraph(f'<b>{num}. {title}</b>' if num else f'<b>{title}</b>', sty_section)]], colWidths=[17*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), C_PRIMARY), ('TOPPADDING', (0,0), (-1,-1), 10),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 10), ('LEFTPADDING', (0,0), (-1,-1), 14)]))
    return t

_n = [0]
def ibox(text, bg=None, border=None):
    _n[0] += 1
    s = ms(f'IB{_n[0]}', fontName='Helvetica', fontSize=10.5, textColor=C_BLACK, leading=15, leftIndent=4, alignment=TA_JUSTIFY)
    t = Table([[Paragraph(text, s)]], colWidths=[16.4*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), bg or C_LIGHT), ('LINERIGHT', (0,0), (0,-1), 3, border or C_PRIMARY),
                           ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                           ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
    return t
def wbox(text): return ibox('[!] ' + text, bg=C_YELLOW_BG, border=C_YELLOW_BD)
def tbox(text): return ibox('[*] ' + text, bg=C_GREEN_BG, border=C_GREEN_BD)
def blt(text): return Paragraph('- ' + text, sty_bullet)

def kv(rows, c1=5*cm, c2=11.4*cm):
    data = []
    for i, (k, v) in enumerate(rows):
        _n[0] += 1
        data.append([Paragraph(k, ms(f'KH{_n[0]}', fontName='Helvetica-Bold', fontSize=10, textColor=C_PRIMARY, leading=14)),
                     Paragraph(v, ms(f'KV{_n[0]}', fontName='Helvetica', fontSize=10, textColor=C_BLACK, leading=14))])
    t = Table(data, colWidths=[c1, c2])
    ts = [('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5), ('LEFTPADDING', (0,0), (-1,-1), 8),
          ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')), ('VALIGN', (0,0), (-1,-1), 'TOP')]
    for i in range(0, len(rows), 2): ts.append(('BACKGROUND', (0,i), (-1,i), C_LIGHTGRAY))
    t.setStyle(TableStyle(ts)); return t

def mtbl(headers, rows, widths=None, bold_rows=()):
    _n[0] += 1
    sh = ms(f'MH{_n[0]}', fontName='Helvetica-Bold', fontSize=10, textColor=C_WHITE, alignment=TA_CENTER, leading=14)
    sc = ms(f'MC{_n[0]}', fontName='Helvetica', fontSize=9.5, textColor=C_BLACK, alignment=TA_CENTER, leading=14)
    sb = ms(f'MB{_n[0]}', fontName='Helvetica-Bold', fontSize=9.5, textColor=C_BLACK, alignment=TA_CENTER, leading=14)
    data = [[Paragraph(h, sh) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), sb if i in bold_rows else sc) for c in row])
    if widths is None:
        w = 16.4*cm / len(headers); widths = [w]*len(headers)
    t = Table(data, colWidths=widths)
    ts = [('BACKGROUND', (0,0), (-1,0), C_PRIMARY), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
          ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
          ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]
    for i in range(1, len(rows)+1, 2): ts.append(('BACKGROUND', (0,i), (-1,i), C_LIGHTGRAY))
    t.setStyle(TableStyle(ts)); return t

def fig(name, width=16.4*cm, caption=None):
    path = os.path.join(FIGDIR, name)
    if not os.path.exists(path):
        return [Paragraph(f'[figura {name} não encontrada]', sty_note)]
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    img = Image(path, width=width, height=width*h/w)
    out = [img]
    if caption: out.append(Paragraph(caption, sty_caption))
    return [KeepTogether(out)]

SP = Spacer

def on_first_page(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(C_PRIMARY); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(C_ACCENT); canvas.rect(0, h-2.5*cm, w, 2.5*cm, fill=1, stroke=0); canvas.rect(0, 0, w, 1.6*cm, fill=1, stroke=0)
    canvas.restoreState()

def on_page(canvas, doc):
    w, h = A4
    canvas.saveState()
    canvas.setFillColor(C_PRIMARY); canvas.rect(0, 0, w, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE); canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(w/2, 0.38*cm, f'Forest Fires — Regressão Linear e Ridge  |  Análise de Dados  |  Pág. {doc.page}')
    canvas.restoreState()

def build():
    s = []
    # CAPA
    s += [SP(1, 5.5*cm), Paragraph('FOREST FIRES', sty_cover_title), SP(1, 0.2*cm),
          Paragraph('Análise de Dados, Regressão Linear e Ridge', sty_cover_sub), SP(1, 0.8*cm),
          HRFlowable(width='55%', thickness=2, color=C_ACCENT, spaceAfter=18),
          Paragraph('Dataset: Forest Fires — UCI Machine Learning Repository', sty_cover_meta),
          Paragraph('Parque Natural de Montesinho, Portugal', sty_cover_meta), SP(1, 0.8*cm),
          Paragraph('Outubro de 2026', sty_cover_meta), SP(1, 0.5*cm),
          Paragraph('Handout para apresentação em grupo — 7 participantes', sty_cover_meta), PageBreak()]

    # SUMÁRIO
    s += [SP(1, 0.5*cm), sec_hdr('', 'Sumário'), SP(1, 0.5*cm)]
    secs = [('1', 'Entendendo o Dataset'), ('2', 'Investigação Exploratória: o que a variável alvo esconde'),
            ('3', 'Preparação e Pré-processamento dos Dados'), ('4', 'Baseline e Regressão Linear (OLS)'),
            ('5', 'Regressão Ridge'), ('6', 'Avaliação, Comparação e o Modelo em Duas Partes'),
            ('7', 'Interpretação dos Resultados e Conclusão')]
    idx = []
    for num, title in secs:
        idx.append([Paragraph(num, ms('IN'+num, fontName='Helvetica-Bold', fontSize=13, textColor=C_ACCENT, alignment=TA_CENTER, leading=18)),
                    Paragraph(title, ms('IT'+num, fontName='Helvetica', fontSize=12, textColor=C_BLACK, leading=18))])
    t = Table(idx, colWidths=[1.4*cm, 15*cm])
    ts = [('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10), ('LEFTPADDING', (0,0), (-1,-1), 10),
          ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor('#DEE2E6'))]
    for i in range(len(secs)): ts.append(('BACKGROUND', (0,i), (-1,i), C_LIGHT if i % 2 == 0 else C_LIGHTGRAY))
    t.setStyle(TableStyle(ts))
    s += [t, SP(1, 0.4*cm),
          ibox('<b>Objetivo:</b> prever a área queimada (ha) em incêndios florestais a partir de variáveis meteorológicas e '
               'índices FWI (Fire Weather Index), comparando Regressão Linear com Regressão Ridge (regularização L2). '
               'O caminho até a resposta acabou valendo mais que a resposta: o trabalho mostra por que este dataset '
               'resiste a qualquer modelo linear, e o que isso ensina sobre preparação de dados.'),
          PageBreak()]

    # SEC 1
    s += [sec_hdr('1', 'Entendendo o Dataset'), SP(1, 0.4*cm), Paragraph('Origem e contexto', sty_subsection),
          Paragraph('O dataset <b>Forest Fires</b> foi coletado no Parque Natural de Montesinho, nordeste de Portugal, '
                    'e publicado por Cortez e Morais (2007) no UCI Machine Learning Repository. Reúne <b>517 ocorrências</b> '
                    'de incêndio registradas entre 2000 e 2003, cada uma com as condições meteorológicas do momento e os '
                    'índices do sistema canadense FWI. Um detalhe do registro vai pesar em toda a análise: a área é anotada '
                    'com duas casas decimais, de modo que <b>area = 0 significa área abaixo de 0,01 ha</b>, e não ausência de fogo.',
                    sty_body), SP(1, 0.25*cm), Paragraph('Variáveis do dataset', sty_subsection),
          mtbl(['Coluna', 'Tipo', 'Descrição'], [
              ['X, Y', 'Inteiro', 'Coordenadas espaciais na grade do parque (1 a 9)'],
              ['month', 'Texto', 'Mês do ano (jan – dec)'], ['day', 'Texto', 'Dia da semana (mon – sun)'],
              ['FFMC', 'Decimal', 'Fine Fuel Moisture Code — umidade dos combustíveis finos'],
              ['DMC', 'Decimal', 'Duff Moisture Code — umidade da camada orgânica do solo'],
              ['DC', 'Decimal', 'Drought Code — seca acumulada no solo profundo'],
              ['ISI', 'Decimal', 'Initial Spread Index — velocidade inicial de propagação'],
              ['temp', 'Decimal', 'Temperatura do ar (°C)'], ['RH', 'Inteiro', 'Umidade relativa do ar (%)'],
              ['wind', 'Decimal', 'Velocidade do vento (km/h)'], ['rain', 'Decimal', 'Chuva nas últimas 24h (mm/m<super>2</super>)'],
              ['area (*)', 'Decimal', 'VARIÁVEL ALVO — área queimada (hectares)']], widths=[2.8*cm, 2*cm, 11.6*cm]),
          SP(1, 0.1*cm), Paragraph('(*) variável que queremos prever (alvo / target)', sty_note),
          SP(1, 0.15*cm), Paragraph('Primeiro olhar sobre os dados', sty_subsection),
          kv([('Valores ausentes', 'Nenhum em nenhuma das 13 colunas.'),
              ('Variável rain', 'Mais de 98% dos registros têm rain = 0; variância quase nula, sem poder preditivo.'),
              ('Sazonalidade', 'Agosto e setembro concentram 69% das ocorrências; jan, may e nov têm 1 ou 2 registros; apr e dec, 9 cada.'),
              ('Correlações', 'Nenhuma variável numérica passa de |0,07| de correlação com log1p(area); os índices FWI são correlacionados entre si, o que justifica testar o Ridge.')],
             c1=3.6*cm, c2=12.8*cm),
          PageBreak()]

    # SEC 2
    s += [sec_hdr('2', 'Investigação Exploratória: o que a variável alvo esconde'), SP(1, 0.4*cm),
          Paragraph('Visão geral numérica', sty_subsection),
          mtbl(['Métrica', 'area (ha)', 'temp (°C)', 'RH (%)', 'wind (km/h)'], [
              ['Mínimo', '0,00', '2,2', '15', '0,4'], ['Mediana', '0,52', '19,3', '42', '4,0'],
              ['Média', '12,85', '18,9', '44', '4,0'], ['Máximo', '1090,84', '33,3', '100', '9,4'],
              ['Desvio-padrão', '63,66', '5,8', '16', '1,8']]),
          SP(1, 0.2*cm),
          Paragraph('A tabela já dá o aviso: a média da área (12,85 ha) é 25 vezes a mediana (0,52 ha), com poucos '
                    'incêndios enormes puxando a média enquanto metade dos registros fica abaixo de meio hectare. A análise '
                    'exploratória foi atrás desse descompasso e encontrou algo que a transformação logarítmica usual não resolve.',
                    sty_body)]
    s += fig('fig_alvo.png', caption='Figura 1 — A variável alvo antes e depois do log. O pico em zero não se move; os valores positivos, isolados, são quase normais.')
    s += [Paragraph('A transformação resolve a assimetria, mas não o pico', sty_subsection),
          Paragraph('O painel do meio é o que costuma aparecer como "alvo transformado", e ele não se parece com uma normal '
                    'porque não tem como: <b>247 dos 517 incêndios (47,8%) têm area exatamente igual a zero</b>. Uma '
                    'transformação monotônica leva 247 valores iguais em 247 valores iguais, de modo que nenhum log, raiz ou '
                    'Box-Cox desloca esse pico. Já o painel da direita isola os 270 registros com área positiva, e aí o '
                    'log(area) é praticamente normal: skewness de 0,30, teste de Shapiro-Wilk sem rejeitar a normalidade '
                    '(p ~ 0,24) e Box-Cox escolhendo lambda ~ 0, que é o próprio log.', sty_body),
          wbox('O alvo não é apenas assimétrico: é <b>semicontínuo com inflação de zeros</b>. Há duas perguntas escondidas numa '
               'só variável — o incêndio passou de 0,01 ha? e, se passou, quanto queimou? — e a seção 6 as trata separadamente.'),
          PageBreak()]

    # SEC 3
    s += [sec_hdr('3', 'Preparação e Pré-processamento dos Dados'), SP(1, 0.4*cm),
          Paragraph('Com base na EDA, aplicamos seis transformações para deixar os dados prontos para a regressão:', sty_body), SP(1, 0.2*cm)]
    etapas = [
        ('(1) Transformação log1p(area)', 'Aplicamos log(1 + area) ao alvo. A transformação estabiliza a escala dos valores positivos (skewness de 12,8 cai para 1,2) e põe o erro em escala multiplicativa, adequada a áreas que vão de 0,1 a 1 000 ha. A massa em zero continua lá e recebe tratamento próprio na seção 6.', C_LIGHT, C_PRIMARY),
        ('(2) Remoção de rain', 'Descartada por variância quase nula (98,5% dos valores iguais a zero).', C_YELLOW_BG, C_YELLOW_BD),
        ('(3) Agrupamento dos meses raros', 'jan, may, nov, apr e dec, todos com menos de 10 registros, viraram a categoria "outros". Uma dummy ajustada em dois pontos é ruído puro: antes do agrupamento, month_dec liderava o ranking de coeficientes do OLS com nove registros.', C_YELLOW_BG, C_YELLOW_BD),
        ('(4) One-Hot Encoding', 'month e day viraram colunas binárias, com drop_first=True para evitar a armadilha das dummies. Resultado: 22 preditores.', C_LIGHT, C_PRIMARY),
        ('(5) Divisão treino/teste (80/20)', '413 amostras de treino e 104 de teste, com random_state=42. O modelo aprende no treino e é avaliado em dados que nunca viu.', C_GREEN_BG, C_GREEN_BD),
        ('(6) Padronização com StandardScaler', 'Cada feature centralizada (média 0) e escalada (desvio 1), com o scaler ajustado só no treino. Na validação cruzada ele entra num Pipeline e é reajustado em cada dobra, sem vazamento.', C_LIGHT, C_PRIMARY),
    ]
    for title, desc, bg, brd in etapas:
        s += [ibox(f'<b>{title}</b><br/>{desc}', bg=bg, border=brd), SP(1, 0.12*cm)]
    s += [SP(1, 0.2*cm), Paragraph('Resultado do pipeline', sty_subsection),
          mtbl(['Etapa', 'Features', 'Observação'], [
              ['Dataset original', '12 preditores + 1 alvo', '13 colunas'],
              ['Após remoção de rain e agrupamento + OHE', '22 preditores', '7 dummies de mês, 6 de dia'],
              ['Após divisão e padronização', '22 × 413 treino / 22 × 104 teste', 'fit no treino, transform no teste']],
               widths=[4.4*cm, 4.4*cm, 7.6*cm]),
          PageBreak()]

    # SEC 4
    s += [sec_hdr('4', 'Baseline e Regressão Linear (OLS)'), SP(1, 0.4*cm),
          Paragraph('Primeiro, a régua: o baseline', sty_subsection),
          Paragraph('Antes de qualquer modelo, registramos o desempenho de prever sempre a média do treino. Todo modelo precisa '
                    'vencer essa régua; se não vence, as features não estão acrescentando informação. Essa referência faltava na '
                    'primeira versão do trabalho, e sem ela um R<super>2</super> de 0,03 parece "baixo mas positivo" em vez do que é: '
                    'indistinguível de zero.', sty_body),
          Paragraph('O que é a Regressão Linear', sty_subsection),
          Paragraph('A <b>Regressão Linear Ordinária</b> (OLS) encontra o hiperplano que minimiza a soma dos quadrados dos '
                    'resíduos. A solução é analítica, <b>B = (X\'X)<super>-1</super>X\'y</b>, e exige que X\'X seja invertível, o que fica '
                    'instável quando as features são correlacionadas.', sty_body),
          ibox('<b>y_pred = b0 + b1·x1 + b2·x2 + ... + bn·xn</b><br/><br/>y_pred = log(1+area) estimado   |   b0 = intercepto   |   bi = coeficientes   |   xi = features'),
          SP(1, 0.25*cm), Paragraph('Resultados obtidos', sty_subsection),
          mtbl(['Modelo', 'Conjunto', 'RMSE', 'MAE', 'R<super>2</super>'], [
              ['Baseline (média)', 'Treino', '1,3746', '1,1439', '0,0000'],
              ['Baseline (média)', 'Teste', '1,4830', '1,2028', '-0,0006'],
              ['OLS', 'Treino', '1,3382', '1,0996', '0,0523'],
              ['OLS', 'Teste', '1,4610', '1,1736', '0,0288']]),
          SP(1, 0.2*cm),
          wbox('O OLS fica 0,02 de RMSE abaixo do baseline no teste e, como a seção 6 mostra, <b>acima</b> dele na validação cruzada. '
               'Uma diferença que troca de sinal conforme a avaliação está dentro do ruído.'),
          PageBreak()]

    # SEC 5
    s += [sec_hdr('5', 'Regressão Ridge'), SP(1, 0.4*cm), Paragraph('O que é', sty_subsection),
          Paragraph('A <b>Regressão Ridge</b> acrescenta à função de custo do OLS uma <b>penalização L2</b>, que encolhe os '
                    'coeficientes em direção a zero e torna o modelo menos sensível à multicolinearidade.', sty_body),
          ibox('<b>Custo Ridge = Soma dos Quadrados dos Resíduos + α × soma de bi<super>2</super></b><br/><br/>'
               'Primeiro termo = OLS (minimiza o erro)<br/>Segundo termo = penalidade (pune coeficientes grandes)<br/>'
               '<b>α</b> controla a intensidade da regularização: α = 0 é o OLS; alfa tendendo ao infinito zera todos os coeficientes'),
          SP(1, 0.25*cm), Paragraph('Como escolhemos o α', sty_subsection),
          Paragraph('Usamos o <b>RidgeCV</b> com 200 valores de α entre 0,001 e 10 000 (escala logarítmica) e validação cruzada '
                    'de 10 dobras. O α escolhido foi <b>10 000, o teto da grade</b>: a validação cruzada pediu a maior '
                    'penalização disponível e teria pedido mais se houvesse.', sty_body)]
    s += fig('fig_ridge_path.png', width=14.5*cm, caption='Figura 2 — Trajetória dos 22 coeficientes conforme α cresce. Cada linha é uma feature; a tracejada marca o α escolhido, onde todas já convergiram para zero.')
    s += [Paragraph('A figura 2 é a peça central da seção. Num dataset com sinal, a validação cruzada para em algum ponto da '
                    'região em que as curvas estão dobrando, onde o ruído já foi amortecido e os efeitos reais sobrevivem. '
                    'Aqui ela caminhou até a parede direita. As linhas que se cruzam no meio do caminho mostram outra coisa: '
                    'a ordem de "importância" das features muda conforme o α, de modo que não existe uma resposta única para '
                    'qual variável pesa mais.', sty_body),
          tbox('<b>Resultados:</b> RMSE 1,3721 / MAE 1,1420 / R<super>2</super> 0,0037 no treino; RMSE 1,4812 / MAE 1,2018 / R<super>2</super> 0,0018 no teste. '
               'Com α = 10 000, as previsões no teste têm desvio-padrão de <b>0,014</b>, contra <b>1,49</b> do alvo: '
               'o modelo prevê, na prática, a média. É o que a regularização deve fazer quando as features são ruído.'),
          PageBreak()]

    # SEC 6
    s += [sec_hdr('6', 'Avaliação, Comparação e o Modelo em Duas Partes'), SP(1, 0.4*cm),
          Paragraph('Métricas utilizadas', sty_subsection),
          kv([('RMSE', 'Raiz do erro quadrático médio. Penaliza mais os erros grandes; mesma unidade do alvo (log_area).'),
              ('MAE', 'Erro absoluto médio. Mais robusto a valores extremos.'),
              ('R<super>2</super>', 'Proporção da variância explicada. R<super>2</super> = 0 equivale a prever a média; negativo é pior que a média. '
                     'Sob validação cruzada, um modelo sem sinal fica levemente negativo, porque a média de cada dobra de '
                     'treino difere da média da dobra de teste.')], c1=2*cm, c2=14.4*cm),
          SP(1, 0.3*cm), Paragraph('Comparativo geral', sty_subsection),
          mtbl(['Modelo', 'RMSE Treino', 'RMSE Teste', 'MAE Teste', 'R<super>2</super> Teste', 'CV RMSE (10-fold)'], [
              ['Baseline (média)', '1,3746', '1,4830', '1,2028', '-0,0006', '1,3878 ± 0,1735'],
              ['Linear (OLS)', '1,3382', '1,4610', '1,1736', '0,0288', '1,4000 ± 0,1577'],
              ['Ridge (α = 10<super>4</super>)', '1,3721', '1,4812', '1,2018', '0,0018', '1,3869 ± 0,1729']],
               widths=[3.4*cm, 2.4*cm, 2.4*cm, 2.3*cm, 2.3*cm, 3.6*cm]),
          SP(1, 0.2*cm),
          Paragraph('Os três modelos ficam colados. No holdout o OLS aparece à frente; na validação cruzada, que usa os 517 '
                    'registros e é a estimativa mais confiável, o Ridge empata com o baseline na terceira casa decimal e o OLS '
                    'fica atrás dos dois. Quando duas avaliações honestas invertem a ordem, a diferença entre os modelos é ruído.',
                    sty_body)]
    s += fig('fig_residuos.png', width=9.2*cm, caption='Figura 3 — Resíduos no conjunto de teste. A faixa horizontal em torno de -1 são os incêndios com area = 0.')
    s += [          Paragraph('Diagnóstico dos resíduos', sty_subsection),
          Paragraph('Como o Ridge prevê um valor quase constante, o gráfico de resíduos reproduz o próprio alvo: uma faixa em '
                    'torno de -1 (os incêndios com area = 0) e uma nuvem acima (os positivos). A "heterocedasticidade" e a cauda '
                    'do Q-Q plot são a inflação de zeros reaparecendo nos resíduos, não uma violação leve de pressuposto.', sty_body),
          PageBreak(), sec_hdr('6', 'O modelo em duas partes (hurdle)'), SP(1, 0.4*cm),
          Paragraph('A seção 2 mostrou que o problema é a inflação de zeros. A forma clássica de modelar um alvo assim é dividi-lo '
                    'em duas etapas: uma <b>classificação</b> (regressão logística) para "o incêndio passou de 0,01 ha?", e uma '
                    '<b>regressão</b> em log(area) só para os 270 que passaram, onde o alvo é quase normal. Se as variáveis '
                    'meteorológicas tivessem algum sinal, ele apareceria em pelo menos uma das etapas. Ambas foram avaliadas com '
                    'previsões fora da dobra (10-fold).', sty_body),
          mtbl(['Etapa', 'Modelo', 'Métrica', 'Resultado', 'Referência'], [
              ['1 — passou de 0,01 ha?', 'Logística (C = 0,1)', 'AUC', '0,534', '0,500 = sorteio'],
              ['1 — passou de 0,01 ha?', 'Logística (C = 0,1)', 'Acurácia', '0,542', '0,522 = classe majoritária'],
              ['2 — quanto queimou?', 'Ridge α = 1 / 10 / 100', 'RMSE', '1,571 / 1,560 / 1,547', '1,527 = prever a média'],
              ['2 — quanto queimou?', 'Ridge α = 1 / 10 / 100', 'R<super>2</super>', '-0,063 / -0,048 / -0,031', '0 = prever a média']],
               widths=[3.6*cm, 3.4*cm, 2*cm, 4*cm, 3.4*cm])]
    s += [SP(1, 0.2*cm)]
    s += fig('fig_hurdle.png', caption='Figura 4 — Proporção de incêndios com área mensurável por mês e por dia da semana. Em nenhum recorte a proporção se afasta muito dos 52% gerais.')
    s += [Paragraph('Nenhuma das etapas encontra sinal. A classificação fica no nível do sorteio, a regressão nos positivos perde '
                    'para a média em todos os α testados (os três valores estão lá justamente para mostrar que o α não muda o '
                    'resultado), e a proporção de incêndios com área mensurável gira em torno de 50% em todo mês e em todo dia '
                    'da semana. Março e outubro ficam um pouco abaixo, com 35% e 33%, o que é consistente com fogos de '
                    'primavera e outono serem menores, mas é uma diferença de poucos pontos em amostras pequenas.', sty_body),
          tbox('O modelo em duas partes é a abordagem estatisticamente correta para este alvo, e justamente por isso o resultado '
               'nulo dele é informativo: as variáveis descrevem as condições no momento da ignição, e a área final depende do '
               'que não está na tabela.'),
          PageBreak()]

    # SEC 7
    s += [sec_hdr('7', 'Interpretação dos Resultados e Conclusão'), SP(1, 0.4*cm),
          Paragraph('Por que os coeficientes não devem ser interpretados', sty_subsection)]
    s += fig('fig_coefs.png', width=15.5*cm, caption='Figura 5 — Top 15 coeficientes. Repare na escala: os do Ridge são de 20 a 50 vezes menores, e DC troca de sinal entre os painéis.')
    s += [Paragraph('No OLS os maiores coeficientes são DMC, month_outros e month_sep, com DC negativo. No Ridge todos ficam '
                    'abaixo de 0,005 e DC passa a positivo. Variáveis que a intuição colocaria à frente, como temperatura, ISI e '
                    'umidade relativa, têm correlação abaixo de 0,1 com o alvo e não se destacam em nenhum dos dois modelos. '
                    'Quando a ordem e o sinal mudam tanto com a regularização, os coeficientes não estão medindo efeito; estão '
                    'medindo ruído de amostragem. Atribuir um efeito a "dias mais quentes" ou "mais seca" seria ler o ruído '
                    'como se fosse sinal.', sty_body),
          PageBreak(), sec_hdr('7', 'Conclusão'), SP(1, 0.4*cm), Paragraph('OLS vs Ridge', sty_subsection),
          mtbl(['Critério', 'OLS', 'Ridge'], [
              ['Regularização', 'Nenhuma', 'L2 (penaliza bi<super>2</super>)'], ['Multicolinearidade', 'Problemático', 'Robusto'],
              ['Risco de overfitting', 'Maior', 'Menor'], ['Validação cruzada', 'Pior que o baseline', 'Empata com o baseline'],
              ['Escolha neste estudo', '—', '(*) Preferível, por margem pequena']], widths=[5*cm, 5.7*cm, 5.7*cm]),
          SP(1, 0.3*cm), Paragraph('Conclusão', sty_subsection),
          ibox('<b>1.</b> A transformação logarítmica está correta, mas resolve só metade do problema: normaliza os valores '
               'positivos e não tem como tocar na massa de 47,8% de zeros. O alvo é semicontínuo, e o tratamento adequado é o '
               'modelo em duas partes.<br/><br/>'
               '<b>2.</b> Mesmo com esse tratamento, as variáveis meteorológicas e os índices FWI não explicam nem <b>se</b> o '
               'incêndio ultrapassa 0,01 ha nem <b>quanto</b> ele queima quando ultrapassa. O melhor modelo linear é, na prática, '
               'a média, e a literatura desde Cortez e Morais (2007) encontra o mesmo com modelos não lineares.<br/><br/>'
               '<b>3.</b> Entre OLS e Ridge, o Ridge é preferível por não piorar o baseline e por manter os coeficientes '
               'pequenos e estáveis, mas a diferença é marginal.<br/><br/>'
               '<b>4.</b> O ganho real viria de dados que não estão na tabela: tempo até o início do combate, tipo de vegetação, '
               'declividade, e um alvo que separasse área medida de área abaixo do limiar.'),
          SP(1, 0.3*cm), Paragraph('Próximos passos sugeridos', sty_subsection)]
    for item in ['Buscar variáveis de resposta ao incêndio (tempo de combate, meios empregados) e de terreno (vegetação, declividade)',
                 'Modelos não lineares (Random Forest, Gradient Boosting) dentro da estrutura em duas partes, para confirmar que o limite é dos dados e não do modelo',
                 'Lasso e Elastic Net, que zerariam explicitamente as features sem sinal',
                 'Análise espacial das coordenadas X e Y, única dimensão do dataset ainda pouco explorada']:
        s += [blt(item)]
    s += [SP(1, 0.3*cm),
          Paragraph('Notebook completo: analise_forestfires_v2.ipynb  |  Dataset: forestfires.csv — UCI Machine Learning Repository', sty_note)]
    return s

OUTPUT = 'relatorio_forestfires_v2.pdf'
doc = SimpleDocTemplate(OUTPUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2*cm,
                        title='Forest Fires — Análise de Dados e Regressão (v2)', author='CESMAC — Grupo de Análise de Dados',
                        subject='Regressão Linear e Ridge — Forest Fires Dataset')
doc.build(build(), onFirstPage=on_first_page, onLaterPages=on_page)
print(f'PDF gerado: {OUTPUT}  ({os.path.getsize(OUTPUT)/1024:.0f} KB)')
