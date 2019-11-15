# Installation

1. Requirements:
    - Python 3
    - Pip already installed

1. Install `pip install Django`
1. Testing `python -c "import django; print(django.get_version())"`
1. Install the rest frame work
    ```shell 
    pip install djangorestframework
    pip install markdown       # Markdown support for the browsable API.
    pip install django-filter  # Filtering support
    pip install pygments  # We'll be using this for the code highlighting
    ```

# Run
1. Create project 
    ```bash
    django-admin startproject mekongx
    cd mekongx
    python manage.py runserver
    ```
    
1. Create app inside of project
    ```bash
    python manage.py startapp snippets
    ```

1. Create model at models.py
```python
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)
```
    
1. Migrate the models by 
    ```shell
    python manage.py makemigrations snippets
    python manage.py migrate
    ```


