from robocorp.tasks import task
from robocorp import vault, workitems

from atlassian import Confluence

from bs4 import BeautifulSoup

def tables_to_json(html):
    '''Uses BeautifulSoup4 to extract all tables from a given html block.'''

    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    # Extract table data
    table_data = []
    for table in tables:
        headers = []
        rows = []
        for th in table.find("tr").find_all("th"):
            headers.append(th.text.strip())
        for row in table.find_all("tr")[1:]:
            rows.append([td.text.strip() for td in row.find_all("td")])
        table_data.append({"headers": headers, "rows": rows})

    # Convert to JSON format
    return table_data

@task
def my_confluence_automation():
    '''Reads a chosen page from Confluence, and creates output work items of
    all found tables.'''

    # Add a connection
    atlassian_secrets = vault.get_secret("Atlassian")

    confluence = Confluence(
        url=atlassian_secrets["confluence_url"],
        username=atlassian_secrets["confluence_user"],
        password=atlassian_secrets["confluence_token"],
        cloud=True)

    # Get page_id from input work item. Assumes only one item.
    item = workitems.inputs.current

    # Get page content from Confluence
    page = confluence.get_page_by_id(item.payload["page_id"], expand="body.storage", status=None, version=None)

    try:
        table = tables_to_json(page['body']['storage']['value'])
        if table:
            workitems.outputs.create(payload=table, save=True)
            
    except Exception as err:
        item.fail(code="CAN_NOT_PARSE_TABLES", message=str(err))