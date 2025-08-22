| <img src="docs/chatbot.svg" width="128"> |
| - |

# Chatbot

## Overview

This project is a simple chatbot application. It provides a user-friendly interface for interacting with the chatbot, allowing users to ask questions and receive responses.

## User Interface (UI)

| <a href="https://robertovicario-chatbot.hf.space"><img src="docs/cover.png" alt="UI" width="512"></a> |
| :-: |
| **Home - Chatbot** |

## Prerequisites

> [!IMPORTANT]
>
> - Docker
> - Docker Compose

## Instructions

Usage:

```sh
bash cmd.sh {start|stop|setup|clear|build|deploy}
```

### `setup`

If you haven't built the project yet, you can do so by running:

```sh
bash cmd.sh setup
```

Once the setup process is complete, the project will be accessible at `localhost:7860`.

> [!WARNING]
>
> If this port is already in use, search for all occurrences of `7860` within the project and replace them with your preferred port number. After making these changes, you'll need to rebuild the project for the modifications to take effect.

### `start`

The program will run in debug mode, meaning frontend changes will be rendered upon reload. However, if you make changes to the backend, you will need to restart the program by running:

```sh
bash cmd.sh start
```

### `stop`

To stop the program, simply run:

```sh
bash cmd.sh stop
```

> [!TIP]  
> For a quicker way to stop, use `ctrl + C` to force stop the program.

### `clear`

If you need to clear all containers and their orphaned dependencies, you can run:

```sh
bash cmd.sh clear
```

### `build`

To generate the static files for the project, run the following command:

```sh
bash cmd.sh build
```

After the build process completes, the static files will be available in the `build` directory.

### `deploy`

To deploy the application to production, you can use the following command:

```sh
bash cmd.sh deploy
```

This project leverages GitHub Actions for CI/CD. The deployment workflow is configured to automatically build the project and deploy it to the HuggingFace Spaces environment.

## License

This project is distributed under [GNU General Public License version 3](https://opensource.org/license/gpl-3-0). You can find the complete text of the license in the project repository.
