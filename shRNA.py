# -*- coding: utf-8 -*-

print('\nInstalando todas as bibliotecas relacionadas\n')
import os
import os.path
import zipfile
import pathlib
import shutil
import re
import time
from tkinter import filedialog
from tkinter import filedialog as dlg
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pyunpack import Archive
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import urllib.parse
import html5lib
import lxml
from lxml import etree
import csv
from Bio.Seq import Seq
from Bio.Seq import MutableSeq
from Bio import AlignIO
import Bio.Align.Applications
from Bio.Align import AlignInfo
from Bio.Align.Applications import MuscleCommandline

# tornando a janela do navegador oculta
options = webdriver.ChromeOptions()
options.add_argument("--headless")

# Selecionando a pasta Downloads do computador
print('\nSelecione a pasta de Downloads do seu computador\n')

downloads = filedialog.askdirectory()
downloads = str(downloads)

# Informando o ID do gene
print('\nDigite o ID do gene')
ID = input("ID: ")

# Identificando o gene a partir do ID
print('\nReconhecendo o gene...\n')
navegador = webdriver.Chrome(chrome_options=options)
navegador.get("https://www.ncbi.nlm.nih.gov/datasets/tables/genes/")
time.sleep(5)
gene = navegador.find_element_by_xpath('//*[@id="btn-get-started"]').click()
time.sleep(5)
gene = navegador.find_element_by_xpath('//*[@id="id-type-select"]/div[1]').click()
time.sleep(5)
gene = navegador.find_element_by_xpath('//*[@id="gene_id"]').click()
time.sleep(5)
gene = navegador.find_element_by_xpath('//*[@id="id-list-text"]')
time.sleep(5)
gene.send_keys(ID)
resultado = navegador.find_element_by_xpath('//*[@id="dlg-add-genes-button"]/div').click()
time.sleep(5)
resultado = navegador.page_source.encode('utf-8')
html = BeautifulSoup(resultado, 'html.parser')
time.sleep(5)
gene = html.find_all('td')[2].get_text()
NOME_DO_GENE = str(gene)
if gene == 'none':
    gene = 'Gene não identificado'
    print('\n' + gene)
else:
    print('\n GENE: ' + NOME_DO_GENE)

# Buscando a sequência
print('\n NCBI buscando as sequências dos transcritos...\n')
time.sleep(5)
navegador = webdriver.Chrome()
NCBI = 'https://www.ncbi.nlm.nih.gov/gene/' + ID
NCBI = str(NCBI)
time.sleep(5)
navegador.get(NCBI)
time.sleep(5)
transcritos = navegador.find_element_by_xpath(
    "//a[contains(text(),'Transcript table')]").click()  # busca mais precisa de uma palavra no botão!
time.sleep(5)
transcritos = navegador.find_element_by_xpath('//*[@id="data-table"]/div[1]/table/thead/tr/th[1]/div/input').click()
time.sleep(5)
download = navegador.find_element_by_xpath('//*[@id="button-open-download-menu"]/div').click()
time.sleep(5)
download = navegador.find_element_by_xpath('//*[@id="action-bar"]/div[2]/div/ul/li[2]/span[2]').click()
time.sleep(5)
download = navegador.find_element_by_xpath('//*[@id="protein-sequences"]').click()
time.sleep(5)
download = navegador.find_element_by_xpath('//*[@id="download-dataset-dialog--button"]/span').click()
time.sleep(10)
ncbi = downloads + '/' + 'ncbi_dataset.zip'
print(ncbi)
destino = os.path.dirname(os.path.abspath(__file__))
time.sleep(5)
shutil.move(ncbi, destino)
time.sleep(5)
pasta = zipfile.ZipFile('ncbi_dataset.zip', 'r')
time.sleep(5)
transcritos = pasta.read('ncbi_dataset/data/rna.fna')  # acessa o arquivo dos alinhamentos dentro da pasta zipada
with open('temp.fas', 'wb') as f:
    f.write(transcritos)
    f.close()
pasta.close()
os.remove('ncbi_dataset.zip')
muscle_cline = MuscleCommandline(r"muscle3.8.31_i86win32.exe", input=r'temp.fas',
                                 out=r'aln.fas')  # executa o alinhamento de sequências pelo MUSCLE
muscle_cline = str(muscle_cline)  # transforma a linha de comando em string
os.system(muscle_cline)  # cola a string no terminal e roda
aln = AlignIO.read('aln.fas', 'fasta')
aln = AlignInfo.SummaryInfo(aln)
consensus = aln.gap_consensus(threshold=1.0, ambiguous='X', require_multiple=0)
consensus = str(consensus)
print(consensus)
os.remove('temp.fas')  # exclui o arquivo
print('\n siDirect buscando a sequência a partir do número de acesso...\n')
time.sleep(5)
navegador = webdriver.Chrome(chrome_options=options)
navegador.get("http://sidirect2.rnai.jp/")
time.sleep(5)
seq = navegador.find_element_by_xpath('//*[@id="useq"]')
time.sleep(5)
seq = navegador.find_element_by_xpath('//*[@id="useq"]').clear()
time.sleep(5)
seq = navegador.find_element_by_xpath('//*[@id="useq"]')
time.sleep(5)
seq.send_keys(consensus)
time.sleep(10)

# Definindo os parâmetros das opções
print('\nDefinindo os parâmetros de busca no siDirect...\n')
click = navegador.find_element_by_xpath('/html/body/form/h3/font/a/img').click()
click = navegador.find_element_by_xpath('//*[@id="more1"]').click()
click = navegador.find_element_by_xpath('//*[@id="options"]/div[1]/table/tbody/tr/td[1]/p[2]/input').click()
click = navegador.find_element_by_xpath('//*[@id="functional_options"]/p[2]/input[3]').click()
click = navegador.find_element_by_xpath('//*[@id="nrdbSpe"]').click()
click = navegador.find_element_by_xpath('//*[@id="nrdbSpe"]/option[1]').click()
click = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[4]/input[1]').click()
GC_minimo = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[4]/input[2]').clear()
GC_minimo = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[4]/input[2]')
GC_minimo.send_keys('30')
GC_maximo = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[4]/input[3]').clear()
GC_maximo = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[4]/input[3]')
GC_maximo.send_keys('50')
click = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[5]/input[1]').click()
seq = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[5]/input[2]').clear()
seq = navegador.find_element_by_xpath('//*[@id="options"]/div[4]/p[5]/input[2]')
seq.send_keys('WWNNNNNNNNNNNNNNNNSNN')

# Gerando os siRNAs
time.sleep(5)
print('\nGerando lista de siRNA...\n')
click = navegador.find_element_by_xpath('/html/body/form/p[2]/input').click()
html = navegador.page_source.encode('utf-8')
with open('temp.html', 'wb') as file:
    file.write(html)
    file.close()
html = open('temp.html')
html = BeautifulSoup(html, 'html.parser')
html = html.find('table')
html = str(html)
seq = re.findall(">(\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w\w*)\n", html)
os.remove('temp.html')
alvo = []
for i in seq:
    i = str(i)
    i = MutableSeq(i)
    alvo.append(i)
    i = i.pop()
for i in alvo:
    i = i.pop()
loop = 'TTCAAGAGA'
cauda = 'TT'
seq_alvo = []
for i in alvo:
    i = str(i)
    seq_alvo.append(i)
for i in alvo:
    i = i.reverse_complement()
seq_senso = []
for i in seq_alvo:
    i = str(i)
    seq_senso.append(i)
seq_guia = []
for i in alvo:
    i = str(i)
    seq_guia.append(i)
alvo_loop = []
for i in seq_alvo:
    i = MutableSeq(i)
    i = i + loop
    i = str(i)
    alvo_loop.append(i)
guia_cauda = []
for i in seq_guia:
    i = MutableSeq(i)
    i = i + cauda
    i = str(i)
    guia_cauda.append(i)
shRNA = zip(alvo_loop, guia_cauda)
shRNA = list(shRNA)
RNAi = []
for i in shRNA:
    i = ''.join(i)
    RNAi.append(i)

# tm da seed
print('\nAnotando a Tm da sequência seed\n')
tm = re.findall("(..\d.\d*) Â", html)
TM = [tm[i:i + 2] for i in range(0, len(tm), 2)]
seed = []
for i in TM:
    del i[1]
    for j in i:
        seed.append(j)
tm = []
for i in seed:
    seed = []
    for j in i:
        j = j.replace('>', '')
        j = j.replace('"', '')
        seed.append(j)
    seed = ''.join(seed)
    tm.append(seed)
for i in tm:
    i = float(i)

print('\nCalculando o percentual de GC e contando os possíveis alvos da sequência senso\n')

alvos_senso = []
GC_SENSO = []
NUM_ALVOS_SENSO = []
for i in seq_senso:

    # Calculando o percentual de GC
    DNA_senso = Seq(i)
    GC_senso = (((DNA_senso.count("G")) + (DNA_senso.count("C"))) / len(DNA_senso)) * 100
    GC_SENSO.append(GC_senso)

    # contando os alvos do senso
    navegador = webdriver.Chrome(chrome_options=options)
    navegador.get("https://www.genscript.com/tools/sirna-target-finder")
    time.sleep(5)
    off = navegador.find_element_by_xpath('//*[@id="sequence"]')
    time.sleep(5)
    off.send_keys(i)
    time.sleep(5)
    click = navegador.find_element_by_xpath('//*[@id="mainContent2"]/div/div/form/div[11]/input[1]').click()
    time.sleep(5)
    html = navegador.page_source.encode('utf-8')
    html = BeautifulSoup(html, 'html.parser')
    html = etree.HTML(str(html))
    off = html.xpath('//*[@id="mainContent2"]/div/p[1]')[0].text
    off = str(off)
    off = off.split('ref|')
    del off[0]
    if off == []:
        none = 'none'
        NUM_ALVOS_SENSO.append(none)
        alvos_senso.append(none)
    else:
        target1 = []
        num_alvos_senso = []
        for i in off:
            i = list(i)
            offtarget = []
            for j in i:
                j = j.replace('|', '')
                j = j.replace(';', '')
                j = j.replace(' ', '')
                offtarget.append(j)
                alvossenso = ''.join(offtarget)
            num_alvos_senso.append(alvossenso)
            alvo = len(alvossenso)
            target1.append(alvo)
        Target1 = len(target1)
        alvos_senso.append(Target1)
        NUM_ALVOS_SENSO.append(num_alvos_senso)
        TOTAL_ALVOS_SENSO = []
        for i in NUM_ALVOS_SENSO:
            ALVOS_S = []
            for j in i:
                navegador = webdriver.Chrome(chrome_options=options)
                navegador.get("https://www.ncbi.nlm.nih.gov/nuccore/" + j)
                time.sleep(5)
                alvo = navegador.page_source.encode('utf-8')
                html = BeautifulSoup(alvo, 'html.parser')
                time.sleep(5)
                alvo = html.find_all('h1')[1]
                alvo = str(alvo)
                alvo = re.findall("<h1>(.*)</h1>", alvo)
                print(alvo)
                for k in alvo:
                    ALVOS_S.append(k)
            TOTAL_ALVOS_SENSO.append(ALVOS_S)
        print(TOTAL_ALVOS_SENSO)

alvos_guia = []
GC_GUIA = []
NUM_ALVOS_GUIA = []
for i in seq_guia:

    # Calculando o percentual de GC
    DNA_guia = Seq(i)
    GC_guia = (((DNA_guia.count("G")) + (DNA_guia.count("C"))) / len(DNA_guia)) * 100
    GC_GUIA.append(GC_guia)

    # Contando os alvos do guia
    navegador = webdriver.Chrome(chrome_options=options)
    navegador.get("https://www.genscript.com/tools/sirna-target-finder")
    time.sleep(5)
    off = navegador.find_element_by_xpath('//*[@id="sequence"]')
    time.sleep(5)
    off.send_keys(i)
    click = navegador.find_element_by_xpath('//*[@id="mainContent2"]/div/div/form/div[11]/input[1]').click()
    time.sleep(5)
    html = navegador.page_source.encode('utf-8')
    html = BeautifulSoup(html, 'html.parser')
    html = etree.HTML(str(html))
    off = html.xpath('//*[@id="mainContent2"]/div/p[1]')[0].text
    off = str(off)
    off = off.split('ref|')
    del off[0]
    if off == []:
        none = 'none'
        NUM_ALVOS_GUIA.append(none)
        alvos_guia.append(none)
    else:
        target2 = []
        num_alvos_guia = []
        for i in off:
            i = list(i)
            offtarget = []
            for j in i:
                j = j.replace('|', '')
                j = j.replace(';', '')
                j = j.replace(' ', '')
                offtarget.append(j)
                alvosguia = ''.join(offtarget)
            num_alvos_guia.append(alvosguia)
            alvo = len(alvosguia)
            target2.append(alvo)
        Target2 = len(target2)
        alvos_guia.append(Target2)
        NUM_ALVOS_GUIA.append(num_alvos_guia)
        TOTAL_ALVOS_GUIA = []
        for i in NUM_ALVOS_GUIA:
            ALVOS_G = []
            for j in i:
                navegador = webdriver.Chrome(chrome_options=options)
                navegador.get("https://www.ncbi.nlm.nih.gov/nuccore/" + j)
                time.sleep(5)
                alvo = navegador.page_source.encode('utf-8')
                html = BeautifulSoup(alvo, 'html.parser')
                time.sleep(5)
                alvo = html.find_all('h1')[1]
                alvo = str(alvo)
                alvo = re.findall("<h1>(.*)</h1>", alvo)
                for k in alvo:
                    ALVOS_G.append(k)
            TOTAL_ALVOS_GUIA.append(ALVOS_G)
        print(TOTAL_ALVOS_GUIA)

resultados = pd.DataFrame(list(
    zip(RNAi, seq_senso, GC_SENSO, guia_cauda, GC_GUIA, alvos_senso, TOTAL_ALVOS_SENSO, alvos_guia, TOTAL_ALVOS_GUIA)),
                          columns=['shRNA', 'Senso', 'GC', 'Guia', 'GC', 'Alvos em H. sapiens para a senso',
                                   'Descrição', 'Alvos em H. sapiens para a guia', 'Descrição'])
print(resultados)
resultados.to_csv('Resultado.csv')