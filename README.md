<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c46708ea-f5fa-48ff-a2b2-cdc6130247f3" />
Smart Dorm Map

Contributors:
This was a group project for Fundamentals of Programming Course. 

🏫 Project Overview

Smart Dorm Map is a Python-based desktop application designed to help university dorm residents easily view and reserve shared spaces such as study rooms, Mountain View lounges, and TV lounges.
The system provides a visual 2D map interface for dorm blocks (A1, A2, B1, and B2) and allows users to check availability, book specific time slots, and view real-time occupancy updates — all from a simple and intuitive GUI.

⚙️ Features

🏢 Interactive Dorm Map – Displays A1, A2, B1, and B2 blocks in a clean grid layout.

🕒 Time-Slot Reservations – Users can reserve a room for specific one-hour slots (8 AM – 11 PM).

👤 User Input – Each reservation records the reserver’s name and timestamp.

🎨 Color-Coded Status

🟢 Green → Available

🟡 Yellow → Reserved for a time slot

🔴 Red → Fully booked

💾 Data Persistence – All reservations are automatically saved to room_status.txt and reloaded on startup.

📊 Occupancy Counters – Shows total reserved rooms per dorm block.

🧭 Menu Bar

Reset All Rooms

View Summary of Reservations

About Section

🌄 Aesthetic Interface – Includes a blurred dorm background and modern visual alignment (Tkinter + Pillow).

💻 Technologies Used

Python 3.13

Tkinter – GUI framework

Pillow (PIL) – Image handling for background

OS & Datetime Modules – File storage and timestamps
Results

The Smart Dorm Map successfully provides an efficient way to visualize and manage dormitory space usage.
It accurately tracks reservations, prevents double-booking conflicts, and ensures persistence across sessions.
The interface was tested for reliability and optimized for presentation and user experience.

🚀 Future Enhancements

Add database or cloud integration for real-time multi-user access.

Implement user authentication for better identity tracking.

Add email or notification system for upcoming reservations.

Deploy the app as a web-based dashboard accessible from mobile or browser.
