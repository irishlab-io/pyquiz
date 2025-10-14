# pyquiz

A simple and interactive terminal-based quiz application written in Python.

### Requirements
- Python 3.13 or higher
- No external dependencies required (uses only Python standard library)

## How to Play

1. The quiz will display a welcome message and tell you how many questions there are
2. For each question:
   - Read the question carefully
   - Review the four options (a, b, c, d)
   - Type the letter of your answer and press Enter
   - You'll immediately see if your answer was correct and get an explanation
3. At the end, you'll see your final score and grade

### Python

Run the quiz application:

```
python3 apps/main.py
```

### Docker

```bash
docker buildx create \ 
  --name multiarch-builder \
  --driver docker-container \
  --bootstrap \
  --use
docker buildx build -t pyquiz .
docker run --rm -ti pyquiz
```

## Contributing

[Contributions](.github/CONTRIBUTING.md) are welcome! Feel free to:

- Add more questions to `questions.json`
- Improve the user interface
- Add new features
- Fix bugs
- Improve documentation

## License

This project is licensed under the MIT License - see the [LICENSE](.github/LICENSE) file for details.

## About this project

This project is a sample repo used during the [OWASP MTL | Le "Shift-Left" en pratique: Intégrer la sécurité avec les pre-commit hooks](https://www.eventbrite.ca/e/le-shift-left-en-pratique-integrer-la-securite-avec-les-pre-commit-hooks-tickets-1758558167819?utm-campaign=social&utm-content=attendeeshare&utm-medium=discovery&utm-term=listing&utm-source=cp&aff=ebdsshcopyurl) demonstration I have conducted in October 2025.

## Author
<!-- my website is still broken :( -->
[irishlab.io](www.irishlab.io)
