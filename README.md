# Peer-to-Peer Chat Application

This project is a Peer-to-Peer (P2P) chat application built using Python. The application allows multiple users to connect and communicate with each other through a decentralized peer-to-peer network. It demonstrates basic networking concepts using sockets and threading to enable real-time communication between peers.

The application is designed for the **CS216** course, where the goal is to simulate communication between peers using sockets, similar to how blockchain nodes might communicate.

## Features

- **Send Messages**: Allows sending text messages to specific peers.
- **Query Active Peers**: Displays a list of all active peers currently connected.
- **Connect to Peers**: Manually connect to another peer for direct communication.
- **Peer Maintenance**: Automatically removes inactive peers that are no longer reachable.
- **Handshake Protocol**: Ensures the peers can identify and establish a connection before communication begins.
- **Graceful Shutdown**: Allows the server to close all connections safely.

## Team 
Team Name = Devil_Coders


- **Aditya Naskar** - 230002005
- **Aniket Goyal** - 230002009
- **Armaanjot Singh** - 230041005

## Prerequisites

Before running the project, ensure you have Python installed (preferably version 3.x) and that the following libraries are available:

- `socket`
- `threading`
- `time`
- `datetime`

These libraries are part of Python's standard library, so no additional installation is required.

## How to Run

Follow these steps to run the Peer-to-Peer Chat application on your machine:

### 1. Clone the repository
First, clone this repository to your local machine using the following command:

```bash
[git clone https://github.com/your_username/peer-to-peer-chat.git](https://github.com/Eclipsiess/BlockChain_Project.git)
cd peer-to-peer-chat

