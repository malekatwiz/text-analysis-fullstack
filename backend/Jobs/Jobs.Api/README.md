# Jobs API

Is a minimal ASP.NET Core Web API for managing job postings.

## Features

- Create a new job posting
  - On successful job creation into MongoDB
  - New event is published via Redis Pub/Sub
  - Return 201 (Accepted) status code
