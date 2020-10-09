import scrapy
import json
import re

global num
offerId = str()
adult = bool()
availability = description= str()
color = str()
imageLink = condition = isBundle =  ageGroup = gender = str()
additionalImageLinks = list()
googleProductCategory = title = link = str()
price = list()
batchId = merchantId = num = int(0)

class Product(scrapy.Item):
    
    
    batchId = scrapy.Field()
    merchantId = scrapy.Field(serializer=int)
    method = scrapy.Field()
    ageGroup = scrapy.Field()
    isBundle = scrapy.Field()
    adult = scrapy.Field()
    condition = scrapy.Field()
    googleProductCategory = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field(serializer=dict)
    product = scrapy.Field(serializer=dict)
    additionalImageLinks = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    offerId = scrapy.Field()
    imageLink = scrapy.Field()
    availability = scrapy.Field()
    color = scrapy.Field()
    gender = scrapy.Field()
    additionalImageLinks = scrapy.Field(serializer=list)





    

class BolsaDaChica(scrapy.Spider):
    name = "chica_api"
    custom_settings = {
        'STATS_DUMP': 'False',
    }
    start_urls = [
        'https://bolsadachica.com.br/produto/bau-bag/',
        'https://bolsadachica.com.br/produto/bolsa-bag/',
        'https://bolsadachica.com.br/produto/bolsa-carol/',
        'https://bolsadachica.com.br/produto/bolsa-cat/',
        'https://bolsadachica.com.br/produto/bolsa-tela/',
        'https://bolsadachica.com.br/produto/bolsa-livia/',
        'https://bolsadachica.com.br/produto/bolsa-lola/',
        'https://bolsadachica.com.br/produto/bolsa-lu/',
        'https://bolsadachica.com.br/produto/bolsa-mila/',
        'https://bolsadachica.com.br/produto/bolsa-geometrica/',
        'https://bolsadachica.com.br/produto/bolsa-colori/',
        'https://bolsadachica.com.br/produto/bolsa-red-dog/',
        'https://bolsadachica.com.br/produto/carteira-colored-stone/',
        'https://bolsadachica.com.br/produto/carteira-luna/',
        'https://bolsadachica.com.br/produto/bolsa-perola/',
        'https://bolsadachica.com.br/produto/mochila-liza/',
        'https://bolsadachica.com.br/produto/mochila-scoolbag/',
        'https://bolsadachica.com.br/produto/bolsa-small-cat/',
        'https://bolsadachica.com.br/produto/bolsa-cassia/',
        'https://bolsadachica.com.br/produto/bolsa-nadia/'

    ]
    
    global num
    
    
    def parse(self, response):
        print("\n" + response.url)
        
        num = int(0)
        num = self.crawler.stats.get_value('item_scraped_count')

        description = response.css("#tab-description p::text").get() + "\n" + response.css(".woocommerce-product-details__short-description p::text").get()

        produto_e_suas_variacoes = response.css("[id^='product-'] form").xpath('@data-product_variations').get()

        todas_imagens = response.css("#main img[src*='600']").xpath('@src').getall()
        

        price = response.css(".woocommerce-Price-amount.amount bdi::text").get()
        price = price.replace(",", ".")
        price = {
            'value': price,
            'currency': 'BRL'
            }
        



        
        Product2 = Product()
        
        if type(produto_e_suas_variacoes)== str:
            false = bool(0)
            true = bool(1)
            mydict = eval(produto_e_suas_variacoes)
            tamanho = int(0)
            colors = colorsB = list()
            i = cont = int(-1)
            tamanho = len(mydict)
            ima = bool(True)
            additionalImageLinks = list()
            additionalImageLinks.clear()
            batch = dict()
            nume = str()

            while cont < tamanho - 1:
                cont += 1
                colors.append(mydict[cont]["attributes"]["attribute_cor"])
            


            
            todas_imagensB = todas_imagens.copy()
            colorsB = colors.copy()

            
            print(todas_imagens)

            for ch in colors:
                #print(ch)

                

                for image in todas_imagens:
                    

                    
                    if ch.lower()[0:len(ch)-1] in image.lower():
                        
                        #print(ch.lower()[0:len(ch)-1] + " está em " + image.lower())
                        todas_imagensB.remove(image)

                        try:
                            
                            colorsB.remove(ch)

                        except:
                            pass
                            #print("A cor " + ch + " tem imagens correspondentes.")

                        #break
                    #else:
                        #print(ch.lower()[0:len(ch)-1] + " não está em " + image.lower())
                    

                

                        
            #print("imagens excluídas:")
            #print(todas_imagensB)
            
            while i < tamanho - 1:
                i += 1

                #id

                offerId = mydict[i]["variation_id"]
                batch['offerId'] = offerId

                #title

                title = response.css(".entry-title::text").get()
                batch['title'] = title

                #description

                description = limpa(description)
                batch['description'] = description

                #link

                link = response.url
                batch['link'] = link


                #imageLink 

                imageLink = mydict[i]["image"]["url"]
                batch['imageLink'] = imageLink
                

                #color

                color = mydict[i]["attributes"]["attribute_cor"]

                print("numero: " + str(i) + "\n")
                print(mydict[i]["attributes"])

 
                              
                batch['color'] = color

                
                #additionalImageLinks
                try:
                
                    if color == colorsB[0]:
                        #print(color + " é igual a " + colorsB[0] + "?")

                        additionalImageLinks = todas_imagensB.copy()

                    else:
                        additionalImageLinks.clear()
                                  
                        for image in todas_imagens:
                    
                                       
                            if color.lower()[0:len(color)-1] in image.lower():
                            #print("Estamos no loop de baixo: " + color.lower()[0:len(color)-1] + " está em " + image.lower())
                            
                            #try:
                            
                                additionalImageLinks.append(image)
                            
                            
                except:

                    additionalImageLinks = todas_imagensB.copy()
                            
                               

                                                                

                batch['additionalImageLinks'] =  additionalImageLinks
                

                #availability

                txt = mydict[i]["availability_html"]
                x = re.findall("[0-9]", txt)
                availability = str("0")
                
                for to in x:
                    availability += to

                if int(availability)>0:
                    batch['availability'] = "in stock"

                else:

                    batch['availability'] = "out of stock"
                

                #price

                batch['price'] = price
                

                #googleProductCategory

                if 'Carteira' in title:
                    googleProductCategory = "2668"

                elif 'Mochila' in title:
                    googleProductCategory = "100"

                else:
                    googleProductCategory = "3032"

                batch['googleProductCategory'] = googleProductCategory
      

                #condition

                condition = "new"

                batch['condition'] = condition


                #adult

                adult = bool(1)

                batch['adult'] = adult
                    

                #isBundle

                isBundle = "no"

                batch['isBundle'] = isBundle



                #ageGroup

                ageGroup = "adult"

                batch['ageGroup'] = ageGroup


         

                #gender

                gender = "female"

                batch['gender'] = gender
                
                

                #targetCountry
                
                batch['targetCountry'] = 'BR'


                # contentLanguage
                
                batch['contentLanguage'] = 'pt'


                #channel
                
                batch["channel"] = "online"

                

                #product

                Product2['product'] = batch
                

                #method

                Product2['method'] = 'insert'

                #batchId

                if i != 0:

                    if num == 0 or num == None:
                        nume = str("0") + str(i)

                    else:
                        nume = str(num) + str(i)

                    num = int(nume)

                Product2['batchId'] = num

                #merchantId
                
                Product2['merchantId'] = 227343072
                

                yield Product2
        


def limpa(a):
    conta_posi_letra = int(-1)
        
    string_limpa = a
        
    for b in a:
        conta_posi_letra += 1
    
 
        if b == "<":
            guarda_posi_inicial = conta_posi_letra
    
        elif b == ">":
            guarda_posi_final = conta_posi_letra  
  
            substring_original = a[int(guarda_posi_inicial): int(guarda_posi_final) + 1]
         
            substring = substring_original.split(" ")
   
            if len(substring) > 1:
                string_limpa_inicial = substring[0] + ">"
      
    
                string_limpa = a.replace(substring_original, string_limpa_inicial)
    

    return string_limpa
