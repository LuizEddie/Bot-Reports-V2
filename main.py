import os
import json
import csv
from datetime import date
import time
from google_play_scraper import app, reviews, Sort
from urllib import request

class MainClass:

    appData = []
    header = ["Nome", "Nota", "Total de Avaliações", "Total de Comentários", "Desenvolvedor",
              "Versão Atual", "Lançamento", "Data Ultima Atualização", "Hospedagem", "Downloads Totais", "Comentários"]
    csv_data = []
    log_path = ""
    csv_path = ""
    playstore_path = "https://play.google.com/store/apps/details?id="

    def __init__(self):
        pass

    def read_json_data(self):
        json_path = open('Links.json', 'r', encoding="utf8")
        data = json.load(json_path)

        print("Dados Carregados")
        return data['links']

    def set_app_data(self, apps):
        count = 0
        self.appData = []
        for appl in apps:
            try:
                result = app(
                    appl['url'],
                    lang='pt',  # defaults to 'en'
                    country='br',  # defaults to 'us'
                )

                self.appData.append({'Nome': str(appl['name']),
                                     'Downloads Totais': str(result['installs']),
                                     'Nota': str(self.get_review_from_app(appl)),
                                     'Total de Avaliações': str(result['ratings']),
                                     'Total de Comentários': str(result['reviews']),
                                     'Desenvolvedor': str(result['developer']),
                                     'Versão Atual': str(result['version']),
                                     'Lançamento': str(result['released']),
                                     'Data Ultima Atualização' : str(self.get_last_update_app(appl)),
                                     'Hospedagem' :  str(self.get_host(result['developer'])),
                                     'Comentários' : self.get_comments(appl['url'])})

            except Exception as e:
                self.appData.append({'Nome': str(appl['name']),
                                     'Downloads Totais': "Offline",
                                     'Nota': "Offline",
                                     'Total de Avaliações': "Offline",
                                     'Total de Comentários': "Offline",
                                     'Desenvolvedor': "Offline",
                                     'Versão Atual': "Offline",
                                     'Lançamento': "Offline",
                                     'Data Ultima Atualização' : "Offline",
                                     'Hospedagem' :  "Offline",
                                     'Comentários' : "Offline"})

            count = count + 1

            print("Lendo... " + str((count / len(apps)) * 100) + "%")

    def get_last_update_app(self, url):
        try:
            html = str(request.urlopen(self.playstore_path + url['url']).read())
            tmpline = '<div class="BgcNfc">Updated</div><span class="htlgb"><div class="IQ1z0d"><span class="htlgb">'
            stringstart = html.find(tmpline)
            stringend = stringstart + len(tmpline)
            dateDirty = html[stringend:stringend+100]
            date = html[stringend:stringend+dateDirty.find('<')]
            return date
        except Exception as e:
            return "Offline"

    def get_review_from_app(self, url):
        try:
            html = str(request.urlopen(self.playstore_path + url['url']).read())
            tmpline = '<div class="BHMmbe"'
            stringstart = html.find(tmpline)
            stringend = stringstart + len(tmpline)
            review = html[stringend+48:stringend+51]
            return review
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

    def create_csv_file(self, app_name):
        self.csv_path = "log/" + str(date.today()) + " " + str(time.time()) + " " + app_name + ".csv"

        file = open(self.csv_path, "x", encoding="utf8")

        file.close()

    def write_csv_file(self):
        file = open(self.csv_path, "w", encoding="utf8", newline='')
        writer = csv.DictWriter(file, self.header)

        writer.writeheader()

        writer.writerows(self.appData)

        '''for appl in self.appData:
            self.csv_data.append([str(appl['Nome']),
                                  str(appl['Nota']),
                                  str(appl['Total de Avaliações']),
                                  str(appl['Total de Comentários']),
                                  str(appl['Desenvolvedor']),
                                  str(appl['Versão Atual']),
                                  str(appl['Lançamento']),
                                  str(appl['Data Ultima Atualização']),
                                  str(appl['Hospedagem']),
                                  str(appl['Downloads Totais'])])'''

        file.close()


    def write_log_file(self):
        file = open(self.log_path, "w", encoding="utf8")
        file.write(str(date.today()) + str(time.time()) + "\n")

        for appl in self.appData:
            file.write("\n")
            file.write("Nome: " + appl['Nome'] + "\n")
            file.write("Nota: " + appl['Nota'] + "\n")
            file.write("Total de Avaliações: " + appl['Total de Avaliações'] + "\n")
            file.write("Total de Comentários: " + appl['Total de Comentários'] + "\n")
            file.write("Desenvolvedor: " + appl['Desenvolvedor'] + "\n")
            file.write("Versão Atual: " + appl['Versão Atual'] + "\n")
            file.write("Lançamento: " + appl['Lançamento'] + "\n")
            file.write("Data Ultima Atualização: " + appl['Data Ultima Atualização'] + "\n")
            file.write("Hospedagem: " + appl['Hospedagem'] + "\n")
            file.write("Downloads Totais: " + appl['Downloads Totais'] + "\n")
            file.write("Comentários: \n\n" )
            try:
                for com in appl['Comentários']:
                    file.write("Comentário: " + str(com['Comentario']) + "\n")
                    file.write("Nota: " + str(com['Nota']) + "\n")
                    file.write("Data: " + str(com['Data']) + "\n")
            except Exception as e:
                file.write("Offline" + "\n")
            '''for com in appl['Comentários']:
                file.write("Comentário: " + str(com['Comentario']) + "\n")
                file.write("Nota: " + str(com['Nota']) + "\n")
                file.write("Data: " + str(com['Data']) + "\n")'''

            file.write("--------------------------------" + "\n")
        file.write("\n")
        file.write("END")
        file.close()

        #self.read_log_file()

    def read_log_file(self):
        os.system("cls||clear")
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
            os.system("cls||clear")
            print("Bem-Vindo! Escolha a opção desejada:\n")
            option = input("1 - Relatório todos os apps\n"
                           "2 - Relatório app específico\n"
                           "3 - Sair\n"
                           "Digite a opção: ")



            if option == "1":
                os.system("cls||clear")
                #self.create_log_file("all")
                self.set_app_data(self.read_json_data())
                self.get_data()
                self.save_data_menu("All")
            elif option == "2":
                os.system("cls||clear")
                self.show_app_menu()
            elif option == "3":
                os.system("cls||clear")
                print("Saindo...")
            else:
                os.system("cls||clear")
                print("Erro, escolha a opção correta")

            os.system("pause")

    def show_app_menu(self):
        apps = self.read_json_data()

        option = ""
        while option != "0":
            os.system("cls||clear")
            for count in range(len(apps)):
                print(str(count + 1) + " - " + apps[count]['name'])

            print("0 - Voltar")

            option = input("Digite o número o app que você deseja obter o relatório: ")

            if option == "0":
                os.system("cls||clear")
                print("Voltando")
            elif not option.isnumeric() or int(option) > len(apps) or int(option) < 0:
                os.system("cls||clear")
                print("Erro, escolha a opção correta")
                os.system("pause")
            else:
                os.system("cls||clear")
                app = [apps[(int(option) - 1)]]
                self.set_app_data(app)
                self.get_data()
                self.save_data_menu(app[0]['name'])
                #self.create_log_file(app[0]['name'])
                #self.set_app_data(app)
                os.system("pause")

    def save_data_menu(self, app_name):
        option = ""
        while(option != "1" and option != "2"):
            option = input("Você deseja salvar o log do relatório?\n"
                           "Digite o número correspondente a sua opção:\n"
                           "1 - Sim\n"
                           "2 - Não\n")

            if option == "1":
                self.create_log_file(app_name)
                self.create_csv_file(app_name)
                self.write_log_file()
                self.write_csv_file()
                print("Arquivo criado, acesse a pasta log/ para visualizá-lo\n")
                os.system("pause")
                os.system("cls||clear")
            elif option == "2":
                os.system("cls||clear")
                print("Voltando...")
            else:
                print("Erro, selecione a opção correta.\n\n")

    def get_data(self):
        for appl in self.appData:
            print("\n")
            print("Nome: " + str(appl['Nome']) + "\n")
            print("Nota: " + str(appl['Nota']) + "\n")
            print("Total de Avaliações: " + str(appl['Total de Avaliações']) + "\n")
            print("Total de Comentários: " + str(appl['Total de Comentários']) + "\n")
            print("Desenvolvedor: " + str(appl['Desenvolvedor']) + "\n")
            print("Versão Atual: " + str(appl['Versão Atual']) + "\n")
            print("Lançamento: " + str(appl['Lançamento']) + "\n")
            print("Data Ultima Atualização: " + str(appl['Data Ultima Atualização']) + "\n")
            print("Hospedagem: " + str(appl['Hospedagem']) + "\n")
            print("Downloads Totais: " + str(appl['Downloads Totais']) + "\n")
            print("Comentários: \n\n" )
            try:
                for com in appl['Comentários']:
                    print("Comentário: " + str(com['Comentario']) + "\n")
                    print("Nota: " + str(com['Nota']) + "\n")
                    print("Data: " + str(com['Data']) + "\n")
                    print("--------------------------------" + "\n")
            except Exception as e:
                print("Offline")
        print("\n")
        print("END")

try:
    mainClass = MainClass()
    mainClass.menu()

except Exception as e:
    print("Erro " + str(e))