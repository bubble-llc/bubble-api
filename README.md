# bubble-api

# Install
- "pip install -r requirments.txt"

# Run server
- "./start_gunicorn.sh"

# Test API in Postman

curl --location --request GET 'http://0.0.0.0:8000/feed?zipcode=78703&category_name=What%27s%20happening?'

curl --location --request GET 'http://0.0.0.0:8000/feed?zipcode=78703'

curl --location --request POST 'http://0.0.0.0:8000/add_post_to_category' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "steventt07",
    "category_name": "What'\''s happening?",
    "content": "My thirs post",
	"title": "Lalala",
    "zipcode": "78703"
}'

curl --location --request POST 'http://0.0.0.0:8000/remove_post_from_category' \
--header 'Content-Type: application/json' \
--data-raw '{
    "post_id": "a6fd26ba-3cef-4734-9610-a6e4ac578d25",
    "category_name": "What'\''s happening?"
}'
