# Gemini Pro 1.5 chatbot streamlit app

![]()

## Setup

1. Clone the repository to your local machine.

```sh
    git clone https://github.com/ausarhuy/gemini-pro-chatbot-with-streamlit.git
```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. You need an GOOGLE_API_KEY to use the gemini-pro models. Visit [Google AI Studio](https://aistudio.google.com/app/apikey), create and copy your api key.

4. Set up your environment variables for email notifications by creating a `.env` file in the project root with the following content:

    ```env
    GOOGLE_API_KEY="Your key"
    ```

## Usage

Run the streamlit UI with the command:

```sh
streamlit run app.py
```

You can also configure your streamlit app in config.toml file.

## License

This project is open-sourced under the [MIT License](LICENSE).

## Contributing

Feel free to contribute to this project. Suggested improvements, bug reports, or pull requests are always welcome.

## Support

For any questions, issues, or assistance with this project, please open an issue in the repository.