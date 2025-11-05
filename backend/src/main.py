from dotenv import load_dotenv
load_dotenv()

import uvicorn
from core.app import CoreApp


app = CoreApp(
    title="RAG backend API", 
    version="0.1.0"
)
app.register_routes()

@app.get("/")
async def root():
    return {"message": "Welcome, V1"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

