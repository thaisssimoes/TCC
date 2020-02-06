import os
import face_recognition
from datetime import datetime

QUANTIDADE_TOTAL_FOTOS = 120
QUANTIDADE_TOTAL_INDIVIDUOS =22
class ReconhecimentoFacial():
    def importarEnderecoImagens(self, endereco):
        self.individuos = {}
        for root, dirs, files in os.walk(endereco):
            for name in files:
                arquivo = name.split('-')
                if arquivo[0] not in self.individuos.keys():
                    self.imagens = list()
                    self.imagens.append(endereco +  name)
                    self.individuos[arquivo[0]] = self.imagens
                else:
                    self.individuos[arquivo[0]].append(endereco + name)
        return self.individuos

    def compararTodos(self, endereco, dicionario_imagens):

        for individuo_origem, lista_imagem_origem in dicionario_imagens.items():
                lista_imagem_origem.sort()
                print(individuo_origem)
                for individuo_comparado, lista_imagem_comparada in dicionario_imagens.items():
                    lista_imagem_comparada.sort()
                    #for imagem_origem in lista_imagem_origem:
                    for imagem_comparada in range(0, len(lista_imagem_comparada)):
                        tempoAntes = datetime.now()
                        imagem_origem = endereco+"/"+individuo_origem + "-1.png"
                        known_image = face_recognition.load_image_file(imagem_origem)
                        unknown_image = face_recognition.load_image_file(dicionario_imagens[individuo_comparado][imagem_comparada])
                        self.results = self.verificarResultado(face_recognition.face_encodings(known_image),
                                                                   face_recognition.face_encodings(unknown_image))
                        tempoDepois = datetime.now()
                        tempoReconhecimento= tempoDepois - tempoAntes
                        self.exportarResultado(individuo_origem, imagem_origem, individuo_comparado, dicionario_imagens[individuo_comparado][imagem_comparada], self.results, tempoReconhecimento)

    def verificarResultado(self, rosto_conhecido, rosto_desconhecido):
        if len(rosto_desconhecido) == 0 and len(rosto_conhecido) == 0:
            self.results = "Problema nas duas imagens"
        elif len(rosto_desconhecido) == 0:
            self.results = "Problema na imagem comparada."
        elif len(rosto_conhecido) == 0:
            self.results = "Problema na imagem de origem."
        else:
            known_encoding = rosto_conhecido[0]
            unknown_encoding = rosto_desconhecido[0]
            self.results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        return self.results

    def exportarResultado(self, individuo_origem, imagem_origem, individuo_comparado, imagem_comparada, resultados, tempoReconhcimento):
        f = open("resultado-face_recognition-2.csv", "a")
        f.write(individuo_origem + ";" + imagem_origem + ";"+ individuo_comparado +";"+ imagem_comparada + ";" + str(resultados) +  ";" + str(tempoReconhcimento) + "\n")
        f.close()

endereco_imagens = '/home/thais/Imagens/Base'

reconhecerRostos = ReconhecimentoFacial()

tempoAntes = datetime.now()
print("Começou às: ", tempoAntes)
dicionario_imagens = reconhecerRostos.importarEnderecoImagens(endereco_imagens)

reconhecerRostos.compararTodos(endereco_imagens, dicionario_imagens)

tempoDepois = datetime.now()
print("Acabou às: ", tempoDepois)
print("Durou: ",tempoDepois - tempoAntes)
