import os
import face_recognition
from datetime import datetime

QUANTIDADE_TOTAL_FOTOS = 541

class TesteFacial():
    def importarImagens(self, endereco):

        self.imagens = list()
        self.directory = {}
        for root, dirs, files in os.walk(endereco, topdown=False):
            for name in dirs:
                self.imagens = os.listdir(endereco + "/" + name)
                self.directory[name] = self.imagens
        return self.directory

    def compararPasta(self, endereco, imagens):
       for pasta, lista_imagem in imagens.items():
           for item in lista_imagem:
               for i in range(len(lista_imagem)):
                   known_image = face_recognition.load_image_file(endereco + pasta + "/" + item)
                   unknown_image = face_recognition.load_image_file(endereco + pasta + "/" + lista_imagem[i])
                   self.results = self.verificarResultado(face_recognition.face_encodings(known_image),
                                                          face_recognition.face_encodings(unknown_image))

                   self.exportarResultado(pasta, item, lista_imagem[i], self.results)

    def compararGrupo(self, endereco_pastas, endereco_grupo, imagens):
        for pasta, lista_imagem in imagens.items():
            for item in lista_imagem:
                for i in range(1, QUANTIDADE_TOTAL_FOTOS + 1):
                    known_image = face_recognition.load_image_file(endereco_pastas + pasta + "/" + item)
                    unknown_image = face_recognition.load_image_file(endereco_grupo + str(i) + ".png")
                    self.results = self.verificarResultado(face_recognition.face_encodings(known_image),
                                                           face_recognition.face_encodings(unknown_image))

                    self.exportarResultado(pasta, item, str(i) + ".png", self.results)
                    #print("Imagem origem"+item+"Imagem comparada:"+ str(i) + ".png")
    #mudar o nome de item=imagem_origem e lista_imagem=imagem_comparada
    def exportarResultado(self, pasta, item, lista_imagem, results):
        f = open("resultado-face_recognition-pastas.csv", "a")
        f.write(pasta+";"+item+";"+lista_imagem+";"+str(results)+"\n")
        f.close()


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

endereco_pastas = '/home/thais/Imagens/Reconhecimento Facial/Base de dados oclusão - Pastas/'
endereco_grupo = '/home/thais/Imagens/Reconhecimento Facial/Base de dados oclusão - Geral/'

teste = TesteFacial()
dicionario_imagens = teste.importarImagens(endereco_pastas)
print(datetime.now())
teste.compararPasta(endereco_pastas,dicionario_imagens)
print(datetime.now())
