# RFQ-BOT

RFQ-BOT is a project designed to automate the process of generating and managing Requests for Quotations (RFQs). This bot helps streamline the procurement process by automating repetitive tasks and ensuring accuracy in RFQ generation.

## Features

- Automated RFQ generation
- Template-based RFQ creation
- Email integration for sending RFQs
- Tracking and managing RFQ responses
- User-friendly interface

## Installation

To install and run the RFQ-BOT, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/RFQ-BOT.git
    ```
2. Navigate to the project directory:
    ```bash
    cd RFQ-BOT
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the RFQ-BOT, use the following command:
### Start the backend
Add .env in the backend folder with your info
```
GEMINI_API_KEY=
EMAIL_HOST=imap.gmail.com # change this to your email host
EMAIL_USER=
EMAIL_PASS= # gmail app password (look up how to create one online)
CC_EMAILS=
```

```bash
cd backend

uvicorn backend:app --reload
```

### Start the frontend on a separate terminal window
```bash
cd frontend

streamlit run app.py
```

## Configuration

Before running the bot, make sure to configure the necessary settings in the `config.json` file. This includes email settings, RFQ templates, and other relevant parameters.

## Contributing

We welcome contributions to the RFQ-BOT project. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Create a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or support, please contact the project maintainer at [christopheraliu07@gmail.com](mailto:christopheraliu07@gmail.com).
