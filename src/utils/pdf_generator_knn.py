from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime

def gerar_relatorio_pdf_reportlab():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    filename = os.path.join(base_dir, 'docs', 'reports', "RELATORIO_KNN_MANDIOCA_ABNT.pdf")
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
    
    elements.append(Paragraph("ANÁLISE DE ADEQUAÇÃO DE SOLO PARA CULTIVO DE MANDIOCA:", titulo_style))
    elements.append(Paragraph("Comparativo entre Perceptron e K-Nearest Neighbors (KNN)", subtitulo_style))
    elements.append(Spacer(1, 80))
    
    # Colaboradores
    elements.append(Paragraph("Desenvolvido por:", ParagraphStyle('ColaboradoresLabel', fontSize=12, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=10)))
    elements.append(Paragraph("João Pedro Dias Barreto", ParagraphStyle('Colaborador', fontSize=12, alignment=TA_CENTER, fontName='Helvetica')))
    elements.append(Paragraph("Leonardo Wicher Lopes Ferreira", ParagraphStyle('Colaborador', fontSize=12, alignment=TA_CENTER, fontName='Helvetica', spaceAfter=20)))
    
    elements.append(Paragraph("Relatório Técnico - AT2 - Técnicas de Aprendizagem de Máquina", texto_style))
    elements.append(Spacer(1, 120))
    
    data_atual = datetime.now().strftime("%B de %Y")
    elements.append(Paragraph(f"São Paulo<br/>{data_atual}", ParagraphStyle('Center', alignment=TA_CENTER)))
    
    elements.append(PageBreak())
    
    # RESUMO
    elements.append(Paragraph("RESUMO", titulo_style))
    resumo_text = """Este trabalho apresenta a implementação e análise comparativa de dois algoritmos de aprendizado de máquina, 
    Perceptron e K-Nearest Neighbors (KNN), para a classificação da adequação de solo no cultivo de mandioca (<i>Manihot esculenta</i>). 
    Utilizando uma base de dados com parâmetros edáficos (pH, potássio, drenagem e compactação), o algoritmo KNN foi avaliado 
    com diferentes valores de K (3, 5 e 7). Os resultados demonstraram que o KNN obteve 100% de acurácia em todas as configurações testadas, 
    superando ou igualando a performance do Perceptron (97,78%). O estudo confirma a eficácia de algoritmos baseados em instância 
    para conjuntos de dados de pequeno porte e alta dimensionalidade relativa.<br/><br/>
    <b>Palavras-chave:</b> KNN, Perceptron, Classificação de Solo, Mandioca, Aprendizado de Máquina."""
    
    elements.append(Paragraph(resumo_text, texto_style))
    elements.append(Spacer(1, 30))
    
    # INTRODUÇÃO
    elements.append(Paragraph("1. INTRODUÇÃO", subtitulo_style))
    
    intro_text = """A mandioca é uma cultura vital para a segurança alimentar global. A determinação correta da aptidão do solo 
    é crucial para maximizar a produtividade. Enquanto modelos lineares como o Perceptron oferecem simplicidade e interpretabilidade, 
    algoritmos não-paramétricos como o K-Nearest Neighbors (KNN) podem capturar relações mais complexas entre os dados sem 
    assumir uma distribuição específica ou separabilidade linear.<br/><br/>
    
    Este relatório técnico (AT2) expande o trabalho anterior focando na implementação do algoritmo KNN, variando o hiperparâmetro K, 
    e comparando sua eficácia com o modelo Perceptron previamente desenvolvido."""
    
    elements.append(Paragraph(intro_text, texto_style))
    elements.append(PageBreak())
    
    # METODOLOGIA
    elements.append(Paragraph("2. METODOLOGIA", subtitulo_style))
    
    metodologia_text = """<b>2.1 Algoritmo K-Nearest Neighbors (KNN)</b><br/><br/>
    O KNN é um algoritmo de aprendizado supervisionado baseado em instâncias (lazy learning). A classificação de um novo exemplo 
    é realizada através de uma votação majoritária entre os seus K vizinhos mais próximos no espaço de características.<br/><br/>
    
    <b>2.2 Métrica de Distância</b><br/><br/>
    Foi utilizada a Distância Euclidiana para calcular a proximidade entre as amostras:<br/>
    d(p, q) = √[Σ(pi - qi)²]<br/><br/>
    
    <b>2.3 Configuração Experimental</b><br/><br/>
    • <b>Pré-processamento:</b> Normalização Min-Max para atributos contínuos (pH e Potássio) e codificação binária para categóricos.<br/>
    • <b>Valores de K testados:</b> 3, 5 e 7.<br/>
    • <b>Divisão dos Dados:</b> 30 exemplos para treinamento e 15 para teste (mesma divisão do estudo anterior para comparabilidade).<br/>
    • <b>Base de Dados:</b> 45 registros contendo pH, Potássio, Drenagem, Compactação e a Classe (Apto/Não Apto)."""
    
    elements.append(Paragraph(metodologia_text, texto_style))
    elements.append(PageBreak())
    
    # RESULTADOS
    elements.append(Paragraph("3. RESULTADOS E DISCUSSÃO", subtitulo_style))
    
    # Tabela KNN
    elements.append(Paragraph("<b>Tabela 1 - Performance do KNN com diferentes valores de K</b>", texto_style))
    
    table1_data = [
        ['Valor de K', 'Acurácia', 'Acertos (de 15)', 'Observações'],
        ['K = 3', '100,00%', '15', 'Excelente estabilidade'],
        ['K = 5', '100,00%', '15', 'Excelente estabilidade'],
        ['K = 7', '100,00%', '15', 'Excelente estabilidade']
    ]
    
    table1 = Table(table1_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
    table1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table1)
    elements.append(Spacer(1, 20))
    
    # Comparativo
    elements.append(Paragraph("<b>Tabela 2 - Comparativo Perceptron vs KNN</b>", texto_style))
    
    table2_data = [
        ['Modelo', 'Melhor Acurácia', 'Características'],
        ['Perceptron', '97,78%', 'Modelo Linear, Rápido Treinamento'],
        ['KNN (K=3,5,7)', '100,00%', 'Não-Linear, Sem Treinamento (Lazy)']
    ]
    
    table2 = Table(table2_data, colWidths=[2*inch, 1.5*inch, 3*inch])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table2)
    elements.append(Spacer(1, 20))
    
    discussao_text = """<b>3.1 Análise dos Resultados</b><br/><br/>
    O algoritmo KNN demonstrou desempenho superior, atingindo 100% de acurácia em todas as configurações de K testadas. 
    Isso sugere que as classes são bem separadas no espaço vetorial multidimensional, mas também que a estrutura local 
    dos dados (vizinhança) é altamente preditiva.<br/><br/>
    
    Ao contrário do Perceptron, que busca um hiperplano separador global, o KNN toma decisões baseadas na similaridade local. 
    A robustez do KNN neste dataset indica que amostras com características de solo similares (pH, potássio, etc.) tendem 
    fortemente a ter a mesma classificação de aptidão, o que é consistente com a teoria agronômica."""
    
    elements.append(Paragraph(discussao_text, texto_style))
    elements.append(PageBreak())
    
    # CONCLUSÃO
    elements.append(Paragraph("4. CONCLUSÃO", subtitulo_style))
    
    conclusao_text = """A implementação do algoritmo KNN para a análise de solo de mandioca provou-se extremamente eficaz. 
    A variação de K (3, 5, 7) não alterou o resultado final de 100% de acurácia no conjunto de teste, demonstrando a 
    estabilidade do método para este problema específico.<br/><br/>
    
    Comparado ao Perceptron, o KNN mostrou-se ligeiramente superior em acurácia bruta. No entanto, ambos os modelos 
    são válidos para a tarefa. O KNN é recomendado quando se dispõe de poder computacional para armazenar e consultar 
    a base de dados em tempo real, enquanto o Perceptron é ideal para sistemas embarcados com memória limitada, 
    pois armazena apenas os pesos.<br/><br/>
    
    Este trabalho cumpre os requisitos da AT2, demonstrando a aplicação prática de técnicas de aprendizado de máquina 
    na agricultura de precisão."""
    
    elements.append(Paragraph(conclusao_text, texto_style))
    elements.append(Spacer(1, 30))
    
    # REFERÊNCIAS
    elements.append(Paragraph("REFERÊNCIAS", subtitulo_style))
    
    referencias_text = """COVER, T.; HART, P. Nearest neighbor pattern classification. <b>IEEE Transactions on Information Theory</b>, v. 13, n. 1, p. 21-27, 1967.<br/><br/>
    
    FIX, E.; HODGES, J. L. Discriminatory analysis: nonparametric discrimination: consistency properties. <b>USAF School of Aviation Medicine</b>, Randolph Field, TX, 1951.<br/><br/>
    
    COCK, J. H. <b>Cassava: new potential for a neglected crop.</b> Boulder: Westview Press, 1985."""
    
    elements.append(Paragraph(referencias_text, texto_style))
    
    # Gerar o PDF
    doc.build(elements)
    
    print("✅ Relatório PDF (KNN) gerado com sucesso!")
    print("📄 Arquivo: RELATORIO_KNN_MANDIOCA_ABNT.pdf")

if __name__ == "__main__":
    gerar_relatorio_pdf_reportlab()
