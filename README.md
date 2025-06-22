# EMKicks KE E-Commerce App

## Table of Contents

1. [Introduction](#introduction)
2. [Repository Structure](#repository-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

## Introduction
* Welcome to EMKicks — your go-to e-commerce application for premium sneakers and jerseys!
* This app powers the backend services for managing products, users, orders, and secure payments, delivering a fast and seamless shopping experience.
* Whether you're hunting for the latest kicks or repping your favorite team with new jerseys, EMKicks has you covered!

## Repository Structure
* The repo has two directories: **Backend** and **Fronted**

### Backend
* The backend consists of:
* **app.py**: Entry point of the application
* **create_app.py**: Application factory
* **config.py**: Configuration settings
* **form.py**: Form classes and validation
* **models.py**: Database models
* **routes/**: Application routes and views
* **utils/**: Utility functions and helpers
* **migrations/**: stores migrations scripts
* **requirements.txt**: dependencies

## Installation
* To get started with this repository, follow these steps
1. **Clone the repository**: Clone the repository to your local machine
    ```sh
        git clone https://github.com/Emogy-reunion/emkicks_ecommerce_app.git
    ```

## Usage
1. **Navigate to the project directory**:
* To run the backend navigate to the directory containing the backend code
    ```sh
        cd emkicks_ecommerce_app
        cd Backend
    ```
2. **Create virtual environment**: Ensure you have python and virtualenv installed. Create and then activate a virtual environment
    ```sh
        python3 -m virtualenv myenv : in this case myenv in the environment (feel free to name it as you like)
        source myenv/bin/activate
    ```

3. **Install dependencies**: Install the required dependencies from `requirements.txt`
    ```sh
        pip install -r requirements.txt
    ```

4. **Run the application**
    ```sh
        python3 app.py
    ```
* This application should now be running, and you can access it in your browser at  `http://127.0.0.1:5000`.

## Contributing
* Contributions are welcome! Whether you're fixing a bug, improving the documentation, or adding new features, your help is appreciated.
* To contribute:
1. **Fork** the repository
2. **Clone** your fork
    ```sh
        git clone https://github.com/Emogy-reunion/emkicks_ecommerce_app.git
    ```
3. **Create a new branch** for your changes
    ```sh
        git checkout -b feature/your-feature-name
    ```
4. **Make your changes** and commit them
    ```sh
        git commit -m "Add: A short description of your change"
    ```
5. **Push** to your fork
    ```
    git push origin feature/your-feature-name
    ```
6. **Open a pull a request** and describe your changes
* Please make sure to follow the project's code style and write clear, concise commit messages.

## License
* This project is licensed under the MIT License

## Contact
* If you have any questions, feel free to reach out

### **Mark Victor Mugendi**
### **Email:** markvictormugendi@gmail.com
