"""Jaguar Conservation Agent - Using Microsoft Agent Framework"""
import asyncio
import os
import json
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient, AzureOpenAISettings
from src.services.graphdb_service import get_graphdb_service

# Load environment variables
load_dotenv()


def query_jaguar_database(sparql_query: str) -> str:
    """
    Query the GraphDB database using SPARQL. Use this tool when users ask questions about jaguars, jaguar populations, conservation efforts, habitats, threats, or any jaguar-related data. You must generate a valid SPARQL query based on the jaguar ontology. The tool will return raw JSON results from GraphDB that you must interpret and convert into natural language responses for the user.
    
    Args:
        sparql_query: A valid SPARQL query to execute against the jaguar GraphDB aligning with this ontology:
        
        JAGUAR ONTOLOGY SCHEMA:
        @prefix : <http://example.org/ontology#>.
        @prefix ex: <http://example.org/resource/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
        @prefix owl: <http://www.w3.org/2002/07/owl#>.

        #############################
        # Refined and New Ontology Classes #
        #############################

        :Animal a owl:Class.
        :Mammal a owl:Class ; rdfs:subClassOf :Animal.
        :BigCat a owl:Class ; rdfs:subClassOf :Mammal.
        :Jaguar a owl:Class ; rdfs:subClassOf :BigCat ;
            rdfs:comment "The Panthera onca species.".

        :Prey a owl:Class ; rdfs:subClassOf :Animal.
        :Livestock a owl:Class ; rdfs:subClassOf :Prey.
        :Herbivore a owl:Class ; rdfs:subClassOf :Prey.
        :Mesopredator a owl:Class ; rdfs:subClassOf :Prey.
        :Fish a owl:Class ; rdfs:subClassOf :Prey.
        :Reptile a owl:Class ; rdfs:subClassOf :Prey.

        :JaguarPopulation a owl:Class ;
            rdfs:comment "A group or population of jaguars.".

        :Habitat a owl:Class.
        :Forest a owl:Class ; rdfs:subClassOf :Habitat.
        :Rainforest a owl:Class ; rdfs:subClassOf :Forest.
        :Wetland a owl:Class ; rdfs:subClassOf :Habitat.
        :Grassland a owl:Class ; rdfs:subClassOf :Habitat.
        :Shrubland a owl:Class ; rdfs:subClassOf :Habitat.
        :WaterBody a owl:Class ; rdfs:subClassOf :Habitat.

        :Location a owl:Class.
        :Country a owl:Class ; rdfs:subClassOf :Location.
        :State a owl:Class ; rdfs:subClassOf :Location.
        :Region a owl:Class ; rdfs:subClassOf :Location.
        :MountainRange a owl:Class ; rdfs:subClassOf :Location.
        :HabitatArea a owl:Class ; rdfs:subClassOf :Location.

        :DietType a owl:Class.
        :CarnivoreDiet a :DietType.

        :Observation a owl:Class ;
            rdfs:label "Observation" ;
            rdfs:comment "An event recording the sighting of an animal.".

        :Person a owl:Class ;
            rdfs:label "Person" ;
            rdfs:comment "A human observer or researcher involved in recording animal sightings.".
        :Researcher a owl:Class ; rdfs:subClassOf :Person.
        :Rancher a owl:Class ; rdfs:subClassOf :Person.
        :Conservationist a owl:Class ; rdfs:subClassOf :Person.
        :IndigenousPerson a owl:Class ; rdfs:subClassOf :Person.
        :Tourist a owl:Class ; rdfs:subClassOf :Person.
        :LawEnforcement a owl:Class ; rdfs:subClassOf :Person.

        :ConservationOrganization a owl:Class ;
            rdfs:label "Conservation Organization" ;
            rdfs:comment "An organization involved in monitoring and protecting wildlife.".
        :GovernmentAgency a owl:Class ; rdfs:subClassOf :ConservationOrganization.
        :NGO a owl:Class ; rdfs:subClassOf :ConservationOrganization.
        :AcademicInstitution a owl:Class ; rdfs:subClassOf :ConservationOrganization.

        :Threat a owl:Class.
        :AnthropogenicThreat a owl:Class ; rdfs:subClassOf :Threat.
        :HabitatLoss a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :HabitatFragmentation a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :Poaching a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :IllegalWildlifeTrade a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :HumanWildlifeConflict a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :BorderBarrier a owl:Class ; rdfs:subClassOf :AnthropogenicThreat.
        :EnvironmentalThreat a owl:Class ; rdfs:subClassOf :Threat.
        :ClimateChange a owl:Class ; rdfs:subClassOf :EnvironmentalThreat.
        :Wildfire a owl:Class ; rdfs:subClassOf :EnvironmentalThreat.

        :ConservationEffort a owl:Class.
        :RecoveryPlan a owl:Class ; rdfs:subClassOf :ConservationEffort.
        :WildlifeCorridor a owl:Class ; rdfs:subClassOf :ConservationEffort.
        :RewildingProgram a owl:Class ; rdfs:subClassOf :ConservationEffort.
        :CommunityEngagement a owl:Class ; rdfs:subClassOf :ConservationEffort.
        :InternationalCooperation a owl:Class ; rdfs:subClassOf :ConservationEffort.
        :MonitoringTechnique a owl:Class.
        :CameraTrap a owl:Class ; rdfs:subClassOf :MonitoringTechnique.
        :ScatDetection a owl:Class ; rdfs:subClassOf :MonitoringTechnique.
        :GPSTracking a owl:Class ; rdfs:subClassOf :MonitoringTechnique.

        :LegalFramework a owl:Class.
        :Act a owl:Class ; rdfs:subClassOf :LegalFramework.
        :Convention a owl:Class ; rdfs:subClassOf :LegalFramework.

        :CulturalSignificance a owl:Class.
        :EconomicBenefit a owl:Class.

        :Event a owl:Class.

        #############################
        # Ontology Properties #
        #############################

        :hasObservation a owl:ObjectProperty ;
            rdfs:domain :Animal ;
            rdfs:range :Observation ;
            rdfs:comment "Links an animal to one of its observation events.".

        :observedDate a owl:DatatypeProperty ;
            rdfs:domain :Observation ;
            rdfs:range xsd:date ;
            rdfs:comment "The date on which the observation took place.".

        :observedBy a owl:ObjectProperty ;
            rdfs:domain :Observation ;
            rdfs:range :Person ;
            rdfs:comment "The person who recorded the observation.".

        :monitoredByOrg a owl:ObjectProperty ;
            rdfs:domain :Animal ;
            rdfs:range :ConservationOrganization ;
            rdfs:comment "Links an animal to the conservation organization that monitors it.".

        :monitoredByTechnique a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :MonitoringTechnique ;
            rdfs:comment "Indicates the technique used to monitor the jaguar.".

        :locatedInCountry a owl:ObjectProperty ;
            rdfs:domain :State ;
            rdfs:range :Country ;
            rdfs:comment "Specifies the country in which a state is located.".

        :locatedIn a owl:ObjectProperty ;
            rdfs:domain :Habitat ;
            rdfs:range :Location ;
            rdfs:comment "Specifies the state or administrative region in which a habitat is located.".

        :occursIn a owl:ObjectProperty ;
            rdfs:domain :Animal ;
            rdfs:range :Location ;
            rdfs:comment "Indicates a state where an animal has been observed or is known to occur.".

        :name a owl:DatatypeProperty ;
            rdfs:domain :Animal ;
            rdfs:range xsd:string.

        :habitat a owl:ObjectProperty ;
            rdfs:domain :Animal ;
            rdfs:range :Habitat.

        :hasDietType a owl:ObjectProperty ;
            rdfs:domain :Animal ;
            rdfs:range :DietType.

        :hasLifespan a owl:DatatypeProperty ;
            rdfs:domain :Animal ;
            rdfs:range xsd:integer ;
            rdfs:comment "Lifespan in years.".

        :scientificName a owl:DatatypeProperty ;
            rdfs:domain :Animal ;
            rdfs:range xsd:string.

        :hasGender a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "Gender of the jaguar (e.g., Male, Female).".

        :hasIdentificationMark a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "Unique spot pattern or other distinguishing mark.".

        :hasMonitoringStartDate a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date when monitoring of the individual jaguar began.".

        :hasLastSightingDate a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the last confirmed sighting of the individual jaguar.".

        :wasKilled a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was killed.".

        :causeOfDeath a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:string ;
            rdfs:comment "The cause of death for the jaguar.".

        :originatesFrom a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :Location ;
            rdfs:comment "Indicates the origin location of a dispersing jaguar.".

        :hasOffspring a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :Jaguar ;
            rdfs:comment "Links a jaguar to its offspring.".

        :isOrphaned a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was orphaned.".

        :isRehabilitated a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar underwent rehabilitation.".

        :isReleased a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:boolean ;
            rdfs:comment "Indicates if the jaguar was released into the wild.".

        :rescuedBy a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :ConservationOrganization ;
            rdfs:comment "The organization that rescued the jaguar.".

        :reintroducedBy a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :ConservationOrganization ;
            rdfs:comment "The organization that reintroduced the jaguar.".

        :hasRescueDate a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the jaguar's rescue.".

        :hasReleaseDate a owl:DatatypeProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range xsd:date ;
            rdfs:comment "Date of the jaguar's release.".

        :facesThreat a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :Threat ;
            rdfs:comment "Indicates a threat faced by the jaguar.".

        :implementsEffort a owl:ObjectProperty ;
            rdfs:domain :ConservationOrganization ;
            rdfs:range :ConservationEffort ;
            rdfs:comment "Indicates a conservation effort implemented by an organization.".

        :connectsHabitat a owl:ObjectProperty ;
            rdfs:domain :WildlifeCorridor ;
            rdfs:range :HabitatArea ;
            rdfs:comment "Indicates which habitat areas a wildlife corridor connects.".

        :hasAcreage a owl:DatatypeProperty ;
            rdfs:domain :HabitatArea ;
            rdfs:range xsd:integer ;
            rdfs:comment "The size of the habitat area in acres.".

        :hasPopulationEstimate a owl:DatatypeProperty ;
            rdfs:domain :JaguarPopulation ;
            rdfs:range xsd:integer ;
            rdfs:comment "Estimated number of jaguars in a population.".

        :isDependentOn a owl:ObjectProperty ;
            rdfs:domain :JaguarPopulation ;
            rdfs:range :JaguarPopulation ;
            rdfs:comment "Indicates if one jaguar population is dependent on another (e.g., for dispersal).".

        :namedBy a owl:ObjectProperty ;
            rdfs:domain :Jaguar ;
            rdfs:range :Person ;
            rdfs:comment "The person or group who named the jaguar.".

        SPARQL Query Examples:
        - Find by [Name]:
            SELECT ?jaguar ?label WHERE {
            BIND(ex:[Name] AS ?jaguar)
            OPTIONAL { ?jaguar rdfs:label ?label . }
            }

        - Find all properties about [Name]:
            SELECT ?jaguar ?p ?o WHERE {
            BIND(ex:[Name] AS ?jaguar)
            OPTIONAL { ?jaguar ?p ?o . }
            }
            
        - Find by gender: 
        SELECT ?jaguar ?label ?gender WHERE { ?jaguar a :Jaguar . OPTIONAL { ?jaguar rdfs:label ?label . } OPTIONAL { ?jaguar :hasGender ?gender . } }
        
        - Find killed jaguars: 
        SELECT ?jaguar ?label ?causeOfDeath WHERE { ?jaguar a :Jaguar . ?jaguar :wasKilled true . OPTIONAL { ?jaguar rdfs:label ?label . } OPTIONAL { ?jaguar :causeOfDeath ?causeOfDeath . } }
        
        - Count jaguars: 
        SELECT (COUNT(?jaguar) as ?count) WHERE { ?jaguar a :Jaguar . }
        
        - Always try to make a simple query first and only add complexity if needed.
    
    Returns:
        JSON string containing query results from GraphDB
    """
    try:
        graphdb = get_graphdb_service()
        result = graphdb.execute_sparql_query(sparql_query)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "query": sparql_query})


def create_jaguar_agent():
    """
    Create and return a native Agent Framework agent for jaguar conservation.
    
    Returns:
        Agent Framework ChatAgent instance
    """
    # System prompt for the agent
    system_prompt = """You are a helpful assistant with access to a comprehensive jaguar database stored in GraphDB. 
When users ask questions about jaguars, jaguar populations, conservation efforts, habitats, threats, or any jaguar-related information, 
use the query_jaguar_database function with a valid SPARQL query. Always try to use the function to get accurate data from the database.

When using the function:
- Make sure to form a simple query and only add complexity if needed.
- Make sure your queries are based on the provided jaguar ontology. Don't make up properties or classes not in the ontology.
- Answer based on the data retrieved, never your training data.

When responding:
- Show the used SPARQL one time and one time only
- Formulate a readable answer based on the query results
- Use **bold** for emphasis when appropriate
- Use bullet points or numbered lists for multiple items
- Use code blocks with ``` for SPARQL queries when showing them
- Break up long responses into paragraphs
- Be concise but comprehensive in your answers
- Always mention that the information comes from the jaguar database"""
    
        # OpenAI settings
    settings = OpenAISettings(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-4")
    )
    
    # Create client
    client = OpenAIResponsesClient(settings=settings)
    
    # Create and return native Agent Framework agent
    agent = asyncio.run(client.create_agent(
        name="JaguarConservationAgent",
        instructions=system_prompt,
        model=os.getenv("OPENAI_MODEL", "gpt-4"),
        tools=[query_jaguar_database],
        tool_choice="auto"
    ))
    
    return agent


# Global agent instance (singleton)
_jaguar_agent = None


def get_jaguar_agent():
    """Get or create the jaguar conservation agent"""
    global _jaguar_agent
    if _jaguar_agent is None:
        _jaguar_agent = create_jaguar_agent()
    return _jaguar_agent
