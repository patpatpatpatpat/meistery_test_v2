# ProductSale

API details:

`GET "/api/userinformation/:userId"`

Expected Response:
`{ userInformation: { name: string, email: string, age: number, gender: string, city: string, country: string, userId: string } }`

`GET "/api/sales/:userId"`
Expected Response:

```
    {
        sales: {
            date: string
            id: string
            product: string
            revenue: string
            sales_number: string
            userId: string
        }
    }
```

`GET "/api/aggregated_data/:userId"`

Expected Response:

```
{
    "aggregatedData":{
        "avgSaleCurrentUser": number,
        "avgSale": number,
        "mostExpensiveProduct":{
            "userId": string,
            "id": string,
            "date": string,
            "product": string,
            "sales_number": string,
            "revenue": string
        },
        "mostRevenueEarningProduct":{
            "name": string,
            "revenue": number
        },
        "mostSoldProduct":{
            "name": string,
            "count": number
        }
    }
}
```
