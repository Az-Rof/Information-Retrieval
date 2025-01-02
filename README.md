# Information Retrieval - Final Project

This repository contains the final project for the Information Retrieval course. It is designed to be run with Python 3.8 and utilizes a relational database for data management.

## Prerequisites

Before you begin, ensure you have Python 3.8 installed on your machine. If not, you can download and install it from [Python's official website](https://www.python.org/downloads/release/python-380/).

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Cloning the Repository

To clone the repository and navigate into the project directory, run the following commands in your terminal:

```bash
git clone https://github.com/your-username/information-retrieval.git
cd information-retrieval
```

### Setting Up the Database

1. **Import the database** using the SQL dump provided in the repository. If you are using MySQL, you can import the database with the following command:

   ```bash
   mysql -u username -p database_name < path/to/your/database_file.sql
   ```

   Replace `username`, `database_name`, and `path/to/your/database_file.sql` with your MySQL username, the name of your database, and the path to your SQL dump file, respectively.

### Setting Up the Python Environment

1. **Create a virtual environment** (optional but recommended) to isolate the project dependencies:

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   - **Windows:**

     ```bash
     .\venv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

3. **Install the required Python packages** from the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

To run the project, execute the following command from the root directory of the project:

```bash
python main.py
```

## Authors

- **Ramada** - _Initial work_ - [Ramados](https://github.com/ramadaaditya)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
