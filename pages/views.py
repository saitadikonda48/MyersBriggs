from django.shortcuts import render

from .forms import TextInputField, TwitterHandleField

from bs4 import BeautifulSoup
import urllib.request
import certifi
import pymongo


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.pymongo
inty = db.introversion
postos = db.posts

# Create your views here.
def home_view(request, *args, **kwargs):	# *args, **kwargs
	textInputField = TextInputField(request.POST or None)
	twitterHandleField = TwitterHandleField(request.POST or None)

	# extraversionField = ExtraversionField(request.POST or None)
	# intuitionField = IntuitionField(request.POST or None)
	# feelingField = FeelingField(request.POST or None)
	# perceptionField = PerceptionField(request.POST or None)
	# myersBriggsTypesField = MyersBriggsTypesField(request.POST or None)

	twitter_search = False

	if request.method == "POST":
		if textInputField.is_valid():
			username_data = textInputField.cleaned_data.get('username')
			text_field_data = textInputField.cleaned_data.get('text_field')
			extraversion_data = textInputField.cleaned_data.get('extraversion_field')
			intuition_data = textInputField.cleaned_data.get('intuition_field')
			feeling_data = textInputField.cleaned_data.get('feeling_field')
			perception_data = textInputField.cleaned_data.get('perception_field')
			

			obj = {
				'username': username_data,
				'T/F': feeling_data[0],
				'N/S': intuition_data[0],
				'P/J': perception_data[0],
				'E/I': extraversion_data[0],
			}
			found = postos.find_one({'username': username_data})
			if (found is None):
				obj['posts'] = [text_field_data]
				obj['variance'] = 0
				obj['stdDev'] = 0
				obj['average'] = len(text_field_data.split(' '))
				obj['avgWordLength'] = (len(text_field_data)-obj['average'])/obj['average']
				postos.insert_one(obj)
			else:
				found['posts'].append(text_field_data)
				obj['posts'] = found['posts']
				hello = len(text_field_data.split(' '))
				totalPosts = len(found['posts'])
				obj['average'] = (found['average']*totalPosts+hello)/totalPosts+1
				obj['stdDev'] = (found['stdDev'] + (hello-obj['average']) * (hello-obj['average'])) /(totalPosts+1)
				avgWordLength = (len(text_field_data)-obj['average'])/obj['average']
				obj['avgWordLength'] = (avgWordLength + found['avgWordLength']*totalPosts)/totalPosts
				obj['variance'] = obj['stdDev'] * obj['stdDev']
				postos.replace_one({'username': username_data}, obj)
			
			if text_field_data:
				twitter_search = False
				context = {
					"username_data":username_data,
					"text_field_data":text_field_data,
					"extraversion_data":extraversion_data,
					"intuition_data":intuition_data,
					"feeling_data":feeling_data,
					"perception_data":perception_data,
				}
				return render(request, "results.html", context)
			else:
				pass

		"""
		Currently the user can type in values into the boxes and 
		"""

	context = {
		"textInputField":textInputField,
		"twitterHandleField":twitterHandleField,
		# "myersBriggsTypesField":myersBriggsTypesField,
		# "extraversionField":extraversionField,
		# "intuitionField":intuitionField,
		# "feelingField":feelingField,
		# "perceptionField":perceptionField,

		"twitter_search":twitter_search,

	}
	return render(request, "home_view.html", context)


def table_view(request, *args, **kwargs):	# *args, **kwargs
	firstArr = ['1','2','3']
	e = postos.count({"E/I":"E"})
	ii = postos.count({"E/I":"I"})
	f = postos.count({"T/F":"T"})
	t = postos.count({"T/F":"F"})
	n = postos.count({"N/S": "N"})
	s = postos.count({"N/S": "S"})
	p = postos.count({"P/J": "J"})
	j = postos.count({"P/J": "P"})

	e1 = inty.find_one({'_id': 'E'})
	i1 = inty.find_one({'_id': 'I'})
	n1 = inty.find_one({'_id': 'N'})
	s1 = inty.find_one({'_id': 'S'})
	t1 = inty.find_one({'_id': 'T'})
	f1 = inty.find_one({'_id': 'F'})
	p1 = inty.find_one({'_id': 'P'})
	j1 = inty.find_one({'_id': 'J'})
	del e1['_id']
	del i1['_id']
	del s1['_id']
	del n1['_id']
	del t1['_id']
	del f1['_id']
	del p1['_id']
	del j1['_id']

	arrE = {}
	arrI = {}
	arrT = {}
	arrF = {}
	arrJ = {}
	arrP = {}
	arrN = {}
	arrS = {}

	for i in e1:
		if e1[i] > e/5:
			arrE[i] = e1[i]
	for i in i1:
		if i1[i] > ii/5:
			if i in arrE and (arrE[i] * ii/e) < i1[i]:
				del arrE[i]
			else:
				if i in arrE:
					arrI[i] = i1[i] * e / ii - arrE[i]
				else:
					arrI[i] = i1[i] * e / ii
	for i in arrE:
		if i in arrI:
			arrE[i] = arrE[i] * ii / e - i1[i]
		else:
			arrE[i] = arrE[i] * ii / e



	for i in t1:
		if t1[i] > t/10:
			arrT[i] = t1[i]
	for i in f1:
		if f1[i] > f/10:
			if i in arrT and (arrT[i] *f/t) < f1[i]:
				del arrT[i]
			else:
				if i in arrT:
					arrF[i] = f1[i] * t/f - arrT[i]
				else:
					arrF[i] = f1[i] * t/f
	for i in arrT:
		if i in arrF:
			arrT[i] = arrT[i] * f/t - f1[i]
		else:
			arrT[i] = arrT[i] * f/t

	for i in j1:
		if j1[i] > j/12:
			arrJ[i] = j1[i]
	for i in p1:
		if p1[i] > p/5:
			if i in arrJ and (arrJ[i]*p/j) < p1[i]:
				del arrJ[i]
			else:
				if i in arrJ:
					arrP[i] = p1[i] * j / p - arrJ[i]
				else:
					arrP[i] = p1[i] * j / p
	for i in arrJ:
		if i in arrP:
			arrJ[i] = arrJ[i] * p / j - p1[i]
		else:
			arrJ[i] = arrJ[i] * p / j

	for i in n1:
		if n1[i] > n/10:
			arrN[i] = n1[i]
	for i in s1:
		if s1[i] > s/10:
			if i in arrN and (arrN[i] * s/ n) < s1[i]:
				del arrN[i]
			else:
				if i in arrN:
					arrS[i] = s1[i] * n /s - arrN[i]
				else:
					arrS[i] = s1[i] * n/s
	for i in arrN:
		if i in arrS:
			arrN[i] = arrN[i] * s / n - s1[i]
		else:
			arrN[i] = arrN[i] * s / n

	arrE = sorted(arrE.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrI = sorted(arrI.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrN = sorted(arrN.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrS = sorted(arrS.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrT = sorted(arrT.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrF = sorted(arrF.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrP = sorted(arrP.items(), key=lambda x: x[1])[-21:-1][::-1]
	arrJ = sorted(arrJ.items(), key=lambda x: x[1])[-21:-1][::-1]
	context = {}
	context['arrE'] = arrE
	context['arrI'] = arrI
	context['arrJ'] = arrJ
	context['arrP'] = arrP
	context['arrF'] = arrF
	context['arrT'] = arrT
	context['arrN'] = arrN
	context['arrS'] = arrS
	
	return render(request, "table_view.html", context)