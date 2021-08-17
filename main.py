import os
import json
from datetime import date
import time
from google_play_scraper import app, reviews, Sort
import urllib

class MainClass:

    appData = []
    log_path = ""
    playstore_path = "https://play.google.com/store/apps/details?id="

    def __init__(self):
        pass

    def read_json_data(self):
        json_path = open('Links.json', 'r', encoding="utf8")
        data = json.load(json_path)

        print("Dados Carregados")
        #links = data['links']
        return data['links']
        #self.get_app_data(links)

    def get_app_data(self, apps):
        count = 0
        self.appData = []
        for appl in apps:
            try:
                result = app(
                    appl['url'],
                    lang='pt',  # defaults to 'en'
                    country='br',  # defaults to 'us'
                )

                self.appData.append({'Nome': appl['name'],
                                     'Downloads Totais': result['installs'],
                                     'Nota': result['score'],
                                     'Total de Avaliações': result['ratings'],
                                     'Total de Comentários': result['reviews'],
                                     'Desenvolvedor': result['developer'],
                                     'Versão Atual': result['version'],
                                     'Lançamento': result['released'],
                                     'Data Ultima Atualização' : self.get_last_update_app(appl),
                                     'Hospedagem' :  self.get_host(result['developer']),
                                     'Comentários' : self.get_comments(appl['url'])})

            except Exception as e:
                self.appData.append({"Nome": appl['name'],
                                    "Status": "Offline"})

            count = count + 1

            print("Lendo... " + str((count / len(apps)) * 100) + "%")

        self.write_log_file()


    def get_last_update_app(self, url):
        try:
            html = str(urllib.request.urlopen(self.playstore_path + url['url']).read())
            tmpline = '<div class="BgcNfc">Updated</div><span class="htlgb"><div class="IQ1z0d"><span class="htlgb">'
            stringstart = html.find(tmpline)
            stringend = stringstart + len(tmpline)
            dateDirty = html[stringend:stringend+100]
            date = html[stringend:stringend+dateDirty.find('<')]
            return date
        except Exception as e:
            return "Offline"


    def get_host(self, dev):
        if dev == "Multilaser Mobile" or dev == "Giga Security":
            return "Brasil"
        else:
            return "China"

    def create_log_file(self, app_name):
        self.log_path = "log/" + str(date.today()) + " " + str(time.time()) + " " + app_name +".txt"

        file = open(self.log_path, "x", encoding="utf8")

        file.close()

        #self.read_json_data()

    def write_log_file(self):
        file = open(self.log_path, "w", encoding="utf8")
        file.write(str(date.today()) + str(time.time()) + "\n")

        for appl in self.appData:
            file.write("\n")
            file.write("Nome: " + str(appl['Nome']) + "\n")
            file.write("Nota: " + str(appl['Nota']) + "\n")
            file.write("Total de Avaliações: " + str(appl['Total de Avaliações']) + "\n")
            file.write("Total de Comentários: " + str(appl['Total de Comentários']) + "\n")
            file.write("Desenvolvedor: " + str(appl['Desenvolvedor']) + "\n")
            file.write("Versão Atual: " + str(appl['Versão Atual']) + "\n")
            file.write("Lançamento: " + str(appl['Lançamento']) + "\n")
            file.write("Data Ultima Atualização: " + str(appl['Data Ultima Atualização']) + "\n")
            file.write("Hospedagem: " + str(appl['Hospedagem']) + "\n")
            file.write("Downloads Totais: " + str(appl['Downloads Totais']) + "\n")
            file.write("Comentários: \n\n" )
            for com in appl['Comentários']:
                file.write("Comentário: " + str(com['Comentario']) + "\n")
                file.write("Nota: " + str(com['Nota']) + "\n")
                file.write("Data: " + str(com['Data']) + "\n")
                file.write("--------------------------------" + "\n")
        file.write("\n")
        file.write("END")
        file.close()

        self.read_log_file()

    def read_log_file(self):

        file = open(self.log_path, "r", encoding="utf8")
        print(file.read())
        file.close()

    def get_comments(self, link):
            try:
                results, continuation_token = reviews(
                    link,
                    lang='pt',  # defaults to 'en'
                    country='br',  # defaults to 'us'
                    sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
                    count=10,  # defaults to 100
                    filter_score_with=None  # defaults to None(means all score)
                )

                resultList = []

                for result in results:
                    resultList.append({'Comentario': result['content'],
                                       'Nota': result['score'],
                                       'Data': result['at']})

                return resultList

            except Exception as e:
                return "Offline"

    def menu(self):

        option = ""

        while option != "3":
            print("Bem-Vindo! Escolha a opção desejada:\n")
            option = input("1 - Relatório todos os apps\n"
                           "2 - Relatório app específico\n"
                           "3 - Sair\n"
                           "Digite a opção: ")



            if option == "1":
                self.create_log_file("all")
                self.get_app_data(self.read_json_data())
                os.system("pause")
            elif option == "2":
                #print("Em desenvolvimento")
                self.show_app_menu()

            elif option == "3":
                print("Saindo")

            else:
                print("Erro, escolha a opção correta")

    def show_app_menu(self):
        apps = self.read_json_data()

        option = ""
        while option != "0":
            for count in range(len(apps)):
                print(str(count + 1) + " - " + apps[count]['name'])

            print("0 - Voltar")

            option = input("Digite o número o app que você deseja obter o relatório: ")

            if option == "0":

                print("Voltando")
            elif int(option) > len(apps) or int(option) < 0:

                print("Erro, escolha a opção correta")
            else:
                app = [apps[(int(option) - 1)]]
                self.create_log_file(app[0]['name'])
                self.get_app_data(app)
                os.system("pause")

try:
    mainClass = MainClass()

    '''mainClass.create_log_file()'''
    '''mainClass.read_json_data()'''
    mainClass.menu()

    os.system("pause")

except Exception as e:
    print("Erro " + str(e))