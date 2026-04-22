📡 FDMA-Based YouTube Style TCP Server
🧠 Overview

This project simulates a YouTube-like content delivery system using a TCP client-server architecture, inspired by the FDMA (Frequency Division Multiple Access) communication model.

Each content category acts as a dedicated channel with fixed bandwidth, and multiple users share that bandwidth dynamically when they join a channel.

The system also includes rule-based content filtering to ensure users only see relevant content from their selected channel, reducing distraction and improving focus.

🚀 Features
📡 FDMA Simulation
Fixed bandwidth per channel
Dynamic sharing among connected users
🌐 Multi-client TCP Server
Supports multiple users simultaneously using threading
🎯 Channel System
music, gaming, tech, sports, news
🔍 Search Functionality
Search content within the selected channel
🎬 Recommendation System
Random content suggestions per channel
📊 Live Channel Status
Shows number of users and bandwidth per user
🧹 Automatic Cleanup
Removes users when they disconnect

⚙️ Tech Stack
Python 3
Socket Programming (TCP)
Multithreading
Random module

🏗️ System Architecture
Client → TCP Connection → Server
                ↓
        Channel Selection (JOIN)
                ↓
        FDMA Bandwidth Allocation
                ↓
     Content Filtering & Response
📡 FDMA Logic

Each channel has a fixed bandwidth:

Total Bandwidth per channel = 200 kHz

If users join a channel:

Bandwidth per user = Total Bandwidth / Number of Users

Example:

1 user → 200 kHz
2 users → 100 kHz each
4 users → 50 kHz each
