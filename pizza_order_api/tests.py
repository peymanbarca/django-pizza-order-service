from rest_framework.test import APITestCase
import uuid


class APITest(APITestCase):

    def test_create_new_order(self):

        order_info = {"customer_name": "Peyman Yazdanian","customer_email": "p.yazdanian74@gmail.com"}
        order_items = [
            {
                "pizza_flavour": "Margarita",
                "pizza_size": "small",
                "pizza_count": 2
            },
            {
                "pizza_flavour": "Salami",
                "pizza_size": "medium",
                "pizza_count": 2
            },
            {
                "pizza_flavour": "Margarita",
                "pizza_size": "large",
                "pizza_count": 3
            }
        ]

        data = {
            'order_info' : order_info,
            'order_items' : order_items
        }
        response = self.client.post(path='/api/order/create', data=data, format="json")

        status = response.status_code
        self.assertEqual(status, 201)

        response_data = response.json()
        self.assertEqual(response_data['status'], "success")
        id = response_data['order']['id']
        print('Order with Id {} created.'.format(id))

        return id

    def test_fetch_orders(self):

        new_order_id = self.test_create_new_order()

        # Test Search API

        customer_name_search_phrase = 'Peyman'
        status_search_phrase = 'new'
        response = self.client.get(path='/api/order/search?page=1&limit=10&customer_name={}&status={}'
                                   .format(customer_name_search_phrase, status_search_phrase))


        response_data = response.json()
        self.assertEqual(response_data['status'],'success')
        total = response_data['total']
        print('{} orders fethed for customer_name_search_phrase : {}, status : {} '
              .format(total, customer_name_search_phrase, status_search_phrase))
        if total > 0:
            for order in response_data['orders']:
                customer_name = order['customer_name']
                status = order['status']

                self.assertTrue(str(customer_name).__contains__(customer_name_search_phrase))
                self.assertEqual(status, status_search_phrase)

        # Test Retrieve Single Order API
        response = self.client.get(path='/api/order/{}'.format(new_order_id))

        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')

        # Test Retrieve Single Order API (for not found case)
        fake_order_id = uuid.uuid4()
        response = self.client.get(path='/api/order/{}'.format(fake_order_id))
        self.assertEqual(response.status_code, 404)
