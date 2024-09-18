# Complete Guide to Generating FetchXML Queries for Dataverse


FetchXML is a proprietary XML-based query language used to retrieve data from Microsoft Dataverse. It's widely used in applications like Microsoft Dynamics 365 and the Power Platform. FetchXML supports a wide range of operations such as filtering, sorting, aggregation, joins, and more.

This document covers **all types of FetchXML queries**, from basic retrieval to advanced queries including aggregations and joins. We will explore each aspect of FetchXML in detail, providing examples where applicable.

## Tool Use
Ask the user to enter their dataverse org url, if they have not mentioned the same.

### get_all_entity_names
The user provided table(entity) name might not be the exact dataverse entity logical name. Use 'get_all_entity_names' to get a list of all entites present on the user's dataverse org and select the one entity that matches the most with the name provided by the user. While selecting, discard Microsoft internal tables and focus on user tables. Pass the org url to this function.

### get_entity_metadata
The user provided attributes may not be accurate or the user may not have provided the attribues. To get all details such as attribute names and their types, use 'get_entity_metadata'. Pass the exact dataverse logical name and the org url to this function.

### run_fetchxml_query
Before responding the user with the query, test the query using 'run_fetchxml_query' function. Pass the candidate Fetch XML and the org url to this function and it will return the results after executing the query or the error that may have occoured.

## Table of Contents
1. [What is FetchXML?](#what-is-fetchxml)
2. [Basic FetchXML Structure](#basic-fetchxml-structure)
3. [Attributes in FetchXML](#attributes-in-fetchxml)
4. [Conditions and Filtering](#conditions-and-filtering)
    - Equality and Inequality Operators
    - Range Filters
    - Null Checks
    - Logical Operators
5. [Joins in FetchXML](#joins-in-fetchxml)
6. [Sorting Data](#sorting-data)
7. [Paging and Limiting Results](#paging-and-limiting-results)
8. [Aggregations and Grouping](#aggregations-and-grouping)
9. [Aliases and Projections](#aliases-and-projections)
10. [FetchXML with Functions](#fetchxml-with-functions)
11. [FetchXML Advanced Options](#fetchxml-advanced-options)
12. [Sample Queries](#sample-queries)

---

## What is FetchXML?
FetchXML is a query language specifically designed for Microsoft Dataverse, which allows users to retrieve and manipulate data through XML-based queries. These queries can be run through the Dataverse API, in the Dynamics 365 platform, or in PowerApps.

FetchXML queries are structured using XML tags and support a wide variety of operations, including:
- Filtering records
- Sorting results
- Aggregating data
- Fetching related records via joins

## Basic FetchXML Structure

A basic FetchXML query consists of a root `<fetch>` tag and an `<entity>` tag that specifies which entity (table) you want to query. Within the `<entity>`, you define which attributes (fields) to retrieve and apply filters or sorting as needed.

### Example
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <attribute name="accountnumber" />
    <attribute name="revenue" />
  </entity>
</fetch>
```

In this example, we are fetching the `name`, `accountnumber`, and `revenue` fields from the `account` entity.

### Fetch Tag Attributes
The `<fetch>` tag can have additional attributes to control how the query is executed:
- `count`: Specifies the maximum number of records to retrieve.
- `page`: Indicates the page number of results to retrieve (used for paging).
- `top`: Limits the number of records returned.
- `distinct`: Ensures unique results.
- `aggregate`: Used when performing aggregations.

### Example
```xml
<fetch count="10" page="1" distinct="false">
  <entity name="contact">
    <attribute name="fullname" />
    <attribute name="emailaddress1" />
  </entity>
</fetch>
```

This example fetches the first 10 records from the `contact` entity, returning the `fullname` and `emailaddress1` fields.

## Attributes in FetchXML

The `<attribute>` tag specifies the fields to retrieve from the entity. You can list multiple attributes in a single query. If you want to fetch all attributes, you can use the `all-attributes` tag.

### Example: Retrieving Specific Attributes
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <attribute name="telephone1" />
  </entity>
</fetch>
```

### Example: Retrieving All Attributes
```xml
<fetch>
  <entity name="account">
    <all-attributes />
  </entity>
</fetch>
```

## Conditions and Filtering

Filtering in FetchXML is done using the `<filter>` and `<condition>` tags. The `<filter>` tag groups conditions together and allows combining them with logical operators like `and` and `or`.

### Equality and Inequality Operators

You can filter records based on equality (`eq`), inequality (`neq`), greater than (`gt`), less than (`lt`), etc.

#### Example: Simple Equality Filter
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <filter>
      <condition attribute="accountnumber" operator="eq" value="12345" />
    </filter>
  </entity>
</fetch>
```

#### Example: Greater Than and Less Than
```xml
<fetch>
  <entity name="account">
    <attribute name="revenue" />
    <filter>
      <condition attribute="revenue" operator="gt" value="50000" />
    </filter>
  </entity>
</fetch>
```

### Range Filters

FetchXML supports range filters like `between` and `not-between`.

#### Example: Between Filter
```xml
<fetch>
  <entity name="account">
    <attribute name="revenue" />
    <filter>
      <condition attribute="revenue" operator="between">
        <value>10000</value>
        <value>50000</value>
      </condition>
    </filter>
  </entity>
</fetch>
```

### Null Checks

You can check for null or non-null values using `null` and `not-null`.

#### Example: Null Check
```xml
<fetch>
  <entity name="account">
    <attribute name="websiteurl" />
    <filter>
      <condition attribute="websiteurl" operator="not-null" />
    </filter>
  </entity>
</fetch>
```

### Logical Operators

Use the `and` or `or` operators in the `<filter>` tag to combine conditions.

#### Example: Combining Conditions with AND
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <filter type="and">
      <condition attribute="revenue" operator="gt" value="50000" />
      <condition attribute="primarycontactid" operator="not-null" />
    </filter>
  </entity>
</fetch>
```

## Joins in FetchXML

FetchXML allows you to perform inner and outer joins between related entities using the `<link-entity>` tag. This is useful for retrieving related records in a single query.

### Inner Join Example
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <link-entity name="contact" from="accountid" to="accountid" link-type="inner">
      <attribute name="fullname" />
    </link-entity>
  </entity>
</fetch>
```

In this query, we are joining the `contact` entity to the `account` entity, retrieving the `fullname` of the contacts associated with each account.

### Outer Join Example
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <link-entity name="contact" from="accountid" to="accountid" link-type="outer">
      <attribute name="fullname" />
    </link-entity>
  </entity>
</fetch>
```

## Sorting Data

To sort records, use the `<order>` tag. You can specify the attribute to sort by and the direction (`asc` or `desc`).

### Example: Sorting in Ascending Order
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <order attribute="name" descending="false" />
  </entity>
</fetch>
```

### Example: Sorting in Descending Order
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <order attribute="revenue" descending="true" />
  </entity>
</fetch>
```

## Paging and Limiting Results

To limit the number of results returned, use the `top` or `count` attributes in the `<fetch>` tag. Paging can be done by setting the `page` and `paging-cookie` attributes.

### Example: Paging Results
```xml
<fetch count="10" page="2">
  <entity name="contact">
    <attribute name="fullname" />
  </entity>
</fetch>
```

In this example, the second page of 10 records is retrieved.

## Aggregations and Grouping

FetchXML supports aggregations using functions like `sum`, `avg`, `count`, and `min/max`. To use these, set the `aggregate="true"` attribute in the `<fetch>` tag.

### Example: Sum Aggregation
```xml
<fetch aggregate="true">
  <entity name="account">
    <attribute name="revenue" aggregate="sum" alias="total_revenue" />
  </entity>
</fetch>
```

### Grouping Data

You can group data using the `groupby` function. This is useful for reporting purposes.

#### Example: Grouping and Counting
```xml
<fetch aggregate="true">
  <entity name="account">
    <attribute name="industrycode" groupby="true" alias="industry" />
    <attribute name="accountid" aggregate="count" alias="account_count" />
  </entity>
</fetch>
```

## Aliases and Projections

Aliases can be used to reference fields in your query, especially when dealing with aggregations or joined entities.

### Example: Using Aliases
```xml
<fetch>
  <entity name="account">
    <attribute name="name" alias="account_name" />
    <attribute name="accountnumber" alias="acc_num" />
  </entity>
</fetch>
```

## FetchXML with Functions

FetchXML can execute functions such as `startswith`, `endswith`, `contains`, and others for text-based filters.

### Example: Using Text Functions
```xml
<fetch>
  <entity name="contact">
    <attribute name="fullname" />
    <filter>
      <condition attribute="fullname" operator="startswith" value="John" />
    </filter>
  </entity>
</fetch>
```

## FetchXML Advanced Options

FetchXML includes advanced options for performance optimization and execution control, such as:
- `no-lock`: Avoids locking the records while reading them.
- `distinct`: Fetches only distinct records.
- `top`: Limits the number of results.

### Example: Advanced FetchXML
```xml
<fetch distinct="true" no-lock="true" top="5">
  <entity name="contact">
    <attribute name="fullname" />
  </entity>
</fetch>
```

## Sample Queries

### Example 1: Retrieve Active Accounts
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <filter>
      <condition attribute="statecode" operator="eq" value="0" />
    </filter>
  </entity>
</fetch>
```

### Example 2: Retrieve Accounts with Revenue Greater Than $100,000
```xml
<fetch>
  <entity name="account">
    <attribute name="name" />
    <filter>
      <condition attribute="revenue" operator="gt" value="100000" />
    </filter>
  </entity>
</fetch>
```

---

This comprehensive guide covers the full range of FetchXML capabilities, including filtering, joins, aggregation, sorting, paging, and advanced querying techniques. Use these examples as templates to build more complex queries for your Dataverse solutions.


## Sample Outputs

### Sample Query

```xml
<fetch>
  <entity name="crd3e_sales">
    <attribute name="crd3e_sales1" />
    <attribute name="crd3e_salesamount" />
  </entity>
</fetch>
```

### Sample Output
```json
{"@odata.context": "https://example.crm.dynamics.com/api/data/v9.2/$metadata#crd3e_saleses(crd3e_sales1,crd3e_salesamount,_transactioncurrencyid_value,transactioncurrencyid,crd3e_salesid,transactioncurrencyid())", "value": [{"@odata.etag": "W/\"1674155\"", "_transactioncurrencyid_value": "8db2faa4-956f-ef11-a66e-6045bd059140", "crd3e_salesid": "78e021cd-8c05-41d3-a9bd-0f01dc69f4b0", "crd3e_sales1": "Sales 5", "crd3e_salesamount": 400.0}, {"@odata.etag": "W/\"1674154\"", "_transactioncurrencyid_value": "8db2faa4-956f-ef11-a66e-6045bd059140", "crd3e_salesid": "6a8a9c60-0e25-423b-bc74-0f75ee8874f3", "crd3e_sales1": "Sales 4", "crd3e_salesamount": 250.0}, {"@odata.etag": "W/\"1674153\"", "_transactioncurrencyid_value": "8db2faa4-956f-ef11-a66e-6045bd059140", "crd3e_salesid": "8cfd7f7d-dcb7-40a1-acc6-534f1a1252e4", "crd3e_sales1": "Sales 3", "crd3e_salesamount": 300.0}, {"@odata.etag": "W/\"1674151\"", "_transactioncurrencyid_value": "8db2faa4-956f-ef11-a66e-6045bd059140", "crd3e_salesid": "b9803167-af8e-497c-8741-c2a49ebe3b6e", "crd3e_sales1": "Sales 1", "crd3e_salesamount": 150.0}, {"@odata.etag": "W/\"1674152\"", "_transactioncurrencyid_value": "8db2faa4-956f-ef11-a66e-6045bd059140", "crd3e_salesid": "20078e1c-fe25-47ab-9348-e0e415fd3ef9", "crd3e_sales1": "Sales 2", "crd3e_salesamount": 200.0}]}
```