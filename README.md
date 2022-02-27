
## Our team

- Alexandr Reznik
- Dragos Paul Vecerdea
- Sanskar Chawla
- Daksh Shah

# MOPR: Merchant Online Presence Rater 

A tool that will consume information about a business and scan the web for their online presence including but not limited to reviews, map location and social media profiles.

## Using

To run the script
- make sure python (version 3) is installed
- provide `.api_key` file containing Google Cloud Platform API key. https://developers.google.com/knowledge-graph
- provide `.yelp_api_key` file containing Yelp API key. https://www.yelp.com/developers/documentation/v3/authentication
- provide `config.json` file described later
- run `pip install -r requirements.txt`
- run MOPR by executing `python scrapping.py input.json` where `input.json` is the input file
- after the script is executed the result would be generated in `output.json` file

## Logic

Every local business gets points for
- being present at Google Knowlege Graph
- being present at Yelp
- getting a reviews

Review score is calculated as `max(max_review_count, review_count) / max_review_count * review_coefficient`. A place gets maximum amount of points for getting a number of review higher or equal to the number provided in config as "max_review_count"


## Example config.json

```
{
    "coefficients": 
    {
        "google": 2,
        "yelp": 2,
        "reviews": 6,
        "max_review_count": 100
    }
}
```

## Example input.json

```
[
    {"name":"CAFE COCO LIMITED","address":"25/27, Cowley Road, Oxford, United Kingdom, OX4 1HP"},
    {"name":"CAFE ABANTU LIMITED","address":"97 Bramley Way, Hardwick, Cambridge, United Kingdom, CB23 7XE"}
]
```

## Example output.json

```
[
    {"name": "CAFE COCO LIMITED", "rating": 6.04},
    {"name": "CAFE ABANTU LIMITED", "rating": 2}
]
```