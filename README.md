# Meridian GPU Miner

Welcome to the Meridian GPU Miner repository! This miner utilizes CUDA for efficient mining operations of the Meridian
token.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nessshon/meridian-gpu-miner.git

2. **Navigate to the Repository:**
   ```bash
   cd meridian-gpu-miner
   ```

3. **Run the Installation Script:**
   ```bash
   ./install.sh
   ```
   This script will install the required dependencies.


1. **Create a .env File:**
   ```bash
   nano .env
   ```
   Replace placeholders with your actual information.
   ```env
   MNEMONICS=a b c
   RECIPIENT_ADDRESS=UQ...
   GPUS_COUNT=8

   TIMEOUT=5
   ITERATIONS=999999999999999
   GIVERS_COUNT=1000
   BOOST_FACTOR=128
   ```

## Usage

<blockquote>
If you have your own Lite Server, you can provide a custom configuration by creating a global-config.json file in the data folder.
</blockquote>

**Start the Miner:**

   ```bash
   ./run.sh
   ```

**Note:** Ensure you have the necessary NVIDIA GPU drivers and CUDA toolkit installed for proper GPU mining.

## Disclaimer

This miner is provided for educational and experimental purposes. Use it responsibly and ensure compliance with local
regulations. The developers are not responsible for any misuse or unintended consequences resulting from the use of this
software.
