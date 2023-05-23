#  E-commerce webapp for 'HAVEN' brand + REST API

### Check the app's [website](https://havengoods.ru/)

API contains following endpoints:
* POST /api-token-auth/ - token authentication with username & password
* GET /api/v1/products/ - get the whole products list
* POST /api/v1/products/ - create new product
* PUT /api/v1/products/pk/ - update product
* DELETE /api/v1/products/pk/ - delete product
* GET /api/v1/basket-items/ - the whole basket of the current authenticated user
* POST /api/v1/basket-items/ - create a new basket item or increase quantity of existing item
* DELETE /api/v1/basket-items/pk/ - delete basket item
