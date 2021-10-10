Backend Technical Test
======================
RESTFull API for an online marketplace.

Database table:

Product code  | Name  |  Price |
|---|---|---|
|  001 |  Lavender heart | £9.25  |
|  002 |  Personalised cufflinks | £45.00  |
|  003 |  Kids T-shirt | £19.95 |

One can perform CRUD operations and has below mentioned five endpoints:

* GET /products - A list of products, names, and prices in JSON.
* POST /product - Create a new product from a JSON body.
* GET /product/{product_id} - Return a single product by id in JSON.
* PUT /product/{product_id} - Update a product's name or price by id.
* DELETE /product/{product_id} - Delete a product by id.

HOWTO: Run Unittests
--------------------

```shell
make test
```

HOWTO: Start Flask App
----------------------

```shell
make runserver
```
