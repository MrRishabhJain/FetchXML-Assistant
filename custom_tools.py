from query_runner import get_fetchxml_results, get_odata_results

def get_all_entity_names(org_url):
    entities = []
    odata_query = "EntityDefinitions?$filter=IsCustomEntity eq true&$select=LogicalName"
    result, _ = get_odata_results(odata_query, org_url)
    print(f"Found {len(result['value'])} entities on user's environment.")
    for entity in result['value']:
        entities.append(entity['LogicalName'])
    return str(entities)


def get_entity_metadata(org_url, entity_name):
    metadata = []
    odata_query = f"EntityDefinitions(LogicalName='{entity_name}')?$expand=Attributes($select=LogicalName,AttributeType)&$select=Attributes"
    result, _ = get_odata_results(odata_query, org_url)
    print(f"Found {len(result['Attributes'])} attributes.")
    for attribute in result['Attributes']:
        metadata.append({
            "LogicalName": attribute['LogicalName'],
            "AttributeType": attribute['AttributeType']
        })
    return str(metadata)


def run_fetchxml_query(fetch_xml_query, org_url):
    results, success = get_fetchxml_results(fetch_xml_query, org_url)
    if success:
        print(f"Fetch XML executed successfully.")
    return str(results)


if __name__ == '__main__':
    pass