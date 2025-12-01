
from langchain_core.tools import tool
from src.core.mcp.client import MCPClient
from datetime import datetime

@tool("get_tenant_departments", return_direct=False)
async def get_tenant_departments(token: str):
    """
    Fetch all tenant departments (lite version).

    Makes a GET request to:
        /tenantdepartment/GetAllTenantDepartmentsLite/{date}}

    Returns:
        List of department objects in the form:
        [
            {
                "id": 123,
                "name": "Project Alpha",
                "created_at": "2023-10-01T12:34:56Z"
            }
        ]
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token,verify_ssl=False)
    dept= await client.request("GET", f"/tenantdepartment/GetAllTenantDepartmentsLite/{current_date}")
    return dept

@tool(
    "get_organizations_for_filters",
    return_direct=False
)
async def get_organizations_for_filters(token: str) -> list[dict]:
    """
    Fetches organizations with IDs for filter options.

    Returns:
        list[dict]: Organization objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=True)
    result = await client.request("GET", f"/Organization/GetOrganizationListWithIdForFilters/{current_date}")
    formatted = []
    for p in result:
        formatted.append({
            "id": p["id"],
            "name": p.get("name")
            
        })
    return {
    "result": formatted
    
}


@tool(
    "get_organization_positions_lite",
    return_direct=False
)
async def get_organization_positions_lite(token: str) -> list[dict]:
    """
    Fetches all organization position options (lite).

    Returns:
        list[dict]: Position objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/Organization/GetAllOrganizationPositionsLite/{current_date}")


@tool(
    "get_people_key_contacts",
    return_direct=False
)
async def get_people_key_contacts(token: str) -> list[dict]:
    """
    Fetches key contacts for people.

    Returns:
        list[dict]: People/contact objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/People/GetPeopleKeyContacts/{current_date}")


@tool(
    "get_all_tags",
    return_direct=False
)
async def get_all_tags(token: str) -> list[dict]:
    """
    Fetches all organization tags.

    Returns:
        list[dict]: Tag objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/Organization/GetAllTags/{current_date}")


@tool(
    "get_organization_types_filter",
    return_direct=False
)
async def get_organization_types_filter(token: str) -> list[dict]:
    """
    Fetches organization type filter options.

    Returns:
        list[dict]: Organization type objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/Organization/GetAllOrgTypesFilterOptions/{current_date}")


@tool(
    "get_person_types_filter",
    return_direct=False
)
async def get_person_types_filter(token: str) -> list[dict]:
    """
    Fetches person type list for filtering.

    Returns:
        list[dict]: Person type objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/Settings/Get/PersonTypeListForFilter/0/{current_date}")

@tool(
    "get_tenant_regions_filter",
    return_direct=False
)
async def get_tenant_regions_filter(token: str) -> list[dict]:
    """
    Fetches tenant region filter options.

    Returns:
        list[dict]: Region objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/TenantRegion/GetAllTenantRegionForFilter/{current_date}")


@tool(
    "get_election_terms_filter",
    return_direct=False
)
async def get_election_terms_filter(token: str) -> list[dict]:
    """
    Fetches election terms for filtering.

    Returns:
        list[dict]: Election term objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/electionterm/GetAllElectionTermForFilter/{current_date}")


@tool(
    "get_all_roles",
    return_direct=False
)
async def get_all_roles(token: str) -> list[dict]:
    """
    Fetches all available roles.

    Returns:
        list[dict]: Role objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/People/GetAllRoles/{current_date}")


@tool(
    "get_people_title_list",
    return_direct=False
)
async def get_people_title_list(token: str) -> list[dict]:
    """
    Fetches all people title records.

    Returns:
        list[dict]: Title objects.
    """
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    client = MCPClient(token, verify_ssl=False)
    return await client.request("GET", f"/People/getAllPeopleTitleList/{current_date}")









