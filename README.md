
### Steps to Run the Application
1. **Start the AcaPy Authority Agent** on your server by executing `./run_demo authority --events --no-auto` from the demo directory in the AcaPy folder
2. **Build the Docker image** from the project root folder by running `docker-compose up --build`
3. **Open the HTML file** in a web browser to access the frontend.

### Additional information for developing
- **Updating Virtual Python Environment**: run `pip freeze > requirements.txt`-> ist das noch notwendig? Wie update ich meinen Dockerfile?

### Additional Considerations for FastAPI
- **Asynchronous Programming**: Embrace asynchronous programming for handling network IO. This can lead to better performance, especially under high load, which is crucial for your use case.
- **Error Handling**: Implement error handling in your FastAPI application. FastAPI has built-in support for request validation, error handling, etc.
- **Testing**: FastAPI simplifies testing your application. Use FastAPI's test client to write tests for your application.
- **Security**: Ensure the security of your application. FastAPI provides several tools and plugins for security, such as OAuth2 with Password (and hashing), JWT tokens, etc.
- **Deployment**: When deploying your FastAPI application, you'll need an ASGI server such as Uvicorn or Hypercorn. Also, consider using Docker for consistent and isolated environments.

### Final Steps
- Thoroughly test your FastAPI application to handle various scenarios and loads.
- Use FastAPI's automatic documentation (available at `/docs` or `/redoc` URL paths) to test and document your API endpoints.
- Keep iterating based on feedback and testing.

By following these steps, you can leverage FastAPI's performance benefits and asynchronous capabilities for your project. Remember, the success of your application depends not only on the chosen technology but also on good design, thorough testing, and continuous iteration based on user feedback.
