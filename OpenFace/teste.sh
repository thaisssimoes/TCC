#!/bin/bash

cd ~/Documentos/TCC/"Reconhecimento facial"/openface/demos/;


counter=1
while [ $counter -le 52 ]
do
	echo "                               " 
	echo "*******Pasta $counter**********" 
	echo "                               " 
	echo "                               " >> ~/PycharmProjects/TCC/OpenFace/Resultados/Resultados-Pastas.docx
	echo "*******Pasta $counter**********" >> ~/PycharmProjects/TCC/OpenFace/Resultados/Resultados-Pastas.docx
	echo "                               " >> ~/PycharmProjects/TCC/OpenFace/Resultados/Resultados-Pastas.docx
 	./compare.py  ~/Imagens/"Reconhecimento Facial"/"Base de dados oclusão - Pastas"/1/{*.png,*.png} &>> ~/PycharmProjects/TCC/OpenFace/Resultados/Resultados-Pastas.docx
	((counter++))
done
echo All done




