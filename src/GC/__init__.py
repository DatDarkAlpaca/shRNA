def fetch_gc_senso(senso_sequences: list):
    results = []

    for senso in senso_sequences:
        results.append(((senso.count('G')) + (senso.count('C'))) / len(senso) * 100)

    return results


def fetch_gc_guide(senso_guides: list):
    results = []

    for senso in senso_guides:
        results.append((senso.count('G') + senso.count('C')) / len(senso) * 100)

    return results


def fetch_target_senso(senso_sequences):
    results = []

    for sequence in senso_sequences:
        pass


'''
    alvos_senso = []
    NUM_ALVOS_SENSO = []

    for i in seq_senso:

        navegador = webdriver.Chrome(chrome_options=options)
        navegador.get("https://www.genscript.com/tools/sirna-target-finder")

        off = navegador.find_element_by_xpath('//*[@id="sequence"]')

        off.send_keys(i)

        click = navegador.find_element_by_xpath('//*[@id="mainContent2"]/div/div/form/div[11]/input[1]').click()

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

            # Total:
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


def total_senso_target():
    pass
'''