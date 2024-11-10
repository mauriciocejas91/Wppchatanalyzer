# Wpp Chat Analyzer

A Python-based tool to analyze WhatsApp chat data with various visualization options. It allows you to analyze message statistics by day, week, or month, and generate a chart for better insights into chat activity.

## Table of Contents
- [Description](#description)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

## Description
WhatsApp Chat Analyzer helps users analyze WhatsApp chat history from exported `.txt` or `.zip` files. It provides analysis of message counts by participant over time (daily, weekly, or monthly). Users can visualize this data in a table or a chart.

## Dependencies

This script requires the following Python libraries:

- `pandas` - For data manipulation and analysis.
- `re` - For regular expressions to parse WhatsApp chat data.
- `ttkbootstrap` - For modern and stylish Tkinter-based GUI.
- `tkinterdnd2` - For drag-and-drop file support in the GUI.
- `matplotlib` - For generating charts.
- `zipfile` - For handling `.zip` chat backups.
- `os` - For basic file operations.

To install all dependencies, you can use the following `pip` command:

`pip install pandas ttkbootstrap tkinterdnd2 matplotlib`

## Installation

1. Clone this repository:

`git clone https://github.com/mauriciocejas91/WppChatAnalyzer.git`

2. Navigate to the project directory:

`cd wppchatanalyzer`

3. Install the required dependencies:

`pip install -r requirements.txt`

## Usage

1. Launch the application:

`python freqan-gui6.py`

2. Once the GUI window opens, click the "Select WhatsApp Chat File" button to load your `.txt` or `.zip` WhatsApp chat export.

3. Use the buttons at the top to choose the analysis type: **Daily**, **Weekly**, or **Monthly**. The data will be displayed in the table.

4. You can also visualize the message statistics in a bar chart by clicking the "Visualize Chart" button.

5. Drag and drop `.txt` or `.zip` files into the application window to load the chat data.

## Features

- **Drag-and-drop support**: Load chat files easily with drag-and-drop functionality.
- **Flexible analysis**: Choose between daily, weekly, or monthly analysis.
- **Message count by participant**: Track the number of messages sent by each participant in each time period.
- **Chart visualization**: Generate a stacked bar chart for a visual representation of message counts.
- **WhatsApp-like theme**: The interface mimics WhatsApp's color scheme for a familiar experience.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
