import strawberry
from strawberry.asgi import GraphQL

from .graphql import RentRadarGraphQLAPI

schema = strawberry.Schema(query=RentRadarGraphQLAPI)

app = GraphQL(schema)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
