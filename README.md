# ARES

**Open-source, multimodal personal AI assistant** — natural language, voice, tools, live information, computer vision, and device control, built to work across multiple platforms.

## Overview

ARES understands natural language, talks by voice, uses tools, accesses live information, understands images, and controls supported device functions. The core AI logic is designed to stay platform-independent, with device-specific functionality handled in dedicated platform and tool adapters.

## Platforms

- Android
- macOS (Intel)
- Linux
- Web/Desktop, where useful

> iOS is **not** part of the project roadmap.

## Core Capabilities

### NLP / AI Brain
- Natural-language conversation
- Intent understanding
- Context handling
- Tool/function calling
- Multi-step task planning
- Summarization and general reasoning

### Voice
- Speech-to-text
- Text-to-speech
- Voice commands
- Spoken responses

```
Microphone -> Speech-to-text -> ARES -> Tools/AI -> Text-to-speech -> Speaker
```

### Computer Vision
- Camera input
- Image understanding
- OCR / text reading
- Object recognition
- Image processing

```
Camera -> OpenCV/image processing -> Vision model -> ARES
```

### Camera + Custom Filters
Cyberpunk, Noir, Vintage, VHS, Neon, Sketch, Pixel, and custom user-created filters.

```
"ARES, take a photo and apply the neon filter."
```

### Tools
Safe, explicit tools such as:
- Opening supported applications
- Playing music
- Searching the web
- Getting weather
- Working with files
- Camera actions
- System functions where the platform permits them

**Safety rule:** ARES never executes arbitrary AI-generated shell commands directly. All tool use goes through an allowlisted tool system with argument validation and permissions.

### Weather
A live-information tool:
```
User: "ARES, what's the weather?"
ARES -> weather service -> current/forecast data -> natural-language response
```

### Memory
Planned memory system:
- Conversation history
- User preferences
- Projects/tasks
- Useful long-term information

Possible future storage: SQLite for structured data, with vector/semantic memory added later if needed.

## Architecture

```
                         ARES
                           |
                  AI ORCHESTRATOR
                           |
       +-------------------+-------------------+
       |                   |                   |
      NLP                  CV                Voice
       |                   |                   |
       +-------------------+-------------------+
                           |
                         Tools
                           |
       +---------+---------+---------+---------+
       |         |         |         |         |
    Weather    Music     Apps      Camera     Web
```

**Platform layer:** Android, macOS (Intel), Linux

The core AI logic remains as platform-independent as possible. Device-specific functionality belongs in platform/tool adapters.

## Project Structure

```
ARES/
|-- core/
|   |-- brain.py
|   |-- memory.py
|   |-- router.py
|   `-- config.py
|-- tools/
|   |-- apps.py
|   |-- music.py
|   |-- weather.py
|   |-- files.py
|   `-- web.py
|-- voice/
|   |-- speech_to_text.py
|   `-- text_to_speech.py
|-- vision/
|   |-- camera.py
|   |-- filters.py
|   |-- ocr.py
|   `-- vision_model.py
|-- platforms/
|   |-- android/
|   |-- macos/
|   `-- linux/
|-- tests/
|-- README.md
|-- .gitignore
`-- requirements.txt
```

## Roadmap

| Version | Milestone |
|---------|-----------|
| v0.1 | Basic command-line chatbot |
| v0.2 | Connect the chatbot to a real LLM |
| v0.3 | Add NLP/tool calling and a safe tool registry |
| v0.4 | Add live weather and web information |
| v0.5 | Add application launching and other safe desktop tools |
| v0.6 | Add music controls |
| v0.7 | Add speech-to-text and text-to-speech |
| v0.8 | Add computer vision |
| v0.9 | Add camera and custom filters |
| v1.0 | Add memory and polish the complete assistant experience |
| v2.x | Expand to Android, macOS Intel, and Linux clients/platform adapters |

**First milestone:**
```
User -> Python CLI -> ARES -> response
```

After that: real AI brain -> tools -> voice/CV -> platform support.

## Getting Started

**Requirements:** Python 3.13+

```bash
git clone https://github.com/<your-username>/ARES.git
cd ARES
```

Setup and run instructions will expand as each version lands — see the Roadmap above.

## Security

- Never commit API keys.
- Keep secrets in environment variables or a local `.env` file ignored by Git.
- Never pass arbitrary LLM-generated text into shell execution.
- Validate tool names and arguments.
- Use permissions for sensitive device actions.
- Design platform-specific capabilities explicitly.

## Contributing

ARES is built incrementally so each version stays understandable, testable, and committed to GitHub. Issues and pull requests are welcome.

## License

_TBD_