# Global and Local Chat

Implements global and local chat systems into Minecraft: Bedrock edition

## What are the "global" and "local" chat systems?

**Global Chat**: Messages starting with `!` are broadcast to all players on the server. Example: `!hello everyone`

**Local Chat**: Regular messages are only sent to players within 100 blocks of you. If no one is nearby, you'll see "No one heard you..."

## Usage

- Type normally to chat locally: `hello` (100 block radius)
- Prefix with `!` for global chat: `!hello` (all players)

Compatible with [Chatrelay](https://github.com/niko-at-chalupa/endstone-chatrelay)