# improvements

-   move status codes into constants file

```py
status = 400
status = 200
```

should become

```
status = HTTP_CODE_BAD_REQUEST
status = HTTP_CODE_SUCCESS
```

-   move http methods to constants file (No naked literals)

```py
@app.route("/delete/<buggy_id>", methods=["POST", "GET"])
@cookie_required
def del_buggy(buggy_id):
    if request.method == "POST":
        ...
    elif request.method == "GET":
        return page_not_found(404)
```

should become

```py
@app.route("/delete/<buggy_id>", methods=[HTTP_METHOD_POST, HTTP_METHOD_GET])
@cookie_required
def del_buggy(buggy_id):
    if request.method == HTTP_METHOD_POST:
        ...
    elif request.method == HTTP_METHOD_GET:
        return page_not_found(HTTP_CODE_NOT_FOUND)
```

-   as little repetition as possible
-   minimise exception handling

```py
except Exception as e:
```

should become

```py
except sql.Error as e:
```

-   no formatting sql strings (taint checking)

```py
cur.execute(f"INSERT INTO buggies ({keys}) VALUES ({values})")
```
