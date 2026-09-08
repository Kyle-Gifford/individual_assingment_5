# Borrow'r

Borrow'r is a small item-lending web application built with **Python, Flask, Jinja2, JavaScript, HTML, and CSS**. Users can create accounts, list items they own, search available inventory, borrow items from other users, return borrowed items, manage an account balance, and optionally attach item images through a separate image-upload service.

The project is designed as a lightweight full-stack web application demonstrating Flask routing, server-rendered templates, in-memory application state, client-side filtering, and HTTP integration between independently running services.

## Features

- User sign-up and login
- User control panel with account balance
- Add funds to an account
- Create item listings with name, condition, value, daily rate, and optional image
- View items owned by the current user
- Filter owned items by loan status
- Search available items by name
- Prevent users from borrowing their own items
- Prevent borrowing items that are already loaned
- Require sufficient account funds before borrowing
- Track currently borrowed items
- Return borrowed items and make them available again
- Integrate with an independently hosted image-upload service
- Client-side JavaScript filtering without additional search requests

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3, Flask |
| Templates | Jinja2 |
| Frontend | HTML, CSS, JavaScript |
| State | In-memory Python dictionaries/lists |
| Image integration | HTTP-based external image-upload service |
| Development server | Flask built-in server |

The repository pins Flask and its supporting packages in `requirements.txt`.

## Project Structure

```text
.
├── borrowr.py
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── borrowd.js
│       ├── my_items.js
│       ├── my_script.js
│       └── search.js
└── templates/
    ├── add_funds.j2
    ├── add_item.j2
    ├── borrowd.j2
    ├── index.j2
    ├── login.j2
    ├── my_items.j2
    ├── search.j2
    ├── signup.j2
    ├── test.j2
    ├── user_cp.j2
    └── view.j2
```

## How the Application Works

Borrow'r is centered around two in-memory data structures defined in `borrowr.py`:

```python
user_data = {...}
items_db = []
```

`user_data` stores registered users, their funds, owned-item IDs, borrowed-item IDs, and the currently active user.

`items_db` stores item records such as:

```python
{
    "id": "0",
    "name": "Cordless Drill",
    "condition": "good",
    "value": 80,
    "rate": 5,
    "owner": "owner@example.com",
    "status": "unloaned",
    "days_loaned": "1",
    "image_url": "..."
}
```

Because this state is stored only in Python memory, application data is reset whenever the Flask process restarts.

## Application Flow

```text
Landing Page
    |
    +--> Sign Up / Log In
            |
            v
      User Control Panel
       /      |       \
      /       |        \
 Add Funds  My Items   Search
              |          |
              |          +--> View Item
              |                  |
              |                  +--> Borrow
              |
              +--> Add Item
                      |
                      +--> Optional Image Upload

User Control Panel
        |
        +--> Borrow'd Items
                  |
                  +--> Return Item
```

## User Accounts

### Sign Up

New users register through:

```text
/signup
```

The sign-up form collects:

- name
- email
- password

If the submitted email is not already registered, the application creates a new user with:

- a starting balance of `0`
- an empty owned-items list
- an empty borrowed-items list

The newly created user becomes the active user and is redirected to the control panel.

### Login

Users log in through:

```text
/login
```

The server checks the submitted email and password against the in-memory user data. Successful login sets that email as the application's active user.

### Logout

```text
/logout
```

Logging out clears the active-user value and redirects to the landing page.

> This project does not currently use Flask sessions, cookies, password hashing, or a persistent user database. The active user is stored as a global application value.

## User Control Panel

Authenticated users are directed to:

```text
/user_cp
```

The control panel displays the current user's:

- name
- account balance

It also provides navigation to:

- Add Funds
- My Items
- Search
- Borrow'd Items
- Logout

## Adding Funds

Users can modify their balance from:

```text
/add_funds
```

The application attempts to parse the submitted amount as an integer and adds it to the active user's current balance.

This balance is later used as an eligibility check when attempting to borrow an item.

### Current funds behavior

Before a borrow is approved, Borrow'r checks:

```python
if user["funds"] < item["rate"]:
    return redirect("/")
```

The current implementation verifies that the user has at least the item's rate available, but it **does not deduct the rate from the user's balance** after borrowing.

## Item Listings

Authenticated users can create listings at:

```text
/add_item
```

Each item includes:

| Field | Description |
| --- | --- |
| `id` | Sequential item identifier |
| `name` | Listing name |
| `condition` | `excellent`, `good`, `fair`, or `poor` |
| `value` | Integer item value |
| `rate` | Integer lending rate |
| `owner` | Email of the user who created the listing |
| `status` | `unloaned` or `loaned` |
| `days_loaned` | Currently initialized to `"1"` |
| `image_url` | Optional URL supplied by the image service |

New listings begin with:

```text
status = unloaned
```

The item ID is based on the current length of `items_db`, and that ID is also added to the owner's `items_owned` list.

## Image Upload Integration

Borrow'r is designed to work with a **separate image-upload web service**.

The Borrow'r repository does not contain that service. The application expects it to be independently available at:

```text
http://localhost:64799
```

The image service host and port are configured in `borrowr.py`:

```python
img_host = "localhost"
img_port = 64799
```

### Upload flow

When the Add Item page is rendered, Borrow'r constructs an upload URL similar to:

```text
http://localhost:64799/upload/<borrowr-host>/<borrowr-port>/<item-id>
```

The user is sent to that service by clicking **Upload Image**.

After an upload, the image service is expected to redirect or call back to Borrow'r at:

```text
/img_uploaded/<item_id>/<filename>
```

Borrow'r then constructs an image URL pointing to the upload service:

```text
http://localhost:64799/static/uploads/<filename>
```

That URL is temporarily stored and attached to the next item created through the Add Item form.

### Running without the image service

The core Borrow'r application can still be started without the image service, but the **Upload Image** feature will not work unless a compatible service is listening at the configured host and port.

## Viewing Owned Items

The route:

```text
/my_items
```

renders only listings whose `owner` matches the active user.

The page loads item data into the HTML and uses `static/js/my_items.js` to build and filter the table in the browser.

Available filters are:

```text
loaned
unloaned
all
```

Filtering happens entirely in JavaScript and does not issue a new request to the Flask backend.

## Searching Inventory

Available inventory is exposed through:

```text
/search
```

The server only includes items that satisfy both conditions:

```text
status == "unloaned"
owner != active_user
```

This means users do not see their own listings as borrowable search results and already-loaned items are excluded.

### Client-side search

`static/js/search.js` performs case-insensitive substring filtering on item names as the user types.

Conceptually:

```javascript
item.name.toLowerCase().includes(query.toLowerCase())
```

Matching items are dynamically inserted into the results table and include links to:

- View
- Borrow

No AJAX request or server-side search query is required.

## Viewing an Item

Individual listings can be viewed at:

```text
/view/<id>
```

The page displays the item's:

- image, when available
- name
- item number
- condition
- value
- rate

It also provides a **Borrow Now** action.

## Borrowing Logic

Borrowing is handled by:

```text
/borrow/<id>
```

Before an item is loaned, the backend validates several conditions.

### 1. A valid active user and item must exist

If either is missing, the request is rejected.

### 2. Users cannot borrow their own items

The application checks whether the requested item ID appears in the user's `items_owned` collection.

### 3. The item must be available

The item must have:

```text
status = unloaned
```

An already-loaned item cannot be borrowed again.

### 4. The user must have sufficient funds

The user's balance must be at least the item's configured rate.

If all checks pass, Borrow'r changes:

```text
unloaned -> loaned
```

and records the item ID in the user's borrowed-items list:

```python
item["status"] = "loaned"
user["items_borrowd"].append(id)
```

The user is then redirected to the Borrow'd Items page.

## Borrowed Items

Currently borrowed listings are available at:

```text
/borrowd
```

The backend creates a list containing items whose IDs appear in the active user's `items_borrowd` collection.

`static/js/borrowd.js` then:

- renders those items into a table
- supports case-insensitive name filtering
- displays the item's value, rate, and `days_loaned`
- creates a Return link for each item

## Returning an Item

Returns are handled through:

```text
/return_item/<id>
```

The backend validates that:

- the user exists
- the item exists
- the item does not belong to that user
- the item is currently marked `loaned`

A successful return changes the item back to:

```text
status = unloaned
```

and removes the item ID from the current user's borrowed-items collection.

The listing then becomes available to search and borrow again.

## Routes

| Route | Methods | Purpose |
| --- | --- | --- |
| `/` | GET | Landing page or redirect to control panel |
| `/signup` | GET, POST | Create an account |
| `/login` | GET, POST | Authenticate a user |
| `/logout` | GET | Clear the active user |
| `/user_cp` | GET | User control panel |
| `/add_funds` | GET, POST | Display or update account balance |
| `/add_item` | GET, POST | Create an item listing |
| `/cancel_add_item` | GET | Cancel item creation and clear pending image |
| `/my_items` | GET | View items owned by the active user |
| `/search` | GET | Search available inventory |
| `/view/<id>` | GET | View a specific item |
| `/borrow/<id>` | GET | Borrow an available item |
| `/borrowd` | GET | View currently borrowed items |
| `/return_item/<id>` | GET | Return a borrowed item |
| `/img_uploaded/<item_id>/<filename>` | GET | Receive image-upload callback |

## Installation

### Requirements

The original project was developed with:

```text
Python 3.9.7
Flask 2.2.2
```

The complete pinned dependencies are provided in `requirements.txt`.

### 1. Clone the repository

```bash
git clone https://github.com/Kyle-Gifford/individual_assingment_5.git
cd individual_assingment_5
```

### 2. Create a virtual environment

On Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Borrow'r

Start the Flask application with:

```bash
python borrowr.py
```

If no local `credentials.py` file supplies a port, Borrow'r defaults to:

```text
64126
```

Open:

```text
http://localhost:64126
```

in a browser.

The development server starts with Flask debug mode enabled.

## Optional Port Configuration

`borrowr.py` attempts to load the application port from:

```python
from credentials import port
```

If that import is unavailable, the application falls back to port `64126`.

A local `credentials.py` can therefore contain:

```python
port = 5000
```

`credentials.py` is excluded by the repository's `.gitignore`.

If the Borrow'r port changes, make sure the external image-upload service can still redirect back to the correct application port.

## Quick Start

```bash
git clone https://github.com/Kyle-Gifford/individual_assingment_5.git
cd individual_assingment_5

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python borrowr.py
```

Then visit:

```text
http://localhost:64126
```

A typical test flow is:

1. Create an account.
2. Add funds.
3. Add one or more item listings.
4. Create or log into another user account.
5. Search for the first user's available item.
6. View and borrow the item.
7. Confirm that it appears under Borrow'd Items.
8. Return the item.
9. Confirm that it becomes available again.

Because application state is in memory, all users and listings created during the test are lost when the Flask process exits.

## Frontend JavaScript

Borrow'r uses JavaScript primarily for rendering and filtering item tables.

### `search.js`

- reads available item data embedded in the page
- filters by item-name substring
- creates View and Borrow links dynamically

### `my_items.js`

- renders the current user's listings
- filters by `loaned`, `unloaned`, or `all`

### `borrowd.js`

- renders currently borrowed items
- filters borrowed items by item name
- dynamically creates Return links

### `my_script.js`

This file is currently present as a general script include but contains no application logic.

## Templates

The frontend is server-rendered with Jinja2 templates.

| Template | Purpose |
| --- | --- |
| `index.j2` | Landing page |
| `signup.j2` | Account registration |
| `login.j2` | Login |
| `user_cp.j2` | User control panel |
| `add_funds.j2` | Add funds |
| `add_item.j2` | Create item listing / image upload |
| `my_items.j2` | Owned-item inventory |
| `search.j2` | Available-item search |
| `view.j2` | Item details |
| `borrowd.j2` | Borrowed-item management |

## Data Model

Borrow'r does not use a database. Its data model is represented directly with Python dictionaries and lists.

### User data

A user record contains approximately:

```python
{
    "name": "Example User",
    "email": "user@example.com",
    "password": "password",
    "funds": 0,
    "items_owned": [],
    "items_borrowd": []
}
```

### Item data

An item record contains approximately:

```python
{
    "id": "0",
    "name": "Example Item",
    "condition": "good",
    "value": 100,
    "rate": 10,
    "owner": "user@example.com",
    "status": "unloaned",
    "days_loaned": "1"
}
```

An `image_url` field is added when an image has been uploaded before the item is submitted.

## Concepts Demonstrated

This project demonstrates:

- Flask application structure
- URL routing
- GET and POST request handling
- HTML form processing
- Jinja2 server-side rendering
- Redirect-based application flow
- Python data modeling with dictionaries and lists
- Authentication-flow fundamentals
- Ownership and availability checks
- Lending-state transitions
- Client-side DOM manipulation
- Client-side search and filtering
- Separation between backend and frontend responsibilities
- HTTP integration between independently developed services

## Repository

Project source:

https://github.com/Kyle-Gifford/individual_assingment_5

---

Borrow'r is a compact full-stack project focused on Flask web development, lending workflow logic, frontend filtering, and integration with an external HTTP service.
