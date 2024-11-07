# Agent-Assignment

This project demonstrates an autonomous agent system where agents communicate asynchronously, handle messages, and interact with the POLYGON AMOY blockchain. Each agent can generate random messages, process messages, and perform POLYGON AMOY ERC-20 token transactions based on specific keywords.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Code Overview](#code-overview)

---

## Features

- **Message Generation**: Agent 1 generates random messages from a list of words.
- **Message Handling**: Agent 2 listens to messages, performs actions if they contain specific keywords:
  - **"hello"**: Prints a message containing "hello".
  - **"crypto"**: Initiates an ERC-20 token transfer if the balance is sufficient.
- **POLYGON AMOY Interaction**: Agent 2 can check ERC-20 token balance and perform token transfers using Web3.
- **Message Routing**: A `MessageRouter` routes messages between Agent 1 and Agent 2.

---

### Prerequisites

1. **Python 3.7+**

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/dasSubhajit1999/agent-assigment.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd agent-assigment
   ```

3. **Create a Python Virtual Environment**:

   ```bash
   python3 -m venv agentenv
   ```

   - If `venv` is not installed, you can install it with:
     ```bash
     sudo apt install python3-venv
     ```

4. **Activate the Virtual Environment**:

   ```bash
   source agentenv/bin/activate
   ```

5. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Create a `.env` File**:

   - Copy the keys from `.env.example` file provided in the repository:
     ```bash
     cp .env.example .env
     ```

7. **Add Your Keys to the `.env` File**:
   - Open the `.env` file and replace placeholder values with your actual keys, including `AMOY_RPC_URL`, `SOURCE_ADDRESS`, `TARGET_ADDRESS`, `PRIVATE_KEY`, and `BNB_TOKEN_CONTRACT_ADDRESS`.

## Running the Project

To start the agents and the message routing system:

```bash
python main.py
```

- **Agent 1** (named "ALICE") generates random messages every 2 seconds.
- **Agent 2** (named "BOB") receives and processes messages routed by the `MessageRouter`.

Messages containing **"hello"** print a custom message, while messages containing **"crypto"** trigger a token transfer if the balance is sufficient.

---

### Running Tests

To run the test suite:

```bash
python -m unittest test_agent.py
```

## Code Overview

### Agent.py

Defines the `Agent` class, which includes:

- **generate_random_messages()**: Generates random messages every 2 seconds.
- **check_erc20_balance()**: Checks and prints the POLYGON AMOY address's ERC-20 balance every 10 seconds.
- **\_\_transferToken()**: Transfers 1 token if the balance is sufficient.
- **handle_messages()**: Processes messages, printing a message if it contains "hello" or triggering a token transfer if it contains "crypto".

### MessageRouter.py

Defines the `MessageRouter` class, which facilitates asynchronous message routing between two agents:

- **route_messages()**: Continuously transfers messages from `agent1.outbox` to `agent2.inbox` and vice versa.

### main.py

The main entry point that initializes `Agent` instances and a `MessageRouter`, then starts the following tasks:

- **Message Generation** (Agent 1)
- **Message Routing** (between Agent 1 and Agent 2)
- **ERC-20 Balance Checking** (Agent 1)
- **Message Handling** (Agent 2)

---
