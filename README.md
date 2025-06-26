[![codecov](https://codecov.io/gh/MG814/mc_accounts/graph/badge.svg?token=C4OJFGSWMX)](https://codecov.io/gh/MG814/mc_accounts)

# Accounts Microservice

A microservice responsible for managing user accounts within the **MediCare** system. It handles authentication, registration, and the management of user data and their residential addresses.

## Overview

The Accounts Microservice consists of two main modules:

- **accounts** - user management, including login, registration, logout, and data updates
- **address** - handling of user residential addresses

The microservice is integrated with **Auth0** as the authentication provider, offering ready-to-use login and registration panels. The token callback is handled by the **API Gateway**, while the microservice communicates directly with Auth0 for user registration, login, and data updates.


## Features

### Accounts Module

- User login
- New account registration
- Logout
- Updating user data
- Integration with Auth0

### Address Module

- Adding residential addresses
- Editing existing addresses
- Managing user address data

## 🛠 Technologies

- **python 3.13**
- **django 5.1** 
- **djangorestframework 3.15.2** 
- **psycopg2-binary 2.9.10**
- **django-environ 0.11.2** 
- **requests 2.32.3** 
- **drf-spectacular 0.28.0**
- **factory-boy 3.3.1**
- **coverage 7.7.0** 
- **bandit 1.7.9** 
- **ruff 0.6.3** 
- **safety 3.2.7** 

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/MG814/mc_accounts.git
cd mc_accounts
```

#### 2. Running the entire application:

```bash
docker-compose up --build
```

#### 3. Migrations (in a separate terminal):

```bash
docker-compose exec web-accounts python src/manage.py migrate
```

