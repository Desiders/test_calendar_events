## Test task "Calendar events web application"
### Description:
Create a calendar events web application, which allows to create, edit and delete events.

Web application should have a login page, where user can login or register.

Event can be private or public. Private events can be viewed only by the owner, public events can be viewed by all users.

## Migrations

To start migrations run the following command:

```bash
just migrate
```

## Installation

- Install [Docker](https://docs.docker.com/get-docker/), [Docker Compose](https://docs.docker.com/compose/install/) and [just](https://github.com/casey/just#installation)
- Clone this repository `git clone https://github.com/Desiders/test_calendar_events.git`
- Copy `.env.example`d to `.env` and fill it with your data

## Running and stopping the application

Create `.env` file in the root directory of the project and fill it with the following content

To start the server run the following command:

```bash
just up
```

This command will build the application and start the server.

To stop the server run the following command:

```bash
just down
```

## Swagger (docs)

To view swagger docs go to `http://0.0.0.0:5000/docs` or any other host and port you specified in `.env` file.

## Development

### Configure tailwindcss

To compile tailwind css run the following command:

```bash
just tailwindcss
```