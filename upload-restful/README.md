A simple shopping list server-side REST API - as a CGI script just because:-)

Jeremy did this in Django with REST plugins, MVC, ORMs etc.
I just wanted to do it "plain".

### Creating the Database

To create the databse, go into private/SQL and follow the instructions in
that directory's README.

### REST API

This simple shopping list example application provides REST endpoints for creating and deleting shopping lists and listing the available lists. It provides the ability to list the items within a shopping list and to add items and remove items from a list.

**Endpoint:** `/api`

**Methods**: `GET`,`POST`

**Description:** Get details of the all the registered shopping lists or create a new list.

**Request/Response:** 

`GET`: JSON data: A list of JSON objects containing `name (string)` and `owner (string)`

Returns 200 OK

`POST`: JSON data: A JSON object containing `name (string)` and `owner (string)` for the new list.

Returns 201 CREATED if the new list was created, 409 CONFLICT if a list of the same name already exists, 400 BAD REQUEST if parameters are missing or the list is otherwise invalid - a JSON response identifies the missing parameters.

**Endpoint:** `/api/{list_name}`

**Methods**: `GET`, `POST`, `DELETE`

**Description:** `GET` - Get a list of all the items in the specified shopping list. `POST` - Add an item to the specified shopping list. `DELETE` - Delete the specified shopping list and all its items.

**Request/Response:** 

`GET`: JSON data: A list of JSON objects, each representing a shopping list item 
 
 - `id (integer)`: The id of the item (used for deleting the item),
 - `name (string)`, 
 - `description (string)`, 
 - `quantity (integer)`, 
 - `price (decimal)`, 
 - `shopping_list (string)`: The name of the shopping list that this item belongs to.

 Returns 200 OK if the request succeeded or 404 NOT FOUND if the specified shopping list couldn't be found.

`POST`: JSON data: Either a single object or a list of JSON objects, representing one or more shopping list items with each containing:
 
 - `name (string)`, 
 - `description (string)`, 
 - `quantity (integer)`, 
 - `price (decimal)`

  Returns 201 CREATED if the request succeeded and the list was updated with the new item(s), 404 NOT FOUND if the specified shopping list couldn't be found or 400 BAD REQUEST if parameters are missing or the list is otherwise invalid - a JSON response identifies the missing parameters.
   
`DELETE`: Deletes the list, specified by `list_name` in the URL and all of its items.

 Returns 200 OK if the request succeeded or 404 NOT FOUND if the specified shopping list couldn't be found.

**Endpoint:** `/api/{list_name}/{item_id}`

**Methods**: `DELETE`

**Description:** `DELETE` (no data required) - Delete the item with the specified id from the specified shopping list based on the parameters provided in the URL.

**Request/Response:** `DELETE`: Returns 200 OK if the item was deleted, 404 NOT FOUND if the item couldn't be found.

#### Curl Examples (to test whether it's working)

set url = http://www.doc.ic.ac.uk/~dcw/shopping-restful/api

curl -X GET -i -H 'Content-Type: application/json' $url

returns the current lists..

curl -X POST -i -d '{"owner":"dcw", "name": "NewList"}' -H 'Content-Type: application/json' $url

returns {"owner":"dcw", "name": "NewList"} plus various info messages including one saying 201

curl -X GET -i -H 'Content-Type: application/json' $url

returns 1 more list than before - including NewList

curl -X POST -i -d '{"owner":"dcw", "name": "Lunch"}' -H 'Content-Type: application/json' $url

creates the new list Lunch.

curl -X GET -i -H 'Content-Type: application/json' $url/Lunch

lists the empty contents of the new list

curl -X DELETE -i -H 'Content-Type: application/json' $url/Lunch

deletes list Lunch, no output; nb: doing it a second time gives

["list <<Lunch1>> does not exist"]

curl -X POST -d '{"name":"pear", "description": "a pear", "quantity": "2", "price": "9.73"}' -H 'Content-Type: application/json' $url/Lunch

adds an item to the new list

curl -X GET -H 'Content-Type: application/json' $url/Lunch

lists the items in the new list (2 pears):

[{"quantity":2,"description":"a pear","name":"pear","id":7,"price":9.73}]
