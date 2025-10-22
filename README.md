# DNS Server

This is a DNS Server that was built following along with the [codecrafters](https://codecrafters.io) guide for building a DNS server. It is a learning tool/toy implementation and should never be used for anything serious.

## Development

This project is happiest running in a [devcontainer](https://devcontainers.github.io). The devcontainer will do all of the work to setup the project and download dependencies. In Github there's an option to open it immediately in a dev container and if you're running in VSCode you'll have the option:

- To run the server with autoreload on change use the Tasks Run Task > Run DNS Server (autoreload)
- To run without reload but debugging use the Run and Debug side panel
- Ro run tests use the testing sidebar

For running from the command line use the pipenv scripts

- `pipenv run dev` to run with autoreaload
- `pipenv run start` to run without autoreload
- `pipenv run test` to run tests
