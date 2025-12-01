from src.core.mcp.tools.filter_tools.filter_tools import get_tenant_departments, get_organizations_for_filters, get_organization_positions_lite, get_people_key_contacts, get_all_tags, get_organization_types_filter, get_person_types_filter, get_tenant_regions_filter, get_election_terms_filter, get_all_roles, get_people_title_list
print("=========================================",get_tenant_departments.name)
print(type(get_tenant_departments))
print(get_tenant_departments.description)
FILTER_TOOLS = [
    get_tenant_departments,
    get_organizations_for_filters,
    get_organization_positions_lite,
    get_people_key_contacts,
    get_all_tags,
    get_organization_types_filter,
    get_person_types_filter,
    get_tenant_regions_filter,
    get_election_terms_filter,
    get_all_roles,
    get_people_title_list
]