
## Our team

- Alexandr Reznik
- Dragos Paul Vecerdea
- Sanskar Chawla
- Daksh Shah

# MOPR: Merchant Online Presence Rater 

A tool that will consume information about a list of businesses and scan the web for their online presence including but not limited to reviews, map location and social media profiles. Using this acquired knowledge it would rate these businesses.

## Requirements

### Python 3

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### API Keys
- Provide `.api_key` file containing Google Cloud Platform API key. https://developers.google.com/knowledge-graph
- Provide `.yelp_api_key` file containing Yelp API key. https://www.yelp.com/developers/documentation/v3/authentication

### Configuration

- We have provided `config.json` file, with the weights for different types of information. You can fine tune this according to your use case. 

## Executing
```
python scrapping.py input.json
``` 

The script saves the results in `output.json`.

## Logic

Every local business gets points for
- being present at Google Knowlege Graph
- being present at Yelp
- getting reviews

Review score is calculated as:

> max(max_review_count, review_count) / max_review_count * review_coefficient 

A place gets maximum amount of points for getting a number of review higher or equal to the number provided in config as "max_review_count"

## Sample input.json

```
[
    {"name":"CAFE COCO LIMITED","address":"25/27, Cowley Road, Oxford, United Kingdom, OX4 1HP"},
    {"name":"CAFE ABANTU LIMITED","address":"97 Bramley Way, Hardwick, Cambridge, United Kingdom, CB23 7XE"}
]
```

## Sample output.json

```
[
    {"name": "CAFE COCO LIMITED", "rating": 6.04},
    {"name": "CAFE ABANTU LIMITED", "rating": 2}
]
```