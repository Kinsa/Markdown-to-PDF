# Getting Set Up (First Time)

[Install UV](https://docs.astral.sh/uv/getting-started/installation/):

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Source the `~/.zshrc` file for changes to take effect:

```sh
$ source ~/.zshrc
```

[Use UV to install the latest Python just for it's use](https://docs.astral.sh/uv/guides/install-python/). Use the latest LTS release.

```sh
$ uv python install
```

#### Create and activate a virtual environment first

```sh
$ uv venv .venv
$ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Then install fpdf2

- [fpdf2 Installation Docs](https://py-pdf.github.io/fpdf2/index.html#installation)
- [Installing and using Mistletoe to convert Markdown files to PDF](https://py-pdf.github.io/fpdf2/CombineWithMarkdown.html)

```sh
$ uv pip install fpdf2 mistletoe
```

#### Configure PyCharm to use the uv environment

[Docs](https://www.jetbrains.com/help/pycharm/uv.html)

