---
title: Markiyan_Pyts_CV_With_Streaming
app_file: gradio_streaming_app.py
sdk: gradio
sdk_version: 5.39.0
---
## Deploy Gradio To Hugging Face
```
uv pip compile pyproject.toml -o requirements.txt --python-version 3.10
```

```
uv run gradio deploy
```