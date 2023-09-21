# IRC to Telegram Bridge

## Description

This Python program serves as an IRC to Telegram bridge, allowing messages from one or more IRC channels to be relayed to a specified Telegram channel. The program connects to an IRC server, joins specified IRC channels, and monitors incoming messages for specific patterns. When a message matches the pattern, it is forwarded to the Telegram channel using the Pyrogram library.

## Usage

1. **Configuration:**
   - Configuration values such as the IRC server address, IRC channels, IRC server port, Telegram channel ID, Telegram API ID, and Telegram API hash can be set in a `config.json` file.

   Example `config.json`:
   ```json
   {
       "server": "irc.example.com",
       "channels": "#channel1,#channel2,#channel3",
       "port": 6667,
       "telegram_channel_id": "YOUR_TELEGRAM_CHANNEL_ID",
       "api_id": "YOUR_API_ID",
       "api_hash": "YOUR_API_HASH"
   }
   ```

2. **Execution:**
   - Run the Python script, and it will read the configuration from `config.json` and establish connections to the IRC server and Telegram.
   - It continuously monitors IRC channels for messages matching a specified pattern and forwards them to the Telegram channel.

3. **To Do:**
   - **Error Handling:** Enhance error handling and logging for better error reporting and recovery.
   - **Dynamic Configuration:** Implement the ability to update configuration values while the program is running.
   - **Message Rate Limiting:** Implement message rate limiting to prevent flooding the Telegram channel.
   - **Support for More Message Patterns:** Allow configuration of multiple message patterns to match.
   - **Multi-Threading:** Implement multi-threading for better performance when handling a large number of messages.
   - **User Interface:** Create a user-friendly interface for configuring the bridge, if desired.
   - **Testing:** Add unit tests and integration tests to ensure program reliability.

This IRC to Telegram bridge program is a flexible and extensible solution for connecting IRC channels to Telegram channels. It can be customized and improved to meet specific use cases and requirements.
