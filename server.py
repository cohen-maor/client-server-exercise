import json
import socketio

from aiohttp import web
from matplotlib.ticker import MaxNLocator

from excel_handler import save_or_update_socket_summary

import matplotlib.pyplot
matplotlib.use('TkAgg') # use Tkinter GUI toolkit to display the plot window
import matplotlib.pyplot as plt

from datetime import datetime

import threading


data_lock = threading.Lock()

connected_clients = set()
client_ram = {}  # {sid: RAM usage percent from client}

timestamps = []
client_counts = []
avg_ram_usages = []

sio = socketio.AsyncServer(cors_allowed_origins='*', aync_mode='aiohttp')
app = web.Application()

sio.attach(app)

@sio.event
async def connect(sid):
    with data_lock:
        connected_clients.add(sid)
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    with data_lock:
        connected_clients.discard(sid)
        client_ram.pop(sid, None)
    print(f"Client disconnected: {sid}")

@sio.on('message')
async def message(sid, data):
    print("Socket ID: ", sid)
    print("Received resource summary:", data)

    save_or_update_socket_summary(sid, data)

    try:
        ram_percent = float(data["memory"]["used_percent"])
        with data_lock:
            client_ram[sid] = ram_percent
    except (KeyError, ValueError, TypeError) as e:
        print(f"Error extracting RAM % from {sid}: {e}")


def start_visualization():
    plt.ion()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Initial empty lines
    line1, = ax1.plot([], [], 'b-', label='Connected Clients')
    line2, = ax2.plot([], [], 'r-', label='Avg RAM Usage (%)')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Clients', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.autoscale_view(scaley=True)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax2.set_ylabel('RAM %', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(0, 100)  # Fix RAM axis scale to 0–100%

    ax1.set_title('Connected Clients & Avg RAM Usage Over Time')
    fig.autofmt_xdate()

    while True:
        with data_lock:
            now = datetime.now()
            timestamps.append(now)

            num_clients = len(connected_clients)
            ram_values = list(client_ram.values())
            avg_ram = sum(ram_values) / len(ram_values) if ram_values else 0

            client_counts.append(num_clients)
            avg_ram_usages.append(avg_ram)

            line1.set_data(timestamps, client_counts)
            line2.set_data(timestamps, avg_ram_usages)

            ax1.set_xlim(timestamps[0], timestamps[-1])
            ax1.relim()
            ax1.autoscale_view(scaley=True)

            ax2.relim()
            ax2.autoscale_view(scaley=False)
            ax2.set_ylim(0, 100)

        print('num_clients:', num_clients)
        print('avg_ram_usages:', avg_ram_usages)
        print('client_counts:', client_counts)

        plt.pause(2)

if __name__ == '__main__':
    threading.Thread(target=start_visualization, daemon=True).start()
    web.run_app(app, port=4000)