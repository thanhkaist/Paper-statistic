import re
import operator
import unidecode
from bs4 import BeautifulSoup
import json, csv

import plotly.plotly as py
import plotly.graph_objs as go

datasetFolderName = "datasets/" 
fileName = datasetFolderName + "initial_accepted_papers_ICML19.txt"

titles_dataset = []
n_authors_per_paper = dict()
authors_dataset = dict()
institution_dataset = dict()


def fill_datasets(fileName):

	with open(fileName, 'r') as file:
		for paper in file:
			soup = BeautifulSoup(paper, features="html.parser")
			titles_dataset.append( soup.b.get_text() )
			list_authors = soup.i.get_text().split('· ')
			number_authors = len(list_authors )

			if number_authors not in n_authors_per_paper:
				n_authors_per_paper[number_authors] = 1
			else:
				n_authors_per_paper[number_authors] += 1


			tmp_institution_set = set()
			for i in range( number_authors ):

				author_afiliation = list_authors[i].split(" (")

				tmp_author = author_afiliation[0][0:]
				tmp_author = unidecode.unidecode(tmp_author)


				if tmp_author not in authors_dataset:
					authors_dataset[tmp_author] = 1
				else:
					authors_dataset[tmp_author] += 1

				tmp_institution = author_afiliation[1].rstrip(") ").rstrip(")").replace('"', '')

				# some authors have not updated their institution
				# if tmp_institution == '':
				# 	print(list_authors)

				# clearing some blank spaces at the end of each instituion, removing
				# accents and making strings case insensitive
				tmp_institution = tmp_institution.rstrip()
				tmp_institution = tmp_institution.lstrip()
				tmp_institution = unidecode.unidecode(tmp_institution).lower()
				tmp_institution_set.add(tmp_institution)

				# if  tmp_institution not in institution_dataset:
				# 	institution_dataset[tmp_institution] = 1
				# else:
				# 	institution_dataset[tmp_institution] += 1


			for i in tmp_institution_set:

				if  i not in institution_dataset:
					institution_dataset[i] = 1
				else:
					institution_dataset[i] += 1


def save_datasets_to_file():

	tmp = sorted(institution_dataset.items(), key=operator.itemgetter(1),reverse=True)
	with open(datasetFolderName+'institution_dataset.csv', 'w') as f:
		for key in tmp:
			f.write("%s;%s\n"%(key[0], key[1]))
	f.close()

	json1 = json.dumps(sorted(n_authors_per_paper.items(), key=operator.itemgetter(0)))
	json2 = json.dumps(sorted(authors_dataset.items(), key=operator.itemgetter(1),reverse=True))
	json3 = json.dumps(sorted(institution_dataset.items(), key=operator.itemgetter(1),reverse=True))

	f1 = open(datasetFolderName + "n_authors_per_paper.json","w")
	f2 = open(datasetFolderName + "authors_dataset.json","w")
	f3 = open(datasetFolderName + "institution_dataset.json","w")

	f1.write(json1)
	f2.write(json2)
	f3.write(json3)

	f1.close()
	f2.close()
	f3.close()

if __name__ == "__main__":
	fill_datasets(fileName)
	save_datasets_to_file()