# Read tables from Confluence pages

This example shows how to read content from [Atlassian Confluence](https://www.atlassian.com/software/confluence), specifically anything in the tables.

- Configure your Confluence connection parameters in the Vault, you'll need URL, username and token. See other connection methods [here](https://atlassian-python-api.readthedocs.io/index.html).
- Takes in a Page ID as input work item. Change the example work items to match your own Page IDs.
- Reads the page content, and parses all tables in to one JSON using [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/).
- Creates an output work item of the table data.