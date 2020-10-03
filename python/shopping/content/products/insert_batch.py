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
      'entries': [{'batchId': 8,
 'merchantId': merchant_id,
 'method': 'insert',
 'product': {'additionalImageLinks': ['https://bolsadachica.com.br/wp-content/uploads/2018/04/foto-9-600x400.jpg',
                                      'https://bolsadachica.com.br/wp-content/uploads/2018/04/foto-10-600x400.jpg',
                                      'https://bolsadachica.com.br/wp-content/uploads/2018/04/foto-67-600x400.jpg',
                                      'https://bolsadachica.com.br/wp-content/uploads/2018/04/bolsa-lu-rosa-fundo-branco-e1600130113442-300x300.jpeg'],
             'adult': True,
             'ageGroup': 'adult',
             'availability': 'out of stock',
             'channel': 'online',
             'color': 'Caramelo',
             'condition': 'new',
             'contentLanguage': 'pt',
             'description': 'A Tela é uma bolsa feminina estilosa e '
                            'poderosa\xa0 e você pode usá-la em todas as '
                            'oportunidades que tiver para sair de casa. Além '
                            'de\xa0todos os itens pessoais que você leva, sem '
                            'se preocupar com o tamanho ou volume pois essa '
                            'bolsa possui um amplo espaço\xa0 interno, ela '
                            'combina facilmente. Portanto, calças brancas, '
                            'pretas, jeans, vestidos ou saias são muito '
                            'bem-vindos com essa linda bolsa.\xa0 Utilize-a '
                            'com cores claras ou escuras. Dessa forma, preto e '
                            'branco são escolhas certeira, evite cores quentes '
                            'tais como amarelo ou vermelho.\n'
                            'Material: couro sintético',
             'gender': 'female',
             'google_product_category': '3032',
             'imageLink': 'https:\\/\\/bolsadachica.com.br\\/wp-content\\/uploads\\/2018\\/04\\/foto-9.jpg',
             'isBundle': 'no',
             'link': 'https://bolsadachica.com.br/produto/bolsa-tela/',
             'offerId': 312,
             'price': {'currency': 'BRL', 'value': '100.00'},
             'targetCountry': 'BR',
             'title': 'Bolsa Feminina Tela'},
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
