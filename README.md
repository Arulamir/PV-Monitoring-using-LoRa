# LoRa communication for PV monitoring

## Overview
This repository contains an end-to-end IoT communication system that collects sensor data via LoRa, transmits it using MQTT, and stores it in a MySQL database. The system is divided into two main components running on different devices: a Raspberry Pi acting as a LoRa gateway and a server computer responsible for database storage.

The project demonstrates practical integration of wireless communication, message brokering, and backend data persistence in a distributed architecture.

---

## System Architecture

LoRa Node  →  Raspberry Pi (LoRa Gateway)  
             →  MQTT Broker  
             →  Server PC (MQTT Subscriber)  
             →  MySQL Database

---

## 1. LoRa Gateway (Raspberry Pi)

**File:** `Lora_Gateway.py`

### Description
This program runs on a Raspberry Pi equipped with an RFM95 (LoRa) module. It is responsible for:

- Initializing SPI communication
- Configuring the RFM9x LoRa module (915 MHz)
- Receiving sensor packets from LoRa nodes
- Parsing sensor values:
  - DC Voltage
  - AC Voltage
  - AC Current
  - Temperature
- Calculating communication metrics:
  - RSSI
  - Bit rate
  - Packet loss statistics
- Logging transmission statistics into a CSV file
- Publishing sensor data to an MQTT broker

### MQTT Topics Used
- `teganganDC`
- `arusAC`
- `teganganAC`
- `suhu`

### Technologies Used (Gateway)
- Python
- paho-mqtt
- adafruit_rfm9x
- SPI (busio, digitalio)
- Raspberry Pi hardware

---

## 2. Receive and Save Service (Server PC)

**File:** `receive_and_save_data.py`

### Description
This program runs on a computer acting as a data server. It performs the following tasks:

- Connects to the MQTT broker
- Subscribes to sensor topics
- Receives real-time sensor measurements
- Connects to a MySQL database
- Inserts incoming data into the database table

### Database Information
- Database: `db_lora`
- Table: `tb_pv_fix`
- Columns:
  - Tegangan_pv
  - Arus
  - Tegangan
  - Suhu

Each received data packet is stored using an SQL INSERT operation.

### Technologies Used (Server)
- Python
- paho-mqtt
- mysql-connector-python
- MySQL Server

---

## Deployment Environment

### Raspberry Pi (Gateway)
- Raspberry Pi with RFM95 LoRa module
- Python 3
- SPI enabled

### Server PC
- Python 3
- MySQL Server installed
- Access to MQTT broker

---

## Project Objective

This project demonstrates:

- LoRa-based wireless communication
- MQTT publish/subscribe messaging architecture
- Distributed IoT system design
- Real-time data logging to a relational database
- Integration between embedded hardware and backend systems

The implementation showcases practical skills in IoT systems, networking, and database integration, making it suitable for professional portfolio presentation.

