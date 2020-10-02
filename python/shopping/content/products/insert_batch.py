#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Adds several products to the specified account, in a single batch."""

from __future__ import absolute_import
from __future__ import print_function
import json
import sys

from shopping.content import common
from shopping.content.products import sample
from six.moves import range

# Number of products to insert.
BATCH_SIZE = 1


def main(argv):
  # Authenticate and construct service.
  service, config, _ = common.init(argv, __doc__)
  merchant_id = config['merchantId']

  batch = {
      'entries': [{
          'batchId': 123,
          'merchantId': merchant_id,
          'method': 'insert',
          'product': {'additionalImageLinks': ['https://bolsadachica.com.br/wp-content/uploads/2018/04/Mochila-School-Bag-Rato-600x686.jpeg',
                           'https://bolsadachica.com.br/wp-content/uploads/2018/04/Mochila-School-Bag-Rato-lateral-600x745.jpeg'],
           'adult': bool(1),
           'ageGroup': 'adult',
           'targetCountry': 'BR',
           'contentLanguage': 'pt',
           "channel": "online",
           'offerId': '123',
           'availability': 'in stock',
           'color': 'Bege',
           'condition': 'new',
           'description': 'A Mochila Schoolbag é admirável, arrebatadora, combina '
                          'facilmente jeans, camisetas e camisas. Todos os itens que uma '
                          'mulher necessita para viver poderão ser facilmente colocados '
                          'dentro dela. Portanto, não deixe nada de fora por causa do '
                          'tamanho, leve desde roupas a acessórios de higiene pessoal. '
                          'Ideal para ocasiões de trabalho, academia e viagens. Desse '
                          'modo, evite o uso desse item em looks minimalistas, ocasiões '
                          'formais ou naquele primeiro encontro. Utilize-a com cores '
                          'cores neutras, estampas e listras.\n'
                          'Material: couro sintético',
           'gender': 'female',
           'googleProductCategory': '100',
           'imageLink': 'https:\\/\\/bolsadachica.com.br\\/wp-content\\/uploads\\/2018\\/04\\/foto-40.jpg',
           'isBundle': 'no',
           'link': 'https://bolsadachica.com.br/produto/mochila-scoolbag/',
           'price': {'currency': 'BRL', 'value': '160.00'},
           'title': 'Mochila Schoolbag'},
          } ],
  }

  request = service.products().custombatch(body=batch)
  result = request.execute()

  if result['kind'] == 'content#productsCustomBatchResponse':
    entries = result['entries']
    for entry in entries:
      product = entry.get('product')
      errors = entry.get('errors')
      if product:
        print('Product "%s" with offerId "%s" was created.' %
              (product['id'], product['offerId']))
      elif errors:
        print('Errors for batch entry %d:' % entry['batchId'])
        print(json.dumps(errors, sort_keys=True, indent=2,
                         separators=(',', ': ')))
  else:
    print('There was an error. Response: %s' % result)


if __name__ == '__main__':
  main(sys.argv)
