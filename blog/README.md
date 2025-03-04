# A blog

This simple blgo application integrates [Esmerald][esmerald], [Saffier][saffier] and
[Esmerald Admin][esmerald_admin] making it simpler to show case any PoC needed.

## Requirements

* Python 3.8+
* Python virtual environment at your choice
* Docker

## Installation

1. There are two ways you can install the requirements:

    ```shell
    $ pip install -r development.txt
    ```

    Or you can simply run:

    ```shell
    $ make requirements
    ```
2. Start docker for local development.

   ```shell
   $ docker compose up
   ```
3. Export environment variables to make your development easier.

    ```shell
    $ export ESMERALD_SETTINGS_MODULE=blog.configs.development.settings.DevelopmentAppSettings
    $ export SAFFIER_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/blog
    ```
4. Run the existing migrations

    ```shell
    $ saffier migrate
    ```
5. Start the local development.
   
    ```shell
    esmerald runserver
    ```
6. Access the local documentation.

    ```shell
    http://localhost:8000/docs/swagger # for Swagger
    http://localhost:8000/docs/redoc # for Redoc
    http://localhost:8000/docs/stoplight # for Stoplight
    ```

### Create your superuser

If you want to fully take advantage of the superuser within this project, you must create one.

```shell
esmerald run --directive createsuperuser --first-name <YOUR-NAME> --last-name <LAST-NAME> --email <YOUR-EMAIL> --username <YOUR-USER> --password <YOUR-PASSWORD>
```

If the user you are trying to create already exists, you will get an error message:

```shell
User with email <EMAIL> already exists.
```

## Testing

To run the tests tou can simply run:

```shell
$ pytest
```

Or alternatively:

```shell
$ make test
```

[esmerald]: https://esmerald.dev
[saffier]: https://saffier.tarsild.io
[esmerald_admin]: https://esmerald-admin.tarsild.io
