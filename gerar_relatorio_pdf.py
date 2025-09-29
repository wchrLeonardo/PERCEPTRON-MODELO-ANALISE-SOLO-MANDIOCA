from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime

def gerar_relatorio_pdf_reportlab():
    filename = "RELATORIO_PERCEPTRON_MANDIOCA_ABNT.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=72, bottomMargin=72)
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    texto_style = ParagraphStyle(
        'CustomText',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica'
    )
    
    # Lista de elementos do PDF
    elements = []
    
    # CAPA
    elements.append(Spacer(1, 50))
    elements.append(Paragraph("FACULDADE DE TECNOLOGIA DE SÃO PAULO", titulo_style))
    elements.append(Paragraph("CURSO SUPERIOR DE TECNOLOGIA EM DESENVOLVIMENTO DE SOFTWARE MULTIPLATAFORMA", subtitulo_style))
    elements.append(Spacer(1, 50))
    
    elements.append(Paragraph("ANÁLISE DE ADEQUAÇÃO DE SOLO PARA CULTIVO DE MANDIOCA UTILIZANDO PERCEPTRON:", titulo_style))
    elements.append(Paragraph("Uma Abordagem de Aprendizado de Máquina", subtitulo_style))
    elements.append(Spacer(1, 80))
    
    # Colaboradores
    elements.append(Paragraph("Desenvolvido por:", ParagraphStyle('ColaboradoresLabel', fontSize=12, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=10)))
    elements.append(Paragraph("João Pedro Dias Barreto", ParagraphStyle('Colaborador', fontSize=12, alignment=TA_CENTER, fontName='Helvetica')))
    elements.append(Paragraph("Leonardo Wicher Lopes Ferreira", ParagraphStyle('Colaborador', fontSize=12, alignment=TA_CENTER, fontName='Helvetica', spaceAfter=20)))
    
    elements.append(Paragraph("Relatório Técnico - Projeto de Aprendizado de Máquina", texto_style))
    elements.append(Spacer(1, 120))
    
    data_atual = datetime.now().strftime("%B de %Y")
    elements.append(Paragraph(f"São Paulo<br/>{data_atual}", ParagraphStyle('Center', alignment=TA_CENTER)))
    
    elements.append(PageBreak())
    
    # RESUMO
    elements.append(Paragraph("RESUMO", titulo_style))
    resumo_text = """Este trabalho apresenta o desenvolvimento e implementação de um modelo de Perceptron para 
    classificação binária da adequação de solo para o cultivo de mandioca (<i>Manihot esculenta</i>). O sistema 
    desenvolvido analisa quatro parâmetros edáficos fundamentais: pH do solo, concentração de potássio, 
    qualidade da drenagem e presença de compactação. O modelo alcançou 97,78% ± 4,44% de acurácia na 
    validação cruzada, demonstrando alta eficácia na predição da adequação do solo. A implementação inclui 
    uma interface gráfica intuitiva para aplicação prática por agricultores e técnicos agrícolas.<br/><br/>
    <b>Palavras-chave:</b> Perceptron, Agricultura de Precisão, Classificação de Solo, Aprendizado de Máquina, Mandioca."""
    
    elements.append(Paragraph(resumo_text, texto_style))
    elements.append(Spacer(1, 30))
    
    # INTRODUÇÃO
    elements.append(Paragraph("1. INTRODUÇÃO", subtitulo_style))
    
    intro_text = """A mandioca (<i>Manihot esculenta</i>) constitui uma das principais culturas alimentares do mundo, sendo 
    especialmente relevante para a segurança alimentar em países tropicais. No Brasil, representa importante 
    fonte de carboidratos e matéria-prima para diversos produtos industriais.<br/><br/>
    
    A adequação do solo representa fator determinante para o sucesso do cultivo da mandioca, influenciando 
    diretamente na produtividade e qualidade das raízes tuberosas. Fatores como pH, disponibilidade de 
    nutrientes, drenagem e estrutura física do solo são parâmetros críticos que determinam a viabilidade 
    econômica do cultivo.<br/><br/>
    
    Tradicionalmente, a avaliação da adequação do solo baseia-se na experiência empírica dos produtores ou 
    em análises laboratoriais interpretadas por técnicos especializados. Esta abordagem apresenta limitações 
    relacionadas à subjetividade da interpretação, custos elevados e tempo prolongado para obtenção de 
    resultados.<br/><br/>
    
    Neste contexto, técnicas de aprendizado de máquina emergem como ferramentas promissoras para 
    automatização e otimização da tomada de decisão na agricultura de precisão."""
    
    elements.append(Paragraph(intro_text, texto_style))
    elements.append(PageBreak())
    
    # METODOLOGIA
    elements.append(Paragraph("2. METODOLOGIA", subtitulo_style))
    
    metodologia_text = """<b>2.1 Descrição do Modelo</b><br/><br/>
    O modelo implementado baseia-se na arquitetura clássica do Perceptron monocamada, com as seguintes características:<br/>
    • Arquitetura: 4 neurônios de entrada correspondentes aos atributos de entrada<br/>
    • Função de ativação: Degrau unitário (step function)<br/>
    • Saída: Classificação binária (0 = não apto, 1 = apto)<br/><br/>
    
    <b>2.2 Função de Ativação</b><br/><br/>
    A função de ativação degrau foi implementada conforme:<br/>
    f(x) = 1, se x ≥ 0<br/>
    f(x) = 0, se x &lt; 0<br/><br/>
    Onde x representa a soma ponderada das entradas mais o bias.<br/><br/>
    
    <b>2.3 Algoritmo de Treinamento</b><br/><br/>
    O treinamento utiliza a regra Delta: Δw<sub>i</sub> = η × e × x<sub>i</sub><br/>
    Onde η = taxa de aprendizado, e = erro (saída desejada - saída obtida), x<sub>i</sub> = entrada i<br/><br/>
    
    <b>2.4 Base de Dados</b><br/><br/>
    O dataset foi construído com base em conhecimento agronômico estabelecido, contendo 45 exemplos 
    balanceados com os seguintes atributos:<br/>
    • pH do solo (4,0 - 8,0)<br/>
    • Potássio em mg/dm³ (40 - 200)<br/>
    • Drenagem (0=ruim, 1=boa)<br/>
    • Compactação (0=presente, 1=ausente)<br/>
    • Classe alvo: Adequado (0=não, 1=sim)<br/><br/>
    
    <b>Distribuição das classes:</b><br/>
    • Solos adequados: 22 exemplos (48,9%)<br/>
    • Solos inadequados: 23 exemplos (51,1%)"""
    
    elements.append(Paragraph(metodologia_text, texto_style))
    elements.append(PageBreak())
    
    # RESULTADOS - TABELAS
    elements.append(Paragraph("3. RESULTADOS E DISCUSSÃO", subtitulo_style))
    
    # Tabela 1 - Performance
    elements.append(Paragraph("<b>Tabela 1 - Resultados da validação cruzada 5-fold</b>", texto_style))
    
    table1_data = [
        ['Métrica', 'Valor'],
        ['Acurácia Média', '97,78% ± 4,44%'],
        ['Épocas Médias', '4,2 ± 1,1'],
        ['Melhor Fold', '100,00%'],
        ['Pior Fold', '88,89%']
    ]
    
    table1 = Table(table1_data, colWidths=[2*inch, 2*inch])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table1)
    elements.append(Spacer(1, 20))
    
    # Tabela 2 - Taxa de Aprendizado
    elements.append(Paragraph("<b>Tabela 2 - Impacto da taxa de aprendizado na performance</b>", texto_style))
    
    table2_data = [
        ['Taxa (η)', 'Acurácia (%)', 'Épocas', 'Observações'],
        ['0,01', '93,33 ± 5,44', '24,3 ± 6,2', 'Convergência lenta'],
        ['0,05', '95,56 ± 3,14', '17,0 ± 12,0', 'Moderada'],
        ['0,10', '95,56 ± 6,29', '5,3 ± 1,2', 'Balanceada'],
        ['0,20', '97,78 ± 3,14', '8,7 ± 0,9', 'Ótima'],
        ['0,50', '100,00 ± 0,00', '5,3 ± 1,2', 'Excelente']
    ]
    
    table2 = Table(table2_data, colWidths=[1*inch, 1.5*inch, 1*inch, 1.8*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table2)
    elements.append(Spacer(1, 20))
    
    # Tabela 3 - Importância dos Fatores
    elements.append(Paragraph("<b>Tabela 3 - Importância dos fatores (pesos absolutos médios)</b>", texto_style))
    
    table3_data = [
        ['Fator', 'Peso Médio', 'Importância'],
        ['Distância do pH Ideal', '0,40', 'Crítica'],
        ['Ausência de Compactação', '0,31', 'Alta'],
        ['Boa Drenagem', '0,11', 'Média'],
        ['Potássio Normalizado', '0,07', 'Baixa']
    ]
    
    table3 = Table(table3_data, colWidths=[2.5*inch, 1*inch, 1*inch])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table3)
    elements.append(PageBreak())
    
    # DISCUSSÃO CRÍTICA
    elements.append(Paragraph("4. DISCUSSÃO CRÍTICA", subtitulo_style))
    
    discussao_text = """<b>4.1 Vantagens do Modelo</b><br/><br/>
    • <b>Alta Interpretabilidade:</b> O Perceptron permite compreensão direta da importância de cada fator 
    através dos pesos sinápticos, facilitando a validação agronômica dos resultados.<br/><br/>
    • <b>Simplicidade Computacional:</b> A implementação requer recursos computacionais mínimos, 
    viabilizando aplicação em dispositivos móveis e sistemas embarcados.<br/><br/>
    • <b>Convergência Rápida:</b> O modelo converge em média após 4,2 épocas, demonstrando eficiência no 
    aprendizado dos padrões.<br/><br/>
    • <b>Performance Robusta:</b> Acurácia de 97,78% indica alta confiabilidade para aplicação prática.<br/><br/>
    
    <b>4.2 Limitações Identificadas</b><br/><br/>
    • <b>Linearidade dos Dados:</b> O Perceptron assume separabilidade linear das classes, limitando sua 
    aplicação a problemas linearmente separáveis.<br/><br/>
    • <b>Tamanho da Base de Dados:</b> Dataset com 45 exemplos pode ser insuficiente para capturar toda a 
    variabilidade das condições de campo.<br/><br/>
    • <b>Fatores Não Considerados:</b> Importantes parâmetros como matéria orgânica, micronutrientes e 
    aspectos climáticos não foram incluídos no modelo.<br/><br/>
    
    <b>4.3 Regras de Decisão Interpretáveis</b><br/><br/>
    <b>Solo ADEQUADO quando:</b><br/>
    • pH próximo a 6,0 (±0,5)<br/>
    • Solo não compactado<br/>
    • Drenagem adequada<br/>
    • Potássio > 100 mg/dm³<br/><br/>
    
    <b>Solo INADEQUADO quando:</b><br/>
    • pH < 5,0 ou pH > 7,0<br/>
    • Presença de compactação<br/>
    • Drenagem deficiente<br/>
    • Combinação de múltiplos fatores limitantes"""
    
    elements.append(Paragraph(discussao_text, texto_style))
    elements.append(PageBreak())
    
    # CONCLUSÃO
    elements.append(Paragraph("5. CONCLUSÃO", subtitulo_style))
    
    conclusao_text = """O presente trabalho demonstrou a viabilidade e eficácia da aplicação do algoritmo Perceptron 
    para classificação da adequação de solo para cultivo de mandioca. O modelo desenvolvido alcançou 
    performance excepcional (97,78% de acurácia), convergência rápida e alta interpretabilidade dos 
    resultados.<br/><br/>
    
    A análise dos pesos sinápticos confirmou conhecimentos agronômicos estabelecidos, identificando o pH 
    como fator mais crítico, seguido pela ausência de compactação do solo. Esta concordância entre os 
    resultados do modelo e o conhecimento técnico valida a abordagem metodológica adotada.<br/><br/>
    
    A interface gráfica desenvolvida viabiliza a aplicação prática do sistema, democratizando o acesso à 
    tecnologia de suporte à decisão na agricultura. O sistema pode contribuir significativamente para 
    otimização do uso da terra, redução de custos de análise e melhoria da produtividade agrícola.<br/><br/>
    
    O trabalho contribui para o avanço da agricultura de precisão no Brasil, demonstrando que técnicas 
    simples de aprendizado de máquina podem gerar impacto significativo quando aplicadas adequadamente a 
    problemas agronômicos específicos."""
    
    elements.append(Paragraph(conclusao_text, texto_style))
    elements.append(Spacer(1, 30))
    
    # REFERÊNCIAS
    elements.append(Paragraph("REFERÊNCIAS", subtitulo_style))
    
    referencias_text = """COCK, J. H. <b>Cassava: new potential for a neglected crop.</b> Boulder: Westview Press, 1985. 191 p.<br/><br/>
    
    EL-SHARKAWY, M. A. Cassava biology and physiology. <b>Plant Molecular Biology</b>, v. 56, n. 4, p. 481-501, 2003.<br/><br/>
    
    FAO - FOOD AND AGRICULTURE ORGANIZATION. <b>FAOSTAT - Crops and livestock products.</b> Roma: FAO, 2021.<br/><br/>
    
    IBGE - INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. <b>Levantamento sistemático da 
    produção agrícola.</b> Rio de Janeiro: IBGE, 2022. 85 p.<br/><br/>
    
    KOHAVI, R. A study of cross-validation and bootstrap for accuracy estimation and model selection. 
    <b>Proceedings of the 14th International Joint Conference on Artificial Intelligence</b>, v. 2, p. 1137-1143, 1995.<br/><br/>
    
    ROSENBLATT, F. The perceptron: a probabilistic model for information storage and organization in the 
    brain. <b>Psychological Review</b>, v. 65, n. 6, p. 386-408, 1958."""
    
    elements.append(Paragraph(referencias_text, texto_style))
    
    # Gerar o PDF
    doc.build(elements)
    
    print("✅ Relatório PDF gerado com sucesso!")
    print("📄 Arquivo: RELATORIO_PERCEPTRON_MANDIOCA_ABNT.pdf")
    print("📊 Conteúdo: Relatório completo com formatação ABNT")
    print("🎯 Localização: Pasta atual do projeto")

if __name__ == "__main__":
    gerar_relatorio_pdf_reportlab()