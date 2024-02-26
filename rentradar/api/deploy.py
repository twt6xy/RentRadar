import strawberry
from starlette.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from .graphql import RentRadarGraphQLAPI

schema = strawberry.Schema(query=RentRadarGraphQLAPI)
app = GraphQL(schema)

app = CORSMiddleware(
    app,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
