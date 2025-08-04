# Draft Dockerfile - Customize as needed
FROM mcr.microsoft.com/playwright/python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN playwright install chromium
CMD ["pytest", "--alluredir=allure-results"]
