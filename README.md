# BirthdayCalc

BirthdayCalc is a simple Python application for calculating birthdays and related information. It includes infrastructure-as-code support with Terraform and can be containerized with Docker.

## Features
- Calculate days until your next birthday
- Infrastructure as code with Terraform
- Docker support for easy deployment

## Project Structure
- `app.py`: Main application logic
- `requirements.txt`: Python dependencies
- `Dockerfile`: Containerization setup
- `setup.sh`: Setup script
- `terraform/`: Terraform configuration files

## Getting Started

### Prerequisites
- Python 3.x
- pip
- (Optional) Docker
- (Optional) Terraform

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BrianDavisson/birthdaycalc.git
   cd birthdaycalc
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
Run the application:
```bash
python app.py
```

### Docker
Build and run with Docker:
```bash
docker build -t birthdaycalc .
docker run --rm birthdaycalc
```

### Terraform
See the `terraform/` directory for infrastructure setup instructions.

## License
MIT
