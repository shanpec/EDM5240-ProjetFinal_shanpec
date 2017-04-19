#coding: utf-8

import csv
import requests
import html
from bs4 import BeautifulSoup

urltest="http://www.restomontreal.ca/s/?restaurants=Montreal&c=&f=&d=MONTREAL&sort=&limit=45&page=2"

fichier="2restos.csv"

#Comme on va fouiller dans un site internet, on laisse entetes comme signature, pour que le site sache qui c'est qui vient chercher des choses chez eux.
entetes={
    "User-Agent":"Bonjour ! Je m'appelle Shannon Pécourt et je fouille ici pour un cours de journalisme.",
    "From":"pecourt.shannon@courrier.uqam.ca",
    }

#Read local files in BeautifulSoup
    #contenu=requests.get(page1.html, headers=entetes)
    # faire une boucle qui lit chaque page
    #Voir le github Journalisme-UQAM, dans le travail de Carl Vaillancourt : script-Carlv91
    
fichier="restos.csv"

nom=[]
where=[]
arrondissement=[]
arrondissement2=[]
prix=[]
cuisine1=[]
cuisine2=[]
cuisine3=[]
cuisine4=[]
cuisine5=[]
cuisine6=[]
cuisine7=[]
telephone=[]

urlpr=[]

# for n in range(1,5):
#Cette ligne va chercher l'information dans le fichier voulu, selon le numéro.
# contenu1 = open("restomontreal1.html")
#Cette ligne va récupérer le code html de la page
# page1 = BeautifulSoup(contenu1,"html.parser")

#On aura besoin de 10 pages.
for n in range(1,11):
    url1="http://www.restomontreal.ca/s/?restaurants=Montreal&c=&f=&sort=&limit=500&page={}".format(n)
# url1="http://www.restomontreal.ca/s/?restaurants=Montreal&c=&f=&sort=&limit=1000&page=1"
    contenu1=requests.get(url1, headers=entetes)
    #Cette ligne va récupérer le code html de la page
    page1=BeautifulSoup(contenu1.text, "html.parser")
# print(page1)
    
    for carre in page1.find_all("div", id="div_restaurant"):
        #Avant toute chose, on s'occupe du cas où il y a plusieurs emplacements pour une chaîne de restaurants.
        #On caractérise alors cette situation-ci en cherchant la classe de la div unique dans laquelle se trouve toujours les termes "PLusoeurs emplacements"
        if carre.find("div", class_="coolFont") is not None:
            # print("YEAH RIGHT")
            #CAS OU IL Y A PLUSIEURS EMPLACEMENTS
            #On va aller dans l'url liée aux mots "Voir les ... adresses" pour trouver une page sembalble à la page de recherche.
            #À partir de là, on va lire les informations comme quand il n'y a qu'un emplacement
            poupeerusse=carre.find("a", class_="orange-outline-but")
            poupeerusse1=poupeerusse['href']
            urlpr.append(poupeerusse1)
            
            #MORCEAU DE CODE REMPLACÉ PAR LA LIGNE 65
            #Pour isoler l'url qui nous intéresse, comme le site est bien fait, on va split à 'href="' et '" title='
            # if poupeerusse is not None:
            #     poupeerusse1=str(poupeerusse).split('href="')
            #     poupeerusse2=poupeerusse1[1].split('" title=')
            #     #Les url qu'on a récupéré étaient en encodage uri (ou html), ce qui le lien erroné quand on voulait l'utiliser.
            #     #On a donc du importer le module html
            #     poupeerusse3=html.unescape(poupeerusse2[0])
            #     urlpr.append(poupeerusse3)
            #     # print(poupeerusse2[0])
            #     # print(poupeerusse3)
            # else:
            #     print("PROBLEME")
            #Maintenant, on a nos urlpr, c'est à dire qu'on a créé un cas à part pour les restaurants à Plusieurs emplacements.
            #Et c'est un cas dont nous allons nous occuper plus particulièrment et à part, après les cas normaux.
            #MORCEAU DE CODE REMPLACÉ PAR LA LIGNE 57
        
        else:
        #     print("1 seul emplacement")
        
            # CAS OU IL N'Y A PAS QU'UN EMPLACEMENT
        #Ici, c'est la partie où on extrait les données qui nous intéressent des pages de recherches. 
        #(Elle sera copiée telle quelle pour le traitement des restaurants à plusieurs emplacements en raison de la construction identique des pages concernées.)
        
            nomrest=carre.find("h2")
            nom.append(nomrest.text) 
            
            #On récolte les adresses des restaurants
            adresse=carre.find("span", class_="TextBlack12")
            # print(adresse.text)
            # Parfois, le restaurant n'a étrangement pas d'adresse. Dans ce cas, on va noter "adresse inconnue" à la place
            if adresse is None:
                where.append("Adresse inconnue du site")
            else:
                where.append(adresse.text)
            
            #On va récolter les arrondissements et les classer en 2 listes (futures colonnes) distinctes pour quand il y en a 2.
            arrond=carre.find("div", class_="TextDarkGreen12")
            # print(arrond.text)
            #Comme pour l'adresse ou le prix, l'arrondissement n'est pas toujours indiqué. On va prendre en compte cette éventualité.
            if arrond is None:
              arrondissement.append("Arrondissement inconnu du site")
            else:
                arrondi=arrond.text
                arrondis=arrondi.split(" / ")
                arrond1=arrondis[0]
                # print(arrondis)
                if len(arrondis)==1:
                    arrondissement.append(arrond1)
                    arrondissement2.append(None)
                elif len(arrondis)==2:
                    arrond2=arrondis[1]
                    arrondissement.append(arrond1)
                    arrondissement2.append(arrond2)
                    #La prochaine ligne est là en cas de problème, pour signaler dans quel
                else:
                    print("Ho-Oh--{}".format(len(arrondis)))
                # print(arrond)
            
            
            # On va alors trier les prix et le(s) type(s) de cuisine. Comme ils sont sur la même ligne, on va les récolter en même temps, puis les séparer pour s'en occuper.
            prixEtsorte=carre.find("div", class_="slickFont").text
            # print(prixEtsorte.text)
            #On sépare le prix et le type de cuisine dans une liste avec 2 éléments.
            pricetype=prixEtsorte.split("\xa0\xa0")
            # print(pricetype)
        
            #On s'aperçoit que restomontreal n'a parfois pas d'estimation de prix pour un restaurant.
            #Malgré cela, le prix va quand même se trouver dans le premier élément de pricetype, et si il n'y en a pas, l'élément prix sera un None.
            prixx=pricetype[0].strip()
            #On va compter le nombre d'unités de prix, soit de $, dans le prix pour pouvoir calculer des moyennes en unités de prix plus tard.
            #Lorsque qu'on se retrouve avec 2 gammes de prix; on va dire ajouter une demi-unité de prix au plus petit, soit 2,5 pour $$,$$$ par exemple.
            prix.append(prixx)
            # priix=[]
            # prix = []; prix.append("$"); prix.append("$$"); prix.append("$$"); prix.append("$,$$"); prix.append("$,$$");
            for i in range(0,len(prix)):
                    prix[i] = prix[i].replace("$$$,$$$$","3.5")
                    prix[i] = prix[i].replace("$$,$$$$","3.0") #Là, on avait $$,$$$$
                    prix[i] = prix[i].replace("$$,$$$","2.5")
                    prix[i] = prix[i].replace("$,$$$$","2.5") #Là, on avait $,$$$$
                    prix[i] = prix[i].replace("$,$$$","2.0") #Là, on avait $,$$$
                    prix[i] = prix[i].replace("$,$$","1.5")
                    prix[i] = prix[i].replace("$$$$","4")
                    prix[i] = prix[i].replace("$$$","3")
                    prix[i] = prix[i].replace("$$","2")
                    prix[i] = prix[i].replace("$","1")
            
            
            #Donc les différents éléments des cuisines vont se trouver dans le 2ème élément de pricetype.
            #On va avoir besoin de les séparer et de les mettre dans 7 listes pour pouvoir faciliter le traitement ultérieur des choses.
            #Parce que oui, selon restomontreal.ca, un même restaurant peut avoir jusqu'à 7 types de cuisines en même temps ! (-.-")
            cuisines=pricetype[1].split(", ")
            if len(cuisines)==1:
                cuisine1.append(cuisines[0])
                cuisine2.append(None)
                cuisine3.append(None)
                cuisine4.append(None)
                cuisine5.append(None)
                cuisine6.append(None)
                cuisine7.append(None)
            elif len(cuisines)==2:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(None)
                cuisine4.append(None)
                cuisine5.append(None)
                cuisine6.append(None)
                cuisine7.append(None)
            elif len(cuisines) == 3:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(cuisines[2])
                cuisine4.append(None)
                cuisine5.append(None)
                cuisine6.append(None)
                cuisine7.append(None)
            elif len(cuisines) == 4:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(cuisines[2])
                cuisine4.append(cuisines[3])
                cuisine5.append(None)
                cuisine6.append(None)
                cuisine7.append(None)
            elif len(cuisines) == 5:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(cuisines[2])
                cuisine4.append(cuisines[3])
                cuisine5.append(cuisines[4])
                cuisine6.append(None)
                cuisine7.append(None)
            elif len(cuisines) ==6:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(cuisines[2])
                cuisine4.append(cuisines[3])
                cuisine5.append(cuisines[4])
                cuisine6.append(cuisines[5])
                cuisine7.append(None)
            else:
                cuisine1.append(cuisines[0])
                cuisine2.append(cuisines[1])
                cuisine3.append(cuisines[2])
                cuisine4.append(cuisines[3])
                cuisine5.append(cuisines[4])
                cuisine6.append(cuisines[5])
                cuisine7.append(cuisines[6])
            # #Mon dieu c'est enfin fini, c'est pas trop tôt ! 
        
            # Le numéro de téléphone du restaurant n'est pas nécessairement utile à notre but, mais la même classe indique si le restaurant est fermé ou pas.
            tele=carre.find("div", class_="TextBlackBold12")
            telephone.append(tele.text)
    
    # print(cuisine)



# print(urlpr)

#Il est maintenant temps de s'occuper d'aller chercher les informations contenues dans les urlpr, soit les url des restaurants à plusieurs emplacements.
#On va traiter chacune de ces url comme si elle était une page de recherche.
for chose in urlpr:
    #Cette ligne va chercher l'information dans l'url voulue.
    contenupr=requests.get(chose, headers=entetes)
    #Cette ligne va récupérer le code html de la page
    pagepr=BeautifulSoup(contenupr.text, "html.parser")
    
    for carre in pagepr.find_all("div", id="div_restaurant"): 
        nomrest=carre.find("h2")
        nom.append(nomrest.text) 
        
        #On récolte les adresses des restaurants
        adresse=carre.find("span", class_="TextBlack12")
        # print(adresse.text)
        # Parfois, le restaurant n'a étrangement pas d'adresse. Dans ce cas, on va noter "adresse inconnue" à la place
        if adresse is None:
            where.append("Adresse inconnue du site")
        else:
            where.append(adresse.text)
        
        #On va récolter les arrondissements et les classer en 2 listes (futures colonnes) distinctes pour quand il y en a 2.
        arrond=carre.find("div", class_="TextDarkGreen12")
        # print(arrond.text)
        #Comme pour l'adresse ou le prix, l'arrondissement n'est pas toujours indiqué. On va prendre en compte cette éventualité.
        if arrond is None:
          arrondissement.append("Arrondissement inconnu du site")
        else:
            arrondi=arrond.text
            arrondis=arrondi.split(" / ")
            arrond1=arrondis[0]
            # print(arrondis)
            if len(arrondis)==1:
                arrondissement.append(arrond1)
                arrondissement2.append(None)
            elif len(arrondis)==2:
                arrond2=arrondis[1]
                arrondissement.append(arrond1)
                arrondissement2.append(arrond2)
                #La prochaine ligne est là en cas de problème, pour signaler dans quel
            else:
                print("Ho-Oh--{}".format(len(arrondis)))
            # print(arrond)
        
        
        # On va alors trier les prix et le(s) type(s) de cuisine. Comme ils sont sur la même ligne, on va les récolter en même temps, puis les séparer pour s'en occuper.
        prixEtsorte=carre.find("div", class_="slickFont").text
        # print(prixEtsorte.text)
        #On sépare le prix et le type de cuisine dans une liste avec 2 éléments.
        pricetype=prixEtsorte.split("\xa0\xa0")
        # print(pricetype)
    
        #On s'aperçoit que restomontreal n'a parfois pas d'estimation de prix pour un restaurant.
        #Malgré cela, le prix va quand même se trouver dans le premier élément de pricetype, et si il n'y en a pas, l'élément prix sera un None.
        prixx=pricetype[0].strip()
        #On va compter le nombre d'unités de prix, soit de $, dans le prix pour pouvoir calculer des moyennes en unités de prix plus tard.
        #Lorsque qu'on se retrouve avec 2 gammes de prix; on va dire ajouter une demi-unité de prix au plus petit, soit 2,5 pour $$,$$$ par exemple.
        prix.append(prixx)
        # priix=[]
        # prix = []; prix.append("$"); prix.append("$$"); prix.append("$$"); prix.append("$,$$"); prix.append("$,$$");
        for i in range(0,len(prix)):
                prix[i] = prix[i].replace("$$$,$$$$","3.5")
                prix[i] = prix[i].replace("$$,$$$$","3.0") #Là, on avait $$,$$$$
                prix[i] = prix[i].replace("$$,$$$","2.5")
                prix[i] = prix[i].replace("$,$$$$","2.5") #Là, on avait $,$$$$
                prix[i] = prix[i].replace("$,$$$","2.0") #Là, on avait $,$$$
                prix[i] = prix[i].replace("$,$$","1.5")
                prix[i] = prix[i].replace("$$$$","4")
                prix[i] = prix[i].replace("$$$","3")
                prix[i] = prix[i].replace("$$","2")
                prix[i] = prix[i].replace("$","1")
        
        
        #Donc les différents éléments des cuisines vont se trouver dans le 2ème élément de pricetype.
        #On va avoir besoin de les séparer et de les mettre dans 7 listes pour pouvoir faciliter le traitement ultérieur des choses.
        #Parce que oui, selon restomontreal.ca, un même restaurant peut avoir jusqu'à 7 types de cuisines en même temps ! (-.-")
        cuisines=pricetype[1].split(", ")
        if len(cuisines)==1:
            cuisine1.append(cuisines[0])
            cuisine2.append(None)
            cuisine3.append(None)
            cuisine4.append(None)
            cuisine5.append(None)
            cuisine6.append(None)
            cuisine7.append(None)
        elif len(cuisines)==2:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(None)
            cuisine4.append(None)
            cuisine5.append(None)
            cuisine6.append(None)
            cuisine7.append(None)
        elif len(cuisines) == 3:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(cuisines[2])
            cuisine4.append(None)
            cuisine5.append(None)
            cuisine6.append(None)
            cuisine7.append(None)
        elif len(cuisines) == 4:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(cuisines[2])
            cuisine4.append(cuisines[3])
            cuisine5.append(None)
            cuisine6.append(None)
            cuisine7.append(None)
        elif len(cuisines) == 5:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(cuisines[2])
            cuisine4.append(cuisines[3])
            cuisine5.append(cuisines[4])
            cuisine6.append(None)
            cuisine7.append(None)
        elif len(cuisines) ==6:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(cuisines[2])
            cuisine4.append(cuisines[3])
            cuisine5.append(cuisines[4])
            cuisine6.append(cuisines[5])
            cuisine7.append(None)
        else:
            cuisine1.append(cuisines[0])
            cuisine2.append(cuisines[1])
            cuisine3.append(cuisines[2])
            cuisine4.append(cuisines[3])
            cuisine5.append(cuisines[4])
            cuisine6.append(cuisines[5])
            cuisine7.append(cuisines[6])
        # #Mon dieu c'est enfin fini, c'est pas trop tôt ! 
        
        
    
        #Le numéro de téléphone du restaurant n'est pas nécessairement utile à notre but, mais la même classe indique si le restaurant est fermé ou pas.
        tele=carre.find("div", class_="TextBlackBold12")
        telephone.append(tele.text)

#On vérifie qu'il n'y a pas de trou/décalages dans les listes qui vont devenir les colonnes.     
# print(len(nom))
# print(len(where))
# print(len(arrondissement))
# print(len(arrondissement2))
# print(len(prix))
# print(len(telephone))
# print(len(cuisine1))
# print(len(cuisine2))
# print(len(cuisine3))
# print(len(cuisine4))
# print(len(cuisine5))
# print(len(cuisine6))
# print(len(cuisine7))
# print(prix)

    



# prix=$:[0-20]
# prix=$$:[20-30]
# prix=$$$:[30-45]
# prix=$$$$:[45-]

#Présentation du devoir à la fin ? Dans une page html ?




#METTRE NOS RESULTATS DANS LE CSV:
#Par restaurant, on commence par mettre toutes les informations le concernant dans une liste restaurant:
for i in range(1,len(nom)):
    restaurant=[]
    restaurant.append(nom[i])
    restaurant.append(where[i])
    restaurant.append(arrondissement[i])
    restaurant.append(arrondissement2[i])
    restaurant.append(telephone[i])
    restaurant.append(prix[i])
    restaurant.append(cuisine1[i])
    restaurant.append(cuisine2[i])
    restaurant.append(cuisine3[i])
    restaurant.append(cuisine4[i])
    restaurant.append(cuisine5[i])
    restaurant.append(cuisine6[i])
    restaurant.append(cuisine7[i])
    print(restaurant)

## Ensuite, on prend chaque liste comme étant une ligne, et on l'ajoute à restos.csv
## Inspiré du travail final de Carl Vaillancourt (https://github.com/Journalisme-UQAM/script-Carlv91/blob/master/jhr-corrige.py)
    dataresto = open(fichier,"a") 
    donneeraffinee = csv.writer(dataresto)
    donneeraffinee.writerow(restaurant)










#Attention ! les liens ne fonctionnent plus à partir de la 100ème page, soit du 1000ème item.
#La partie de code concernant Yelp est donc abandonnée
#YELP
#Les pages de Yelp sont plus fixes que celles de restomontreal, donc pas besoin de faire aussi compliqué. Mais elles ont l'air de changer un peu chaque jour
#Contrairement à restomontreal, on ne peut pas modifier le nombre de restos qui s'affichent par page.
#Comme la limite par page est de 10 et qu'il y a 5197 restos, il y aura 592 pages à analyser.
# for n in range(0,5920,10):
#     # print(n)
#     yurl="https://fr.yelp.ca/search?find_loc=Montreal,+QC&start={}&cflt=restaurants".format(n)
#     print(yurl)
    
    

# url2="https://www.yelp.ca/search?find_desc=Restaurants&find_loc=Montreal%2C+QC&ns=1"
# contenu2=requests.get(url2, headers=entetes)
# #Cette ligne va récupérer le code html de la page
# page2=BeautifulSoup(contenu2.text, "html.parser")

#for resto in page2.find_all("div", class_="biz-listing-large"):
    # tempynom=resto.find("a", class_="biz-name js-analytics-click")
    # ynom=tempynom.text.strip()
    # nom.append(ynom)
    
    # tempyadresse=resto.find("address")
    # yadresse=tempyadresse.text.strip()
    # where.append(yadresse)
    #L'écriture du résultat est un peu bizarre, mais elle reste compréhensible et passe dans Google Maps.
    
    # tempyarrond=resto.find("span", class_="neighborhood-str-list")
    # yarrond=tempyarrond.text.strip()
    # arrondissement.append(yarrond)
    
    #Parfois, les restos n'ont pas de gamme de prix dans Yelp, et ça retourne une erreur bloquante (None).
    #On va donc utiliser une sécurité pour écrire "Inconnu" dans ce cas. On utilise donc un if/else.
    # tempyprix=resto.find("span", class_="business-attribute price-range")
    # if tempyprix is None:
    #     prix.append("Inconnu")
    # else:
    #     yprix=tempyprix.text.strip()
    #     prix.append(yprix)
    
    #On dirait que ça donne des problèmes quand les restos ont plusieurs sortes
    #À retravailler ! Trouver un moyen de les classer dans plusieurs colonnes ?
#     tempysorte=resto.find("span", class_="category-str-list")
#     ysorte=tempysorte.text.strip()
#     ysortes=ysorte.split(",")
#     # print(ysortes)
#     cuisine1.append(ysortes[0])
#     if len(ysortes)==2:
#         cuisine2.append(ysortes[1].strip())
        
# print(cuisine1)
# print(cuisine2)
    