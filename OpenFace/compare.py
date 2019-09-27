#!/usr/bin/env python
#encoding: utf-8

import time
start = time.time()
from datetime import datetime
import argparse
import cv2 #opencv
import os
import numpy as np
np.set_printoptions(precision=2) #precisão de pontos flutuantes
import openface

ENDERECO = "/home/thais/Imagens/Base/"

class ReconhecimentoFacial():
		
		
	def getRep(self, imgPath):
		bgrImg = cv2.imread(imgPath) #lê a imagem
		if bgrImg is None:
			raise Exception("Unable to load image: {}".format(imgPath))
		rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB) #muda esquema de cores

		start = time.time()
		bb = align.getLargestFaceBoundingBox(rgbImg)
		if bb is None:
			raise Exception("{}".format(imgPath)) #Unable to find a face

		start = time.time()
		"""
		Transform and align a face in an image.
	
		Parametros:
		-imgDim (int) – The edge length in pixels of the square the image is resized to.
		-rgbImg (numpy.ndarray) – RGB image to process. Shape: (height, width, 3)
		-bb (dlib.rectangle) – Bounding box around the face to align. Defaults to the largest face.
		-landmarks (list of (x,y) tuples) – Detected landmark locations. Landmarks found on bb if not provided.
		-landmarkIndices (list of ints) – The indices to transform to.
		-skipMulti (bool) – Skip image if more than one face detected.

		"""		
		alignedFace = align.align(args.imgDim, rgbImg, bb,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
		if alignedFace is None:
			raise Exception("Unable to align image: {}".format(imgPath))

		start = time.time()
		rep = net.forward(alignedFace)

		return rep


	def importarEnderecos(self, endereco):
		self.individuos = {}
		for root, dirs, files in os.walk(endereco):
			for name in files:
				arquivo = name.split('-')
				if arquivo[0] not in self.individuos.keys():
					self.imagens = list()
					self.imagens.append(endereco + "/" + name)
					self.individuos[arquivo[0]] = self.imagens
				else:
					self.individuos[arquivo[0]].append(endereco + "/" + name)
		return self.individuos

	def resultados(self, dicionario_imagens):
		for individuo_origem, lista_imagem_origem in dicionario_imagens.items():
			print(individuo_origem)
			for individuo_comparado, lista_imagem_comparada in dicionario_imagens.items():
				#for imagem_origem in lista_imagem_origem:
				for imagem_comparada  in range(0, len(lista_imagem_comparada)):
					tempoAntes = datetime.now()
					imagem_origem = ENDERECO + individuo_origem + "-1.png"
					imagem2 = False
					imagem1= False
					try:
						imagem_origem_aux = self.getRep(imagem_origem)
					except:
						imagem1 = True
					try:
						imagem_comparada_aux= self.getRep(dicionario_imagens[individuo_comparado][imagem_comparada])
					except:
						imagem2 = True

					tempoDepois = datetime.now()
					tempoReconhecimento = tempoDepois - tempoAntes

					if (imagem1 == True) or (imagem2 == True):
						if imagem1 and imagem2:
							resultado = "{};{};{};{};Problema nas duas imagens;{}".format(individuo_origem, "1", individuo_comparado, imagem_comparada,tempoReconhecimento)

						elif imagem1 and not imagem2:
							resultado = "{};{};{};{};Problema na imagem de origem;{}".format(individuo_origem, "1", individuo_comparado, imagem_comparada,tempoReconhecimento)

						elif imagem2 and not imagem1:
							resultado="{};{};{};{};Problema na imagem comparada;{}".format(individuo_origem, "1", individuo_comparado, imagem_comparada,tempoReconhecimento)

					else:
						d= imagem_origem_aux - imagem_comparada_aux
						if (np.dot(d, d) <= 0.60):
							resultado ="{};{};{};{};[True];{}".format(individuo_origem, "1", individuo_comparado, imagem_comparada,tempoReconhecimento)

						else:
							resultado = "{};{};{};{};[False];{}".format(individuo_origem,"1", individuo_comparado, imagem_comparada,tempoReconhecimento)

					self.exportarResultados(resultado)


	def exportarResultados(self, resultado):
		f= open('/home/thais/PycharmProjects/TCC/OpenFace/Resultados/resultados-openface-final.csv','a')
		f.write(resultado + "\n")
		f.close()





"""
Encaminhamento de pastas
"""
fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

"""
Recebimento/Encaminhamento de argumentos pela linha de comando
"""
parser = argparse.ArgumentParser()
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
		    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
		    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
		    help="Default image dimension.", default=96)
args = parser.parse_args()

"""
Inicialização de variáveis de modelo
"""
start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor) #Use dlib’s landmark estimation to align faces.

"""
Usa subprocesso do Torch para extração de características

Parametros:
model (str) – The path to the Torch model to use.
imgDim (int) – The edge length of the square input image.
"""
net = openface.TorchNeuralNet(args.networkModel, args.imgDim) 

	




"""
Chamada da classe
"""
reconhecerRostos = ReconhecimentoFacial()
tempoAntes = datetime.now()
print("Começou às: ", tempoAntes)
dicionario_imagens = reconhecerRostos.importarEnderecos(ENDERECO)
reconhecerRostos.resultados(dicionario_imagens)
tempoDepois = datetime.now()
print("Acabou às: ", tempoDepois)
print("Durou: ",tempoDepois - tempoAntes)
