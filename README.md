
# Influencer Marketing Platform

This project is a Flask-based web application designed to connect sponsors with influencers for marketing campaigns. The platform includes user roles (Admin, Sponsor, Influencer), campaign management, ad requests, user authentication, and various utility features to streamline the process of influencer marketing.

## Features

- **User Roles**: Support for Admin, Sponsor, and Influencer roles, each with specific permissions and views.
- **Campaign Management**: Sponsors can create, edit, and manage marketing campaigns with specified budgets, visibility, and niches.
- **Ad Requests**: Sponsors can send ad requests to influencers, and influencers can respond to these requests.
- **User Management**: Admins can manage users, campaigns, ad requests, flagged users, and access analytics.
- **Authentication**: Secure user login, registration, and session management with Flask-Login.

## Project Structure

- **Models**:
  - **User**: Manages user information including username, password, role, niche, reach, and flagged status.
  - **Campaign**: Manages marketing campaigns with attributes such as name, description, start and end dates, budget, visibility, and associated sponsor.
  - **AdRequest**: Manages ad requests between sponsors and influencers, including messages, requirements, payment amounts, and status.

- **Routes**:
  - **Admin**: Dashboard, manage users, manage campaigns, manage ad requests, analytics, settings, and user management (edit, delete, flag/unflag).
  - **Sponsor**: Dashboard, create/edit/delete campaigns, manage ad requests, search influencers, and analytics.
  - **Influencer**: Dashboard, manage ad requests, search campaigns, profile settings, and analytics.
  - **Authentication**: Login, registration, logout.

## Requirements

The project relies on the following Python libraries, listed in `requirements.txt`:

```plaintext
blinker==1.6.2
click==8.1.3
colorama==0.4.6
distlib==0.3.6
filelock==3.8.2
Flask==2.3.2
Flask-Login==0.6.2
Flask-SQLAlchemy==3.0.5
greenlet==2.0.1
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
platformdirs==2.6.0
playsound==1.3.0
SQLAlchemy==1.4.45
virtualenv==20.17.1
Werkzeug==2.3.6
```

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/influencer-marketing-platform.git
    ```
   
2. **Navigate to the project directory**:
    ```bash
    cd influencer-marketing-platform
    ```

3. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

5. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the application**:
    ```bash
    python app.py
    ```

7. **Access the application in your browser**:
    ```plaintext
    http://127.0.0.1:5000/
    ```

## Usage

- **Admin**: Admin users can manage all aspects of the platform, including users, campaigns, ad requests, and flagged users. Admins also have access to platform analytics.
- **Sponsor**: Sponsors can create and manage campaigns, send ad requests to influencers, and collaborate with them to execute campaigns.
- **Influencer**: Influencers can view ad requests, respond to them, and manage their profiles and settings.

## Contributing

Contributions to the project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
