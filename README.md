# URL Shortening Service
This is a simple URL shortening service that takes a long URL and returns a shortened version of it. The service is written in Python and uses Flask as the web framework.

## Requirements

* Create a new short URL
* Retrieve an original URL from a short URL
* Update an existing short URL
* Delete an existing short URL
* Get statistics on the short URL (e.g., number of times accessed)

## API Endpoints

### Create a new short URL

```http
POST /shorten
{
  "url": "https://www.example.com/some/long/url"
}
```

### Retrieve an original URL from a short URL

```http
GET /shorten/abc123
```

### Update an existing short URL

```http
PUT /shorten/abc123
{
  "url": "https://www.example.com/some/updated/url"
}
```

### Delete an existing short URL

```http
DELETE /shorten/abc123
```

### Get statistics on the short URL

```http
GET /shorten/abc123/stats
```

## Tech Stack

* Python 3.9.6
* Flask 3.1.10
* SQLite 3.36.0