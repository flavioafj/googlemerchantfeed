import scrapy
import json
import re


identificacao = str()
availability = description= str()
color = str()
image_link = condition = adult = is_bundle =  age_group = gender = str()
additional_image_link = list()
google_product_category = title = price = link = str()

class Product(scrapy.Item):
    
    age_group = scrapy.Field()
    is_bundle = scrapy.Field()
    adult = scrapy.Field()
    condition = scrapy.Field()
    google_product_category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    additional_image_link = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    identificacao = scrapy.Field()
    image_link = scrapy.Field()
    availability = scrapy.Field()
    color = scrapy.Field()
    gender = scrapy.Field()
    additional_image_link = scrapy.Field(serializer=list)



from scrapy.exporters import XmlItemExporter

class ProductXmlExporter(XmlItemExporter):

    def serialize_field(self, field, name, value):
        if field == 'additional_image_link':

            for cada in value:
            
            
                return 'R$ %s' % str(cada)
            return super(Product, self).serialize_field(field, name, cada)

    

class BolsaDaChica(scrapy.Spider):
    name = "chica"
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
        'https://bolsadachica.com.br/produto/bolsa-small-cat/'

    ]

    def parse(self, response):
        print("\n" + response.url)

        description = response.css("#tab-description").get() + "\n" + response.css(".woocommerce-product-details__short-description").get()

        produto_e_suas_variacoes = response.css("[id^='product-'] form").xpath('@data-product_variations').get()

        todas_imagens = response.css("#main img[src*='600']").xpath('@src').getall()
        

        price = response.css(".woocommerce-Price-amount.amount::text").get()
        price = price.replace(",", ".")
        price = price + " BRL"



        
        product = Product()
        
        if type(produto_e_suas_variacoes)== str:
            false = bool(0)
            true = bool(1)
            mydict = eval(produto_e_suas_variacoes)
            tamanho = int(0)
            i = int(-1)
            tamanho = len(mydict)
            ima = bool(True)
            additional_image_link = list()

            
            while i < tamanho - 1:
                i += 1

                #id

                identificacao = mydict[i]["variation_id"]
                product['identificacao'] = identificacao

                #title

                title = response.css(".entry-title::text").get()
                product['title'] = title

                #description

                description = limpa(description)
                product['description'] = description

                #link

                link = response.url
                product['link'] = link


                #image_link 

                image_link = mydict[i]["image"]["url"]
                product['image_link'] = image_link
                

                #additional_image_link

                color = mydict[i]["attributes"]["attribute_cor"]
                
                for image in todas_imagens:
                    
                                       
                    if color in image:
                            
                        try:
                            
                            additional_image_link.append(image)
                            
                            
                        except:
                            
                            additional_image_link.append(" ")
                                                                  

                    product['additional_image_link'] =  additional_image_link
                

                #availability

                txt = mydict[i]["availability_html"]
                x = re.findall("[0-9]", txt)
                availability = str("0")
                for to in x:
	                availability += to
 
                product['availability'] = availability
                

                #price

                product['price'] = price
                

                #google_product_category

                if 'Carteira' in title:
                    google_product_category = "2668"

                elif 'Mochila' in title:
                    google_product_category = "100"

                else:
                    google_product_category = "3032"

                product['google_product_category'] = google_product_category
      

                #condition

                condition = "new"

                product['condition'] = condition


                #adult

                adult = "yes"

                product['adult'] = adult
                    

                #is_bundle

                is_bundle = "no"

                product['is_bundle'] = is_bundle



                #age_group

                age_group = "adult"

                product['age_group'] = age_group


                #color
                              
                product['color'] = color

            

                #gender

                gender = "female"

                product['gender'] = gender
                
                
 


        yield product
        """produto = Product()
        produto['name'] = produto_e_suas_variacoes
       

       
        
        yield produto"""

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
