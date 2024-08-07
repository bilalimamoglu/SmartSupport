# Smart Support

Smart Support is an autonomous sales agent that leverages OpenAI API to generate sales responses, track interactions, and manage leads (potential customers). This tool helps sales representatives reduce manual workload by automating various sales processes.

## Features

- **Lead Management**: Add, update, and retrieve leads.
- **Response Generation**: Generate sales responses using OpenAI API.
- **Sales Pipeline Management**: Track the progress of leads through different stages.
- **Interaction Tracking**: Record and retrieve interactions with leads.
- **Knowledge Base Integration**: Use a product catalog to assist in providing detailed product information.

## Installation

### Using Virtual Environment

1. Clone the repository:

    ```sh
    git clone https://github.com/bilalimamoglu/smart-support.git
    cd smart-support
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables. You can create a `.env` file in the root directory and add:

    ```env
    OPENAI_API_KEY=your-correct-openai-api-key
    ```

### Using Docker

1. Clone the repository:

    ```sh
    git clone https://github.com/bilalimamoglu/smart-support.git
    cd smart-support
    ```

2. Create a `.env` file in the root directory and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your-correct-openai-api-key
    ```

3. Build the Docker image:

    ```sh
    docker build -t smart-support .
    ```

4. Run the Docker container:

    ```sh
    docker run -d --env-file .env -p 8000:8000 --name smart-support-container smart-support
    ```

5. **Updating the Running Container**:

    If you need to update the Docker container (e.g., after fixing the API key):

    ```sh
    docker stop smart-support-container
    docker rm smart-support-container
    docker build -t smart-support .
    docker run -d --env-file .env -p 8000:8000 --name smart-support-container smart-support
    ```

## Usage

1. Make sure the necessary data directories exist:

    ```sh
    mkdir -p data/leads data/responses
    ```

2. Create the db:

    ```sh
    python src/scripts/init_db.py
    ```

3. Run the application:

    ```sh
    chainlit run app.py
    ```

## Configuration

Configuration settings can be found in `src/config/config.py`. Update the settings as needed, including paths for data directories and logging.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. We welcome all contributions.

## License

This project is licensed under the MIT License.

## Acknowledgements

- The community of developers and contributors who have helped in the development of this project.
