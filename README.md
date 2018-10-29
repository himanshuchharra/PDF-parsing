============================
Bottle: Python Web Framework
============================

Bottle is a fast, simple and lightweight WSGI_ micro web-framework for Python_. It is distributed as a single file module and has no dependencies other than the `Python Standard Library <http://docs.python.org/library/>`


RBC bank statement analyser
----------------------------------

REST API for RBC bank statement analyser

Instructions
----------------------------------
1. Create .env file in the root directory of the project add APP_HOST, APP_PORT
2. Run python app/app.py to run the application

RESTAPI Docs
----------------------------------
# Endpoints

**URL** : `/api/v1/analyser`

**Method** : `POST`

**Header** : `NA`

**Auth required** : None

**Permissions required** : None

## Request Body
```curl
curl -X POST \
  http://{url}/api/v1/analyser \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F 'upload=@statement.pdf'
```

## Success Response

**Code** : `201`

**Response**
```json
{
    "status": "success",
    "code": 201,
    "data": {
        "bank_name": "Royal Bank of Canada",
        "name": "LONGHORN ELECTRICAL SERVICE LTD.",
        "account_number": "01659 101-813-4",
        "opening_balance": 12838,
        "closing_balance": 19157.52,
        "from_date": "16/11/2017",
        "to_date": "15/12/2017",
        "currency": "U.S. Dollar",
        "transactions": [
            {
                "date": "17 Nov",
                "description": "Online Banking transfer - 8887",
                "type": "debit",
                "amount": 1000,
                "balance": 11838
            },
            {
                "date": "17 Nov",
                "description": "Online Banking transfer - 6357",
                "type": "credit",
                "amount": 1500,
                "balance": 10338
            }
        ]
    },
    "resource": "analyser"
}
```

## Failure Response

**Code** : `422`

**Response**
```json
{
    "status": "failed",
    "code": 422,
    "errors": {
        "upload": [
            "PDF file is required"
        ]
    }
}
```

**Code** : `500`

**Response**
```json
{
    "status": "failed",
    "code": 500,
    "errors": {
        "internal_server_error": [
            "Failed to analyse the bank statement"
        ]
    }
}
```
