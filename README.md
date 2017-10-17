# demo-jsonapi

A demonstration MuleSoft RESTful API that is based on the [{json:api}](http://jsonapi.org) standard.

## Contents

- [Introduction](#introduction)
- [{json:api} 1.0 and json-schema.org in RAML 1.0 snippets](#jsonapi-10-and-json-schemaorg-in-raml-10-snippets)
- [The Example API's RAML](#the-example-apis-raml)
- [RAML Libraries](#raml-libraries)
- [The Mule App](#the-mule-app)
- [{json:api} Mule Snippets](#jsonapi-mule-snippets)
   - [jsonapi-exceptions.xml](#jsonapi-exceptionsxml)
   - [jsonapi-flows.xml](#jsonapi-flowsxml)
- [TO DO](#to-do)
   
## Introduction

This is a demo of a (almost)fully-baked API that follows Columbia's (developing)
[integration standards](https://wiki.cc.columbia.edu/ea:enterprise_integration).

REST APIs represent data and operations on that data. Let’s outline
what’s needed and the standards we’ve chosen to adopt (in an iterative
fashion):

1. **Model the business process.** This is accomplished by following the
   [TOGAF](http://pubs.opengroup.org/architecture/togaf9-doc/arch/) Architecture Development
   Methodology’s [Business Architecture](http://pubs.opengroup.org/architecture/togaf9-doc/arch/chap08.html)
   Phase (Chapter 8). You need to know what you are trying to
   accomplish with this API before you build it!

2. **Model the data.** This is accomplished by following the TOGAF
   Architecture Development Methodology’s
   [Data Architecture](http://pubs.opengroup.org/architecture/togaf9-doc/arch/chap10.html)
   Phase (Chapter 10). See, for example, CU’s
   [People Data Model](https://wiki.cc.columbia.edu/ea:people_data_model).

3. **Create schemas.** Once a high-level data model is defined, create
   schema definition(s) using
   [our standard](https://wiki.cc.columbia.edu/ea:enterprise_integration:schema_standards)
   which is [json-schema.org](http://json-schema.org/) (RFC
   [draft-wright-json-schema-0](https://tools.ietf.org/html/draft-wright-json-schema-01)1).

4. **Model the application service.** See
   [Application Architecture](http://pubs.opengroup.org/architecture/togaf9-doc/arch/chap11.html)
   Phase (chapter 11). This is a REST API which is generally one small
   microservice in the larger scheme of things.

5. **Create REST resource & method definitions.** We use an
   [API contract language](https://wiki.cc.columbia.edu/ea:enterprise_integration:api_specifications)
   ([RAML](http://raml.org)) to iteratively define the API jointly
   between the API provider and consumer developers. The contract
   language is used in conjunction with a content specification using
   [{json:api}](http://jsonapi.org) which references the schemas
   defined above in a standard self-describing way with various
   metadata.

6. **Implement the API.** Using the RAML definition, scaffold an app
   using MuleSoft's AnyPoint API Platform and Studio to begin
   implementing the various methods on the defined
   resources. **Deliver minimum viable product and iterate.**

As this is a trivial demo, we're going to gloss over steps 1 and 2 and jump right in to {json:api}
modeling in RAML.

## {json:api} 1.0 and json-schema.org in RAML 1.0 snippets

{json:api} standardizes the request-response flow of a RESTful applications. RAML 1.0 is the modeling
language currently supported by MuleSoft although it looks like it may be replaced by OAS 3.0 soon.

To make it easier for a developer to adopt these tools, I've created some
[RAML snippet](https://github.com/n2ygk/raml-snippets) based on the {json:api} specification. You
simply `use` these libraries in your RAML definition.

### Schemas: RAML 1.0 Types
RAML 1.0 is json-schema.org "aligned" and allows `types` (the RAML 1.0 replacement for
`schemas` -- which are now deprecated) to be coded either in RAML or as a json-schema JSON document.
However, when using type inheritance (required for the{json:api} types), one must use RAML 1.0 rather than
JSON. If you later want to covert your RAML type definition to json-schema, it's pretty easy.

### {json:api} request/reply and schema metadata

{json:api} defines standard JSON success and failure responses to all the usual HTTP methods and for request bodies for
POST and PATCH as well as a sophisticated HATEOAS model. I don't pretend to understand how to use it fully yet.
Just take a look at the specification at http://jsonapi.org/format.

## The Example API's RAML

Here's a quick walk through the API's RAML, starting at the root:

### api.raml

[api.raml](src/main/api/api.raml) is the root API document, and one of the few you'll need to edit for your own
app; the others are the app-specific schema definitions.

This API currently has three root-level resources defined: `/locations`, `/widgets`, and, as a debugging
tool (to be described later), `/objects`.

```YAML
#%RAML 1.0
title: demo-jsonapi
description: a sample RESTful API that conforms to jsonapi.org 1.0
version: v1
baseUri: https://test-columbia-demo-jsonapi.cloudhub.io/{version}/api
documentation: 
  - title: About {json:api} 1.0
    content: 
      This is an example of a [jsonapi 1.0](http://jsonapi.org/format) RESTful API
      which uses mediatype (application/vnd.api+json) in requests and responses.
  - title: The jsonApiLibrary (api.*) types
    content: 
      The types defined in library `jsonApiLibrary.raml` are derived directly from the jsonsapi 1.0 
      [specification](https://github.com/json-api/json-api/blob/gh-pages/schema)
      (which is defined using the [json-schema.org](http://json-schema.org/documentation.html) specification).
      They were translated from JSON to YAML and then manually edited in several cases where a json:api
      capability is not directly available in RAML (for instance, _patternProperties_). 
      
      When referencing those types
      in your API, you must prefix them with the library name you've given in the `uses` statement. In this example, that 
      is `api`. For reasons I don't quite understand, you must use this with the same uses key name
      (api) in this main api.raml and any other libraries that reference types defined in jsonApiLibrary.raml such
      as the WidgetType and LocationType definitions.
  - title: The Locations and Widgets types
    content: 
      The Locations and Widget types are the types managed by this sample API. They are all subclasses of the
      api.resource type and also subclass api.attributes from the jsonApiLibrary.raml library. 
uses: 
  api: libraries/jsonApiLibrary.raml
  loc: libraries/LocationType.raml
  wid: libraries/WidgetType.raml
  col: libraries/jsonApiCollections.raml
  cu: libraries/columbiaLibrary.raml
  obj: libraries/ObjectType.raml

# the API's resources:
/widgets:
  displayName: widgets
  description: stuff we have in inventory
  type: 
    col.collection: 
      dataType: wid.Widget
      exampleCollection: !include examples/WidgetCollectionExample.raml
      exampleItem: !include examples/WidgetItemExample.raml
  get:
    is: [ cu.oauth_read_any, col.all-the-things ]
  post:
    is: [ cu.oauth_create_any ]
  /{id}:
    type: 
     col.item:
        dataType: wid.Widget
        exampleItem: !include examples/WidgetItemExample.raml
    get:
      is: [ cu.oauth_read_any, col.sparse ]
    patch:
      is: [ cu.oauth_update_any ]
    delete:
      is: [ cu.oauth_delete_any ]
/locations:
  displayName: locations
  description: inventory locations
  type: 
    col.collection: 
      dataType: loc.Location
      exampleCollection: !include examples/LocationCollectionExample.raml
      exampleItem: !include examples/LocationItemExample.raml
  get:
    is: [ cu.oauth_read_any, col.all-the-things ]
  post:
    is: [ cu.oauth_create_any ]
  /{id}:
    type: 
     col.item:
        dataType: loc.Location
        exampleItem: !include examples/LocationItemExample.raml
    get:
      is: [ cu.oauth_read_any, col.sparse ]
    patch:
      is: [ cu.oauth_update_any ]
    delete:
      is: [ cu.oauth_delete_any ]
/objects:
  displayName: objects
  description: The object store persists all the types used above. Use this utility resource
    to GET or DELETE the entire contents of the object store.
  type: 
    col.collection:
      dataType: obj.Object
      exampleCollection: !include examples/ObjectCollectionExample.raml
      exampleItem: !include examples/ObjectItemExample.raml
  get:
    is: [ cu.oauth_read_any ]
  delete:
    description: DELETES the entire object store
    is: [ cu.oauth_delete_any ]
    responses: 
      204:
        description: Sucessfully deleted. No content returned.
```


## RAML Libraries

This API pulls in several libraries. Note that RAML uses the key before the name of the library file
as the namespace; you have to refer to definitions in the library using _namespace_._definition_.

###  api: libraries/jsonApiLibrary.raml

[jsonApiLibrary.raml]((src/main/api/libraries/jsonApiLibrary.raml) contains the type definitions
from the spec. You don't actually need to know what these are as the collections library references them:

###  col: libraries/jsonApiCollections.raml

#### ResourceTypes: collection, item

[jsonApiCollections.raml](src/main/api/libraries/jsonApiCollections.raml) defines resourceTypes of
`collection` and `item`. Within these definitions are all the HTTP body types, responses, etc. All
you need to do when invoking a collection or item is supply required paramters:

 - **dataType** is the schema for your resource.
 - **exmapleItem** is an example item.
 - **exampleCollection** is an example collection (multiple items).

#### Traits: pageable, sortable, sparse, filterable, includable, all-the-things

You will want to add some traits that mainly apply to collections but some also to items.
These are all directly from the {json:api} spec or the recommendations where the spec doesn't
require them:
 
  - **pageable** for pagination
  - **sortable** to sort
  - **sparse** to limit which types' fields are returned
  - **filterable** for filtering for values of types' fields.
  - **includable** to limit which types are included.

**all-the-things** is a convenience trait that includes all of the above.

### cu: libraries/columbiaLibrary.raml

[columbiaLibrary.raml](src/main/api/libraries/columbiaLibrary.raml) defines Columbia-specific securitySchemes
pnd traits:

#### SecuritySchemes: oauth_2_0 and oauth_2_0_test

**oauth_2_0** is our production OAuth 2.0 service and the one that is integrated with AnyPoint API Manager:
client credentials registered in API Manager are stored in the production OAuth server.

**oauth_2_0_test**, Columbia's test OAuth 2.0 service, is not synced with API Manager; If you need to test with it
and MuleSoft, you'll need to get the credentials sync'd up. Also, the traits are only defined for the oauth_2_0:

#### Traits: CRUD w/OAuth

Use `is: [ cu.oauth_read_columbia ]`, for example, to require a Shibboleth login and `read` scope.
The current list of these is:

 - **oauth_read_columbia**: Authorization Code w/scopes: auth-columbia, read.
 - **oauth_read_any**: Authorization Code w/scopes `read` and one of
   auth-{columbia,facebook,google,linkedin,twitter,windowslive}
   or Client Credentials scope auth-none.
 - **oauth_create_{columbia,any}**: as above with create scope
   **oauth_update_{columbia,any}**: as above with update scope
   **oauth_delete_{columbia,any}**: as above with delete scope

You'll probably want to define some traits specifically for your app. If they are generic enough,
make sure they get added to this library.

###  wid: libraries/WidgetType.raml

This demo app has Widgets in inventory at Locations. Here's the Widget type definition. The key things
to note when you define our own types are:

Your type _extends_ (is a subclass of) the `api.resource` type from {json:api}. This type has
a specific shape that you have to comply with:

- It always has a top-level `type` string which says what type it is.
- It always has a unique `id` string which is the instance identifier. Do not be tempted to hang any
  semantics off the id; Use another attribute for that.
- It has a top-level `data` element which can be a single or array of objects (or empty).
  Under the data element are:
  - The `attribute` element which is a map containing your "useful" attributes. Put your information here.
  - Some additional optional elements like `relationships`.

Once you inherit from `api.resource` this whole framwork is just there. Just need to override/add elements
that are specific to your schema.

Here's the Widget type example, which includes relationships to the Location type. The name of the relationship
is `location`.

```YAML
#%RAML 1.0 Library
usage: Schema for a Widget
uses:
  api: jsonApiLibrary.raml
types:
  Widget:
    type: api.resource
    description: a widget's primary data
    properties:
      attributes:
        properties:
          name:
            required: true
            type: string
            description: catalog name
          qty:
            required: false
            type: integer
            minimum: 0
            description: quantity
      relationships:
        type: WidgetRelationships
        required: false
    additionalProperties: false
    example:
      type: Widget
      id: abc-123
      attributes:
        name: can opener
        qty: 42
      relationships:
        location:
          data: 
            - type: Location
              id: "14"     
            - type: Location
              id: "15"
          links:
            self: /widgets/abc-123/relationships/location
  WidgetRelationships:
    type: object
    description: |
      A widget's relationships: 
        - location
    properties:
      location:
        type: api.relationshipMember
        description: location in inventory
        required: false
    example:
      location:
        data: 
          - type: Location
            id: "14"     
          - type: Location
            id: "15"
        links:
          self: /widgets/abc-123/relationships/location
```

Location and Object are similar. See the source.

## The Mule App

Once you've got fully-baked RAML pulled from the libraries, with all the options filled in, the power of
API Designer or Anypoint Studio becomes apparent: they won't let you create incorrect RAML (especially useful
when defining your types and examples) and APIkit will mock examples responses that work.

See the [Anypoint Studio-generated documentation](doc/index.html) for this app.

The mocked app that API Designer presents
and the Mule APIkit scaffold that is generated are quite complete; APIkit enforces most stuff like checking
for valid mediatypes (Application/vnd.api+json) although it does not enforce RAML securedBy policies (use
the [OAuth2 Scope Enforcement](https://github.com/n2ygk/mulesoft-oauth2-scope-enforcer) custom policy for that
nor does it prevent extra query parameters beyond those that are defined. Also, the default APIkit exception
mappings (e.g. what to return with a 404 status) do not comply with {json:api}. For that there are:

## {json:api} Mule Snippets

The following Mule snippets enhance your API to be {json:api} compatbile.

### jsonapi-exceptions.xml

This module defines a global APIkit exception mapping that replaces the default one. Errors are
returned according to `api.failure` in the jsonApiLibrary. For example:

```JSON
{
    "errors": [
        {
            "id": "b5eebd89-c641-4b1d-9aec-21d680556a58",
            "status": "404",
            "title": "Resource not found",
            "detail": "Value is not found for { key=Widget:123 }"
        }
    ]
}
```

To use these replacement exceptions, change the `api-main` flow's Reference Exception Strategy to
`jsonapi-exception-mapping`.


#### 409 Patch Conflict

It also adds the 409 Conflict response to PATCH. You can throw this from your app code, for example,
in Groovy:
```
throw new PatchConflictException('foobar')
```

This requires that you include the [src/main/java/PatchConflictException.java](src/main/java/PatchConflictException.java).

#### Sidebar: Python can raise Java exceptions but they are wrapped in PyException

Unfortunately, Jython wraps all exceptions in the PyException class: You have to catch `org.python.core.PyException`
and then figure out how to unwrap it and route it to the correct handler. If you can figure out how to get this
to work, please let me know!

```python
import org.mule.module.apikit.exception.BadRequestException
props = message.getInboundProperty('http.query.params')
if 'fail' in props:
  raise org.mule.module.apikit.exception.BadRequestException("foo")
```

### jsonapi-flows.xml

This module defines some common flows and implements them with Mule's Object Store. It is incomplete but a good
starting point.

The flows are:

- **jsonapiGETitem** gets an item of type `flowVars.type`. For now, you must define `type` in the calling flow.
  ![alt-text](get_set_type.png "set flowVars.type before call jsonapiGETitem flow")
- **jsonapiGETcollection** gets a collection. As above `type` must be defined.
- **jsonapiPOSTitem** posts an item. The type is obtain from the item's `type` element.
- **jsonQueryParamsValidation** does a simplistic job of making sure the query parameters are from the {json:api}
  vocabulary; They do no validation beyond that.

## TO DO

- includes
  - add include= queryParameter filtering of returned includes.
- Refactor lots of set payload/set variable cruft by moving into the script elements.
- Get PATCH flow working
- implement pageable, sortable, etc. traits
- Document "how to write Python that uses Java objects"
